"""Internationalisation : segmentation du HTML en fragments traduisibles, URLs traduites."""
import hashlib, json, re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).parent
LANGS = ["fr", "en", "ar", "es"]
TLANGS = ["en", "ar", "es"]

# Chemin FR (clé) -> slug par langue (préfixe de langue ajouté automatiquement)
SLUGS = {
 "": {"en": "", "ar": "", "es": ""},
 "logiciel-de-gestion-commerciale/": {"en": "travel-agency-software/", "ar": "travel-agency-software/", "es": "software-agencia-de-viajes/"},
 "manage-travelife/": {"en": "travelife-manage-erp/", "ar": "travelife-manage-erp/", "es": "travelife-manage-erp/"},
 "systeme-de-reservation-b2b/": {"en": "b2b-booking-system/", "ar": "b2b-booking-system/", "es": "sistema-de-reservas-b2b/"},
 "site-internet-pour-agence-de-voyages/": {"en": "travel-agency-website/", "ar": "travel-agency-website/", "es": "pagina-web-agencia-de-viajes/"},
 "site-web-pour-agence-de-voyages/": {"en": "b2c-booking-website/", "ar": "b2c-booking-website/", "es": "web-de-reservas-b2c/"},
 "agent-ia-travelife-smartcrm/": {"en": "ai-agent-smartcrm/", "ar": "ai-agent-smartcrm/", "es": "agente-ia-smartcrm/"},
 "travelife-omra/": {"en": "umrah-hajj-software/", "ar": "umrah-hajj-software/", "es": "software-umrah-hajj/"},
 "nos-clients/": {"en": "clients/", "ar": "clients/", "es": "clientes/"},
 "nos-partenaires/": {"en": "partners/", "ar": "partners/", "es": "socios/"},
 "tarifs-logiciel-travelife/": {"en": "pricing/", "ar": "pricing/", "es": "precios/"},
 "creation-site-web-agence-de-voyage/": {"en": "website-pricing/", "ar": "website-pricing/", "es": "precios-pagina-web/"},
 "contactez/": {"en": "contact/", "ar": "contact/", "es": "contacto/"},
 "formulaire-site-internet-agences-de-voyages/": {"en": "website-quote/", "ar": "website-quote/", "es": "presupuesto-pagina-web/"},
 "guide-travelife/": {"en": "user-guide/", "ar": "user-guide/", "es": "guia-de-usuario/"},
 "politique-de-confidentialite/": {"en": "privacy-policy/", "ar": "privacy-policy/", "es": "politica-de-privacidad/"},
}

def lang_path(fr_path, lang):
    """Chemin (sans / initial) de la version `lang` d'une page FR, ou None si non traduite."""
    if lang == "fr": return fr_path
    if fr_path not in SLUGS: return None
    return f"{lang}/" + SLUGS[fr_path][lang]

BLOCK = {"p","div","li","ul","ol","h1","h2","h3","h4","h5","h6","section","article","header","footer","nav","aside",
         "main","figure","figcaption","table","thead","tbody","tfoot","tr","td","th","blockquote","details","summary",
         "form","fieldset","dl","dt","dd","select","textarea","hr","br_block","picture","video","iframe"}
SKIP = {"style","script","noscript","svg","code","pre"}
ATTRS = ["alt","aria-label","placeholder","title","data-label"]

def hid(text):
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]

def meaningful(text):
    t = re.sub(r"\{\{[^}]*\}\}", "", text)
    t = re.sub(r"&[a-z#0-9]+;", "", t)
    return bool(re.search(r"[A-Za-zÀ-ÿ]", t))

def has_block(el):
    return any(getattr(d, "name", None) in BLOCK or getattr(d, "name", None) in SKIP for d in el.descendants)

def inner(el):
    return "".join(str(c) for c in el.contents)

def walk(soup, fn_seg, fn_text, fn_attr):
    """Parcourt le DOM : fn_seg(el) pour un élément-feuille (innerHTML), fn_text(node) pour un texte direct mêlé à des blocs."""
    def visit(el):
        for c in list(el.children):
            if isinstance(c, Comment): continue
            if isinstance(c, NavigableString):
                if c.strip() and meaningful(str(c)) and el.name not in SKIP:
                    fn_text(c)
                continue
            if c.name in SKIP: continue
            for a in ATTRS:
                v = c.get(a)
                if v and meaningful(v): fn_attr(c, a)
            if c.name == "input" or c.name == "img": continue
            if not has_block(c):
                txt = c.get_text()
                if meaningful(txt):
                    fn_seg(c)  # les attributs internes (alt…) sont traduits dans le fragment
                    continue
                # pas de texte : chercher attributs plus bas
                for d in c.find_all(True):
                    for a in ATTRS:
                        v = d.get(a)
                        if v and meaningful(v): fn_attr(d, a)
                continue
            visit(c)
    visit(soup)

def parse(html):
    return BeautifulSoup(html, "html.parser")

def extract(html):
    """Retourne la liste ordonnée des fragments FR (texte ou innerHTML) d'un HTML."""
    soup = parse(html); out = []
    def seg(el): out.append(inner(el).strip())
    def txt(node): out.append(str(node).strip())
    def att(el, a): out.append(el[a].strip())
    walk(soup, seg, txt, att)
    return out

class Missing(Exception): pass

def translate(html, table, missing=None):
    """Remplace chaque fragment par sa traduction (table: hash -> texte)."""
    soup = parse(html)
    def get(fr):
        k = hid(fr)
        if k in table and table[k] is not None and str(table[k]).strip() != "":
            return table[k]
        if missing is not None: missing.append(fr)
        return None
    def seg(el):
        fr = inner(el).strip(); t = get(fr)
        if t is None: return
        el.clear()
        frag = BeautifulSoup(t, "html.parser")
        for n in list(frag.contents): el.append(n)
    def txt(node):
        raw = str(node); fr = raw.strip(); t = get(fr)
        if t is None: return
        lead = raw[:len(raw)-len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
        node.replace_with(NavigableString(lead + t + trail))
    def att(el, a):
        t = get(el[a].strip())
        if t is not None: el[a] = t
    walk(soup, seg, txt, att)
    return str(soup)

def load_table(lang):
    p = ROOT / "i18n" / f"{lang}.json"
    table = {}
    if p.exists(): table.update(json.loads(p.read_text(encoding="utf-8")))
    d = ROOT / "i18n" / lang
    if d.exists():
        for f in sorted(d.glob("*.json")):
            table.update(json.loads(f.read_text(encoding="utf-8")))
    return table

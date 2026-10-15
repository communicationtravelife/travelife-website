#!/usr/bin/env python3
"""Construit le site statique Travelife (aperçu local) à partir de src/."""
import json, re, os, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = Path(os.environ.get("DIST", str(ROOT / "dist")))
SITE = "https://travelife.ma"
LOGO = SITE + "/wp-content/uploads/2024/10/logo-travelife-2024.png"
LOGO_W = SITE + "/wp-content/uploads/2024/10/logo-travelife-2024-white.png"
FAVICON = SITE + "/wp-content/uploads/2022/02/cropped-15-32x32.png"
PHONE = "(+212) 5 21 50 06 05"
PHONE_TEL = "+212521500605"
EMAIL = "contact@travelife.ma"
ADDRESS = "Bureau N°6, Office Panorama, 14 Av. Abou Bakr el Kadiri, Casablanca"

# --- Icônes (style Lucide, trait 2px) ---
P = {
 "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.18 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
 "erp": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
 "network": '<circle cx="12" cy="5" r="3"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><path d="M12 8v4M12 12l-5 4.5M12 12l5 4.5"/>',
 "bot": '<rect x="3" y="8" width="18" height="12" rx="3"/><path d="M12 8V4"/><circle cx="12" cy="3" r="1"/><path d="M8 14h.01M16 14h.01"/><path d="M9 18h6"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8"/>',
 "tag": '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
 "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01M8 10h.01M12 10h.01M16 10h.01"/>',
 "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 "crm": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8M8 13h5"/>',
 "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
 "plug": '<path d="M12 22v-5"/><path d="M9 8V2M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
 "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M9 13h6M9 17h6"/>',
 "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
 "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
 "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "trend": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
 "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
 "palette": '<circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.93 0 1.65-.75 1.65-1.69 0-.44-.18-.84-.44-1.13-.29-.29-.44-.65-.44-1.13a1.64 1.64 0 0 1 1.67-1.67h2c3.05 0 5.56-2.5 5.56-5.55C21.97 6.01 17.46 2 12 2z"/>',
 "smartphone": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
 "star": '<path d="M11.5 2.3a.5.5 0 0 1 1 0l2.3 4.7a2 2 0 0 0 1.6 1.1l5.2.8a.5.5 0 0 1 .3.9l-3.8 3.6a2 2 0 0 0-.6 1.9l.9 5.2a.5.5 0 0 1-.8.6l-4.6-2.5a2 2 0 0 0-2 0l-4.6 2.5a.5.5 0 0 1-.8-.6l.9-5.2a2 2 0 0 0-.6-1.9L1.5 9.8a.5.5 0 0 1 .3-.9l5.2-.8a2 2 0 0 0 1.6-1.1z"/>',
 "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
 "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
 "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
 "whatsapp": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M9 10h.01M12 10h.01M15 10h.01"/>',
 "headset": '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
 "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
 "kaaba": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/><path d="M3 10.5l9 4 9-4"/>',
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "ig": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
 "in": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
 "yt": '<path d="M2.5 17a24 24 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24 24 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
 "x": '<path d="M4 4l16 16M20 4 4 20"/>',
}
def icon(name, cls=""):
    p = P.get(name, P["check"])
    c = f' class="i-{name}{(" " + cls) if cls else ""}"'
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

# --- Registre des pages connues (chemins identiques au site WordPress) ---
KNOWN = set()

def rel(target, from_path):
    """Convertit un chemin racine (/slug/) en lien relatif pour l'affichage local."""
    depth = len([s for s in from_path.strip("/").split("/") if s])
    pre = "../" * depth
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1); anchor = "#" + anchor
    t = target.lstrip("/")
    if t == "":
        return (pre + "index.html" + anchor) if target != "" else anchor
    if t.startswith("assets/"):
        return pre + t + anchor
    if not t.endswith("/") and "." in t.split("/")[-1]:
        return pre + t + anchor
    if not t.endswith("/"): t += "/"
    return pre + t + "index.html" + anchor

import sys as _sys
_sys.path.insert(0, str(ROOT))
from i18n import SLUGS, TLANGS, LANGS, lang_path, translate, load_table
from chrome_i18n import CHROME, PAGE_NAMES, LOCALES, LANG_LABEL

TABLES = {}
def T(lang, s):
    if lang == "fr": return s
    return CHROME[lang].get(s, s)

def map_path(path, lang):
    """/slug/#x (FR) -> /<lang>/<slug-traduit>/#x si la page est traduite."""
    if path.startswith("/__fr__/"): return "/" + path[8:]
    if lang == "fr": return path
    base, anchor = (path.split("#", 1) + [""])[:2]
    key = base.lstrip("/")
    if key and not key.endswith("/") and "." not in key.split("/")[-1]: key += "/"
    lp = lang_path(key, lang)
    if lp is None: return path
    return "/" + lp + (("#" + anchor) if anchor else "")

def rewrite_links(body, from_path, lang="fr"):
    def repl(m):
        attr, url = m.group(1), m.group(2)
        u = url
        if u.startswith(SITE):
            path = u[len(SITE):] or "/"
            base = path.split("#")[0]
            if base.strip("/") in KNOWN or base == "/":
                u = path
            else:
                return m.group(0)
        if u.startswith("/") and not u.startswith("//"):
            if attr == "href": u = map_path(u, lang)
            return f'{attr}="{rel(u, from_path)}"'
        return m.group(0)
    return re.sub(r'(href|src)="([^"]*)"', repl, body)

def render_includes(s, lang="fr"):
    def repl(m):
        f = SRC / "partials" / (m.group(1) + ".html")
        t = f.read_text(encoding="utf-8")
        if lang != "fr": t = translate(t, TABLES[lang])
        return t
    for _ in range(2):
        s = re.sub(r"\{\{inc:([a-z0-9_-]+)\}\}", repl, s)
    return s

def render_icons(s, lang="fr"):
    s = render_includes(s, lang)
    s = re.sub(r"\{\{i:([a-z]+)\}\}", lambda m: icon(m.group(1)), s)
    return s

# --- Navigation ---
NAV = [
 ("produits", "Nos produits", [
   ("/logiciel-de-gestion-commerciale/", "erp", "Logiciel de gestion commerciale", "ERP cloud pour agences et tour-opérateurs"),
   ("/manage-travelife/", "layers", "Travelife Manage", "Le parcours de l’agent, de la réservation à la TVA"),
   ("/site-internet-pour-agence-de-voyages/", "globe", "Création de site web B2C", "Site de réservation connecté aux GDS"),
   ("/systeme-de-reservation-b2b/", "network", "Plateforme B2B", "Portail de réservation pour vos partenaires"),
   ("/agent-ia-travelife-smartcrm/", "bot", "SmartCRM & Agent IA", "Qualifiez vos voyageurs 24h/24 sur WhatsApp"),
   ("/travelife-omra/", "kaaba", "Travelife Omra", "Programmes Omra & Hajj de A à Z"),
 ]),
 ("references", "Nos références", [
   ("/nos-clients/", "users", "Nos clients", "Plus de 200 agences nous font confiance"),
   ("/nos-partenaires/", "handshake", "Nos partenaires", "GDS, compagnies, hôtels et paiement"),
 ]),
 ("tarifs", "Tarifs", [
   ("/tarifs-logiciel-travelife/", "calc", "Logiciel de gestion & ERP", "Formules adaptées à chaque agence"),
   ("/creation-site-web-agence-de-voyage/", "tag", "Sites web agence", "Packs site B2C clé en main"),
 ]),
 ("blog", "Blog", "/articles/"),
 ("contact", "Contact", "/contactez/"),
]

def lang_switch(alts, lang):
    """alts: {lang: url_path_root} ; pages non traduites -> accueil de la langue."""
    items = "".join(
        f'<li><a href="/{"__fr__/" if l == "fr" else ""}{alts.get(l, lang_path("", l))}" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == lang else ""}><span>{l.upper()}</span>{LANG_LABEL[l]}</a></li>'
        for l in LANGS)
    return (f'<div class="lang-sw"><button class="lang-btn" aria-expanded="false" aria-label="{T(lang,"Langue")}">{icon("globe")}<span>{lang.upper()}</span>{icon("chev","chev")}</button>'
            f'<ul class="lang-dd">{items}</ul></div>')

def header(active, lang, alts):
    items = []
    for key, label, target in NAV:
        if isinstance(target, str):
            cur = ' aria-current="page"' if key == active else ""
            items.append(f'<li><a href="{target}"{cur}>{T(lang,label)}</a></li>')
        else:
            sub = "".join(
                f'<li><a href="{u}"><span class="dd-ico">{icon(ic)}</span><span><strong>{T(lang,t)}</strong><small>{T(lang,d)}</small></span></a></li>'
                for u, ic, t, d in target)
            cur = ' data-active="1"' if key == active else ""
            items.append(f'<li class="has-dd"><button class="nav-link" aria-expanded="false"{cur}>{T(lang,label)}{icon("chev","chev")}</button><ul class="dd">{sub}</ul></li>')
    sw = lang_switch(alts, lang)
    return f'''<a class="skip" href="#contenu">{T(lang,"Aller au contenu")}</a>
<div class="promo"><span>{icon("zap")}</span><span><b>GO SIYAHA</b><span class="promo-long">{T(lang," — jusqu’à 90 % de vos services Travelife financés par Maroc PME.")}</span><span class="promo-short">{T(lang," : jusqu’à 90 % financé")}</span></span><a href="/go-siyaha-maroc-pme-travelife/">{T(lang,"En savoir plus →")}</a></div>
<header class="site-header">
 <div class="container header-inner">
  <a class="brand" href="/" aria-label="{T(lang,"Travelife — accueil")}"><img src="{LOGO}" alt="{T(lang,"Travelife — logiciel pour agence de voyage")}" width="180" height="40"></a>
  <nav class="nav" id="nav" aria-label="{T(lang,"Navigation principale")}">
   <ul>{"".join(items)}</ul>
   <a class="btn btn--primary nav-mobile-cta" href="/contactez/">{T(lang,"Demander une démo")}</a>
  </nav>
  <div class="header-cta">
   {sw}
   <a class="header-phone" href="tel:{PHONE_TEL}">{icon("phone")}<span dir="ltr">{PHONE}</span></a>
   <a class="btn btn--primary btn--sm" href="/contactez/">{T(lang,"Demander une démo")}</a>
   <button class="burger" aria-label="{T(lang,"Ouvrir le menu")}" aria-expanded="false" aria-controls="nav">{icon("menu")}</button>
  </div>
 </div>
</header>'''

def footer(lang):
    addr = ADDRESS if lang == "fr" else CHROME[lang]["ADDRESS"]
    return f'''<footer class="site-footer">
 <div class="container">
  <div class="footer-grid">
   <div class="footer-brand">
    <img src="{LOGO_W}" alt="Travelife" width="180" height="42" loading="lazy">
    <p>{T(lang,"Logiciel de gestion ERP pour agences de voyages au Maroc et à l’international. Pilotez l’ensemble de vos opérations sur une plateforme cloud unique.")}</p>
    <div class="socials">
     <a href="https://web.facebook.com/travelife.ma" aria-label="Facebook" rel="noopener" target="_blank">{icon("fb")}</a>
     <a href="https://www.instagram.com/travelife.ma/" aria-label="Instagram" rel="noopener" target="_blank">{icon("ig")}</a>
     <a href="https://ma.linkedin.com/showcase/travelife-technologie" aria-label="LinkedIn" rel="noopener" target="_blank">{icon("in")}</a>
     <a href="https://www.youtube.com/channel/UCsOGbqnwRfiWCn9b7Vs0rYg/videos" aria-label="YouTube" rel="noopener" target="_blank">{icon("yt")}</a>
     <a href="https://twitter.com/CTravelife" aria-label="X (Twitter)" rel="noopener" target="_blank">{icon("x")}</a>
    </div>
   </div>
   <div>
    <h4>{T(lang,"Nos solutions")}</h4>
    <ul>
     <li><a href="/logiciel-de-gestion-commerciale/">{T(lang,"Logiciel de gestion (ERP)")}</a></li>
     <li><a href="/manage-travelife/">Travelife Manage</a></li>
     <li><a href="/site-internet-pour-agence-de-voyages/">{T(lang,"Création de site web")}</a></li>
     <li><a href="/systeme-de-reservation-b2b/">{T(lang,"Plateforme B2B")}</a></li>
     <li><a href="/agent-ia-travelife-smartcrm/">{T(lang,"SmartCRM & IA")}</a></li>
     <li><a href="/travelife-omra/">{T(lang,"Travelife Omra")}</a></li>
    </ul>
   </div>
   <div>
    <h4>Travelife</h4>
    <ul>
     <li><a href="/nos-clients/">{T(lang,"Nos clients")}</a></li>
     <li><a href="/nos-partenaires/">{T(lang,"Nos partenaires")}</a></li>
     <li><a href="/tarifs-logiciel-travelife/">{T(lang,"Tarifs")}</a></li>
     <li><a href="/articles/">{T(lang,"Blog")}</a></li>
    </ul>
   </div>
   <div>
    <h4>{T(lang,"Contactez-nous")}</h4>
    <ul class="footer-contact">
     <li>{icon("phone")}<a href="tel:{PHONE_TEL}" dir="ltr">{PHONE}</a></li>
     <li>{icon("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li>{icon("pin")}<a href="https://maps.app.goo.gl/62kjeGMPFvd3VikLA" target="_blank" rel="noopener">{addr}</a></li>
    </ul>
    <div class="gosiyaha">{icon("zap")}<span><b>{T(lang,"Référencé GO SIYAHA")}</b><br>{T(lang,"Jusqu’à 90 % financé par Maroc PME.")}</span></div>
   </div>
  </div>
  <div class="footer-word" aria-hidden="true">travelife</div>
  <div class="footer-bottom">
   <span>© <span id="year">2026</span> Travelife. {T(lang,"Tous droits réservés.")}</span>
   <span>{T(lang,"Cloud Travel Agency Software — made in Morocco")}</span>
  </div>
 </div>
</footer>'''

ORG_ID = SITE + "/#organization"
def org_ld(lang):
    desc = ("Travelife est une plateforme marocaine ERP et SaaS dans le cloud pour agences de voyages et tour-opérateurs : réservations (GDS, API, offline), ventes B2B et B2C, devis, facturation, TVA sur marge, CRM, agent IA et paiements."
            if lang == "fr" else CHROME[lang]["ORG_DESC"])
    return {
     "@context": "https://schema.org", "@type": "Organization", "@id": ORG_ID, "name": "Travelife",
     "alternateName": "Travelife Technologie", "url": SITE + "/", "logo": LOGO, "email": EMAIL, "telephone": "+212521500605",
     "foundingDate": "2013", "description": desc,
     "address": {"@type": "PostalAddress", "streetAddress": "Bureau N°6, Office Panorama, 14 Av. Abou Bakr el Kadiri, Sidi Maarouf", "addressLocality": "Casablanca", "addressCountry": "MA"},
     "contactPoint": [{"@type": "ContactPoint", "telephone": "+212521500605", "email": EMAIL, "contactType": "sales", "areaServed": ["MA", "Africa", "Worldwide"], "availableLanguage": ["French", "English", "Arabic", "Spanish"]}],
     "award": ["African Excellence Awards 2025 — Best Travel Agency Software Company, Morocco (MEA Markets)", "World Summit Awards — meilleure solution numérique innovante au Maroc"],
     "knowsAbout": ["Travel agency software", "Travel ERP", "B2B booking engine", "B2C travel website", "GDS integration", "VAT on margin", "Umrah and Hajj management", "AI agent for travel agencies"],
     "sameAs": ["https://web.facebook.com/travelife.ma", "https://www.instagram.com/travelife.ma/", "https://ma.linkedin.com/showcase/travelife-technologie", "https://twitter.com/CTravelife", "https://www.youtube.com/channel/UCsOGbqnwRfiWCn9b7Vs0rYg/videos"],
    }

SOFTWARE_PAGES = {"", "logiciel-de-gestion-commerciale/", "tarifs-logiciel-travelife/", "manage-travelife/"}
def software_ld(lang, url):
    names = {"fr": "Logiciel de gestion pour agences de voyages", "en": "Travel agency management software", "es": "Software de gestión para agencias de viajes", "ar": "برنامج إدارة وكالات الأسفار"}
    plans = [("Travelife ERP Core", "199"), ("Travelife ERP Business", "399"), ("Travelife ERP Connect", "599")]
    return {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Travelife Manage",
            "alternateName": names[lang], "applicationCategory": "BusinessApplication", "applicationSubCategory": "Travel agency ERP",
            "operatingSystem": "Web (cloud, SaaS)", "inLanguage": ["fr", "en", "ar", "es"], "url": url,
            "publisher": {"@id": ORG_ID},
            "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "EUR", "category": "subscription",
                        "priceSpecification": {"@type": "UnitPriceSpecification", "price": p, "priceCurrency": "EUR", "unitCode": "MON"}} for n, p in plans]}

def faq_ld(body):
    qs = re.findall(r"<details[^>]*>\s*<summary>(.*?)</summary>\s*<div class=\"answer\">(.*?)</div>\s*</details>", body, re.S)
    if not qs: return None
    clean = lambda s: html.unescape(re.sub(r"<[^>]+>", " ", s)).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub(r"\s+", " ", clean(q)), "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", clean(a))}} for q, a in qs]}

FONTS_AR = '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">'

def page(meta, body, lang="fr", fr_key=None):
    path = meta["path"]
    canonical = meta.get("canonical") or (SITE + "/" + path)
    # Versions linguistiques
    alts = {}
    if fr_key is not None and fr_key in SLUGS:
        for l in LANGS: alts[l] = lang_path(fr_key, l)
    ld = [org_ld(lang)]
    if fr_key == "":
        ld.append({"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "name": "Travelife", "url": SITE + "/" + path,
                   "inLanguage": lang, "publisher": {"@id": ORG_ID}})
    if fr_key in SOFTWARE_PAGES:
        ld.append(software_ld(lang, SITE + "/" + path))
    if meta.get("crumbs"):
        home = "" if lang == "fr" else lang_path("", lang)
        items = [{"@type": "ListItem", "position": 1, "name": T(lang, "Accueil"), "item": SITE + "/" + home}]
        if lang == "fr":
            for i, (n, u) in enumerate(meta["crumbs"], start=2):
                items.append({"@type": "ListItem", "position": i, "name": n, "item": SITE + u})
        else:
            items.append({"@type": "ListItem", "position": 2, "name": PAGE_NAMES.get(fr_key, {}).get(lang, meta["title"]), "item": SITE + "/" + path})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    f = faq_ld(body)
    if f: ld.append(f)
    for extra in meta.get("ld", []): ld.append(extra)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    og = meta.get("og") or ""
    robots = meta.get("robots", "follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large")
    if os.environ.get("NOINDEX"): robots = "noindex, nofollow"
    hreflang = ""
    if alts:
        hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="__SITE__/{alts[l]}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="__SITE__/{alts["fr"]}">'
        og_alt = "".join(f'<meta property="og:locale:alternate" content="{LOCALES[l]}">' for l in LANGS if l != lang)
    else:
        og_alt = ""
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    head = f'''<!doctype html>
<html lang="{lang}"{dir_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(meta["title"])}</title>
<meta name="description" content="{html.escape(meta["desc"])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="__CANON__">
{hreflang}
<meta property="og:locale" content="{LOCALES[lang]}">{og_alt}
<meta property="og:type" content="{meta.get("ogtype","website")}">
<meta property="og:title" content="{html.escape(meta["title"])}">
<meta property="og:description" content="{html.escape(meta["desc"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Travelife">
{f'<meta property="og:image" content="{og}">' if og else ''}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Inter:wght@400;450;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
{FONTS_AR if lang == "ar" else ""}
<link rel="stylesheet" href="/assets/style.css">
{ld_html}
</head>
<body{' class="has-dark-hero"' if meta.get('dark') else ''}>'''
    scripts = '<script src="/assets/main.js" defer></script>' + "".join(f'<script src="{s}" defer></script>' for s in meta.get("scripts", []))
    out = head + header(meta.get("nav"), lang, alts) + f'\n<main id="contenu">\n{body}\n</main>\n' + footer(lang) + scripts + "\n</body>\n</html>\n"
    out = render_icons(out, lang)
    out = rewrite_links(out, path, lang)
    out = out.replace("__CANON__", canonical).replace("__SITE__", SITE)
    if lang == "ar":
        parts = re.split(r"(<script.*?</script>|<[^>]+>)", out, flags=re.S)
        out = "".join(x if x.startswith("<") else x.replace(PHONE, f'<bdi dir="ltr">{PHONE}</bdi>') for x in parts)
    return out

def parse_src(text):
    m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->\s*", text, re.S)
    meta = json.loads(m.group(1))
    return meta, text[m.end():]

def translated_meta(meta, lang, table):
    from i18n import hid
    fr_key = meta["path"]
    m = dict(meta)
    m["path"] = lang_path(fr_key, lang)
    m["title"] = table.get(hid(meta["title"]), meta["title"])
    m["desc"] = table.get(hid(meta["desc"]), meta["desc"])
    m["canonical"] = SITE + "/" + m["path"]
    m["crumbs"] = [["x", "/" + m["path"]]] if meta.get("crumbs") else None
    m.pop("robots", None)
    return m

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(SRC / "assets", DIST / "assets")
    for l in TLANGS: TABLES[l] = load_table(l)
    srcs = sorted((SRC / "pages").glob("*.html"))
    parsed = [parse_src(p.read_text(encoding="utf-8")) for p in srcs]
    gen = ROOT / "gen"
    if gen.exists():
        parsed += [parse_src(p.read_text(encoding="utf-8")) for p in sorted(gen.glob("*.html"))]
    for meta, _ in parsed:
        KNOWN.add(meta["path"].strip("/"))
    for k in SLUGS:
        for l in TLANGS: KNOWN.add(lang_path(k, l).strip("/"))
    n = 0; sitemap = []
    for meta, body in parsed:
        key = meta["path"]
        out = DIST / meta["path"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(meta, body, "fr", key if key in SLUGS else None), encoding="utf-8"); n += 1
        if "noindex" not in meta.get("robots", "") and meta.get("canonical", SITE + "/" + key) == SITE + "/" + key:
            sitemap.append((key, key in SLUGS))
        if key in SLUGS:
            for l in TLANGS:
                miss = []
                tbody = translate(body, TABLES[l], miss)
                if miss: print(f"  [{l}] {key}: {len(miss)} fragments non traduits")
                tm = translated_meta(meta, l, TABLES[l])
                o = DIST / tm["path"] / "index.html"
                o.parent.mkdir(parents=True, exist_ok=True)
                o.write_text(page(tm, tbody, l, key), encoding="utf-8"); n += 1
    write_seo_files(sitemap)
    print(f"{n} pages générées")

def write_seo_files(sitemap):
    from datetime import date
    today = date.today().isoformat()
    urls = []
    for key, multi in sitemap:
        if multi:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}/{lang_path(key,l)}"/>' for l in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{key}"/>'
            for l in LANGS:
                urls.append(f"<url><loc>{SITE}/{lang_path(key,l)}</loc><lastmod>{today}</lastmod>{alts}</url>")
        else:
            urls.append(f"<url><loc>{SITE}/{key}</loc><lastmod>{today}</lastmod></url>")
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    if os.environ.get("NOINDEX"):
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = ("User-agent: *\nAllow: /\n\n# Moteurs de réponse IA (GEO) : accès autorisé\n"
                  "User-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\n"
                  "User-agent: ClaudeBot\nAllow: /\n\nUser-agent: Claude-SearchBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\n"
                  "User-agent: Google-Extended\nAllow: /\n\nUser-agent: Applebot-Extended\nAllow: /\n\n"
                  f"Sitemap: {SITE}/sitemap.xml\n")
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    llms = (ROOT / "src" / "llms.txt")
    if llms.exists(): shutil.copy(llms, DIST / "llms.txt")

if __name__ == "__main__":
    main()

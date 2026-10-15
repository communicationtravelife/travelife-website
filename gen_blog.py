#!/usr/bin/env python3
"""Génère les pages blog (index, catégories, articles) dans gen/ à partir de data/posts.json."""
import json, html, math, shutil, urllib.parse
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
GEN = ROOT / "gen"
data = json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))
CATS = {c[0]: {"name": c[1], "slug": c[2]} for c in data["cats"]}
POSTS = data["posts"]
U = lambda s: html.unescape(s or "")
E = lambda s: html.escape(U(s), quote=True)
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fdate(d):
    y, m, j = map(int, d.split("-")); return f"{j} {MOIS[m-1]} {y}"
def rtime(w): return max(2, math.ceil(w / 200))
def main_cat(p):
    order = [63, 64, 62, 1]  # catégorie affichée en priorité
    for c in order:
        if c in p["cat"]: return CATS[c]
    return CATS[1]
CAT_META = {
 "tourisme": ("Tourisme - Travelife", "Découvrez nos articles en relation avec le tourisme - logiciel de gestion pour agence de voyage - travelife.ma", "Tendances, chiffres et analyses du tourisme au Maroc et en Afrique."),
 "digital-marketing": ("Digital marketing - Travelife", "Découvrez nos articles en relation avec le Digital marketing - logiciel de gestion pour agence de voyage - travelife.ma", "Réseaux sociaux, site web, contenu : nos conseils marketing pour les agences de voyages."),
 "nouveaute": ("Nouveauté - Travelife", "Découvrez nos articles en relation avec les nouvelles mis à jour et les nouveautés du secteur de voyage - logiciel de gestion pour agence de voyage", "Mises à jour du logiciel, intégrations, distinctions et actualités Travelife."),
 "fonctionnalites": ("Fonctionnalités - Travelife", "Découvrez nos articles en relation avec les Fonctionnalités du logiciel travelife - logiciel de gestion pour agence de voyage - travelife.ma", "Comment tirer le meilleur des modules Travelife : ERP, CRM, facturation, B2B…"),
}
CAT_ICON = {"tourisme": "globe", "digital-marketing": "trend", "nouveaute": "zap", "fonctionnalites": "layers"}
ORDER = (63, 64, 62, 1)
I = lambda n: "{{i:" + n + "}}"  # icône (rendue par build.py)
INC_CTA = "{{inc:cta}}"

def excerpt(p):
    """Extrait coupé au dernier mot complet."""
    t = U(p["ex"]).strip()
    if " " in t: t = t[:t.rfind(" ")]
    t = t.rstrip(" ,;:.—-–'’")
    return html.escape(t, quote=True) + "…"

def meta_line(p):
    return f'<div class="post-meta"><span>{I("calendar")} {fdate(p["d"])}</span><span>{I("clock")} {rtime(p["w"])} min de lecture</span></div>'

def card(p, cls=""):
    c = main_cat(p)
    alt = E(p["alt"]) or E(p["h1"])
    return (f'<a class="post-card {cls} reveal" href="/{p["s"]}/"><div class="thumb"><img src="{p["img"]}" alt="{alt}" loading="lazy">'
            f'<span class="chip">{c["name"]}</span></div><div class="body">{meta_line(p)}<h3>{E(p["h1"])}</h3><p>{excerpt(p)}</p></div></a>')

def feature(p, label="À la une", eager=True):
    c = main_cat(p)
    alt = E(p["alt"]) or E(p["h1"])
    load = "" if eager else ' loading="lazy"'
    return (f'<a class="mag-feature reveal" href="/{p["s"]}/">\n   <div class="thumb"><img src="{p["img"]}" alt="{alt}"{load}></div>\n'
            f'   <div class="body"><div class="chip-row"><span class="chip chip--o">{label}</span><span class="chip">{c["name"]}</span></div>'
            f'<h2>{E(p["h1"])}</h2><p>{excerpt(p)}</p>{meta_line(p)}<span class="link-arrow">Lire l’article {I("arrow")}</span></div>\n  </a>')

POST_CTA = ('<div class="post-cta reveal"><div><span class="big">90%</span><h3>Votre digitalisation financée par GO SIYAHA</h3>'
            '<p>ERP, site B2C, plateforme B2B et SmartCRM éligibles au programme Maroc PME.</p></div>'
            f'<a class="btn btn--primary btn--sm" href="/go-siyaha-maroc-pme-travelife/">Vérifier mon éligibilité {I("arrow")}</a></div>')

def count(cid): return sum(1 for p in POSTS if cid in p["cat"])

def filter_bar(active):
    items = [("", "Tous", "/articles/", len(POSTS))] + [(CATS[c]["slug"], CATS[c]["name"], f'/category/{CATS[c]["slug"]}/', count(c)) for c in ORDER]
    return '<nav class="filter-bar" aria-label="Catégories">' + "".join(
        f'<a href="{u}"{" class=\"active\" aria-current=\"page\"" if s == active else ""}>{n}<small>{k}</small></a>' for s, n, u, k in items) + "</nav>"

def cat_tiles():
    out = []
    for i, cid in enumerate(ORDER):
        c = CATS[cid]; lead = CAT_META[c["slug"]][2]
        o = " ico--o" if i % 2 else ""
        out.append(f'<a class="mag-cat reveal reveal-d{i}" href="/category/{c["slug"]}/"><span class="ico{o}">{I(CAT_ICON[c["slug"]])}</span>'
                   f'<h3>{c["name"]}</h3><p>{lead}</p><span class="n">{count(cid)} articles {I("arrow")}</span></a>')
    return "".join(out)

def grid_with_cta(posts, at=5):
    cards = [card(p) for p in posts]
    if len(cards) > at: cards.insert(at, POST_CTA)
    return "".join(cards)

def write(name, meta, body):
    (GEN / f"{name}.html").write_text("<!--META " + json.dumps(meta, ensure_ascii=False) + " -->\n" + body, encoding="utf-8")

def main():
    if GEN.exists(): shutil.rmtree(GEN)
    GEN.mkdir()
    # --- Index du blog ---
    first, duo, rest = POSTS[0], POSTS[1:3], POSTS[3:]
    body = f'''<section class="page-hero mag-hero">
 <div class="container">
  <ol class="breadcrumb"><li><a href="/">Accueil</a></li><li>Blog</li></ol>
  <div class="mag-top">
   <div>
    <span class="eyebrow">Le blog Travelife</span>
    <h1>Nos <span class="serif">articles</span></h1>
    <p class="lead">Conseils, tendances du tourisme, nouveautés du logiciel et stratégies digitales pour faire grandir votre agence de voyages.</p>
   </div>
   <div class="mag-count"><div><b>{len(POSTS)}</b>articles publiés</div><div><b>{len(CATS)}</b>thématiques</div></div>
  </div>
  {feature(first)}
 </div>
</section>
<section class="section">
 <div class="container">
  <div class="mag-bar"><h2>Derniers articles</h2>{filter_bar("")}</div>
  <div class="post-duo">{"".join(card(p, "post-card--lg") for p in duo)}</div>
  <div class="post-grid post-grid--mag">{grid_with_cta(rest)}</div>
 </div>
</section>
<section class="section section--sand">
 <div class="container">
  <div class="section-head section-head--left reveal"><span class="eyebrow">Explorer par thème</span><h2>Trouvez les ressources qui font avancer votre agence</h2></div>
  <div class="mag-cats">{cat_tiles()}</div>
 </div>
</section>
{INC_CTA}'''
    write("blog-index", {"path": "articles/", "nav": "blog", "title": "Nos articles - logiciel Travelife pour agence de voyage",
        "desc": "Travelife - Logiciel de gestion pour agence de voyage - Découvrez nos derniers articles sur divers sujets liés au logiciel de voyage, tourime...",
        "canonical": "https://travelife.ma/articles/", "crumbs": [["Blog", "/articles/"]]}, body)

    # --- Catégories ---
    for cid, c in CATS.items():
        posts = [p for p in POSTS if cid in p["cat"]]
        t, d, lead = CAT_META[c["slug"]]
        top = feature(posts[0], "Dernier article") if len(posts) > 4 else ""
        lst = posts[1:] if top else posts
        body = f'''<section class="page-hero mag-hero">
 <div class="container">
  <ol class="breadcrumb"><li><a href="/">Accueil</a></li><li><a href="/articles/">Blog</a></li><li>{c["name"]}</li></ol>
  <div class="mag-top">
   <div>
    <span class="eyebrow">Catégorie · {len(posts)} articles</span>
    <h1>{c["name"]}</h1>
    <p class="lead">{lead}</p>
   </div>
  </div>
  {top}
 </div>
</section>
<section class="section">
 <div class="container">
  <div class="mag-bar"><h2>{"Plus d’articles" if top else "Tous les articles"}</h2>{filter_bar(c["slug"])}</div>
  <div class="post-grid post-grid--mag">{grid_with_cta(lst)}</div>
 </div>
</section>
{INC_CTA}'''
        write(f"cat-{c['slug']}", {"path": f"category/{c['slug']}/", "nav": "blog", "title": t, "desc": d,
            "canonical": f"https://travelife.ma/category/{c['slug']}/", "crumbs": [["Blog", "/articles/"], [c["name"], f"/category/{c['slug']}/"]]}, body)

    # --- Articles ---
    known = [p["s"] for p in POSTS]
    for i, p in enumerate(POSTS):
        c = main_cat(p)
        related = [q for q in POSTS if q is not p and set(q["cat"]) & set(p["cat"])][:3]
        chips = "".join(f'<a class="chip" href="/category/{CATS[x]["slug"]}/">{CATS[x]["name"]}</a>' for x in p["cat"] if x in CATS)
        alt = E(p["alt"]) or E(p["h1"])
        url = f"https://travelife.ma/{p['s']}/"
        q_url = urllib.parse.quote(url, safe="")
        share = ('<div class="art-share">'
                 f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={q_url}" target="_blank" rel="noopener" aria-label="Partager sur LinkedIn">{I("in")}</a>'
                 f'<a href="https://www.facebook.com/sharer/sharer.php?u={q_url}" target="_blank" rel="noopener" aria-label="Partager sur Facebook">{I("fb")}</a>'
                 f'<a href="https://wa.me/?text={q_url}" target="_blank" rel="noopener" aria-label="Partager sur WhatsApp">{I("whatsapp")}</a>'
                 f'<a href="mailto:?subject={urllib.parse.quote(U(p["h1"]))}&amp;body={q_url}" aria-label="Partager par email">{I("mail")}</a></div>')
        minis = "".join(f'<a class="mini-post" href="/{q["s"]}/"><img src="{q["img"]}" alt="{E(q["alt"]) or E(q["h1"])}" loading="lazy"><b>{E(q["h1"])}</b></a>' for q in related)
        body = f'''<div class="read-progress" aria-hidden="true"></div>
<article>
<header class="art-hero">
 <div class="container">
  <ol class="breadcrumb"><li><a href="/">Accueil</a></li><li><a href="/articles/">Blog</a></li><li><a href="/category/{c["slug"]}/">{c["name"]}</a></li></ol>
  <div class="chip-row">{chips}</div>
  <h1>{E(p["h1"])}</h1>
  <p class="art-dek">{excerpt(p)}</p>
  <div class="art-by"><span class="av" aria-hidden="true">T</span><span>Par <b>l’équipe Travelife</b></span><i class="sep"></i><span>{I("calendar")} <time datetime="{p["d"]}">{fdate(p["d"])}</time></span><i class="sep"></i><span>{I("clock")} {rtime(p["w"])} min de lecture</span></div>
 </div>
</header>
<div class="art-cover-wrap"><div class="container">
 <div class="art-cover"><img src="{p["img"]}" alt="{alt}" width="1200" height="590"></div>
</div></div>
<section class="section" style="padding-top:64px">
 <div class="container article-layout article-layout--v2">
  <div>
   <div class="prose" id="article-body" data-id="{p["id"]}" data-root="../" data-url="{url}">
    <div class="loading">Chargement de l’article depuis travelife.ma…</div>
   </div>
   <div class="art-end"><div class="chip-row"><span class="text-muted" style="font-size:.85rem;margin-right:6px">Classé dans</span>{chips}</div>{share}</div>
  </div>
  <aside class="article-aside">
   <div class="aside-card aside-card--cta">
    <span class="eyebrow">Démo gratuite</span>
    <h3>Digitalisez votre agence avec Travelife</h3>
    <ul class="checklist"><li>ERP, CRM, site B2C &amp; plateforme B2B</li><li>Conforme TVA sur marge</li><li>Jusqu’à 90 % financé GO SIYAHA</li></ul>
    <a class="btn btn--primary" style="width:100%" href="/contactez/">Demander une démo</a>
   </div>
   <div class="aside-card">
    <p class="aside-title">À lire aussi</p>
    {minis}
   </div>
  </aside>
 </div>
</section>
</article>
<section class="section section--sand">
 <div class="container">
  <div class="mag-bar"><div><span class="eyebrow">Continuer la lecture</span><h2>Articles similaires</h2></div><a class="btn btn--ghost" href="/category/{c["slug"]}/">Tous les articles {c["name"]} {I("arrow")}</a></div>
  <div class="post-grid">{"".join(card(q) for q in related)}</div>
 </div>
</section>
{INC_CTA}
<script>window.TL_KNOWN={json.dumps(known)};</script>
<script>(function(){{var b=document.querySelector('.read-progress'),a=document.querySelector('article');if(!b||!a)return;function u(){{var r=a.getBoundingClientRect(),h=a.offsetHeight-innerHeight;b.style.transform='scaleX('+Math.min(1,Math.max(0,-r.top/(h>0?h:1)))+')';}}addEventListener('scroll',u,{{passive:true}});u();}})();</script>'''
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": U(p["h1"]), "description": U(p["ds"]),
              "image": p["og"] or p["img"], "datePublished": p["d"], "author": {"@type": "Organization", "name": "Travelife"},
              "publisher": {"@type": "Organization", "name": "Travelife", "logo": {"@type": "ImageObject", "url": "https://travelife.ma/wp-content/uploads/2024/10/logo-travelife-2024.png"}},
              "mainEntityOfPage": f"https://travelife.ma/{p['s']}/"}
        write(f"post-{p['s']}", {"path": f"{p['s']}/", "nav": "blog", "title": U(p["t"]), "desc": U(p["ds"]),
            "canonical": f"https://travelife.ma/{p['s']}/", "og": p["og"] or p["img"], "ogtype": "article",
            "crumbs": [["Blog", "/articles/"], [c["name"], f"/category/{c['slug']}/"], [U(p["h1"]), f"/{p['s']}/"]],
            "ld": [ld], "scripts": ["/assets/blog.js"]}, body)
    print(f"Blog : 1 index, {len(CATS)} catégories, {len(POSTS)} articles")

if __name__ == "__main__":
    main()

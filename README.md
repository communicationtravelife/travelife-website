# Site Travelife — refonte 2026 (FR · EN · AR · ES)

Nouveau site de **travelife.ma** : design moderne, 4 langues, SEO et GEO optimisés.

## Voir le site
Ouvrez `dist/index.html` dans votre navigateur (connexion internet nécessaire pour les images, les polices et les articles du blog).
- Français : `dist/index.html`
- English : `dist/en/index.html`
- العربية : `dist/ar/index.html`
- Español : `dist/es/index.html`

Le dossier **`dist/`** contient le site prêt à publier (à déposer sur Netlify, un hébergeur ou à intégrer dans WordPress).

## Organisation du projet
| Dossier / fichier | Rôle |
|---|---|
| `src/pages/` | Pages en français (source). La 1re ligne `<!--META … -->` contient le titre SEO, la description, l'URL et la canonical. |
| `src/partials/` | Blocs réutilisés (maquettes produit, bandeau logos, appel à l'action…). |
| `src/assets/` | `style.css` (design), `main.js` (menus, onglets, langue), `blog.js` (articles du blog). |
| `src/llms.txt` | Résumé de Travelife pour les moteurs IA (GEO). |
| `i18n/en`, `i18n/ar`, `i18n/es` | Traductions (un fichier JSON = textes traduits). `i18n/source.json` = textes français de référence. |
| `i18n.py`, `chrome_i18n.py` | URLs traduites, traduction du menu et du pied de page. |
| `data/posts.json` | Liste des 48 articles du blog (titres SEO, images, dates). |
| `build.py`, `gen_blog.py` | Scripts qui génèrent le site dans `dist/`. |
| `docs/` | Guides de design, de contenu/SEO et de traduction. |

## Régénérer le site après une modification
Nécessite Python 3 et BeautifulSoup (`pip install beautifulsoup4`) :
```bash
python gen_blog.py
python build.py
```
Version de démonstration non indexée par Google (à utiliser pour un lien de test) :
```bash
NOINDEX=1 DIST=demo python build.py
```

## SEO
- URLs françaises identiques au site WordPress actuel ; titres et méta-descriptions Rank Math conservés.
- Versions EN/AR/ES avec URLs traduites, balises `hreflang` + `x-default`, `sitemap.xml` multilingue.
- Données structurées : Organization, SoftwareApplication (tarifs), FAQPage, BreadcrumbList, BlogPosting.
- `robots.txt` (accès des robots IA autorisé) et `llms.txt`.

Contact : contact@travelife.ma · (+212) 5 21 50 06 05

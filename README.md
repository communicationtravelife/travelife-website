# Site web Travelife (travelife.ma)

Site 100 % statique : uniquement du **HTML, CSS et JavaScript**. Aucun Python, aucune installation, aucun outil à lancer.

## Contenu
- `index.html` et un dossier par page (ex. `logiciel-de-gestion-commerciale/index.html`) : version française, mêmes URL que le site WordPress actuel (référencement conservé).
- `en/`, `es/`, `ar/` : versions anglaise, espagnole et arabe (blog inclus).
- `assets/` : `style.css` (design) et `main.js` (menu, langues, zoom des images).
- `sitemap.xml`, `robots.txt`, `llms.txt` : référencement Google et moteurs IA.

## Voir le site
Les adresses sont propres (sans index.html), comme sur travelife.ma : elles fonctionnent sur un serveur web.
- En ligne : glissez le dossier sur https://app.netlify.com/drop.
- Sur l'ordinateur : VS Code > extension « Live Server » > clic droit sur index.html > Open with Live Server.

## Modifier un texte
Ouvrez le fichier `index.html` de la page concernée (dans chaque langue) avec un éditeur de texte (ex. VS Code ou Bloc-notes), modifiez le texte, enregistrez.
Ne modifiez pas les balises `<title>`, `<meta name="description">`, `<link rel="canonical">` et `hreflang` sans vérifier l'impact SEO.

## Mettre en ligne sur GitHub
```
git add -A
git commit -m "Mise à jour du site"
git push
```

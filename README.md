# Site web Travelife (travelife.ma)

Site 100 % statique : uniquement du **HTML, CSS et JavaScript**. Aucun Python, aucune installation, aucun outil à lancer.

## Contenu
- `index.html` et un dossier par page (ex. `logiciel-de-gestion-commerciale/index.html`) : version française, mêmes URL que le site WordPress actuel (référencement conservé).
- `en/`, `es/`, `ar/` : versions anglaise, espagnole et arabe (blog inclus).
- `assets/` : `style.css` (design) et `main.js` (menu, langues, zoom des images).
- `sitemap.xml`, `robots.txt`, `llms.txt` : référencement Google et moteurs IA.

## Redirections (référencement)
Les anciennes adresses WordPress (`/tag/…`, `/index.php/…`, `/tarifs/`, `/contact/`, pagination, flux RSS, archives par date, anciennes tailles d'images) sont redirigées en 301 vers les nouvelles pages :
- `.htaccess` : pour l'hébergeur actuel (LiteSpeed/Apache). Fichier caché : pensez à l'envoyer avec le reste.
- `_redirects` : pour Netlify ou Cloudflare Pages.
- `404.html` : page affichée pour toute adresse inconnue (non indexée par Google).

GitHub Pages ne lit aucun de ces fichiers : n'hébergez pas le site uniquement sur GitHub Pages.

## Statistiques, cookies et WhatsApp
- `assets/consent.js` (chargé sur toutes les pages) : bandeau cookies en 4 langues. Google Analytics (`G-YCP5KBSJG3`) et le Pixel Meta (`1167280197414116`) ne se chargent qu'après « Accepter ». Lien « Gérer les cookies » en bas de page.
- Bouton WhatsApp flottant : prêt mais désactivé. Pour l'afficher, renseignez le numéro dans `WHATSAPP` en haut de `assets/consent.js`.
- La balise de vérification Google Search Console se trouve dans `index.html`.

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

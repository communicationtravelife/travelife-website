# Refonte Travelife v2 — guide de design (à suivre strictement)

La cliente trouve la v1 trop banale. Objectif : un site **magnifique**, niveau Stripe / Linear / Mews : UI soignée, UX claire, rythme visuel varié, photos et maquettes produit. Le contenu existant de chaque page est déjà dans `src/pages/<page>.html` (v1) : c'est ta source de contenu (textes, H1, H2, FAQ, prix, logos). Tu dois **réécrire entièrement le HTML** de tes pages avec le nouveau design system.

Projet : /home/claude/travelife. Build : `DIST=/tmp/check_<nom> python3 build.py`.
LIS D'ABORD : `src/pages/home.html` (référence absolue du nouveau style), `src/assets/style.css` (toutes les classes), `src/partials/*.html` (maquettes produit réutilisables), puis ta page v1.

## Règles SEO (impératives, inchangées)
- Ligne 1 `<!--META {...} -->` : garder EXACTEMENT path, title, desc, canonical, og, crumbs de la v1. Tu peux ajouter `"dark":true` (hero sombre, header transparent sombre).
- UN SEUL `<h1>` (même texte que la v1). Garder les H2/H3 principaux (mots-clés) — reformulation légère autorisée, pas de suppression de sections de contenu importantes.
- FAQ : structure exacte `<div class="faq"><details><summary>Q</summary><div class="answer"><p>R</p></div></details>…</div>` (schema FAQPage auto). Onglets FAQ possibles (voir home : `.faq-tabs` + `.faq-group`). Mise en page conseillée : `.faq-layout` (colonne gauche titre + carte contact, droite accordéon).
- Liens internes en chemin racine `/slug/`. Prix, chiffres, noms de clients : ne rien inventer (les chiffres déjà présents sur le site sont OK : 200+ agences, 1 500+ compagnies, 500 000 hébergements, 90 % GO SIYAHA, 2013).
- Images : alt descriptifs en français, `loading="lazy"` sauf hero.

## Design system v2 (classes clés)
- Typo : titres Bricolage Grotesque ; mot d'accent en italique serif : `<span class="serif">mot</span>` (1 par titre max, pas partout). Variante dégradée sur fond sombre : `class="serif grad-text"`.
- Hero intérieur : préférer `section.page-hero.page-hero--dark` + META `"dark":true` pour les pages produits (avec `.container` > `ol.breadcrumb` > `.split` texte + visuel : maquette `{{inc:mock-…}}` ou photo dans `.hero-visual .frame` + `.chip-float` positionnés en `style="left:-20px;bottom:30px"`). Pages institutionnelles : `section.page-hero` clair (fond sable).
- Sections : `.section`, `.section--sand` (fond sable chaud), `.section--dark` (encre), `.section--sm`. Alterner blanc / sable / sombre pour le rythme. Jamais deux sections identiques à la suite.
- `.section-head` (eyebrow + h2 + p), `.section-head--left`.
- **Bento** : `.bento` (6 colonnes) + `.tile.span-2|3|4|6` ; variantes `.tile--sand`, `.tile--dark`, `.tile--violet`, `.tile--photo` (avec `<img class="bg">`), `.tile-visual` pour y glisser une mini-maquette. Excellent pour les listes de fonctionnalités.
- **Onglets fonctionnalités** : `.ftabs` > `.ftab-list` (`button.ftab` avec `<b>{{i:x}} Titre</b><span>texte</span>`, aria-selected) + `.ftab-panels` > `.ftab-panel` (hidden sauf le 1er) contenant une maquette. Le JS est déjà prêt.
- **Photo band** : `.photo-band` > `<img>` + `.inner` (h2, p, .btn-row) — grande photo immersive.
- Split image/texte : `.split` (+ `.split--reverse`), image dans `.media.media--photo` (photo) ou `.media` (capture d'écran produit), ajouter 1 `.float-card` pour la profondeur.
- `.stats` > `.stat` (b + span) ; `.steps` > `.step` (.num, h3, ul/p) ; `.timeline` ; `.testimonials` > `figure.quote` (+ `.quote--big`) ; `.pricing` > `.plan` (+ `.plan--featured` sombre, `.badge`, `.price`, `.price-note`, `.checklist`) ; `.table-wrap > table` ; `.logo-grid > .logo-cell > img` ; `.siyaha` (bloc 90 %) ; `.cta-band` via `{{inc:cta}}` en fin de page ; formulaires `.form-card` + `.form-grid` + `.field`.
- Cartes : `.card` (+ `.ico` / `.ico--o` avec `{{i:nom}}`), `.card--feature`. Éviter les murs de cartes identiques : max 6 cartes d'affilée, sinon bento ou onglets.
- `reveal` (+ `reveal-d1/d2/d3` pour décaler) sur les blocs.
- Icônes `{{i:nom}}` : arrow check phone mail pin erp globe network bot users handshake tag calc plane crm wallet plug file building chart shield cloud zap refresh lock clock trend search settings palette smartphone star book play moon whatsapp headset layers target rocket kaaba calendar.

## Maquettes produit réutilisables (partials)
`{{inc:mock-dashboard}}` (ERP tableau de bord), `{{inc:mock-booking}}` (moteur de réservation B2B vols), `{{inc:mock-site}}` (site B2C d'agence), `{{inc:mock-whatsapp}}` (téléphone, conversation Agent IA), `{{inc:mock-invoice}}` (facture TVA sur marge), `{{inc:partners}}` / `{{inc:partners-dark}}` (bandeau logos défilant). Tu peux créer d'autres maquettes inline dans ta page avec les classes `.mock`, `.mock-bar`, `.app-main`, `.app-top`, `.kpis/.kpi`, `.panel`, `.bk` (+ `.t`, `.t.o`, `.t.g`), `.st.ok/.wait/.new`, `.result`, `.site-search`, `.site-cards`. Ne pas modifier les partials existants.

## Photos (Unsplash, licence libre, vérifiées) — format d'URL :
`https://images.unsplash.com/photo-<ID>?auto=format&fit=crop&w=1600&q=75` (w=900 pour les tuiles)
- 1597212618440-806262de4f6b Marrakech, Koutoubia et Atlas enneigé
- 1538600838042-6a0c694ffab5 Chefchaouen, escaliers bleus
- 1489749798305-4fea3ae63d43 Kasbah et palmeraie
- 1510952267577-fc96d5ca660a Chameaux dans le désert
- 1489573280374-2e193c63726c Dunes du Sahara
- 1580746738099-1cb74f972feb Souk, épices
- 1549140600-78c9b8275e9d Arches marocaines ocre
- 1527605158555-853f200063e9 Hublot d'avion, coucher de soleil
- 1529947327457-8f5cb53bc1b6 Aile d'avion, nuages roses
- 1571003123894-1f0594d2b5d9 Piscine d'hôtel de luxe au coucher du soleil
- 1582719508461-905c673771fd Terrasse d'hôtel, transats
- 1540541338287-41700207dee6 Resort tropical, piscine
- 1627728734379-a5f8c099763e La Kaaba (Omra)
- 1553755088-ef1973c7b4a1 Kaaba et pèlerins
- 1580418827493-f2b22c0a76cb Tour de l'horloge, La Mecque
- 1522071820081-009f0129c71c Équipe autour d'ordinateurs
- 1521737852567-6949f3f9f2b5 Réunion d'équipe
- 1553775282-20af80779df7 Casque support client sur bureau
- 1504150558240-0b4fd8946624 Voyageur à l'aéroport (silhouette)
- 1530521954074-e64f6810b32d Voyageur détendu dans un salon d'aéroport
- 1532968899863-5b52ef155913 Hall d'aéroport lumineux
- 1516321318423-f06f85e504b3 Mains sur ordinateur portable
Les images existantes de travelife.ma : garder les vraies captures produit (tableau de bord, site B2C, guide) dans `.media` ; SUPPRIMER les illustrations vectorielles génériques (personnages, cliparts 3D « new-size-travelife-post », « illustration-22 », « anim-icon »), remplacées par des maquettes ou photos. Les logos partenaires/clients restent.

## Vérification visuelle obligatoire
`DIST=/tmp/check_<nom> python3 build.py`, puis `cd /home/claude/travelife && python3 shots.py 1366 "<path1>/,<path2>/" <dossier>` et `python3 shots.py 390 ...` — attention shots.py lit dans `dist/` : lance d'abord aussi `python3 build.py` (sans DIST) si tu veux utiliser shots.py, c'est sans risque. Les photos y apparaissent en dégradé (placeholder), les polices sont réelles. Regarde les captures (outil Read, en recadrant avec PIL si besoin) et corrige : pas de débordement horizontal (le script le signale), alignements, hiérarchie, espaces. Itère jusqu'à ce que ce soit beau.

Réponse finale : fichiers modifiés + 3-5 lignes sur les choix de design + tout point de vigilance.

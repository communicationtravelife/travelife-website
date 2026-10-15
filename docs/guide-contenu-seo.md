# Mission v3 : restaurer, enrichir le contenu et l'optimiser pour le SEO + GEO

Contexte : refonte du site travelife.ma (logiciel SaaS pour agences de voyages). Les pages refaites (src/pages/*.html) ont un beau design (à conserver) mais certains contenus du site en ligne ont été supprimés ou raccourcis (surtout les FAQ). La cliente veut : **aucune perte de contenu**, et un contenu enrichi qui améliore le référencement Google ET la visibilité dans les moteurs IA (GEO : ChatGPT, Perplexity, Google AI Overviews).

Projet : /home/claude/travelife. Lis : AGENT_GUIDE_V2.md (règles de design/SEO, toujours valables), src/assets/style.css (fin du fichier : composants `.tldr`, `.wf`), la page à traiter.

## Étape 1 — Comparer avec le site en ligne
Charge l'outil navigateur (ToolSearch "select:mcp__remote-devices__Claude_Browser__javascript_tool"), puis dans tabId "seed" (page https://travelife.ma/ ouverte) exécute le contenu de /home/claude/travelife/tools/extract.js (copie-le tel quel comme texte), puis `await ORIG('https://travelife.ma/<slug>/')` (pour l'accueil : `https://travelife.ma/`). Tu obtiens le contenu original (titres, paragraphes, listes, FAQ complètes, images). Si une page est très longue, tu peux faire `(await ORIG(url)).slice(0,40000)` puis la suite.
Compare avec la page actuelle et liste ce qui manque ou a été raccourci.

## Étape 2 — Restaurer
- **FAQ : toutes les questions du site en ligne doivent être présentes, avec leurs réponses COMPLÈTES** (texte d'origine intégral, corrigé des fautes ; tu peux l'enrichir mais pas le raccourcir).
- Tout paragraphe / argument / liste de fonctionnalités / information factuelle du site en ligne absent de la page doit être réintégré à un endroit logique, dans le design existant (sans casser la mise en page). Les textes purement décoratifs ou en doublon peuvent rester absents.
- Ne jamais inventer de chiffres, prix, noms de clients ou de partenaires. Faits sûrs : Travelife fondé en 2013, Casablanca, 200+ agences, 1 500+ compagnies aériennes, 500 000 hébergements, référencé Maroc PME / GO SIYAHA (jusqu'à 90 % financé), prix publiés sur les pages tarifs, distinctions : World Summit Awards (meilleure solution numérique Maroc), African Excellence Awards 2025 « Best Travel Agency Software Company – Morocco », téléphone (+212) 5 21 50 06 05, contact@travelife.ma.

## Étape 3 — Enrichir pour le SEO et le GEO
1. **FAQ enrichie** : ajoute 3 à 6 nouvelles questions pertinentes que se posent réellement les agences (formulées comme dans une recherche Google / une question à ChatGPT, avec le mot-clé de la page), réponses de 60 à 120 mots, factuelles, qui commencent par une réponse directe (« Oui. », « Travelife coûte… », « Comptez… ») puis détaillent. Uniquement des informations vraies et déductibles du contenu du site.
2. **Bloc « L'essentiel »** (GEO) juste après le hero de chaque page commerciale, avec le composant `.tldr` :
   `<section class="section--sm"><div class="container"><div class="tldr reveal"><h2>L’essentiel <small>…sous-titre court…</small></h2><ul><li><b>Fait clé :</b> phrase factuelle autonome…</li>…(4 à 6 puces)</ul></div></div></section>`
   Chaque puce = une affirmation autonome, précise, citable telle quelle par une IA (sujet explicite « Travelife… », pas de « il/elle »). Pas sur les pages légales.
3. Vérifie que la page contient au moins une fois, naturellement, l'expression-clé principale (déduite du title) dans le H1 ou le premier paragraphe, et dans un H2.
4. Garde un seul H1, les META inchangées, la structure FAQ exacte (`<div class="faq"><details><summary>…</summary><div class="answer"><p>…</p></div></details>`) — le schema FAQPage est généré automatiquement.

## Vérification
`DIST=/tmp/check_<nom> python3 build.py` (sans erreur) ; vérifie 1 seul `<h1>`, aucun `{{` restant, et fais une capture desktop + mobile de tes pages avec une copie de shots.py lisant ton dossier DIST (ne touche pas à dist/). Ne modifie que tes pages (pas style.css, build.py, partials).
Réponse finale (courte) : par page, nb de questions FAQ avant → après, contenus restaurés, ajouts.

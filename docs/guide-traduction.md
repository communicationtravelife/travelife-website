# Guide de traduction — site Travelife (FR → EN / AR / ES)

Travelife (Casablanca, depuis 2013) édite un logiciel SaaS / ERP cloud pour agences de voyages et tour-opérateurs : ERP « Manage », site web B2C, plateforme de réservation B2B, SmartCRM & Agent IA WhatsApp, module Omra/Hajj. Cible : agences de voyages au Maroc, en Afrique, au Moyen-Orient, en Europe et en Amérique latine.

## Fichier à traduire
Entrée : `/home/claude/travelife/i18n/chunks/cN.json` = objet `{ "<clé>": "<texte FR>" }`.
Sortie : `/home/claude/travelife/i18n/<lang>/cN.json` = **mêmes clés**, valeur = traduction. JSON valide (UTF-8, guillemets échappés `\"`). Aucune clé manquante, aucune clé ajoutée.
Écris le fichier par morceaux si nécessaire (par ex. plusieurs fichiers `cN_a.json`, `cN_b.json` dans le même dossier `i18n/<lang>/` — tous les .json du dossier sont fusionnés), puis valide avec : `python3 -c "import json;a=json.load(open('i18n/chunks/cN.json'));import glob;b={};[b.update(json.load(open(f))) for f in glob.glob('i18n/<lang>/cN*.json')];print(len(a),len(b),set(a)-set(b))"` → l'ensemble des clés manquantes doit être vide.

## Règles de forme (impératives)
- Les valeurs contiennent parfois du HTML : **conserve exactement toutes les balises, attributs, classes, href, src, style** et les jetons `{{i:nom}}` / `{{inc:nom}}` (ne pas traduire, ne pas déplacer à l'intérieur/extérieur d'une balise sauf si la grammaire l'impose ; tu peux réordonner des balises inline entières si l'ordre des mots change). Traduis uniquement le texte visible ET les attributs `alt`, `aria-label`, `title`, `placeholder` présents dans le fragment.
- Ne traduis pas : Travelife, Manage, SmartCRM, GO SIYAHA, Maroc PME, noms de marques/partenaires (Amadeus, Sabre, Hotelbeds, WhatsApp…), noms de personnes, emails, numéros de téléphone, prix (199 €, 1 500 €, MAD…) — adapte seulement le format des nombres à la langue (EN : 1,500 € ; ES : 1.500 € ; AR : chiffres occidentaux 1500، € ou MAD conservés). Noms de villes : forme usuelle de la langue (Casablanca, Marrakech / مراكش…).
- Les espaces insécables ` ` du français (avant ? ! : ;) n'ont pas lieu d'être en EN/ES/AR : supprime-les.
- Garde la même longueur approximative (titres courts restent courts : boutons ≤ 4 mots si possible).
- Les valeurs qui sont uniquement un nom propre/une marque/un nombre restent identiques.

## Qualité & ton
Traduction native, marketing B2B professionnelle, naturelle (pas mot à mot), cohérente d'un bout à l'autre. Tutoiement interdit : EN « you », ES « usted » (vous), AR : arabe standard moderne (فصحى) clair, adapté aux professionnels marocains et du Golfe.

## Glossaire
| FR | EN | ES | AR |
|---|---|---|---|
| agence de voyages | travel agency | agencia de viajes | وكالة الأسفار / وكالات الأسفار |
| logiciel de gestion (commerciale) | (travel agency) management software | software de gestión (comercial) | برنامج إدارة (تجارية) |
| tour-opérateur | tour operator | turoperador | منظم الرحلات |
| agence réceptive (DMC) | DMC / inbound agency | agencia receptiva (DMC) | وكالة الاستقبال (DMC) |
| TVA sur marge | VAT on margin (margin scheme) | IVA sobre el margen | الضريبة على القيمة المضافة على الهامش |
| devis / proforma | quote / proforma | presupuesto / proforma | عرض سعر / فاتورة شكلية |
| facture / avoir | invoice / credit note | factura / nota de crédito | فاتورة / إشعار دائن |
| dossier (client) | booking file | expediente | ملف الحجز |
| règlement / encaissement | payment / collection | pago / cobro | تسوية / تحصيل |
| Demander une démo | Book a demo | Solicitar una demo | اطلب عرضاً توضيحياً |
| démonstration gratuite | free demo | demostración gratuita | عرض توضيحي مجاني |
| Agent IA | AI Agent | Agente IA | وكيل الذكاء الاصطناعي |
| Omra / Hajj | Umrah / Hajj | Umrah / Hajj | العمرة / الحج |
| plateforme B2B | B2B platform / portal | plataforma B2B | منصة B2B |
| site web B2C | B2C website | web B2C | موقع B2C |
| GDS | GDS | GDS | أنظمة التوزيع العالمية (GDS) |
| hébergements | accommodations / hotels | alojamientos | أماكن الإقامة |
| L’essentiel | Key facts | Lo esencial | أهم ما يجب معرفته |

## SEO (très important)
Les clés listées dans `i18n/chunks/meta_keys.json` sont des balises `<title>` (META-TITLE) et meta descriptions (META-DESC). Pour elles, **n'écris pas une traduction littérale** : rédige un title optimisé (≤ 60 caractères, mot-clé principal au début, « | Travelife » à la fin si la place le permet) et une description persuasive de 140 à 155 caractères avec le mot-clé et un appel à l'action.
Mots-clés principaux : EN « travel agency software », « travel agency management software », « B2B booking system », « travel agency website », « Umrah software » ; ES « software para agencias de viajes », « programa de gestión para agencias de viajes », « sistema de reservas B2B », « página web para agencia de viajes » ; AR « برنامج إدارة وكالات الأسفار », « نظام حجز B2B », « موقع إلكتروني لوكالة أسفار », « برنامج إدارة العمرة ».
Dans le corps du texte, utilise naturellement ces expressions là où le français utilise l'équivalent (« logiciel pour agence de voyage », etc.). Les questions de FAQ doivent ressembler à de vraies recherches dans la langue cible.

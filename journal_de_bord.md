# Journal de bord

Pour chaque séance, avec la date : ce qu'on a fait et pourquoi, les problèmes rencontrés, les solutions testées (et pourquoi certaines n'ont pas marché), l'utilisation de l'IA (prompt, pourquoi, ce qu'on en a fait).
Chacune écrit ses propres entrées, en indiquant son prénom.

---

## 24/10/2026 — Amel

**Ce qu'on a fait et pourquoi**
- Lecture des consignes du projet.
- Choix du dataset « Données temps réel de mesure des concentrations de polluants atmosphériques réglementés » (data.gouv.fr, LCSQA). Pourquoi : gros volume (un fichier par jour d'environ 50 000 lignes), données réelles et actuelles, beaucoup de choses à nettoyer.
- Téléchargement de toute l'année 2025 (365 fichiers CSV, 3,7 Go) pour pouvoir étudier les saisons, et des fichiers de métadonnées (stations, zones).

**Problèmes rencontrés**
- La page data.gouv propose 11 ressources (CSV, XML, Excel, guides européens) : il a fallu trier ce qui était utile.
- Les données sont découpées en un fichier par jour.

**Utilisation de l'IA**
- Prompt (Claude Code) : « Analyse les documents qui décrivent le projet sur lequel on doit travailler. On a choisi d'utiliser la base de données suivante : [lien]. Je voudrais que tu nous dises quels fichiers de cette base de données sont intéressants pour nous et à quoi ils correspondent. Je voudrais que tu stockes ces fichiers dans un dossier data en les renommant en fonction de leur utilité. Ne modifie pas le contenu des fichiers pour l'instant. Enfin dis-nous comment nous y prendre pour le projet. »
- Pourquoi : gagner du temps sur le tri des ressources et comprendre la structure du dataset.
- Ce qu'on en a fait : relecture des fichiers retenus et de leur description (data/README.md), vérification sur un fichier ouvert dans Python.

## 26/10/2026 — Amel

**Ce qu'on a fait et pourquoi**
- Vérification que le découpage en un fichier par jour n'est pas un problème : les 365 fichiers ont les mêmes colonnes et chaque fichier ne contient que son jour → on pourra les concaténer.
- Compréhension du rôle des fichiers de métadonnées (stations, zones) et de la façon de les relier aux mesures (`code site` ↔ `NatlStationCode`, `code zas` ↔ `ZoneCode`).

**Problème identifié et solution prévue**
- 17,6 millions de lignes : trop pour être chargées d'un coup. Solution prévue : lire les fichiers un par un dans une boucle, les nettoyer et les réduire à une moyenne journalière avant de les concaténer.

## 03/11/2026 — Amel

- Mise en place du dépôt GitHub pour travailler à deux, d'un fichier d'avancement et d'une répartition des tâches avec Coura.
- Dataset validé par l'enseignante. Après discussion avec elle : idée d'ajouter au dashboard une carte de la France où l'on voit les informations selon l'endroit (une station = un point coloré selon la pollution).
- Amélioration du script de téléchargement (remarque de Claude 2) : il affiche maintenant les vraies erreurs (coupure de connexion) au lieu de les cacher, et efface un fichier à moitié téléchargé pour qu'il soit repris au lancement suivant.

## 03/11/2026 — Amel — Tâche A1 : description d'un fichier de mesures

**Ce qu'on a fait et pourquoi**
Script `scripts/01_exploration_mesures.py` : il ouvre le fichier du 1er janvier 2025 et le décrit avant tout nettoyage, pour savoir ce qu'il contient et repérer les problèmes. Fonctions utilisées : `read_csv`, `shape`, `head`, `dtypes`, `isna().sum()`, `unique()`, `min`/`mean`/`max`, `groupby`, `pd.concat`.

**Description des données (fichier du 1er janvier 2025)**
- **49 968 lignes et 23 colonnes.** Une ligne = la concentration moyenne d'un polluant pendant une heure, dans une station.
- **506 stations**, **70 zones de surveillance**, **17 organismes** (les associations régionales de surveillance, y compris l'outre-mer : Gwad'Air, Atmo Réunion, Madininair, Atmo Guyane), 56 procédures de mesure.
- **9 polluants** : NO, NO2, NOX (exprimé en NO2), O3, PM10, PM2.5, SO2, CO, C6H6 (benzène).
- **Nature des colonnes :**
  - texte (`object`) : dates, organisme, zone, station, typologie, polluant, unité, codes ;
  - nombres décimaux (`float64`) : `valeur`, `valeur brute` (et 3 colonnes vides) ;
  - entier (`int64`) : `validité`.
- **Catégories :**
  - type d'implantation : Urbaine, Périurbaine, Rurale régionale, Rurale près des villes, Rurale nationale ;
  - type d'influence : Fond, Trafic, Industrielle ;
  - type d'évaluation : mesures fixes, mesures indicatives, estimation objective ;
  - code qualité : A, R, N ; validité : 1, -1, 4 ;
  - `Réglementaire` vaut toujours « Oui » et `type de valeur` toujours « moyenne horaire validée » → ces colonnes n'apportent pas d'information.

**Problèmes repérés (à traiter dans le nettoyage, tâche A2)**
- **Données manquantes** : `taux de saisie`, `couverture temporelle`, `couverture de données` sont vides sur les 49 968 lignes → colonnes à supprimer. `valeur` et `valeur brute` manquent sur 2 034 lignes (4 %). `discriminant` est vide sur 6 696 lignes (normal, il ne sert que si une station a plusieurs appareils pour le même polluant).
- **Dates stockées en texte** (`2025/01/01 00:00:00`) → à convertir en dates.
- **Unités** : `µg-m3` et `µg/m3` veulent dire la même chose ; le CO est en `mg-m3` (1 mg = 1 000 µg).
- **Valeurs négatives** pour tous les polluants sauf le benzène (minimum -4,5) : une concentration ne peut pas être négative. Ce sont sans doute de petites erreurs des appareils quand la concentration est presque nulle → à décider : les supprimer ou les mettre à 0.
- **Valeurs très élevées** : PM10 jusqu'à 304,6 µg/m³ et NOX jusqu'à 537 µg/m³. Le 1er janvier, ça peut venir des feux d'artifice et des feux de la nuit du Nouvel An → à vérifier avant de les traiter comme des erreurs.
- **Texte** : `discriminant` mélange majuscules et minuscules (`I` et `i`, et un `j` minuscule) → à vérifier s'il faut les harmoniser.

## 03/11/2026 — Coura

**Ce qu'on a fait et pourquoi**
- Mise en place : copie du dépôt GitHub sur mon ordinateur, configuration de git (nom, e-mail), vérification que je peux envoyer mes modifications sur le dépôt.
- Répartition validée avec Amel : C1 et C2 maintenant, puis C3, C4 et C5. La carte interactive (A6), proposée après la validation du dataset, sera faite par Amel.
- **Tâche C1** : script `scripts/03_metadonnees.py` qui nettoie les deux fichiers de métadonnées et produit `data_clean/stations.csv` (546 stations) et `data_clean/zones.csv` (71 zones). Pourquoi : ces fichiers serviront à relier chaque mesure à un lieu (coordonnées, commune, type de zone, population) pour la carte et l'analyse par lieux.
  - Stations : 9 colonnes gardées sur 17 ; aucun doublon ; codes vérifiés avec une expression régulière ; typologie extraite des adresses web (`.../urban` → `urban`) ; accents retirés des noms de communes (597 → 583 communes : 14 étaient écrites de deux façons) ; coordonnées vérifiées et colonne `territoire` (métropole / outre-mer) ajoutée ; 332 stations fermées avant 2025 (ou ouvertes après) supprimées.
  - Zones : codes vérifiés, type de zone (agglomération, zone à risque, zone régionale) lu dans le code, densité de population calculée.

**Problèmes rencontrés et solutions**
- Deux stations portent parfois le même nom (ex : PASTEUR à Donges et à Chambéry) → codes et villes différents : ce ne sont pas des doublons, on les garde.
- Latitudes négatives et longitudes jusqu'à 55 → ce ne sont pas des erreurs : ce sont les stations des DROM (vérifié en affichant les communes hors d'un rectangle autour de la métropole).
- Les noms des zones écrivent « ZR » ou « ZRE » pour le même type de zone → on lit le type dans le code de la zone, qui est plus fiable.
- La population des zones date du recensement de 2018 → limite à signaler à l'oral.
- Claude n'a pas pu lancer le téléchargement des données (accès à data.gouv.fr bloqué depuis son environnement) → je le lancerai moi-même depuis Anaconda Prompt.
- À vérifier en phase 2 : que toutes les stations des mesures 2025 font partie des 546 stations gardées.

**Utilisation de l'IA**
- Outil : Claude (« Claude 2 »), relié à mon ordinateur.
- Prompt : le prompt de démarrage préparé avec Amel (fichier `PROMPT_CLAUDE_COURA.md`), en résumé : « Fais la mise en place (git, Python, clone du dépôt), lis les fichiers du projet et respecte les règles de CLAUDE.md, réponds à Claude 1 dans CONVERSATION_CLAUDE.md, explique-moi où en est le projet et mes tâches, puis on commence ensemble la tâche C1 en ne travaillant que sur mes fichiers. »
- Pourquoi : gagner du temps sur l'installation et la coordination avec Amel, et avoir une première version du script C1 expliquée étape par étape pour l'oral.
- Ce qu'on en a fait : Claude a écrit et testé le script C1 et me l'a expliqué. Il me reste à le relire et à le lancer moi-même avant de valider la tâche.

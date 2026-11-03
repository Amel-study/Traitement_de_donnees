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
- Ce qu'on en a fait : Claude a écrit et testé le script C1 et me l'a expliqué étape par étape.
- Deuxième prompt : « plus besoin de vérification, passe directement au C2 et regarde ce que Claude 1 a dit ». Claude a fait des recherches sur le web pour les seuils, puis a rédigé `docs/variables_et_graphiques.md` en citant les sources.

**Données manquantes des métadonnées (classement vu au cours 3 : MCAR / MAR / MNAR)**
- Stations, `ActivityEnd` vide pour 510 stations : la date de fin manque parce que la station n'est pas encore fermée. Le fait qu'elle manque dépend donc de la valeur elle-même → **MNAR** (manque « structurel »). On ne remplace rien : une case vide veut dire « station encore ouverte ».
- Zones, `EndTime` vide pour les 71 zones : même raison (zones toujours en vigueur) → MNAR. `ReportingBegin` / `ReportingEnd` sont vides partout : colonnes jamais remplies dans ce fichier → supprimées.
- Aucune autre valeur manquante dans les colonnes gardées : pas de cas MCAR ou MAR dans les métadonnées.

**Tâche C2** (`docs/variables_et_graphiques.md`)
- Liste des variables clés (concentration, polluant, date → mois / saison / jour, type d'influence, région = AASQA, territoire, population et densité de la zone).
- 14 graphiques et tableaux prévus, chacun relié à une question et à une tâche (A4, C4, C5, A6), en plotly express (cours 3).
- Tableau des seuils par polluant : recommandations OMS 2021, valeurs réglementaires UE / France en vigueur en 2025, seuils d'information et d'alerte, nouvelles valeurs UE 2030, avec les sources.
- Problème : certains seuils demandent des moyennes glissantes sur 8 h (ozone, CO) ou des heures consécutives, ce qu'on n'a pas vu en cours → présentés comme une limite. Les seuils horaires pourront être vérifiés jour par jour grâce à la colonne `max horaire` d'Amel.
- Le CO est converti en µg/m³ dans nos fichiers nettoyés → ses seuils en mg/m³ sont multipliés par 1 000.

**Téléchargement des données et passage à l'année complète**
- Je n'arrivais pas à ouvrir Anaconda → j'ai lancé le Python d'Anaconda directement depuis l'invite de commandes Windows (`C:\Users\coura\anaconda3\python.exe scripts\telecharger_donnees.py`).
- Premier lancement : 359 fichiers sur 365. Six jours (11 au 14 août, 6 et 7 décembre) ont échoué à cause d'une coupure de ma connexion internet (message « getaddrinfo failed »). Le script efface les fichiers incomplets, donc un deuxième lancement a récupéré les 6 manquants.
- Lancement du script d'Amel `04_annee_complete.py` sur mon ordinateur : mêmes résultats que chez elle (706 235 lignes journalières, 516 stations).

**Tâche C3** (`scripts/05_fusion.py`)
- Fusion des mesures journalières avec `stations.csv` (sur `code site`) puis avec `zones.csv` (sur `code zas`) grâce à `pd.merge(..., how="left")`. Pourquoi : chaque mesure a maintenant ses coordonnées, sa commune, sa typologie, le type et la population de sa zone.
- Vérifications : même nombre de lignes avant et après (706 235), aucune mesure sans station, sans zone ou sans région. On a choisi `how="left"` plutôt que `inner` pour pouvoir prouver qu'aucune mesure n'est perdue.
- Colonne `nom site` supprimée : 22 stations changent de nom en cours d'année, on garde le nom unique de `stations.csv`.
- Colonnes ajoutées : `region` (dictionnaire organisme → région), `mois`, `saison` (même découpage qu'Amel), `jour semaine`, `week-end`.
- Contrôle de cohérence entre deux colonnes liées : la colonne `territoire` (calculée en C1 à partir des coordonnées GPS) donne « outre-mer » exactement pour les 5 organismes des DROM. Les deux sources sont d'accord.
- Problème : le script met environ 2 minutes à cause de la taille du fichier (167 Mo) → rien à corriger, il ne se lance qu'une fois.

## 03/11/2026 — Amel — Tâche A2 : nettoyage d'un fichier de mesures

**Ce qu'on a fait et pourquoi**
Script `scripts/nettoyage_mesures.py` avec deux fonctions, pour pouvoir les réutiliser sur les 365 jours (A3) :
- `verifier_mesures(mesures)` : fait les contrôles et affiche ce qu'elle trouve, sans rien modifier ;
- `nettoyer_mesures(mesures)` : renvoie une copie nettoyée.

Le fichier s'appelle `nettoyage_mesures.py` (et non `02_...`) car Python ne peut pas importer un fichier dont le nom commence par un chiffre.

**Contrôles (consigne point par point), sur le 1er janvier**
- *Textes / format des codes* (expressions régulières) : tous les `code site` suivent le format `FR` + 5 chiffres, tous les `code zas` le format `FR44ZAG02` → OK. 312 lignes avaient des noms de station avec un espace en trop à la fin (`"Troyes La Tour "`).
- *Colonnes liées* : la date de fin est toujours la date de début + 1 h → la colonne `Date de fin` est inutile. Chaque code de station a un seul nom. Deux noms (« PASTEUR », « SAINT EXUPERY ») sont utilisés par deux stations différentes : c'est normal (deux villes différentes), il faut donc toujours identifier une station par son code, pas par son nom.
- *Validité et code qualité* (tableau de contingence avec `groupby`) : `N` correspond toujours à `validité = -1` (invalide) ; `A` = donnée vérifiée valide ; `R` = donnée brute (pas encore vérifiée) valide ; `validité = 4` n'existe que pour l'ozone (valide aussi).
- *Données manquantes* : les 2 034 lignes sans valeur sont exactement les lignes invalides.
- *Valeurs aberrantes* : 1 097 valeurs négatives (surtout NO et SO2, jusqu'à -4,5). Méthode de l'IQR (au-dessus de Q3 + 1,5 × IQR) : 6 à 7 % des valeurs de PM10 et de NO2 sont « hautes ».

**Choix de nettoyage**
1. Suppression des lignes invalides (`validité = -1`) : elles n'ont pas de valeur, on ne peut rien en faire. → 47 934 lignes.
2. Suppression des **doublons cachés** : une station (FR18058) envoie ses mesures de PM10 et PM2.5 deux fois, même appareil, même heure, même valeur, mais avec un `discriminant` différent. `drop_duplicates` sur toutes les colonnes ne les voyait pas ; on cherche les doublons sur (station, polluant, heure, appareil, valeur). → 47 886 lignes. Le 15 juillet, il n'y en a pas.
3. Suppression de 8 colonnes : 3 vides, `Réglementaire` et `type de valeur` (toujours la même valeur), `valeur brute` (diffère de `valeur` de 0,05 au plus, c'est juste l'arrondi), `Date de fin` (toujours début + 1 h) et `procédure de mesure` (détail technique). → 15 colonnes.
4. Espaces en trop enlevés dans les noms de stations (`strip`).
5. **Normalisation des unités** : le CO est converti de mg/m³ en µg/m³ (× 1 000) et l'unité s'écrit partout `µg/m3` (avant : `µg-m3` ou `µg/m3`). Tous les polluants sont maintenant dans la même unité.
6. Valeurs négatives mises à 0 : l'appareil se trompe légèrement quand l'air est presque propre, la vraie valeur est proche de 0. Les supprimer aurait fait monter les moyennes à tort.
7. La date devient une vraie date (`pd.to_datetime`) au lieu d'un texte.

**Choix de ne pas faire**
- On **ne supprime pas** les valeurs repérées par l'IQR : la pollution a des pics réels (heures de pointe, Nouvel An avec les PM10 à 304 µg/m³), ce ne sont pas des erreurs. Les AASQA les ont d'ailleurs marquées comme valides. On vérifiera en A3, sur l'année entière, s'il existe des valeurs vraiment impossibles.
- `discriminant` (mélange `I` / `i`) n'est pas modifié : c'est juste un identifiant d'appareil, et aucune station n'a à la fois `I` et `i` pour le même polluant.
- Les heures restent en temps universel pour l'instant (à traiter en A4 pour le profil sur une journée).
- Pas de normalisation de type min-max : on veut comparer les vraies concentrations aux seuils réglementaires.

**Résultat** : 1er janvier : 49 968 → 47 886 lignes, 23 → 15 colonnes, 0 valeur manquante (sauf `discriminant`), une seule unité. Durée : 0,2 s par fichier, donc environ 1 min 30 pour les 365.

## 03/11/2026 — Amel — Cours 3 et tâche A3 : passage à l'année complète

**Cours 3**
Ajout du chapitre 3 (data cleansing, graphiques plotly, Streamlit) à la liste de ce qui a été vu en cours (CLAUDE.md), pour que les deux Claude l'utilisent.

**Classement des données manquantes (cours 3 : MCAR / MAR / MNAR)**
Les valeurs manquantes des mesures sont les mesures invalides (`validité = -1`). Elles viennent des appareils (panne, maintenance, calibration) et pas de la valeur de la pollution elle-même : elles sont plutôt **MCAR** ou **MAR** (liées à une station ou à une période de maintenance), pas MNAR. On ne les remplace pas par une moyenne (`fillna`) : sur une heure isolée ce serait inventer une mesure ; on les supprime et on vérifie qu'il reste assez d'heures pour calculer la moyenne du jour (voir plus bas).

**Ce qu'on a fait et pourquoi (A3)**
Script `scripts/04_annee_complete.py` : une boucle sur les 365 fichiers (noms construits avec une f-string, `try/except` pour les dates qui n'existent pas). Pour chaque jour :
1. lecture du fichier et nettoyage avec la fonction `nettoyer_mesures` de A2 (importée) ;
2. réduction à **une ligne par jour, par station et par polluant** avec `groupby` : moyenne, maximum horaire et nombre d'heures mesurées ;
3. pour janvier et juillet seulement, on garde aussi le détail heure par heure (6 colonnes) pour étudier l'évolution sur une journée (A4).
À la fin, `pd.concat` met les 365 jours bout à bout et `to_csv` enregistre les résultats dans `data_clean/`.

**Problème résolu** : 17,6 millions de lignes ne tiennent pas en mémoire d'un coup. En traitant un jour à la fois et en réduisant chaque jour à environ 1 950 lignes, on n'a jamais plus d'un fichier brut en mémoire.

**Résultats**
- 365 jours lus, 17 597 676 lignes brutes → 16 983 009 après nettoyage → **706 235 lignes journalières** (12 colonnes), 516 stations.
- 11 022 moyennes journalières calculées sur **moins de 18 heures** ont été enlevées : la règle européenne demande au moins 75 % des heures du jour pour qu'une moyenne journalière soit valable.
- 2 901 453 lignes horaires pour janvier et juillet.
- Durée : 2 min 50.

**Vérification des valeurs extrêmes sur l'année entière**
Les maximums horaires sont élevés : benzène 180 µg/m³, CO 18 047 µg/m³ (18 mg/m³), PM10 1 160 µg/m³, SO2 873 µg/m³. Après vérification, ils sont presque tous **explicables**, on les garde :
- benzène, SO2, CO : stations **industrielles** (Martigues-Lavera et Berre près des raffineries de l'étang de Berre, Lacq, Grande-Synthe près de l'aciérie) ;
- PM10 : pics le **24 décembre** (Mayotte, Saint-Quentin) et le 31 décembre, soirées de fêtes ;
- ce sont des pics d'**une heure** : les moyennes journalières restent bien plus basses (ex. Ajaccio : 18 mg/m³ de CO sur une heure, mais 1 mg/m³ en moyenne sur la journée).
Un seul cas est douteux (CO à Ajaccio, station trafic) : on le signale mais on le garde, car il a été validé par l'organisme et il n'influence presque pas la moyenne du jour.

**Autres découvertes**
- 22 stations **changent de nom** en cours d'année (ex. « ECOLE M.JACQUIER » devient « Toulouse École m. Jacquier ») → il faut toujours identifier une station par son code.
- Le `type d'influence` dépend du polluant mesuré, pas seulement de la station (ex. une même station est « Industrielle » pour le SO2 et « Fond » pour l'ozone).
- 3 stations ont changé de `type d'implantation` en mai (Rurale près des villes → Périurbaine).
- Les jours sont découpés en heure TU (temps universel), pas en heure française.

## 03/11/2026 — Amel — Tâche A4 : analyse dans le temps

**Ce qu'on a fait et pourquoi**
Script `scripts/06_analyse_temps.py` (15 s). Il lit les fichiers de A3, calcule des tableaux (`describe`, `groupby`, `pivot_table`) et trace 7 graphiques avec **plotly express** (`px.line`, `px.bar`, `px.box`), enregistrés en `.html` dans `resultats/`. On étudie surtout les 4 polluants principaux (NO2, O3, PM10, PM2.5), qui ont le même ordre de grandeur.

**Choix et problèmes**
- **Heure française** : les heures sont en temps universel en métropole. Pour le profil sur une journée, on ajoute 1 h en janvier (heure d'hiver) et 2 h en juillet (heure d'été), avec `pd.Timedelta`. Les stations d'outre-mer sont enlevées de ce graphique (leurs heures sont déjà locales et leur climat est différent), grâce à la liste de leurs organismes et à `isin`.
- **Trafic / fond** : on compare la **moyenne annuelle de chaque station** plutôt que toutes les moyennes journalières. Une station = un point, le boxplot reste lisible.
- Les graphiques `.html` ne sont pas envoyés sur GitHub (5 Mo chacun) : on les recrée en lançant le script.

**Résultats**
1. **Statistiques par polluant** (moyennes journalières, µg/m³) : NO2 moyenne 13,4 (médiane 10,5) ; O3 55,4 ; PM10 15,4 ; PM2.5 8,9. Pour presque tous les polluants, la moyenne est au-dessus de la médiane : il y a quelques jours très pollués qui tirent la moyenne vers le haut (distribution asymétrique, cours 1).
2. **Saisons** : le NO2 et les particules sont plus élevés **en hiver** (NO2 17,8 en février contre 9,5 en juillet ; PM2.5 14,0 en février contre 5,1 en septembre) : chauffage, et l'air froid garde la pollution près du sol. L'**ozone** est au contraire plus élevé **au printemps et en été** (71,5 en juin contre 34,9 en décembre) : il se forme sous l'effet du soleil.
3. **Jour de la semaine** : le NO2 baisse nettement le **dimanche** (10,4 contre 14,9 le vendredi), car il y a moins de circulation. L'ozone ne baisse pas.
4. **Profil sur une journée** (heure française) : en janvier, le NO2 a **deux pics, à 8 h (23,7) et à 18 h (26,7)**, les heures de pointe. En juillet, l'ozone monte toute la journée et atteint son maximum **vers 15-17 h (88)**, quand le soleil est le plus fort, puis redescend la nuit.
5. **Trafic / fond** : les stations **trafic** ont deux fois plus de NO2 que les stations de fond (21,7 contre 10,7 en moyenne annuelle) ; l'écart est plus petit pour les PM10 (19,3 contre 14,2) et très faible pour les PM2.5 (9,7 contre 8,7), qui viennent aussi du chauffage et voyagent plus loin. L'ozone n'est presque mesuré qu'en stations de fond.

## 03/11/2026 — Amel — Vérifications pour Coura et ajout du graphique des saisons

- À la demande de Coura (son Claude ne peut pas télécharger les données) : on a lancé son script `03_metadonnees.py` sur nos données. Les **516 stations** des mesures 2025 sont toutes dans les 546 de `stations.csv`, et les 70 zones dans `zones.csv` : la fusion (C3) ne perdra aucune mesure. 30 stations de `stations.csv` n'ont aucune mesure en 2025.
- Relecture de la proposition de graphiques de Coura (C2) : G1, G3, G4 et G7 étaient déjà faits en A4. Ajout de **G5, boxplot par saison** (une station = un point, moyenne sur la saison). Médiane des stations (µg/m³) : NO2 16,1 en hiver contre 7,9 en été ; PM2.5 12,6 contre 7,3 ; O3 41,2 en hiver contre 69,0 en été. Ça confirme l'évolution par mois.

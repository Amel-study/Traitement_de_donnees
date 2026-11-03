# Avancement du projet

Légende : ✅ fait · 🔄 en cours · ⬜ à faire
Chacune met à jour **ses propres lignes** (statut + date). Les tâches communes se mettent à jour d'un commun accord.

## ✅ Déjà fait (Amel + Claude 1)

| Date | Quoi |
|---|---|
| 24/10/2026 | Lecture des consignes (présentation du projet, séances 1 et 2) |
| 24/10/2026 | Choix des fichiers utiles du dataset data.gouv, téléchargement de l'année 2025 (365 CSV, 3,7 Go, ~17,6 M lignes × 23 colonnes) + métadonnées stations et zones + note explicative, renommage, description dans [data/README.md](data/README.md) |
| 24/10/2026 | Premier profilage d'un fichier (1er janvier) : problèmes repérés (voir plus bas) |
| 26/10/2026 | Vérifications : les 365 fichiers ont les mêmes colonnes, chaque fichier ne contient que son jour (47 000 à 50 000 lignes), 100 % des stations et des zones des mesures se retrouvent dans les métadonnées |
| 03/11/2026 | Lecture des cours 1 et 2 et des TD → plan adapté au cours ; mise en place du GitHub, du script de téléchargement, de ce fichier et du fichier de conversation |

### Problèmes repérés dans les données (à traiter au nettoyage)

- Unité écrite de deux façons : `µg-m3` et `µg/m3` ; le CO est en `mg-m3`.
- Colonnes `taux de saisie`, `couverture temporelle`, `couverture de données` vides à 100 %.
- ~4 % de valeurs manquantes : elles correspondent à `validité = -1` et `code qualité = N` (données invalides).
- `discriminant` souvent vide (normal : sert seulement quand une station a plusieurs appareils pour le même polluant).
- Dates en texte (`2025/01/01 00:00:00`) → à convertir avec `pd.to_datetime`.
- Heures en temps universel (TU) en métropole : +1 h l'hiver, +2 h l'été pour l'heure française.
- Données en partie « brutes » (non vérifiées) → à signaler comme limite dans le rapport.
- Volume : impossible de tout charger d'un coup → traiter les fichiers un par un dans une boucle et réduire chaque jour (moyenne par station et par polluant).

## Répartition des tâches

Principe : chacune a **ses propres fichiers** pour ne pas se marcher dessus dans Git.

### Phase 1 — pour la séance 2

| # | Tâche | Qui | Fichier(s) | Statut |
|---|---|---|---|---|
| 0 | Faire valider le dataset par l'enseignante | Amel + Coura | — | ✅ 03/11 (validé ; idée de carte de France ajoutée, voir A6) |
| A1 | Décrire un fichier de mesures : nb de lignes / colonnes, sens des colonnes, types, valeurs des colonnes de catégories | Amel | `scripts/01_exploration_mesures.py` | ⬜ |
| A2 | Script de nettoyage d'un fichier de mesures (fonction `nettoyer_mesures(df)`) : manquantes, unités, doublons, aberrantes, intervalles, format des codes (regex), colonnes liées (date de fin = début + 1 h, validité ↔ code qualité, 1 code site = 1 nom), CO en mg | Amel | `scripts/02_nettoyage_mesures.py` | ⬜ |
| C1 | Explorer et nettoyer les métadonnées : onglet `AirQualityStations` (garder code, nom, commune, latitude, longitude, altitude, typologie ; transformer les URL du type `.../areaclassification/urban` en `urban` ; vérifier les coordonnées ; doublons ; stations fermées) et onglet `AirQualityZones` (code, nom, population, superficie). Sauver `data_clean/stations.csv` et `data_clean/zones.csv` | Coura | `scripts/03_metadonnees.py` | 🔄 03/11 : script écrit et testé (546 stations ouvertes en 2025, 71 zones), à relire par Coura |
| C2 | Proposer les variables clés et les graphiques / tableaux prévus ; chercher les seuils réglementaires (France / UE) et les recommandations OMS 2021 pour NO2, PM10, PM2.5, O3, SO2, CO, avec les sources | Coura | `docs/variables_et_graphiques.md` | ⬜ |
| J | Journal de bord : chacune écrit ses propres entrées, datées | Amel + Coura | `journal_de_bord.md` | 🔄 |

### Phase 2 — passage à l'année complète et analyse

| # | Tâche | Qui | Fichier(s) | Statut |
|---|---|---|---|---|
| A3 | Boucle sur les 365 fichiers : nettoyage (A2) + moyenne journalière par station et par polluant → `data_clean/mesures_journalieres_2025.csv` ; garder aussi les données horaires de janvier et juillet → `data_clean/mesures_horaires_janvier_juillet.csv` | Amel | `scripts/04_annee_complete.py` | ⬜ |
| C3 | Fusion des mesures avec les stations et les zones (`pd.merge`), ajout des colonnes mois / saison / jour de la semaine | Coura | `scripts/05_fusion.py` | ⬜ |
| A4 | Analyse : statistiques par polluant, évolution mensuelle, profil sur une journée (janvier / juillet), comparaison trafic / fond | Amel | `scripts/06_analyse_temps.py` | ⬜ |
| C4 | Analyse : comparaison des régions et des zones, dépassements de seuils (C2), tableaux de contingence, lien avec la population | Coura | `scripts/07_analyse_lieux.py` | ⬜ |

### Phase 3 — dashboard et oral (quand les graphiques et Streamlit auront été vus en cours)

| # | Tâche | Qui | Fichier(s) | Statut |
|---|---|---|---|---|
| A5 | Structure du dashboard Streamlit, filtres (polluant, région, période), pages | Amel | `app.py` | ⬜ |
| C5 | Graphiques du dashboard (histogrammes, boxplots, courbes) | Coura | `graphiques.py` | ⬜ |
| A6 | **Carte interactive de la France** (proposition, à confirmer) : un point par station, placé grâce à la latitude / longitude de `data_clean/stations.csv`, coloré selon la concentration moyenne ; filtres polluant / période ; infos au survol (nom, commune, type, valeur moyenne, nb de jours de dépassement) ; métropole et outre-mer séparés. Bonus : moyenne par région | Amel | `carte.py` | ⬜ |
| 6 | Relecture croisée du code (chacune relit celui de l'autre) | Amel + Coura | — | ⬜ |
| 7 | Préparation de l'oral | Amel + Coura | `docs/oral.md` | ⬜ |

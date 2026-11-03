# Données du projet — qualité de l'air (LCSQA / Geod'air)

Source : https://www.data.gouv.fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1
Fichiers téléchargés le 24/10/2026, contenu non modifié (seuls les noms ont changé).

| Fichier dans `data/` | Nom d'origine | Contenu |
|---|---|---|
| `mesures_horaires_2025/mesures_horaires_2025-MM-JJ.csv` (365 fichiers) | `temps-reel/2025/FR_E2_2025-MM-JJ.csv` | **Fichier principal.** Concentrations horaires de polluants mesurées par toutes les stations françaises, un fichier par jour (~50 000 lignes × 23 colonnes, séparateur `;`, UTF-8 avec BOM). |
| `metadonnees_stations.xls` | `fr-2026-d-07082026-1.xls` (« Dataset D ») | Référentiel des stations : coordonnées GPS, commune, altitude, typologie, réseau, points de prélèvement, méthodes de mesure. Jointure : `code site` (CSV) ↔ `NatlStationCode` (onglet AirQualityStations). |
| `metadonnees_zones_surveillance.xls` | `fr-2022-b-lcsqa-ineris-20230317.xls` (« Dataset B ») | Référentiel des zones administratives de surveillance (ZAS) : nom, type, population, superficie. Jointure : `code zas` (CSV) ↔ `ZoneCode` (onglet AirQualityZones). |
| `geo/regions.geojson` | `regions-version-simplifiee.geojson` du projet [france-geojson](https://github.com/gregoiredavid/france-geojson) (contours issus des données ouvertes IGN / Etalab) | Contours simplifiés des 13 régions de métropole, pour la carte choropleth (A6). Jointure : `region` (fichier fusionné) ↔ `properties.nom`. |
| `documentation/note_explicative_donnees.pdf` | `mise-a-disposition-des-donnees-qa-e2-20180919.pdf` | Note du LCSQA qui explique le flux E2, les codes de validité/vérification et les datasets B et D. |

## Colonnes des CSV de mesures

| Colonne | Sens |
|---|---|
| Date de début / Date de fin | Heure de début et de fin de la mesure (TU en métropole, heure locale dans les DROM) |
| Organisme | AASQA qui gère la station (AIRPARIF, ATMO SUD…) |
| code zas / Zas | Zone administrative de surveillance (ZAG = agglomération, ZAR = zone à risque, ZR = zone régionale) |
| code site / nom site | Identifiant et nom de la station |
| type d'implantation | Urbaine, Périurbaine, Rurale (nationale / régionale / près des villes) |
| Polluant | NO2, NO, NOX as NO2, PM10, PM2.5, O3, SO2, CO, C6H6 |
| type d'influence | Fond, Trafic, Industrielle |
| discriminant | Distingue plusieurs mesures d'un même polluant sur une même station |
| Réglementaire | Mesure utilisée pour la surveillance réglementaire (Oui) |
| type d'évaluation | mesures fixes, mesures indicatives, estimation objective |
| procédure de mesure | Appareil / méthode utilisés |
| type de valeur | moyenne horaire validée |
| valeur / valeur brute | Concentration (valeur arrondie / valeur brute) |
| unité de mesure | µg-m3 (ou µg/m3), mg-m3 pour le CO |
| taux de saisie, couverture temporelle, couverture de données | Vides dans les fichiers horaires |
| code qualité | A, R, N (N = donnée invalide ; A/R : statut vérifié/brut, à confirmer dans la note) |
| validité | 1 = valide, -1 = invalide, 4 = valide (méthode spécifique ozone) — vocabulaire EEA *observationvalidity* |

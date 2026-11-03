# C2 — Variables clés, graphiques prévus et seuils de référence

Coura (avec Claude 2), 03/11/2026. Document de travail pour la séance 2 et pour les phases 2 et 3.

## 1. Variables clés

| Variable | Fichier (après C3) | Nature | Pourquoi elle compte |
|---|---|---|---|
| `moyenne` (concentration journalière, µg/m³) | `mesures_journalieres_2025.csv` | quantitative continue | **variable principale** : niveau de pollution |
| `max horaire` (µg/m³) | `mesures_journalieres_2025.csv` | quantitative continue | pics de la journée, comparaison aux seuils horaires |
| `valeur` (concentration horaire, µg/m³) | `mesures_horaires_janvier_juillet_2025.csv` | quantitative continue | profil sur une journée, hiver / été |
| `Polluant` | mesures | qualitative (9 modalités) | on analyse surtout NO2, PM10, PM2.5, O3, SO2, CO (ceux qui ont des seuils) |
| `date` → `mois`, `saison`, `jour de la semaine` (créées en C3) | mesures | temporelle → qualitative | « quand pollue-t-on le plus ? » |
| `type d'influence` (Fond, Trafic, Industrielle) | mesures | qualitative | comparer trafic et fond. Attention : dépend du couple station-polluant |
| `type d'implantation` (Urbaine, Périurbaine, Rurale…) | mesures | qualitative | ville / campagne |
| `Organisme` (AASQA, ex : AIRPARIF) | mesures | qualitative | une AASQA par région → sert de **région** |
| `code site` → `nom station`, `commune`, `latitude`, `longitude`, `altitude` | `stations.csv` | identifiant + quantitatives | carte (A6), affichages |
| `territoire` (metropole / outre-mer) | `stations.csv` | qualitative | séparer métropole et DROM (heures TU / heure locale) |
| `code zas` → `type zone`, `population`, `densite` | `zones.csv` | qualitative + quantitatives | lien pollution ↔ population |
| `depassement` (oui / non, à créer en C4) | calculée | qualitative binaire | comptage des jours au-dessus d'un seuil (partie 3) |

## 2. Questions, graphiques et tableaux prévus

Tous les graphiques sont proposés en **plotly express** (vu au chapitre 3, s'affiche dans Streamlit avec `st.plotly_chart`).

| # | Question | Graphique / tableau | Variables | Fonction | Tâche |
|---|---|---|---|---|---|
| G1 | Quels niveaux en 2025 ? | Tableau de statistiques par polluant : moyenne, médiane, écart type, min, Q1, Q3, max, IQR | `moyenne` × `Polluant` | `groupby` + `describe()` | A4 |
| G2 | Comment se répartissent les valeurs ? | Histogramme d'un polluant choisi | `moyenne` | `px.histogram` | C5 |
| G3 | Quand pollue-t-on le plus ? | Courbe de la moyenne mensuelle par polluant | `mois`, `moyenne` | `px.line` | A4 |
| G4 | Profil d'une journée, hiver contre été | Courbe heure par heure, janvier et juillet | heure, `valeur` | `px.line` | A4 |
| G5 | Saisons | Boxplot par saison | `saison`, `moyenne` | `px.box` | A4 / C5 |
| G6 | Effet du trafic | Boxplot NO2 par type d'influence (Fond / Trafic / Industrielle) | `type d'influence`, `moyenne` | `px.box` | C4 / C5 |
| G7 | Semaine contre week-end | Barres de la moyenne NO2 par jour de la semaine | `jour de la semaine` | `px.bar` | A4 |
| G8 | Quelles régions polluent le plus ? | Barres de la moyenne annuelle par région, triées | `Organisme`, `moyenne` | `groupby` + `px.bar` | C4 |
| G9 | Lien avec la population | Nuage de points : densité de la zone contre moyenne annuelle NO2 | `densite`, `moyenne` | `px.scatter` | C4 |
| G10 | Combien de dépassements ? | Tableau : nombre de jours au-dessus de chaque seuil, par polluant | `depassement` | `groupby` + `aggregate` | C4 |
| G11 | Le trafic dépasse-t-il plus souvent ? | Tableau de contingence type d'influence × dépassement OMS (oui / non) | `type d'influence`, `depassement` | `pivot_table` | C4 |
| G12 | Part des jours au-dessus de l'OMS | Camembert jours sous / au-dessus du seuil OMS (polluant choisi) | `depassement` | `px.pie` | C5 |
| G13 | Composition du réseau | Sunburst territoire → typologie → nombre de stations | `stations.csv` | `px.sunburst` | C5 |
| G14 | Où se trouvent les points chauds ? | Carte de la France : stations colorées par concentration, et/ou régions | lat / lon, `moyenne` | `px.choropleth` (vu) + carte à points | A6 (Amel) |

Filtres du dashboard proposés : polluant (`st.selectbox`), période (`st.select_slider` sur les mois), région (`st.multiselect`), métropole / outre-mer.

## 3. Seuils de référence par polluant

Unité : µg/m³, sauf mention contraire. **Attention : dans nos fichiers nettoyés, le CO est converti en µg/m³ (A2), donc ses seuils en mg/m³ doivent être multipliés par 1 000.**

- **OMS 2021** : recommandations sanitaires (pas obligatoires). Les valeurs sur 24 h correspondent au 99e centile, soit 3 à 4 jours de dépassement tolérés par an.
- **UE / France 2025** : valeurs en vigueur pour nos données de 2025 (directive 2008/50/CE, transposée dans le Code de l'environnement). VL = valeur limite (obligatoire), VC = valeur cible, OQ = objectif de qualité. Le chiffre entre parenthèses est le nombre de dépassements autorisés par an et par station.
- **Seuils d'épisode (France)** : seuil d'information-recommandation / seuil d'alerte.
- **UE 2030** : nouvelle directive (UE) 2024/2881, à respecter à partir du 1er janvier 2030 (pour comparaison).

| Polluant | Durée | OMS 2021 | UE / France 2025 | Info / alerte (France) | UE 2030 |
|---|---|---|---|---|---|
| **PM2.5** | année | 5 | VL 25 ; VC 20 ; OQ 10 | — | 10 |
| | jour | 15 | — | — | 25 (18 j) |
| **PM10** | année | 15 | VL 40 ; OQ 30 | — | 20 |
| | jour | 45 | VL 50 (35 j) | info 50 / alerte 80 | 45 (18 j) |
| **NO2** | année | 10 | VL 40 ; OQ 40 | — | 20 |
| | jour | 25 | — | — | 50 (18 j) |
| | heure | — | VL 200 (18 h) | info 200 / alerte 400 (3 h de suite) | 200 (3 h) |
| **O3** | max journalier de la moyenne sur 8 h | 100 | VC 120 (25 j, moyenne sur 3 ans) ; OQ 120 | — | VC 120 (18 j, moyenne sur 3 ans) |
| | saison de pointe (6 mois) | 60 | — | — | — |
| | heure | — | — | info 180 / alerte 240 | — |
| **SO2** | année | — | OQ 50 | — | 20 |
| | jour | 40 | VL 125 (3 j) | — | 50 (18 j) |
| | heure | — | VL 350 (24 h) | info 300 / alerte 500 (3 h de suite) | 350 (3 h) |
| **CO** | jour | 4 mg/m³ (= 4 000) | — | — | 4 mg/m³ (18 j) |
| | max journalier de la moyenne sur 8 h | — | VL 10 mg/m³ (= 10 000) | — | 10 mg/m³ |

## 4. Ce qu'on pourra vraiment calculer avec nos fichiers

| Type de seuil | Calculable ? | Comment |
|---|---|---|
| Seuils sur 24 h (OMS 24 h, PM10 50 et 80, SO2 125, CO 4 000) | oui, toute l'année | comparer `moyenne` (fichier journalier) au seuil, compter les jours par station |
| Seuils horaires (NO2 200, SO2 300 et 350, O3 180 et 240) | oui, en jours | « jour où au moins une heure dépasse » avec `max horaire` ; le nombre exact d'heures n'est possible que pour janvier et juillet (fichier horaire) |
| Seuils annuels (OMS, VL, OQ) | oui | moyenne des moyennes journalières par station et par polluant, en vérifiant qu'il y a assez de jours mesurés |
| Moyennes glissantes sur 8 h (O3 100 / 120, CO 10 000) | non, pas simplement | demande une moyenne glissante, pas vue en cours → à présenter comme une limite |
| Alerte « 3 heures de suite », saison de pointe O3 | non | demande des heures consécutives / 6 mois glissants → limite |

À dire à l'oral : nos données sont en partie des données « temps réel » pas encore vérifiées par les AASQA. On parle donc de **dépassements observés**, pas de non-respect officiel de la réglementation.

## 5. Sources

- OMS : *WHO global air quality guidelines* (2021), tableau 3.26 « Recommended 2021 AQG levels » — https://www.ncbi.nlm.nih.gov/books/NBK574591/table/ch3.tab26/
- France / UE 2025 : Air Pays de la Loire, « Seuils de qualité de l'air 2023 » (cite le décret 2010-1250 et l'arrêté du 07/04/2016) — https://airpl.org/sites/default/files/reports/seuils%20de%20la%20qualit%C3%A9%20de%20l%27air%202023.pdf ; recoupé avec le tableau de la DRIEAT Île-de-France — https://www.drieat.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/valeur_qualite_air.pdf . Texte de loi : article R221-1 du Code de l'environnement (pas consulté directement).
- UE 2030 : ARPAE, *Ecoscienza* n°1/2026, « La nuova direttiva aria UE » — https://www.arpae.it/it/ecoscienza/numeri-ecoscienza/anno-2026/numero-1-anno-2026/aria/3-la-nuova-direttiva-aria-ue-obiettivi-e-criticita-01-2026.pdf ; dates (publication le 20/11/2024, entrée en vigueur le 10/12/2024, valeurs à atteindre au 01/01/2030) : HSY — https://www.hsy.fi/en/air-quality-and-climate/air-protection-and-health/air-quality-regulations/

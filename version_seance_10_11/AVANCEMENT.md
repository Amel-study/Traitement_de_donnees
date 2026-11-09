# Avancement du projet (séance du 10/11/2026)

Légende : ✅ fait · 🔄 en cours · ⬜ à faire

## Phase 1 — description et nettoyage

| # | Tâche | Qui | Fichier(s) | Statut |
|---|---|---|---|---|
| 0 | Faire valider le dataset par l'enseignante | Amel + Coura | — | ✅ |
| A1 | Décrire un fichier de mesures : lignes, colonnes, sens, types, catégories | Amel | `scripts/01_exploration_mesures.py` | ✅ |
| A2 | Nettoyage d'un fichier de mesures : manquantes, doublons, unités, valeurs négatives, textes, colonnes liées | Amel | `scripts/nettoyage_mesures.py` | ✅ |
| C1 | Nettoyage des métadonnées des stations et des zones | Coura | `scripts/03_metadonnees.py` | ✅ |
| C2 | Variables clés, graphiques prévus, seuils de référence | Coura | `docs/variables_et_graphiques.md` | ✅ |

## Phase 2 — année complète et analyse

| # | Tâche | Qui | Fichier(s) | Statut |
|---|---|---|---|---|
| A3 | Boucle sur les 365 fichiers, moyennes journalières par station et par polluant | Amel | `scripts/04_annee_complete.py` | ✅ |
| C3 | Fusion des mesures avec les stations et les zones, colonnes région / mois / saison / jour | Coura | `scripts/05_fusion.py` | ✅ |
| A4 | Analyse dans le temps : polluants, mois, jour de la semaine, journée type, trafic / fond | Amel | `scripts/06_analyse_temps.py` | 🔄 première version (à compléter : comparaison des saisons) |
| C4 | Analyse par lieux : régions, types de zones, densité, dépassements de seuils, contingence | Coura | `scripts/07_analyse_lieux.py` | ⬜ |

## Phase 3 — carte, dashboard et oral

| # | Tâche | Qui | Fichier(s) | Statut |
|---|---|---|---|---|
| A5 | Dashboard Streamlit : pages, filtres (polluant, période, régions) | Amel | `app.py` | ⬜ |
| A6 | Carte de la France : stations et régions | Amel | `carte.py` | ⬜ |
| C5 | Graphiques du dashboard (lieux et seuils) | Coura | `graphiques.py` | ⬜ |
| 6 | Relecture croisée du code | Amel + Coura | — | ⬜ |
| 7 | Préparation de l'oral | Amel + Coura | — | ⬜ |

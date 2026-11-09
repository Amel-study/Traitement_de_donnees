# Version du projet présentée à la séance du 10/11/2026

Binôme : Amel et Coura. Sujet : la pollution de l'air en France en 2025 (données temps réel du LCSQA, data.gouv.fr).

Ce dossier contient l'état du projet présenté le 10/11 : **phase 1 terminée** (description, nettoyage, choix des variables) et **début de la phase 2** (année complète, fusion avec les métadonnées, premières analyses dans le temps). La carte, le dashboard Streamlit et l'analyse par lieux et par seuils sont prévus pour la suite.

## Contenu

| Fichier | Qui | Rôle |
|---|---|---|
| `scripts/telecharger_donnees.py` | Amel | Télécharge les 365 fichiers journaliers de 2025 (3,7 Go) |
| `scripts/01_exploration_mesures.py` | Amel | **A1** : description d'un fichier de mesures (taille, colonnes, types, catégories) |
| `scripts/nettoyage_mesures.py` | Amel | **A2** : fonctions de vérification et de nettoyage d'un fichier journalier |
| `scripts/03_metadonnees.py` | Coura | **C1** : nettoyage des métadonnées des stations et des zones |
| `docs/variables_et_graphiques.md` | Coura | **C2** : variables clés, graphiques prévus, seuils de référence (OMS, UE) |
| `scripts/04_annee_complete.py` | Amel | **A3** : boucle sur les 365 fichiers, moyennes journalières |
| `scripts/05_fusion.py` | Coura | **C3** : fusion des mesures avec les stations et les zones |
| `scripts/06_analyse_temps.py` | Amel | **A4** : premières analyses dans le temps (mois, jour de la semaine, journée type, trafic / fond) |
| `AVANCEMENT.md` | les deux | Ce qui est fait et ce qui reste |
| `journal_de_bord.md` | les deux | Journal de bord jusqu'à cette séance |

## Lancer les scripts

Depuis le dossier principal du projet (celui qui contient `data/`), dans l'ordre :

```bash
python version_seance_10_11/scripts/telecharger_donnees.py
python version_seance_10_11/scripts/01_exploration_mesures.py
python version_seance_10_11/scripts/nettoyage_mesures.py
python version_seance_10_11/scripts/03_metadonnees.py
python version_seance_10_11/scripts/04_annee_complete.py
python version_seance_10_11/scripts/05_fusion.py
python version_seance_10_11/scripts/06_analyse_temps.py
```

Les données nettoyées sont écrites dans `data_clean/` et les graphiques (plotly, à ouvrir dans un navigateur) dans `resultats/`.

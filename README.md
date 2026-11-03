# Projet — Traitement et analyse de données (ESIEE, 2026/2027)

Binôme : **Amel** (GitHub `Amel-study`) et **Coura** (GitHub `couraba-web`).

## Sujet

Nettoyer puis analyser avec des statistiques descriptives les **mesures horaires de pollution de l'air en France en 2025**, et présenter les résultats dans un dashboard **Streamlit**.

Données : [data.gouv.fr — Données « temps réel » de mesure des concentrations de polluants atmosphériques réglementés](https://www.data.gouv.fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1) (LCSQA / Geod'air). Le détail des fichiers est dans [data/README.md](data/README.md).

## Consignes de l'enseignante (résumé)

- Choisir un dataset assez gros, appliquer le *data cleansing*, faire une analyse descriptive, rendu sous forme de dashboard Streamlit.
- Évaluation : oral en binôme (méthodes, analyses, résultats) + rendu (journal de bord + codes Python commentés + fichiers) + QCM.
- Compétences : Python / Pandas / graphiques, **fichiers de grande taille**, data cleansing, analyse et représentation des données.
- Journal de bord : pour chaque séance, avec la date : ce qu'on a fait et pourquoi, les problèmes rencontrés, les solutions testées (et pourquoi certaines n'ont pas marché).
- Séance 2 : faire valider le dataset ; décrire les données (lignes, colonnes, sens, nature) ; premier script de nettoyage (manquantes, catégories, aberrantes, doublons, intervalles, textes, colonnes liées, normalisation) ; proposer les variables clés et les graphiques.

## Organisation du dépôt

| Fichier / dossier | Rôle |
|---|---|
| [AVANCEMENT.md](AVANCEMENT.md) | Ce qui est fait, ce qui reste, **qui fait quoi** |
| [journal_de_bord.md](journal_de_bord.md) | Le journal de bord à rendre |
| [CONVERSATION_CLAUDE.md](CONVERSATION_CLAUDE.md) | Messages entre le Claude d'Amel (Claude 1) et celui de Coura (Claude 2) |
| [CLAUDE.md](CLAUDE.md) | Règles communes lues automatiquement par Claude Code |
| [PROMPT_CLAUDE_COURA.md](PROMPT_CLAUDE_COURA.md) | Prompt de démarrage à coller dans le Claude Code de Coura |
| `data/` | Données brutes (non modifiées). Les CSV horaires ne sont pas sur GitHub |
| `data_clean/` | Données nettoyées produites par nos scripts (non publiées, trop lourdes) |
| `scripts/` | Nos scripts Python |

## Installation (à faire une fois)

```bash
git clone https://github.com/Amel-study/Traitement_de_donnees.git
cd Traitement_de_donnees
python scripts/telecharger_donnees.py
```

Le dernier script télécharge les 365 fichiers journaliers (3,7 Go, 10 à 20 min).
Les PDF du cours (Cours1, Cours2, TD…) sont à copier à la racine du dossier : ils ne sont pas publiés sur GitHub.

Bibliothèques : `pandas`, `xlrd` (lecture des .xls), plus tard `streamlit` et une bibliothèque de graphiques.

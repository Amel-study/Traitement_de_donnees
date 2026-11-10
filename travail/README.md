# Exploration des données — qualité de l'air en France (2025)

Binôme : Amel et Coura.

## Le dataset

« Données temps réel de mesure des concentrations de polluants atmosphériques réglementés », data.gouv.fr (LCSQA).
Un fichier CSV par jour : la concentration de chaque polluant, heure par heure, dans toutes les stations de surveillance de France. Nous avons téléchargé toute l'année 2025 (365 fichiers, 3,7 Go, environ 17,6 millions de lignes).

Ce script étudie **un seul jour, le 1er janvier 2025** : les 365 fichiers ont les mêmes colonnes, donc ce qu'on apprend sur un jour vaut pour toute l'année.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `exploration_mesures.py` | Le script : décrit le fichier sans le modifier |
| `data/mesures_horaires_2025-01-01.csv` | Les données du 1er janvier 2025 (fichier d'origine, non modifié) |
| `resultats_exploration.txt` | Ce que le script affiche |
| `EXPLICATIONS.md` | Le code expliqué ligne par ligne, les résultats et les questions possibles |

Lancement (depuis ce dossier) : `python exploration_mesures.py`

## Description des données

- **49 968 lignes et 23 colonnes.** Une ligne = un polluant, mesuré par une station, pendant une heure.
- **506 stations**, 70 zones de surveillance, 17 organismes régionaux (dont 4 en outre-mer).
- **9 polluants** : NO2, NO, NOX, O3, PM10, PM2.5, SO2, CO, C6H6 (benzène).

| Colonnes | Sens | Type |
|---|---|---|
| Date de début, Date de fin | Heure de début et de fin de la mesure | texte |
| Organisme, code zas, Zas | Organisme de surveillance et zone | texte |
| code site, nom site | Code et nom de la station | texte |
| type d'implantation | Urbaine, Périurbaine, Rurale… | texte |
| type d'influence | Fond, Trafic, Industrielle | texte |
| Polluant, discriminant | Polluant mesuré, numéro d'appareil | texte |
| valeur, valeur brute | Concentration mesurée | nombre décimal |
| unité de mesure | µg-m3, µg/m3 ou mg-m3 | texte |
| code qualité, validité | Statut de la donnée (vérifiée, brute, invalide) | texte / entier |
| Réglementaire, type d'évaluation, type de valeur, procédure de mesure | Informations sur la mesure | texte |
| taux de saisie, couverture temporelle, couverture de données | — | vides |

## Problèmes repérés (à traiter au nettoyage)

1. **Colonnes vides** : `taux de saisie`, `couverture temporelle`, `couverture de données` sont vides sur toutes les lignes.
2. **Colonnes sans information** : `Réglementaire` vaut toujours « Oui » et `type de valeur` toujours « moyenne horaire validée ».
3. **Valeurs manquantes** : 2 034 lignes sans valeur (4 %), ce sont les mesures invalides (`validité = -1`).
4. **Unités** : la même unité est écrite `µg-m3` ou `µg/m3`, et le CO est en `mg-m3` (1 mg = 1 000 µg).
5. **Valeurs négatives** : jusqu'à -4,5, impossible pour une concentration (petites erreurs des appareils quand l'air est presque propre).
6. **Valeurs très élevées** : PM10 jusqu'à 304,6 µg/m³. Le 1er janvier, cela peut venir des feux d'artifice du Nouvel An : à vérifier avant de les supprimer.
7. **Dates** stockées en texte, à convertir en vraies dates.
8. **Texte** : `discriminant` mélange majuscules et minuscules (`I` et `i`).

## Suite du travail

Écrire le script de nettoyage qui corrige ces problèmes, puis l'appliquer aux 365 fichiers.

# Explications du script `exploration_mesures.py`

Pour Coura (et pour réviser avant la présentation).

## À quoi sert le script

On a un gros fichier : les mesures de pollution de toute la France pour le 1er janvier 2025. **Le script ne modifie rien : il regarde le fichier et le décrit** (taille, colonnes, cases vides, valeurs possibles, minimum / maximum) pour repérer les problèmes à corriger avant le nettoyage.

On n'étudie qu'un jour car les 365 fichiers de l'année ont les mêmes colonnes : ce qu'on apprend sur un jour vaut pour toute l'année.

**En une phrase pour l'oral** : « Ce script ouvre le fichier d'une journée et le décrit pour repérer les problèmes à corriger avant le nettoyage. »

## Lancer le script

Depuis le dossier `travail/` (dans Spyder, le répertoire de travail doit être `travail/`) :

```bash
python exploration_mesures.py
```

Le résultat attendu est dans `resultats_exploration.txt`.

## Le code ligne par ligne

| Lignes | Code | Ce que ça fait |
|---|---|---|
| 1-2 | `# ...` | Commentaires : Python les ignore, ce sont des notes pour nous. |
| 4 | `import pandas as pd` | On charge Pandas (l'outil pour les tableaux) et on l'appelle `pd`. |
| 6 | `FICHIER = "data/..."` | Le chemin du fichier, rangé dans une variable en MAJUSCULES car il ne change pas. |
| 9 | `pd.read_csv(FICHIER, sep=';', encoding='utf-8-sig')` | On ouvre le CSV et on le met dans un tableau `mesures`. `sep=';'` : colonnes séparées par des points-virgules (fichier français). `encoding` : pour que les accents s'affichent bien. |
| 12 | `mesures.shape[0]` | `shape` = (lignes, colonnes). `[0]` = le nombre de lignes : **49 968**. |
| 13 | `mesures.shape[1]` | `[1]` = le nombre de colonnes : **23**. |
| 17 | `mesures.head()` | Affiche les **5 premières lignes**. (`\n` dans un texte = saut de ligne.) |
| 21 | `mesures.dtypes` | Le **type** de chaque colonne : `object` = texte, `float64` = nombre à virgule, `int64` = entier. |
| 25 | `mesures.isna().sum()` | Compte les **cases vides** par colonne : `isna()` met `True` dans les cases vides, `sum()` les compte (`True` vaut 1). |
| 28-29 | `colonnes_categories = [...]` | Une liste avec les noms des 11 colonnes de catégories (Polluant, Organisme…). |
| 31 | `for colonne in colonnes_categories:` | Une boucle : on prend les colonnes une par une. |
| 32 | `mesures[colonne].unique()` | Les valeurs de la colonne **sans les répétitions**. |
| 33 | `len(valeurs)` dans un `print(f"...")` | Affiche combien de valeurs différentes. Le `f` permet de mettre des variables entre `{ }`. |
| 34 | `print(valeurs)` | Affiche la liste des valeurs. |
| 37-39 | `len(mesures['code site'].unique())` | Compte les stations (**506**), les zones (**70**) et les procédures de mesure (**56**). |
| 42 | `mesures['Date de début'].min()` | La première date : `2025/01/01 00:00:00`. |
| 43 | `mesures['Date de fin'].max()` | La dernière date : `2025/01/02 00:00:00`. On vérifie qu'il y a bien un seul jour. |
| 48 | `for colonne in ['valeur', 'valeur brute']:` | Une boucle sur les deux colonnes de nombres. |
| 49-51 | `min()`, `mean()`, `max()` | Plus petite valeur, moyenne, plus grande valeur. |
| 52 | `{moyenne:.2f}` | Affiche la moyenne avec **2 chiffres après la virgule**. Résultat : min = **-4.5** (impossible !). |
| 55 | `mesures.groupby('Polluant')['valeur'].min()` | `groupby` range les lignes **par polluant** (une « boîte » par polluant), puis on prend le minimum de chaque boîte. |
| 56-58 | `mean()`, `max()`, `count()` | Pareil pour la moyenne, le maximum et le nombre de mesures. |
| 61 | `pd.concat([...], axis=1)` | On colle les 4 résultats **côte à côte** dans un seul tableau (`axis=1` = en colonnes). |
| 62 | `resume_polluants.columns = [...]` | On donne un nom aux 4 colonnes. |
| 64 | `print(resume_polluants)` | Affiche le tableau : une ligne par polluant. |
| 68 | `groupby('Polluant')['unité de mesure'].unique()` | Les unités utilisées pour chaque polluant. |

## Deux points qui reviennent souvent

**Colonnes de catégories (lignes 28 à 34).** Une colonne de catégories contient toujours les mêmes mots répétés (ex : la colonne Polluant a 49 968 lignes mais seulement 9 polluants différents). `unique()` enlève les répétitions et `len()` les compte. Ça permet de voir :
- que l'unité est écrite de 3 façons (`µg-m3`, `µg/m3`, `mg-m3`) alors que les deux premières veulent dire la même chose ;
- que `Réglementaire` vaut toujours « Oui » → colonne inutile ;
- que `discriminant` mélange majuscules et minuscules (`I` et `i`).

**`groupby` (lignes 55 à 64).** Faire une seule moyenne de toutes les mesures mélangées n'a pas de sens (l'ozone est autour de 44, le CO autour de 0,2). `groupby('Polluant')` range les lignes par polluant puis fait le calcul **dans chaque groupe** : on obtient une moyenne par polluant.

## Ce qu'on obtient

- **49 968 lignes, 23 colonnes** ; 506 stations, 70 zones, 17 organismes, 9 polluants.
- 3 colonnes **vides à 100 %** (`taux de saisie`, `couverture temporelle`, `couverture de données`).
- **2 034 valeurs manquantes** (4 %) : les mesures invalides.
- `discriminant` vide sur 6 696 lignes (normal : ne sert que si une station a plusieurs appareils).

| Polluant | nb mesures | min | moyenne | max |
|---|---|---|---|---|
| NO2 | 8 518 | -1,0 | 12,4 | 100,3 |
| O3 | 6 850 | -2,9 | 44,0 | 103,4 |
| PM10 | 7 790 | -2,0 | 16,0 | 304,6 |
| PM2.5 | 5 702 | -1,0 | 13,4 | 125,4 |
| CO | 398 | -0,05 | 0,22 | 0,68 |

## Les problèmes repérés (pour le nettoyage)

1. 3 colonnes vides + 2 colonnes qui ont toujours la même valeur → à supprimer.
2. 2 034 mesures invalides sans valeur → à supprimer.
3. Unité écrite de deux façons, CO en mg/m³ (1 mg = 1 000 µg) → à harmoniser.
4. **Valeurs négatives** pour presque tous les polluants → impossible, à corriger.
5. PM10 jusqu'à 304 → **pas une erreur** : feux d'artifice du Nouvel An.
6. Dates stockées en texte → à convertir en vraies dates.
7. Majuscules / minuscules dans `discriminant` → à vérifier.

## Questions possibles (et réponses)

- **Pourquoi `sep=';'` ?** Fichier français : le point-virgule sépare les colonnes, la virgule sert aux décimales.
- **Que fait `isna().sum()` ?** `isna()` met `True` dans les cases vides, `sum()` les compte.
- **Différence entre `unique()` et `len(unique())` ?** Le premier donne les valeurs, le second combien il y en a.
- **Pourquoi un seul jour ?** Les 365 fichiers ont les mêmes colonnes ; un jour se lit en 1 seconde, l'année fait 17,6 millions de lignes.
- **À quoi sert `groupby` ?** À faire le même calcul séparément pour chaque groupe (ici chaque polluant).
- **Que fait `axis=1` dans `concat` ?** Colle les tableaux côte à côte (avec `axis=0` : les uns sous les autres).
- **Pourquoi le CO est-il si petit ?** Il est en mg/m³ et pas en µg/m³.

## Si ça ne marche pas

- `FileNotFoundError` : le script n'est pas lancé depuis le dossier `travail/`.
- `ModuleNotFoundError: pandas` : ce n'est pas le Python d'Anaconda → lancer depuis Spyder ou Anaconda Prompt.

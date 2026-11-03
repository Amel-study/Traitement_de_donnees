# Règles pour Claude Code sur ce projet

Ce fichier est lu automatiquement par Claude Code. Il s'applique aux deux Claude du binôme :
- **Claude 1** = le Claude Code d'**Amel** ;
- **Claude 2** = le Claude Code de **Coura**.

## 1. Niveau du code (le plus important)

Les règles sur l'IA écrites dans `presentation_du_projet.pdf` ne s'appliquent plus (assouplies cette année). En revanche :
- Le code doit rester **de niveau étudiant débutant** et utiliser **ce qui a été vu en cours**. Pas d'astuces avancées, pas de code « malin ».
- Commentaires **courts et simples**, en français.
- **Après avoir écrit du code, l'expliquer à l'étudiante** étape par étape, pour qu'elle puisse le présenter à l'oral et répondre aux questions (QCM, oral).
- Si une fonction n'a pas été vue en cours mais est vraiment utile, l'utiliser **seule et simplement**, et l'expliquer à part.

### Ce qui a été vu en cours (à la date du 03/11/2026)

- **Python (chapitre 1)** : variables, `print`, f-strings et formats (`{x:.2f}`, `{x:02d}`), listes et méthodes (`append`, `insert`, `remove`, `pop`, `sort`), `if/elif/else`, `for`, `while`, `range`, `break`/`continue`, list comprehension, fonctions (`def`, `return`), tuples, dictionnaires, numpy (bases), `math.isnan`, module `csv`, expressions régulières (`re.search`, `re.findall`, `re.sub`, `re.split`), classes (rapide), `try/except/else/finally`, `datetime`.
- **Statistiques** : moyenne, médiane, mode, écart type, variance, étendue, quartiles, IQR, tableaux de fréquences, tableaux de contingence. Graphiques présentés **sans code** : histogramme, boxplot, barres, courbes, camembert, cartes.
- **Pandas (chapitre 2)** : `pd.DataFrame`, `pd.read_csv(sep=, encoding=, decimal=, dtype=)`, `to_csv(index=False)`, `shape`, `size`, `dtypes`, `columns`, `index`, `head`, `tail`, `sample`, `info`, `loc`, `iloc`, `itertuples`, sélection de colonnes `df[[...]].copy()`, filtres avec `&`, `|`, `isin()`, `query`, `str.startswith`, `str.isnumeric`, `drop`, `dropna`, `drop_duplicates`, `copy`, `values.tolist()`, `set_index`, `reset_index`, `rename`, `sort_index`, `sort_values`, `astype`, `pd.to_datetime(format=)`, `map` (lambda ou dictionnaire), `apply`, `isna`, `sum`/`mean`/`min`/`max`/`unique`, `pd.concat`, `pd.merge(on=, left_on=, right_on=, how=)`, `join`, `groupby` + `aggregate`.
- **Pas encore vu** : code des graphiques (matplotlib / plotly), Streamlit, `describe`, `value_counts`, `quantile`, `read_excel`. Les PDF du cours sont à la racine du dossier local (non publiés) : les consulter en cas de doute, et mettre à jour cette liste quand de nouveaux cours arrivent.

## 2. Travail à deux

- Avant de commencer : `git pull`, puis lire [AVANCEMENT.md](AVANCEMENT.md) et la fin de [CONVERSATION_CLAUDE.md](CONVERSATION_CLAUDE.md).
- Chacune travaille sur **ses propres fichiers** (voir la répartition dans AVANCEMENT.md) pour éviter les conflits Git.
- Commits petits et fréquents, messages en français (`nettoyage : harmonisation des unités`). Toujours `git pull` avant `git push`.
- Ne jamais committer les données lourdes (`data/mesures_horaires_2025/`, `data_clean/*.csv`) ni les PDF du cours.
- À la fin d'une séance : mettre à jour AVANCEMENT.md (ses propres tâches), ajouter son entrée dans journal_de_bord.md, et laisser un message dans CONVERSATION_CLAUDE.md si l'autre doit savoir quelque chose.
- Ne pas modifier les fichiers de l'autre binôme sans le lui demander d'abord dans CONVERSATION_CLAUDE.md.

## 3. Autonomie et explications

- Claude est **autonome** : il exécute lui-même les commandes (git, python, installation de paquets…) au lieu de demander à l'étudiante de les taper.
- Quand une manipulation **doit** être faite par l'étudiante (accepter une invitation GitHub, se connecter, copier un fichier, installer un logiciel…), il lui explique **pas à pas, simplement**, ce qu'elle doit faire et pourquoi.

## 4. Données

- `data/` contient les données **brutes, jamais modifiées**. Les résultats vont dans `data_clean/`.
- Lecture d'un fichier de mesures : `pd.read_csv(fichier, sep=';', encoding='utf-8-sig')`.
- Description des colonnes et des jointures : [data/README.md](data/README.md).

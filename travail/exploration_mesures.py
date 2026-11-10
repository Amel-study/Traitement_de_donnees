import pandas as pd

FICHIER = "data/mesures_horaires_2025-01-01.csv"

# 1 Lecture du fichier (pour plus tard faut lire dossier)

mesures = pd.read_csv(FICHIER, sep=';', encoding='utf-8-sig')

# 2 taille  tableau
print("Nombre de lignes :", mesures.shape[0])
print("Nombre de colonnes :", mesures.shape[1])

# 3 Aperçu des premières lignes
print("\n Premières lignes ")
print(mesures.head())

#za

# 4 Nom et type de chaque colonne
print("\n Types des colonnes ")
print(mesures.dtypes) #object = texte ; float64 = nombre à virgule ; int64 = nombre entier

# 5 Nombre de valeurs manquantes par colonne
print("\n Valeurs manquantes par colonne ")
print(mesures.isna().sum())



# 6 Colonnes de catégories
colonnes_categories = ['Organisme', "type d'implantation", 'Polluant',
                       "type d'influence", 'discriminant', 'Réglementaire',
                       "type d'évaluation", 'type de valeur',
                       'unité de mesure', 'code qualité', 'validité']

print("\n--- Valeurs des colonnes de catégories ---")
for colonne in colonnes_categories:
    valeurs = mesures[colonne].unique()
    print(f"\n{colonne} : {len(valeurs)} valeurs différentes")
    print(valeurs)

# 7 Combien de stations et de zones différentes ?
print("\nNombre de stations :", len(mesures['code site'].unique()))
print("Nombre de zones :", len(mesures['code zas'].unique()))
print("Nombre de procédures de mesure :",
      len(mesures['procédure de mesure'].unique()))

# 8 Période couverte par le fichier
print("\nPremière date de début :", mesures['Date de début'].min())
print("Dernière date de fin :", mesures['Date de fin'].max())

# 9 Colonnes de valeurs : minimum, moyenne, maximum
print("\n--- Colonnes de valeurs ---")
for colonne in ['valeur', 'valeur brute']:
    minimum = mesures[colonne].min()
    moyenne = mesures[colonne].mean()
    maximum = mesures[colonne].max()
    print(f"{colonne} : min = {minimum}, moyenne = {moyenne:.2f}, max = {maximum}")

# 10 Les mêmes calculs, mais polluant par polluant (groupby)
minimums = mesures.groupby('Polluant')['valeur'].min()
moyennes = mesures.groupby('Polluant')['valeur'].mean()
maximums = mesures.groupby('Polluant')['valeur'].max()
nb_mesures = mesures.groupby('Polluant')['valeur'].count()

# on met les 4 séries côte à côte dans un seul tableau
resume_polluants = pd.concat([nb_mesures, minimums, moyennes, maximums], axis=1)
resume_polluants.columns = ['nb mesures', 'min', 'moyenne', 'max']
print("\n Valeurs par polluant")
print(resume_polluants)

# 11 Quelle unité pour quel polluant ?
print("\n Unité utilisée par polluant")
print(mesures.groupby('Polluant')['unité de mesure'].unique())

# Tâche C3 : fusion des mesures avec les stations et les zones,
# puis ajout de colonnes utiles pour l'analyse (région, mois, saison, jour)
# Entrées : data_clean/mesures_journalieres_2025.csv (A3, Amel)
#           data_clean/stations.csv et data_clean/zones.csv (C1)
# Sortie  : data_clean/mesures_fusionnees_2025.csv
# A lancer depuis le dossier du projet : python scripts/05_fusion.py
# Il faut avoir lancé 03_metadonnees.py et 04_annee_complete.py avant.

import pandas as pd

# --- 1. Lecture des trois fichiers ---
mesures = pd.read_csv("data_clean/mesures_journalieres_2025.csv", sep=";", encoding="utf-8-sig")
stations = pd.read_csv("data_clean/stations.csv", sep=";", encoding="utf-8-sig")
zones = pd.read_csv("data_clean/zones.csv", sep=";", encoding="utf-8-sig")

print("Mesures  :", mesures.shape)
print("Stations :", stations.shape)
print("Zones    :", zones.shape)

# --- 2. Colonnes qu'on veut ajouter aux mesures ---
# les dates d'activité des stations ne servent plus pour l'analyse
stations = stations[["code site", "nom station", "commune", "latitude", "longitude",
                     "altitude", "typologie", "territoire"]].copy()
# le nom de la zone est déjà dans les mesures (colonne "Zas")
zones = zones[["code zas", "type zone", "population", "superficie km2", "densite"]].copy()

# --- 3. Fusion avec pd.merge ---
# how="left" : on garde toutes les lignes des mesures et on leur ajoute
# les informations de leur station, puis de leur zone
nb_lignes_avant = len(mesures)
fusion = pd.merge(mesures, stations, on="code site", how="left")
fusion = pd.merge(fusion, zones, on="code zas", how="left")

# vérifications : le nombre de lignes ne doit pas changer
# et chaque mesure doit avoir trouvé sa station et sa zone
print("\nLignes avant la fusion :", nb_lignes_avant, "/ après :", len(fusion))
print("Mesures sans station trouvée :", fusion["nom station"].isna().sum())
print("Mesures sans zone trouvée    :", fusion["type zone"].isna().sum())

# dans les mesures, 22 stations changent de nom en cours d'année :
# on garde le nom unique de stations.csv ("nom station") et on enlève "nom site"
fusion = fusion.drop(columns=["nom site"])

# --- 4. Région ---
# chaque région a son organisme de surveillance (AASQA) : colonne "Organisme"
regions = {
    "AIR BREIZH": "Bretagne",
    "AIR PAYS DE LA LOIRE": "Pays de la Loire",
    "AIRPARIF": "Île-de-France",
    "ATMO AUVERGNE-RHÔNE-ALPES": "Auvergne-Rhône-Alpes",
    "ATMO BOURGOGNE-FRANCHE-COMTE": "Bourgogne-Franche-Comté",
    "ATMO GRAND EST": "Grand Est",
    "ATMO GUYANE": "Guyane",
    "ATMO HAUTS DE FRANCE": "Hauts-de-France",
    "ATMO NORMANDIE": "Normandie",
    "ATMO NOUVELLE-AQUITAINE": "Nouvelle-Aquitaine",
    "ATMO OCCITANIE": "Occitanie",
    "ATMO REUNION": "La Réunion",
    "ATMO SUD": "Provence-Alpes-Côte d'Azur",
    "GWAD'AIR": "Guadeloupe",
    "HAWA MAYOTTE": "Mayotte",
    "LIG'AIR": "Centre-Val de Loire",
    "MADININAIR": "Martinique",
    "QUALITAIR CORSE": "Corse",
}
fusion["region"] = fusion["Organisme"].map(regions)
print("Mesures sans région          :", fusion["region"].isna().sum())

# --- 5. Colonnes de temps ---
fusion["date"] = pd.to_datetime(fusion["date"], format="%Y-%m-%d")

# mois : de 1 à 12
fusion["mois"] = [d.month for d in fusion["date"]]

# saison : même découpage que dans 06_analyse_temps.py (Amel)
saisons = {12: "hiver", 1: "hiver", 2: "hiver",
           3: "printemps", 4: "printemps", 5: "printemps",
           6: "été", 7: "été", 8: "été",
           9: "automne", 10: "automne", 11: "automne"}
fusion["saison"] = fusion["mois"].map(saisons)

# jour de la semaine : weekday() donne 0 pour lundi ... 6 pour dimanche
noms_jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
fusion["jour semaine"] = [noms_jours[d.weekday()] for d in fusion["date"]]
fusion["week-end"] = fusion["jour semaine"].isin(["samedi", "dimanche"])

# --- 6. Petits tableaux de contrôle ---
print("\nNombre de lignes par saison :")
print(fusion.groupby("saison")["date"].aggregate("count"))
print("\nNombre de lignes par territoire :")
print(fusion.groupby("territoire")["date"].aggregate("count"))
print("\nColonnes finales :", fusion.columns.tolist())

# --- 7. Enregistrement ---
fusion.to_csv("data_clean/mesures_fusionnees_2025.csv", sep=";", index=False, encoding="utf-8-sig")
print("\n-> data_clean/mesures_fusionnees_2025.csv enregistré :", fusion.shape)

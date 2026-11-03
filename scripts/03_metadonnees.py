# Tâche C1 : explorer et nettoyer les métadonnées (stations et zones)
# Entrées : data/metadonnees_stations.xls (onglet AirQualityStations)
#           data/metadonnees_zones_surveillance.xls (onglet AirQualityZones)
# Sorties : data_clean/stations.csv et data_clean/zones.csv
# A lancer depuis le dossier du projet : python scripts/03_metadonnees.py

import re
import pandas as pd


# =====================================================================
# PARTIE 1 : LES STATIONS
# =====================================================================

# --- 1. Lecture du fichier Excel ---
# read_excel marche comme read_csv, mais pour un fichier Excel.
# sheet_name = nom de l'onglet à lire.
stations = pd.read_excel("data/metadonnees_stations.xls", sheet_name="AirQualityStations")

print("=== STATIONS : fichier brut ===")
print("Lignes, colonnes :", stations.shape)
print("Valeurs manquantes par colonne :")
print(stations.isna().sum())

# --- 2. On garde seulement les colonnes utiles ---
colonnes_utiles = ["NatlStationCode", "Name", "Municipality", "Latitude", "Longitude",
                   "Altitude", "AreaClassification", "ActivityBegin", "ActivityEnd"]
stations = stations[colonnes_utiles].copy()

# noms en français ; "code site" = même nom que dans les fichiers de mesures
stations = stations.rename(columns={
    "NatlStationCode": "code site",
    "Name": "nom station",
    "Municipality": "commune",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Altitude": "altitude",
    "AreaClassification": "typologie",
    "ActivityBegin": "debut activite",
    "ActivityEnd": "fin activite",
})


# --- 3. Doublons et format des codes ---
nb_avant = len(stations)
stations = stations.drop_duplicates()
print("\nLignes en double supprimées :", nb_avant - len(stations))

# chaque station doit avoir un code différent
print("Codes différents :", len(stations["code site"].unique()), "pour", len(stations), "stations")

def code_station_correct(code):
    # format attendu : "FR" suivi de 5 chiffres (ex : FR04002)
    if re.search("^FR[0-9]{5}$", code):
        return True
    else:
        return False

nb_corrects = stations["code site"].apply(code_station_correct).sum()
print("Codes au bon format :", nb_corrects, "sur", len(stations))


# --- 4. Typologie : garder seulement le dernier mot de l'adresse ---
# ex : "http://.../areaclassification/urban" -> "urban"
def dernier_mot(adresse):
    morceaux = re.split("/", adresse)  # on coupe à chaque "/"
    return morceaux[-1]                # -1 = dernier élément de la liste

stations["typologie"] = stations["typologie"].apply(dernier_mot)

# tableau de fréquences : nombre de stations par typologie
print("\nNombre de stations par typologie :")
print(stations.groupby("typologie")["code site"].aggregate("count"))


# --- 5. Communes : enlever les accents ---
# la même commune est parfois écrite avec et sans accent
# (ex : "POINTE-A-PITRE" et "POINTE-À-PITRE")
accents = {"À": "A", "Â": "A", "Ç": "C", "É": "E", "È": "E", "Ê": "E", "Ë": "E",
           "Î": "I", "Ï": "I", "Ô": "O", "Û": "U", "Ù": "U", "Œ": "OE"}

def enlever_accents(texte):
    for lettre in accents:
        texte = re.sub(lettre, accents[lettre], texte)
    return texte

print("\nCommunes différentes avant :", len(stations["commune"].unique()))
stations["commune"] = stations["commune"].apply(enlever_accents)
print("Communes différentes après :", len(stations["commune"].unique()))


# --- 6. Coordonnées GPS et altitude ---
print("\nLatitude  : min", stations["latitude"].min(), "/ max", stations["latitude"].max())
print("Longitude : min", stations["longitude"].min(), "/ max", stations["longitude"].max())
print("Altitude  : min", stations["altitude"].min(), "/ max", stations["altitude"].max(), "(en m)")

# rectangle autour de la France métropolitaine (Corse comprise)
en_metropole = ((stations["latitude"] > 41) & (stations["latitude"] < 51.5)
                & (stations["longitude"] > -5.5) & (stations["longitude"] < 10))
stations["territoire"] = en_metropole.map({True: "metropole", False: "outre-mer"})

# on affiche les communes hors du rectangle pour vérifier que ce sont des DROM
hors_metropole = stations[stations["territoire"] == "outre-mer"]
print("Stations hors métropole :", len(hors_metropole))
print(hors_metropole["commune"].unique())


# --- 7. Dates d'activité et stations ouvertes en 2025 ---
# texte "2014-11-04T00:00:00+01:00" -> date
# une case vide (station encore ouverte) devient NaT (= date manquante)
format_date = "%Y-%m-%dT%H:%M:%S+01:00"
stations["debut activite"] = pd.to_datetime(stations["debut activite"], format=format_date)
stations["fin activite"] = pd.to_datetime(stations["fin activite"], format=format_date)

# ouverte en 2025 = ouverte avant 2026 ET (pas de date de fin OU fermée en 2025 ou après)
debut_2025 = pd.to_datetime("2025-01-01", format="%Y-%m-%d")
debut_2026 = pd.to_datetime("2026-01-01", format="%Y-%m-%d")
ouverte_en_2025 = ((stations["debut activite"] < debut_2026)
                   & (stations["fin activite"].isna() | (stations["fin activite"] >= debut_2025)))

nb_avant = len(stations)
stations = stations[ouverte_en_2025].copy()
print("\nStations fermées avant 2025 ou ouvertes après 2025 (supprimées) :", nb_avant - len(stations))
print("Stations gardées :", len(stations))


# --- 8. Enregistrement ---
stations = stations.sort_values("code site")
stations.to_csv("data_clean/stations.csv", sep=";", index=False, encoding="utf-8-sig")
print("-> data_clean/stations.csv enregistré")


# =====================================================================
# PARTIE 2 : LES ZONES DE SURVEILLANCE (ZAS)
# =====================================================================

# --- 1. Lecture ---
zones = pd.read_excel("data/metadonnees_zones_surveillance.xls", sheet_name="AirQualityZones")

print("\n=== ZONES : fichier brut ===")
print("Lignes, colonnes :", zones.shape)
print("Valeurs manquantes par colonne :")
print(zones.isna().sum())
print("Année du recensement de la population :", zones["ResidentPopulationYear"].unique())

# --- 2. Colonnes utiles ---
zones = zones[["ZoneCode", "GeographicalName", "ResidentPopulation", "Area [km2]"]].copy()
zones = zones.rename(columns={
    "ZoneCode": "code zas",        # même nom que dans les fichiers de mesures
    "GeographicalName": "nom zone",
    "ResidentPopulation": "population",
    "Area [km2]": "superficie km2",
})

# --- 3. Doublons et format des codes ---
nb_avant = len(zones)
zones = zones.drop_duplicates()
print("\nLignes en double supprimées :", nb_avant - len(zones))
print("Codes différents :", len(zones["code zas"].unique()), "pour", len(zones), "zones")

def code_zone_correct(code):
    # format attendu : "FR" + 2 chiffres + ZAG, ZAR ou ZRE + 2 chiffres (ex : FR01ZAG01)
    if re.search("^FR[0-9]{2}(ZAG|ZAR|ZRE)[0-9]{2}$", code):
        return True
    else:
        return False

nb_corrects = zones["code zas"].apply(code_zone_correct).sum()
print("Codes au bon format :", nb_corrects, "sur", len(zones))

# --- 4. Type de zone, lu dans le code ---
# Dans les noms on trouve "ZR" et "ZRE" pour le même type : le code est plus fiable.
# ex : "FR01ZAG01" -> caractères 4, 5 et 6 -> "ZAG"
def lettres_type(code):
    return code[4:7]

types_zone = {"ZAG": "agglomeration", "ZAR": "zone a risque", "ZRE": "zone regionale"}
zones["type zone"] = zones["code zas"].apply(lettres_type)
zones["type zone"] = zones["type zone"].map(types_zone)

print("\nNombre de zones par type :")
print(zones.groupby("type zone")["code zas"].aggregate("count"))

# --- 5. Vérification des valeurs et densité de population ---
print("\nPopulation : min", zones["population"].min(), "/ max", zones["population"].max())
print("Superficie : min", zones["superficie km2"].min(), "/ max", zones["superficie km2"].max(), "km2")

# densité = habitants par km2, arrondie à 1 chiffre après la virgule
zones["densite"] = zones["population"] / zones["superficie km2"]
zones["densite"] = zones["densite"].apply(lambda d: round(d, 1))
print("Densité : min", zones["densite"].min(), "/ max", zones["densite"].max(), "hab/km2")

# --- 6. Enregistrement ---
zones = zones.sort_values("code zas")
zones.to_csv("data_clean/zones.csv", sep=";", index=False, encoding="utf-8-sig")
print("-> data_clean/zones.csv enregistré")

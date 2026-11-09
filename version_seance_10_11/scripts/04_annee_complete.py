# A3 - Passage à l'année complète (365 fichiers)
# Pour chaque jour : lecture, nettoyage (fonction de A2), puis réduction
# à une moyenne par jour, par station et par polluant.
# On ne garde jamais les 17,6 millions de lignes en mémoire en même temps.
# Résultats :
#   data_clean/mesures_journalieres_2025.csv        (toute l'année, par jour)
#   data_clean/mesures_horaires_janvier_juillet_2025.csv (détail heure par heure)
# A lancer depuis le dossier du projet, dans un terminal :
#   python scripts/04_annee_complete.py
# Durée : 2 à 3 minutes.

import pandas as pd
from nettoyage_mesures import nettoyer_mesures

DOSSIER = "data/mesures_horaires_2025"

# colonnes qui décrivent une station et un polluant : on regroupe sur elles
COLONNES_GROUPE = ['date', 'Organisme', 'code zas', 'Zas', 'code site',
                   'nom site', "type d'implantation", "type d'influence",
                   'Polluant']

# colonnes gardées pour le détail heure par heure (janvier et juillet)
COLONNES_HORAIRES = ['Date de début', 'code site', 'Polluant',
                     "type d'implantation", "type d'influence", 'valeur']

# une moyenne journalière n'est fiable que si on a assez d'heures :
# la règle européenne demande au moins 75 % des 24 heures, soit 18 heures
NB_HEURES_MIN = 18

liste_jours = []      # les moyennes journalières de chaque jour
liste_horaires = []   # le détail horaire de janvier et juillet
nb_lignes_brutes = 0
nb_lignes_propres = 0

for mois in range(1, 13):
    for jour in range(1, 32):
        date = f"2025-{mois:02d}-{jour:02d}"
        nom_fichier = f"{DOSSIER}/mesures_horaires_{date}.csv"
        try:
            mesures = pd.read_csv(nom_fichier, sep=';', encoding='utf-8-sig')
        except FileNotFoundError:
            # ce jour n'existe pas (ex : 31 février)
            continue

        propres = nettoyer_mesures(mesures)
        nb_lignes_brutes = nb_lignes_brutes + len(mesures)
        nb_lignes_propres = nb_lignes_propres + len(propres)

        # en janvier et juillet, on garde aussi le détail heure par heure
        if mois == 1 or mois == 7:
            liste_horaires.append(propres[COLONNES_HORAIRES].copy())

        # moyenne, maximum et nombre d'heures, par station et par polluant
        propres['date'] = date
        groupes = propres.groupby(COLONNES_GROUPE, as_index=False)['valeur']
        resume_jour = groupes.mean()
        resume_jour = resume_jour.rename(columns={'valeur': 'moyenne'})
        # les trois calculs sont faits sur les mêmes groupes, dans le même
        # ordre : on peut donc ajouter les colonnes directement
        resume_jour['max horaire'] = groupes.max()['valeur']
        resume_jour['nb heures'] = groupes.count()['valeur']

        liste_jours.append(resume_jour)
        print(f"{date} : {len(mesures)} lignes -> {len(resume_jour)} lignes")

# on met tous les jours bout à bout
journalier = pd.concat(liste_jours, ignore_index=True)
horaire = pd.concat(liste_horaires, ignore_index=True)

print("\n===== Bilan =====")
print("Nombre de jours lus :", len(liste_jours))
print("Lignes brutes :", nb_lignes_brutes)
print("Lignes après nettoyage :", nb_lignes_propres)
print("Lignes journalières :", len(journalier))

# on enlève les moyennes calculées sur trop peu d'heures
nb_avant = len(journalier)
journalier = journalier[journalier['nb heures'] >= NB_HEURES_MIN].copy()
print(f"Moyennes sur moins de {NB_HEURES_MIN} h enlevées :", nb_avant - len(journalier))

# la date devient une vraie date et les valeurs sont arrondies
journalier['date'] = pd.to_datetime(journalier['date'], format='%Y-%m-%d')
journalier['moyenne'] = journalier['moyenne'].round(2)

# vérification des valeurs sur l'année entière
print("\nValeurs par polluant sur l'année (µg/m3) :")
print(journalier.groupby('Polluant').aggregate({'moyenne': 'mean',
                                                'max horaire': 'max'}).round(1))
print("\nNombre de stations :", len(journalier['code site'].unique()))

# enregistrement
journalier.to_csv("data_clean/mesures_journalieres_2025.csv",
                  sep=';', index=False, encoding='utf-8-sig')
horaire.to_csv("data_clean/mesures_horaires_janvier_juillet_2025.csv",
               sep=';', index=False, encoding='utf-8-sig')
print("\nFichiers enregistrés dans data_clean/ :")
print("mesures_journalieres_2025.csv :", journalier.shape)
print("mesures_horaires_janvier_juillet_2025.csv :", horaire.shape)

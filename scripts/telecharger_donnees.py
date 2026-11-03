# Télécharge les 365 fichiers de mesures horaires de 2025 depuis data.gouv.fr
# et les range dans data/mesures_horaires_2025 avec nos noms de fichiers.
# A lancer depuis le dossier du projet : python scripts/telecharger_donnees.py
# Durée : 10 à 20 minutes selon la connexion (3,7 Go au total).

import os
import urllib.request

ADRESSE = "https://files.data.gouv.fr/ineris/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/2025/"
DOSSIER = "data/mesures_horaires_2025"

# on crée le dossier s'il n'existe pas encore
os.makedirs(DOSSIER, exist_ok=True)

nb_telecharges = 0
for mois in range(1, 13):
    for jour in range(1, 32):
        date = f"2025-{mois:02d}-{jour:02d}"
        nom_origine = f"FR_E2_{date}.csv"
        nom_fichier = f"{DOSSIER}/mesures_horaires_{date}.csv"

        # si le fichier est déjà là, on ne le retélécharge pas
        if os.path.exists(nom_fichier):
            continue

        try:
            urllib.request.urlretrieve(ADRESSE + nom_origine, nom_fichier)
            nb_telecharges = nb_telecharges + 1
            print(f"OK : {date}")
        except Exception:
            # ce jour n'existe pas (ex : 31 février)
            continue

print(f"Terminé : {nb_telecharges} fichiers téléchargés.")

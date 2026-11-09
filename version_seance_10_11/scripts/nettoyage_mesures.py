# A2 - Nettoyage d'un fichier de mesures (un jour)
# Deux fonctions :
#   - verifier_mesures : contrôles, affiche ce qu'elle trouve, ne modifie rien
#   - nettoyer_mesures : renvoie une copie nettoyée du tableau
# Elles seront réutilisées dans la boucle sur les 365 jours (tâche A3).
# A lancer depuis le dossier du projet.

import re
import pandas as pd

FORMAT_DATE = '%Y/%m/%d %H:%M:%S'


def verifier_mesures(mesures):
    """Contrôles sur un tableau de mesures brut. Ne modifie rien."""

    # 1. Format des codes (expressions régulières)
    # code site : FR + 5 chiffres (ex : FR01011)
    # code zas : FR + 2 chiffres + Z + 2 lettres + 2 chiffres (ex : FR44ZAG02)
    codes_site_faux = [code for code in mesures['code site'].unique()
                       if not re.search(r"^FR\d{5}$", code)]
    codes_zas_faux = [code for code in mesures['code zas'].unique()
                      if not re.search(r"^FR\d{2}Z[A-Z]{2}\d{2}$", code)]
    print("Codes site au mauvais format :", codes_site_faux)
    print("Codes zas au mauvais format :", codes_zas_faux)

    # 2. Colonnes liées : date de fin = date de début + 1 heure ?
    debut = pd.to_datetime(mesures['Date de début'], format=FORMAT_DATE)
    fin = pd.to_datetime(mesures['Date de fin'], format=FORMAT_DATE)
    une_heure = pd.Timedelta(hours=1)
    nb_ecarts_faux = len(mesures[(fin - debut) != une_heure])
    print("Lignes où la mesure ne dure pas 1 heure :", nb_ecarts_faux)

    # 3. Colonnes liées : un code site correspond à un seul nom ?
    noms_par_site = mesures.groupby('code site')['nom site'].unique()
    sites_plusieurs_noms = [code for code in noms_par_site.index
                            if len(noms_par_site[code]) > 1]
    print("Stations avec plusieurs noms :", sites_plusieurs_noms)

    # 4. Colonnes liées : validité et code qualité (tableau de contingence)
    print("\nNombre de lignes par code qualité et validité :")
    print(mesures.groupby(['code qualité', 'validité'])['Polluant'].count())

    # 5. Les valeurs manquantes sont-elles les données invalides ?
    manquantes = mesures[mesures['valeur'].isna()]
    print("\nValidité des lignes sans valeur :", manquantes['validité'].unique())

    # 6. Valeurs négatives (impossible pour une concentration)
    negatives = mesures[mesures['valeur'] < 0]
    print("Nombre de valeurs négatives :", len(negatives))

    # 7. Valeurs élevées : méthode de l'IQR, polluant par polluant
    # (au-dessus de Q3 + 1,5 x IQR, comme les moustaches d'un boxplot)
    print("\nValeurs au-dessus de Q3 + 1,5 x IQR :")
    for polluant in mesures['Polluant'].unique():
        valeurs = mesures[mesures['Polluant'] == polluant]['valeur']
        q1 = valeurs.quantile(0.25)
        q3 = valeurs.quantile(0.75)
        limite = q3 + 1.5 * (q3 - q1)
        nb_hautes = len(valeurs[valeurs > limite])
        print(f"{polluant} : {nb_hautes} valeurs > {limite:.1f}, max = {valeurs.max()}")


def nettoyer_mesures(mesures, afficher=False):
    """Renvoie une copie nettoyée d'un tableau de mesures brut.
    afficher=True : affiche le nombre de lignes après chaque étape."""

    donnees = mesures.copy()
    if afficher:
        print("Départ :", len(donnees), "lignes")

    # Etape 1 : on enlève les données invalides (validité = -1)
    # ce sont exactement les lignes sans valeur
    donnees = donnees[donnees['validité'] != -1].copy()
    if afficher:
        print("Etape 1 - sans les données invalides :", len(donnees), "lignes")

    # Etape 2 : doublons cachés
    # même station, même polluant, même heure, même appareil, même valeur :
    # c'est la même mesure envoyée deux fois avec un discriminant différent
    colonnes_doublon = ['code site', 'Polluant', 'Date de début',
                        'procédure de mesure', 'valeur']
    donnees.drop_duplicates(subset=colonnes_doublon, keep='first', inplace=True)
    if afficher:
        print("Etape 2 - sans les doublons :", len(donnees), "lignes")

    # Etape 3 : colonnes inutiles
    # 3 colonnes toujours vides, 2 colonnes qui ont toujours la même valeur,
    # la valeur brute (presque identique à valeur), la date de fin (toujours
    # début + 1 h) et la procédure de mesure (détail technique)
    colonnes_inutiles = ['taux de saisie', 'couverture temporelle',
                         'couverture de données', 'Réglementaire',
                         'type de valeur', 'valeur brute', 'Date de fin',
                         'procédure de mesure']
    donnees.drop(columns=colonnes_inutiles, inplace=True)

    # Etape 4 : texte - on enlève les espaces en trop autour des noms
    # (ex : "Troyes La Tour " devient "Troyes La Tour")
    donnees['nom site'] = donnees['nom site'].map(lambda x: x.strip())

    # Etape 5 : CO en mg/m3 -> µg/m3 (1 mg = 1000 µg)
    # pour que tous les polluants soient dans la même unité
    lignes_co = donnees['Polluant'] == 'CO'
    donnees.loc[lignes_co, 'valeur'] = donnees.loc[lignes_co, 'valeur'] * 1000

    # Etape 6 : une seule écriture de l'unité
    unites = {'µg-m3': 'µg/m3', 'µg/m3': 'µg/m3', 'mg-m3': 'µg/m3'}
    donnees['unité de mesure'] = donnees['unité de mesure'].map(unites)

    # Etape 7 : valeurs négatives -> 0
    # l'appareil se trompe un peu quand l'air est presque propre
    lignes_negatives = donnees['valeur'] < 0
    if afficher:
        print("Etape 7 - valeurs négatives mises à 0 :", len(donnees[lignes_negatives]))
    donnees.loc[lignes_negatives, 'valeur'] = 0

    # Etape 8 : la date devient une vraie date (et plus du texte)
    donnees['Date de début'] = pd.to_datetime(donnees['Date de début'],
                                              format=FORMAT_DATE)

    # on renumérote les lignes de 0 à n-1
    donnees = donnees.reset_index(drop=True)
    return donnees


# Partie test : ne s'exécute que si on lance ce fichier directement,
# pas quand on importe les fonctions depuis un autre script
if __name__ == "__main__":
    FICHIER = "data/mesures_horaires_2025/mesures_horaires_2025-01-01.csv"
    mesures = pd.read_csv(FICHIER, sep=';', encoding='utf-8-sig')

    print("===== Vérifications sur les données brutes =====")
    verifier_mesures(mesures)

    print("\n===== Nettoyage =====")
    mesures_propres = nettoyer_mesures(mesures, afficher=True)

    print("\n===== Résultat =====")
    print("Taille :", mesures_propres.shape)
    print(mesures_propres.dtypes)
    print(mesures_propres.head())
    print("Unités :", mesures_propres['unité de mesure'].unique())
    print("Valeur minimum :", mesures_propres['valeur'].min())

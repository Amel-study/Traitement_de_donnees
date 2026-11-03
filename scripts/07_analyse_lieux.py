# Tâche C4 : analyse selon les lieux
#   1. dépassement des seuils OMS jour par jour
#   2. moyenne annuelle de chaque station (fichier utile pour la carte A6)
#   3. stations au-dessus des seuils annuels et des seuils sur 24 h
#   4. comparaison des régions
#   5. comparaison des types de zones
#   6. lien avec la densité de population
#   7. nombre de jours au-dessus des seuils (OMS et seuils français)
#   8. part des jours au-dessus de l'OMS par région
#   9. tableaux de contingence
# Les seuils viennent de docs/variables_et_graphiques.md (C2).
# Tableaux affichés et enregistrés dans resultats/ (.csv),
# graphiques plotly enregistrés dans resultats/ (.html, à ouvrir avec un navigateur).
# A lancer depuis le dossier du projet : python scripts/07_analyse_lieux.py
# Il faut avoir lancé 05_fusion.py avant.

import os
import pandas as pd
import plotly.express as px

os.makedirs("resultats", exist_ok=True)

# les 4 polluants principaux (mêmes que dans A4)
POLLUANTS = ['NO2', 'O3', 'PM10', 'PM2.5']

donnees = pd.read_csv("data_clean/mesures_fusionnees_2025.csv", sep=";", encoding="utf-8-sig")
print("Données :", donnees.shape)


# ---------------------------------------------------------------
# 1. Dépassement des recommandations OMS 2021 sur 24 h, jour par jour
# ---------------------------------------------------------------
# en µg/m3 ; pour le CO : 4 mg/m3 = 4000 µg/m3
SEUILS_OMS_24H = {'PM2.5': 15, 'PM10': 45, 'NO2': 25, 'SO2': 40, 'CO': 4000}

donnees['seuil OMS'] = donnees['Polluant'].map(SEUILS_OMS_24H)
# True si la moyenne du jour est au-dessus du seuil
# (False pour les polluants sans seuil : la comparaison avec NaN donne False)
donnees['depasse OMS'] = donnees['moyenne'] > donnees['seuil OMS']


# ---------------------------------------------------------------
# 2. Moyenne annuelle de chaque station, pour chaque polluant
# ---------------------------------------------------------------
colonnes_station = ['code site', 'nom station', 'commune', 'region', 'territoire',
                    'latitude', 'longitude', 'typologie', 'type zone', 'Zas', 'densite',
                    "type d'influence", 'Polluant']

annuel = donnees.groupby(colonnes_station, as_index=False).aggregate(
    {'moyenne': 'mean', 'date': 'count', 'depasse OMS': 'sum'})
annuel = annuel.rename(columns={'moyenne': 'moyenne annuelle',
                                'date': 'nb jours',
                                'depasse OMS': 'jours au-dessus OMS'})
annuel['moyenne annuelle'] = annuel['moyenne annuelle'].round(1)

# fichier pour la carte d'Amel (A6) : toutes les stations, avec le nombre de jours mesurés
annuel.to_csv("data_clean/moyennes_annuelles_stations.csv", sep=";", index=False, encoding="utf-8-sig")

# une moyenne annuelle n'est représentative que si la station a mesuré
# au moins 75 % de l'année (274 jours) : même idée que les 18 h sur 24 en A3
NB_JOURS_MIN = 274
annuel_complet = annuel[annuel['nb jours'] >= NB_JOURS_MIN].copy()
print("\nCouples station-polluant :", len(annuel),
      "/ avec au moins", NB_JOURS_MIN, "jours :", len(annuel_complet))


# ---------------------------------------------------------------
# 3. Combien de stations sont au-dessus des seuils ?
# ---------------------------------------------------------------
# seuils annuels : recommandation OMS et valeur limite UE / France
SEUILS_OMS_AN = {'PM2.5': 5, 'PM10': 15, 'NO2': 10}
VALEURS_LIMITES_AN = {'PM2.5': 25, 'PM10': 40, 'NO2': 40}

lignes = []
for polluant in SEUILS_OMS_AN:
    stations_p = annuel_complet[annuel_complet['Polluant'] == polluant]
    nb_stations = len(stations_p)
    nb_oms = (stations_p['moyenne annuelle'] > SEUILS_OMS_AN[polluant]).sum()
    nb_vl = (stations_p['moyenne annuelle'] > VALEURS_LIMITES_AN[polluant]).sum()
    lignes.append({'Polluant': polluant,
                   'nb stations': nb_stations,
                   'au-dessus OMS': nb_oms,
                   '% OMS': round(100 * nb_oms / nb_stations, 1),
                   'au-dessus valeur limite': nb_vl})
tableau_annuel = pd.DataFrame(lignes)
print("\n===== 3a. Stations dont la moyenne annuelle dépasse les seuils annuels =====")
print(tableau_annuel)
tableau_annuel.to_csv("resultats/stations_seuils_annuels.csv", sep=";", index=False, encoding="utf-8-sig")

# quelles stations dépassent la valeur limite annuelle du NO2 (40 µg/m3) ?
no2_annuel = annuel_complet[annuel_complet['Polluant'] == 'NO2']
print("\nStations au-dessus de 40 µg/m3 de NO2 en moyenne annuelle :")
print(no2_annuel[no2_annuel['moyenne annuelle'] > 40][['nom station', 'commune', "type d'influence", 'moyenne annuelle']])

# seuil OMS sur 24 h : l'OMS tolère 3 à 4 jours de dépassement par an
lignes = []
for polluant in SEUILS_OMS_24H:
    stations_p = annuel_complet[annuel_complet['Polluant'] == polluant]
    nb_stations = len(stations_p)
    nb_plus_de_4 = (stations_p['jours au-dessus OMS'] > 4).sum()
    lignes.append({'Polluant': polluant,
                   'nb stations': nb_stations,
                   'plus de 4 jours au-dessus OMS 24 h': nb_plus_de_4,
                   '%': round(100 * nb_plus_de_4 / nb_stations, 1)})
tableau_24h = pd.DataFrame(lignes)
print("\n===== 3b. Stations avec plus de 4 jours au-dessus de l'OMS 24 h =====")
print(tableau_24h)
tableau_24h.to_csv("resultats/stations_seuils_24h.csv", sep=";", index=False, encoding="utf-8-sig")

# valeur limite PM10 sur 24 h : pas plus de 35 jours au-dessus de 50 µg/m3
pm10 = donnees[donnees['Polluant'] == 'PM10'].copy()
pm10['au-dessus 50'] = pm10['moyenne'] > 50
pm10_stations = pm10.groupby(['code site', 'nom station', 'region'], as_index=False)['au-dessus 50'].sum()
print("\nPM10 : stations avec plus de 35 jours au-dessus de 50 µg/m3 :",
      (pm10_stations['au-dessus 50'] > 35).sum())
print("Les 5 stations avec le plus de jours au-dessus de 50 µg/m3 :")
print(pm10_stations.sort_values('au-dessus 50', ascending=False).head(5))


# ---------------------------------------------------------------
# 4. Comparaison des régions (stations de fond seulement)
# ---------------------------------------------------------------
# On ne garde que les stations de fond : sinon une région avec beaucoup
# de stations au bord des routes paraîtrait plus polluée qu'elle ne l'est.
fond = annuel_complet[(annuel_complet["type d'influence"] == 'Fond')
                      & (annuel_complet['Polluant'].isin(POLLUANTS))]
par_region = fond.groupby(['region', 'Polluant'], as_index=False)['moyenne annuelle'].mean()
par_region['moyenne annuelle'] = par_region['moyenne annuelle'].round(1)

tableau_regions = par_region.pivot_table(index='region', columns='Polluant', values='moyenne annuelle')
print("\n===== 4. Moyenne annuelle des stations de fond par région (µg/m3) =====")
print(tableau_regions)
tableau_regions.to_csv("resultats/regions.csv", sep=";", encoding="utf-8-sig")

fig = px.bar(par_region, x='region', y='moyenne annuelle', color='Polluant', barmode='group',
             title="Moyenne annuelle des stations de fond par région en 2025",
             labels={'region': 'Région', 'moyenne annuelle': 'Concentration (µg/m3)'})
fig.write_html("resultats/regions.html")


# ---------------------------------------------------------------
# 5. Comparaison des types de zones (agglomération, zone à risque, zone régionale)
# ---------------------------------------------------------------
principaux = annuel_complet[annuel_complet['Polluant'].isin(POLLUANTS)]
tableau_zones = principaux.pivot_table(index='type zone', columns='Polluant',
                                       values='moyenne annuelle', aggfunc='median').round(1)
print("\n===== 5. Médiane des moyennes annuelles par type de zone (µg/m3) =====")
print(tableau_zones)

# boxplot : une station = un point
fig = px.box(principaux, x='Polluant', y='moyenne annuelle', color='type zone',
             hover_name='nom station',
             title="Moyennes annuelles des stations selon le type de zone (2025)",
             labels={'moyenne annuelle': 'Concentration (µg/m3)', 'type zone': 'Type de zone'})
fig.write_html("resultats/types_zones.html")


# ---------------------------------------------------------------
# 6. Lien avec la densité de population (NO2, stations de fond)
# ---------------------------------------------------------------
no2_fond = fond[fond['Polluant'] == 'NO2'].copy()

# classes de densité avec pd.cut (cours 3) ; numérotées pour garder l'ordre
bornes = [0, 100, 300, 1000, 4000]
noms_classes = ['1. moins de 100', '2. de 100 à 300', '3. de 300 à 1000', '4. plus de 1000']
no2_fond['classe densite'] = pd.cut(no2_fond['densite'], bins=bornes, labels=noms_classes, right=False)
no2_fond['classe densite'] = no2_fond['classe densite'].astype(str)

par_classe = no2_fond.groupby('classe densite').aggregate({'moyenne annuelle': 'mean', 'code site': 'count'})
par_classe = par_classe.rename(columns={'moyenne annuelle': 'NO2 moyen (µg/m3)', 'code site': 'nb stations'})
print("\n===== 6. NO2 des stations de fond selon la densité de la zone (hab/km2) =====")
print(par_classe.round(1))

# nuage de points : une zone = un point
par_zone = no2_fond.groupby(['Zas', 'type zone', 'densite'], as_index=False)['moyenne annuelle'].mean()
fig = px.scatter(par_zone, x='densite', y='moyenne annuelle', color='type zone', hover_name='Zas',
                 title="NO2 moyen des stations de fond selon la densité de la zone (2025)",
                 labels={'densite': 'Densité de population (hab/km2)',
                         'moyenne annuelle': 'NO2 (µg/m3)', 'type zone': 'Type de zone'})
fig.write_html("resultats/densite_no2.html")


# ---------------------------------------------------------------
# 7. Nombre de jours au-dessus des seuils (une ligne = un jour pour une station)
# ---------------------------------------------------------------
def compter_jours(polluant, colonne, seuil, nom_seuil):
    lignes_p = donnees[donnees['Polluant'] == polluant]
    au_dessus = lignes_p[lignes_p[colonne] > seuil]
    return {'Polluant': polluant,
            'seuil': nom_seuil,
            'valeur (µg/m3)': seuil,
            'jours-stations mesurés': len(lignes_p),
            'jours-stations au-dessus': len(au_dessus),
            '% au-dessus': round(100 * len(au_dessus) / len(lignes_p), 2),
            'stations concernées': len(au_dessus['code site'].unique())}

# "moyenne" = moyenne du jour ; "max horaire" = au moins une heure au-dessus ce jour-là
liste_seuils = [
    compter_jours('PM2.5', 'moyenne', 15, 'OMS 24 h'),
    compter_jours('PM10', 'moyenne', 45, 'OMS 24 h'),
    compter_jours('NO2', 'moyenne', 25, 'OMS 24 h'),
    compter_jours('SO2', 'moyenne', 40, 'OMS 24 h'),
    compter_jours('CO', 'moyenne', 4000, 'OMS 24 h'),
    compter_jours('PM10', 'moyenne', 50, 'information (moyenne du jour)'),
    compter_jours('PM10', 'moyenne', 80, 'alerte (moyenne du jour)'),
    compter_jours('NO2', 'max horaire', 200, 'information (au moins 1 h)'),
    compter_jours('O3', 'max horaire', 180, 'information (au moins 1 h)'),
    compter_jours('O3', 'max horaire', 240, 'alerte (au moins 1 h)'),
    compter_jours('SO2', 'max horaire', 300, 'information (au moins 1 h)'),
]
tableau_seuils = pd.DataFrame(liste_seuils)
print("\n===== 7. Jours au-dessus des seuils =====")
print(tableau_seuils)
tableau_seuils.to_csv("resultats/jours_au_dessus_seuils.csv", sep=";", index=False, encoding="utf-8-sig")


# ---------------------------------------------------------------
# 8. Part des jours au-dessus de l'OMS 24 h, par région
# ---------------------------------------------------------------
avec_seuil = donnees[donnees['Polluant'].isin(['NO2', 'PM10', 'PM2.5'])]
# la moyenne d'une colonne True / False donne la proportion de True
part_region = avec_seuil.groupby(['region', 'Polluant'], as_index=False)['depasse OMS'].mean()
part_region['% jours au-dessus OMS'] = (100 * part_region['depasse OMS']).round(1)

print("\n===== 8. % des jours au-dessus de l'OMS 24 h, par région =====")
print(part_region.pivot_table(index='region', columns='Polluant', values='% jours au-dessus OMS'))

fig = px.bar(part_region, x='region', y='% jours au-dessus OMS', color='Polluant', barmode='group',
             title="Part des jours au-dessus de la recommandation OMS sur 24 h, par région (2025)",
             labels={'region': 'Région', '% jours au-dessus OMS': '% des jours (toutes stations)'})
fig.write_html("resultats/depassements_regions.html")


# ---------------------------------------------------------------
# 9. Tableaux de contingence : lieu × dépassement OMS (oui / non)
# ---------------------------------------------------------------
avec_seuil = avec_seuil.copy()
avec_seuil['depassement'] = avec_seuil['depasse OMS'].map({True: 'au-dessus OMS', False: 'sous OMS'})

for polluant, colonne in [('NO2', "type d'influence"), ('PM2.5', "type d'influence"), ('PM10', 'territoire')]:
    lignes_p = avec_seuil[avec_seuil['Polluant'] == polluant]
    contingence = lignes_p.pivot_table(index=colonne, columns='depassement',
                                       values='moyenne', aggfunc='count')
    total = contingence['au-dessus OMS'] + contingence['sous OMS']
    contingence['% au-dessus'] = (100 * contingence['au-dessus OMS'] / total).round(1)
    print(f"\n===== 9. Contingence {polluant} : {colonne} × dépassement OMS (nb de jours-stations) =====")
    print(contingence)

print("\nGraphiques enregistrés dans resultats/ : regions.html, types_zones.html,"
      " densite_no2.html, depassements_regions.html")

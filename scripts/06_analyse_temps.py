# A4 - Analyse dans le temps
#   1. statistiques descriptives par polluant
#   2. évolution mois par mois
#   3. effet du jour de la semaine
#   4. profil sur une journée (janvier et juillet)
#   5. comparaison trafic / fond / industrielle
#   6. comparaison des saisons
# Les tableaux sont affichés, les graphiques (plotly) enregistrés en .html
# dans le dossier resultats/ (on les ouvre avec un navigateur).
# A lancer depuis le dossier du projet : python scripts/06_analyse_temps.py
# Il faut avoir lancé 04_annee_complete.py avant.

import os
import pandas as pd
import plotly.express as px

os.makedirs("resultats", exist_ok=True)

# les 4 polluants principaux (même ordre de grandeur, en µg/m3)
POLLUANTS = ['NO2', 'O3', 'PM10', 'PM2.5']

# organismes d'outre-mer : leurs heures sont déjà en heure locale
ORGANISMES_OUTRE_MER = ["GWAD'AIR", 'MADININAIR', 'ATMO GUYANE',
                        'ATMO REUNION', 'HAWA MAYOTTE']

NOMS_MOIS = {1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai',
             6: 'juin', 7: 'juillet', 8: 'août', 9: 'septembre',
             10: 'octobre', 11: 'novembre', 12: 'décembre'}
NOMS_JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
              'samedi', 'dimanche']

journalier = pd.read_csv("data_clean/mesures_journalieres_2025.csv",
                         sep=';', encoding='utf-8-sig')
journalier['date'] = pd.to_datetime(journalier['date'], format='%Y-%m-%d')

# ---------------------------------------------------------------
# 1. Statistiques descriptives des moyennes journalières, par polluant
# ---------------------------------------------------------------
stats = journalier.groupby('Polluant')['moyenne'].describe().round(1)
print("===== 1. Moyennes journalières par polluant (µg/m3) =====")
print(stats)
stats.to_csv("resultats/stats_polluants.csv", sep=';', encoding='utf-8-sig')

# on ne garde que les 4 polluants principaux pour la suite
principaux = journalier[journalier['Polluant'].isin(POLLUANTS)].copy()

# ---------------------------------------------------------------
# 2. Evolution mois par mois
# ---------------------------------------------------------------
principaux['mois'] = [x.month for x in principaux['date']]
par_mois = principaux.groupby(['mois', 'Polluant'], as_index=False)['moyenne'].mean()
par_mois['moyenne'] = par_mois['moyenne'].round(1)
par_mois['nom du mois'] = par_mois['mois'].map(NOMS_MOIS)

print("\n===== 2. Moyenne par mois (µg/m3) =====")
print(par_mois.pivot_table(index='mois', columns='Polluant', values='moyenne'))

fig = px.line(par_mois, x='nom du mois', y='moyenne', color='Polluant',
              markers=True, title="Concentration moyenne par mois en 2025",
              labels={'nom du mois': 'Mois', 'moyenne': 'Concentration (µg/m3)'})
fig.write_html("resultats/evolution_mois.html")

# ---------------------------------------------------------------
# 3. Jour de la semaine (weekday() : 0 = lundi ... 6 = dimanche)
# ---------------------------------------------------------------
principaux['jour'] = [NOMS_JOURS[x.weekday()] for x in principaux['date']]
par_jour = principaux.groupby(['jour', 'Polluant'], as_index=False)['moyenne'].mean()
par_jour['moyenne'] = par_jour['moyenne'].round(1)

print("\n===== 3. Moyenne par jour de la semaine (µg/m3) =====")
print(par_jour.pivot_table(index='jour', columns='Polluant', values='moyenne')
      .loc[NOMS_JOURS])

fig = px.bar(par_jour, x='jour', y='moyenne', color='Polluant',
             barmode='group', category_orders={'jour': NOMS_JOURS},
             title="Concentration moyenne selon le jour de la semaine",
             labels={'jour': 'Jour', 'moyenne': 'Concentration (µg/m3)'})
fig.write_html("resultats/jour_semaine.html")

# ---------------------------------------------------------------
# 4. Profil sur une journée (données horaires de janvier et juillet)
# ---------------------------------------------------------------
horaire = pd.read_csv("data_clean/mesures_horaires_janvier_juillet_2025.csv",
                      sep=';', encoding='utf-8-sig')
horaire = horaire[horaire['Polluant'].isin(POLLUANTS)].copy()

# on garde la métropole : liste des stations d'outre-mer, puis filtre
outre_mer = journalier[journalier['Organisme'].isin(ORGANISMES_OUTRE_MER)]
stations_outre_mer = outre_mer['code site'].unique()
horaire = horaire[~horaire['code site'].isin(stations_outre_mer)].copy()

# heure TU -> heure française : +1 h en hiver (janvier), +2 h en été (juillet)
horaire['Date de début'] = pd.to_datetime(horaire['Date de début'],
                                          format='%Y-%m-%d %H:%M:%S')
horaire['mois'] = [x.month for x in horaire['Date de début']]
decalage = {1: 1, 7: 2}
liste_mois = []
for mois in decalage:
    donnees_mois = horaire[horaire['mois'] == mois].copy()
    heure_francaise = donnees_mois['Date de début'] + pd.Timedelta(hours=decalage[mois])
    donnees_mois['heure'] = [x.hour for x in heure_francaise]
    liste_mois.append(donnees_mois)
horaire = pd.concat(liste_mois, ignore_index=True)
horaire['nom du mois'] = horaire['mois'].map(NOMS_MOIS)

profil = horaire.groupby(['nom du mois', 'heure', 'Polluant'],
                         as_index=False)['valeur'].mean()
profil['valeur'] = profil['valeur'].round(1)

print("\n===== 4. Profil horaire du NO2 et de l'O3, heure française (µg/m3) =====")
print(profil[profil['Polluant'].isin(['NO2', 'O3'])]
      .pivot_table(index='heure', columns=['Polluant', 'nom du mois'], values='valeur'))

for polluant in POLLUANTS:
    fig = px.line(profil[profil['Polluant'] == polluant], x='heure', y='valeur',
                  color='nom du mois', markers=True,
                  title=f"{polluant} : concentration moyenne heure par heure (métropole)",
                  labels={'heure': 'Heure (heure française)',
                          'valeur': 'Concentration (µg/m3)',
                          'nom du mois': 'Mois'})
    fig.write_html(f"resultats/profil_horaire_{polluant}.html")

# ---------------------------------------------------------------
# 5. Trafic / fond / industrielle
# ---------------------------------------------------------------
# moyenne sur l'année de chaque station, pour chaque polluant
par_station = principaux.groupby(['code site', 'Polluant', "type d'influence"],
                                 as_index=False)['moyenne'].mean()

print("\n===== 5. Moyenne annuelle des stations selon le type d'influence (µg/m3) =====")
print(par_station.pivot_table(index='Polluant', columns="type d'influence",
                              values='moyenne', aggfunc='mean').round(1))
print("\nNombre de stations :")
print(par_station.pivot_table(index='Polluant', columns="type d'influence",
                              values='moyenne', aggfunc='count'))

fig = px.box(par_station, x='Polluant', y='moyenne', color="type d'influence",
             title="Moyenne annuelle des stations selon le type d'influence",
             labels={'moyenne': 'Moyenne annuelle (µg/m3)'})
fig.write_html("resultats/trafic_fond.html")

# ---------------------------------------------------------------
# 6. Saisons (boxplot)
# ---------------------------------------------------------------
SAISONS = {12: 'hiver', 1: 'hiver', 2: 'hiver',
           3: 'printemps', 4: 'printemps', 5: 'printemps',
           6: 'été', 7: 'été', 8: 'été',
           9: 'automne', 10: 'automne', 11: 'automne'}
principaux['saison'] = principaux['mois'].map(SAISONS)

# moyenne de chaque station sur chaque saison : une station = un point
par_saison = principaux.groupby(['code site', 'Polluant', 'saison'],
                                as_index=False)['moyenne'].mean()

print("\n===== 6. Médiane des stations par saison (µg/m3) =====")
print(par_saison.pivot_table(index='Polluant', columns='saison',
                             values='moyenne', aggfunc='median').round(1)
      [['hiver', 'printemps', 'été', 'automne']])

fig = px.box(par_saison, x='Polluant', y='moyenne', color='saison',
             category_orders={'saison': ['hiver', 'printemps', 'été', 'automne']},
             title="Moyenne des stations selon la saison",
             labels={'moyenne': 'Moyenne sur la saison (µg/m3)'})
fig.write_html("resultats/saisons.html")

print("\nGraphiques enregistrés dans le dossier resultats/")

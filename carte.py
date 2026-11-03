# A6 - Cartes de la France
# Deux cartes, faites avec plotly express :
#   - carte_stations : un point par station, coloré selon la concentration
#   - carte_regions : chaque région colorée selon sa moyenne (choropleth,
#     comme dans le cours Graphiques_plotly)
# Les fonctions renvoient une figure : le dashboard (app.py) les réutilisera
# avec st.plotly_chart. Lancé directement, ce fichier enregistre quelques
# cartes en .html dans resultats/ pour les tester.
# Il faut avoir lancé 05_fusion.py avant.

import json
import pandas as pd
import plotly.express as px

FICHIER_DONNEES = "data_clean/mesures_fusionnees_2025.csv"
FICHIER_REGIONS = "data/geo/regions.geojson"

# seuils OMS 2021 sur 24 heures (µg/m3), d'après docs/variables_et_graphiques.md
# l'ozone n'a pas de seuil sur 24 h : pas de comptage pour lui
SEUILS_OMS_JOUR = {'PM2.5': 15, 'PM10': 45, 'NO2': 25, 'SO2': 40, 'CO': 4000}


def charger_donnees():
    """Lit le fichier fusionné de C3."""
    donnees = pd.read_csv(FICHIER_DONNEES, sep=';', encoding='utf-8-sig')
    donnees['date'] = pd.to_datetime(donnees['date'], format='%Y-%m-%d')
    return donnees


def charger_regions():
    """Lit le fichier des contours des régions (geojson)."""
    with open(FICHIER_REGIONS, encoding='utf-8') as f:
        regions = json.load(f)
    return regions


def filtrer(donnees, polluant, mois_debut=1, mois_fin=12):
    """Garde un polluant et une période (du mois_debut au mois_fin)."""
    filtre = ((donnees['Polluant'] == polluant)
              & (donnees['mois'] >= mois_debut)
              & (donnees['mois'] <= mois_fin))
    return donnees[filtre].copy()


def moyennes_par_station(donnees_filtrees, polluant):
    """Une ligne par station : moyenne, nombre de jours mesurés et
    nombre de jours au-dessus du seuil OMS (si le polluant en a un)."""
    colonnes = ['code site', 'nom station', 'commune', 'region', 'territoire',
                'latitude', 'longitude', "type d'influence"]
    groupes = donnees_filtrees.groupby(colonnes, as_index=False)['moyenne']
    par_station = groupes.mean()
    par_station['moyenne'] = par_station['moyenne'].round(1)
    par_station['jours mesurés'] = groupes.count()['moyenne']

    if polluant in SEUILS_OMS_JOUR:
        seuil = SEUILS_OMS_JOUR[polluant]
        # True vaut 1 : la somme donne le nombre de jours au-dessus du seuil
        donnees_filtrees['au-dessus OMS'] = donnees_filtrees['moyenne'] > seuil
        depassements = donnees_filtrees.groupby(colonnes, as_index=False)['au-dessus OMS'].sum()
        par_station['jours > OMS'] = depassements['au-dessus OMS']
    return par_station


def carte_stations(par_station, polluant, territoire='metropole'):
    """Carte à points : une station = un point coloré selon sa moyenne.
    territoire : 'metropole' ou le nom d'une région d'outre-mer
    (ex : 'La Réunion')."""
    if territoire == 'metropole':
        stations = par_station[par_station['territoire'] == 'metropole']
    else:
        stations = par_station[par_station['region'] == territoire]

    infos = {'commune': True, 'region': True, "type d'influence": True,
             'moyenne': True, 'jours mesurés': True,
             'latitude': False, 'longitude': False}
    if 'jours > OMS' in stations.columns:
        infos['jours > OMS'] = True

    fig = px.scatter_geo(stations, lat='latitude', lon='longitude',
                         color='moyenne', hover_name='nom station',
                         hover_data=infos,
                         color_continuous_scale='YlOrRd',
                         title=f"{polluant} : concentration moyenne par station ({territoire})",
                         labels={'moyenne': 'µg/m3'})
    # on zoome sur les stations et on affiche une carte un peu plus précise
    fig.update_geos(fitbounds='locations', resolution=50,
                    showcountries=True, showland=True, landcolor='whitesmoke')
    fig.update_traces(marker={'size': 8, 'line': {'width': 0.5, 'color': 'grey'}})
    fig.update_layout(margin={'r': 0, 't': 40, 'l': 0, 'b': 0})
    return fig


def carte_regions(donnees_filtrees, polluant, regions):
    """Carte choropleth : chaque région de métropole colorée selon la
    moyenne de ses stations."""
    # d'abord la moyenne de chaque station, puis la moyenne des stations
    # de la région : chaque station compte autant, même avec peu de jours
    metropole = donnees_filtrees[donnees_filtrees['territoire'] == 'metropole']
    par_station = metropole.groupby(['code site', 'region'], as_index=False)['moyenne'].mean()
    par_region = par_station.groupby('region', as_index=False).aggregate(
        {'moyenne': 'mean', 'code site': 'count'})
    par_region = par_region.rename(columns={'code site': 'nb stations'})
    par_region['moyenne'] = par_region['moyenne'].round(1)

    fig = px.choropleth(par_region, geojson=regions, locations='region',
                        featureidkey='properties.nom', color='moyenne',
                        hover_data={'nb stations': True},
                        color_continuous_scale='YlOrRd',
                        title=f"{polluant} : moyenne des stations par région",
                        labels={'moyenne': 'µg/m3', 'region': 'Région'})
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r': 0, 't': 40, 'l': 0, 'b': 0})
    return fig


# Partie test : ne s'exécute que si on lance ce fichier directement
if __name__ == "__main__":
    donnees = charger_donnees()
    regions = charger_regions()

    for polluant in ['NO2', 'PM10', 'O3']:
        donnees_polluant = filtrer(donnees, polluant)
        par_station = moyennes_par_station(donnees_polluant, polluant)
        print(f"{polluant} : {len(par_station)} stations")

        fig = carte_stations(par_station, polluant)
        fig.write_html(f"resultats/carte_stations_{polluant}.html")
        fig = carte_regions(donnees_polluant, polluant, regions)
        fig.write_html(f"resultats/carte_regions_{polluant}.html")

    # exemple d'outre-mer, et exemple de période : l'été pour l'ozone
    donnees_no2 = filtrer(donnees, 'NO2')
    fig = carte_stations(moyennes_par_station(donnees_no2, 'NO2'), 'NO2', 'La Réunion')
    fig.write_html("resultats/carte_stations_NO2_reunion.html")
    donnees_ete = filtrer(donnees, 'O3', mois_debut=6, mois_fin=8)
    fig = carte_stations(moyennes_par_station(donnees_ete, 'O3'), 'O3 (juin-août)')
    fig.write_html("resultats/carte_stations_O3_ete.html")

    print("Cartes enregistrées dans resultats/")

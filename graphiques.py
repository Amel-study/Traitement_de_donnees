# C5 - Graphiques et tableaux de la page « Lieux et seuils » du dashboard
# Chaque fonction reçoit les données déjà filtrées par app.py (un polluant,
# une période, des régions) et renvoie une figure plotly ou un tableau.
# La fonction afficher(), appelée par app.py, les met en page avec Streamlit.
# Numéros G2, G6... = numéros des graphiques dans docs/variables_et_graphiques.md (C2).
# Lancé directement, ce fichier enregistre des exemples en .html dans resultats/.
# Il faut avoir lancé 05_fusion.py avant.

import pandas as pd
import plotly.express as px
import streamlit as st

# mêmes seuils OMS que la carte (A6), pour avoir les mêmes chiffres partout
from carte import SEUILS_OMS_JOUR, charger_donnees, filtrer

# toujours le même ordre, donc les mêmes couleurs d'un graphique à l'autre
ORDRE_INFLUENCE = ['Fond', 'Industrielle', 'Trafic']
# (ordre alphabétique : c'est aussi l'ordre des graphiques d'Amel, donc mêmes couleurs)
UNITE = 'Concentration (µg/m3)'


def moyennes_stations(donnees_filtrees, colonnes):
    """Moyenne de chaque station sur la période : une station = une valeur.
    colonnes : liste des colonnes à garder en plus (ex : ['saison'])."""
    par_station = donnees_filtrees.groupby(['code site', 'nom station'] + colonnes,
                                           as_index=False)['moyenne'].mean()
    par_station['moyenne'] = par_station['moyenne'].round(1)
    return par_station


def histogramme(donnees_filtrees, polluant):
    """G2 : répartition des moyennes journalières (toutes les stations)."""
    fig = px.histogram(donnees_filtrees, x='moyenne', nbins=60,
                       color="type d'influence", barmode='overlay', opacity=0.6,
                       category_orders={"type d'influence": ORDRE_INFLUENCE},
                       title=f"{polluant} : répartition des moyennes journalières",
                       labels={'moyenne': UNITE, "type d'influence": "Type d'influence"})
    fig.update_layout(yaxis_title="Nombre de jours (toutes stations)")
    # trait vertical au niveau du seuil OMS sur 24 h, s'il existe
    if polluant in SEUILS_OMS_JOUR:
        fig.add_vline(x=SEUILS_OMS_JOUR[polluant], line_dash='dash',
                      annotation_text="seuil OMS 24 h")
    return fig


def courbe_jours(donnees_filtrees, polluant):
    """Courbe jour par jour : moyenne de toutes les stations,
    une courbe par type d'influence (fond, trafic, industrielle)."""
    par_jour = donnees_filtrees.groupby(['date', "type d'influence"], as_index=False)['moyenne'].mean()
    par_jour['moyenne'] = par_jour['moyenne'].round(1)
    fig = px.line(par_jour, x='date', y='moyenne', color="type d'influence",
                  category_orders={"type d'influence": ORDRE_INFLUENCE},
                  title=f"{polluant} : moyenne des stations jour par jour",
                  labels={'date': 'Date', 'moyenne': UNITE, "type d'influence": "Type d'influence"})
    # trait horizontal au niveau du seuil OMS sur 24 h, s'il existe
    if polluant in SEUILS_OMS_JOUR:
        fig.add_hline(y=SEUILS_OMS_JOUR[polluant], line_dash='dash',
                      annotation_text="seuil OMS 24 h")
    return fig


def boxplot_influence(donnees_filtrees, polluant):
    """G6 : moyenne de chaque station selon le type d'influence."""
    par_station = moyennes_stations(donnees_filtrees, ["type d'influence"])
    fig = px.box(par_station, x="type d'influence", y='moyenne', color="type d'influence",
                 hover_name='nom station',
                 category_orders={"type d'influence": ORDRE_INFLUENCE},
                 title=f"{polluant} : moyenne des stations selon le type d'influence",
                 labels={'moyenne': UNITE, "type d'influence": "Type d'influence"})
    return fig


def camembert_oms(donnees_filtrees, polluant):
    """G12 : part des jours au-dessus du seuil OMS sur 24 h.
    Renvoie None si le polluant n'a pas de seuil OMS sur 24 h (ex : O3)."""
    if polluant not in SEUILS_OMS_JOUR:
        return None
    seuil = SEUILS_OMS_JOUR[polluant]
    nb_au_dessus = (donnees_filtrees['moyenne'] > seuil).sum()
    nb_sous = len(donnees_filtrees) - nb_au_dessus
    tableau = pd.DataFrame({'situation': ['au-dessus du seuil OMS', 'sous le seuil OMS'],
                            'nb jours': [nb_au_dessus, nb_sous]})
    fig = px.pie(tableau, names='situation', values='nb jours',
                 title=f"{polluant} : part des jours au-dessus de {seuil} µg/m3 (OMS 24 h)")
    return fig


def barres_regions(donnees_filtrees, polluant):
    """G8 : moyenne des stations de fond par région, de la plus haute à la plus basse.
    Seulement les stations de fond, pour ne pas avantager les régions
    qui ont peu de stations au bord des routes."""
    fond = donnees_filtrees[donnees_filtrees["type d'influence"] == 'Fond']
    par_station = moyennes_stations(fond, ['region'])
    par_region = par_station.groupby('region', as_index=False)['moyenne'].mean()
    par_region['moyenne'] = par_region['moyenne'].round(1)
    par_region = par_region.sort_values('moyenne', ascending=False)
    fig = px.bar(par_region, x='region', y='moyenne',
                 title=f"{polluant} : moyenne des stations de fond par région",
                 labels={'region': 'Région', 'moyenne': UNITE})
    return fig


def nuage_densite(donnees_filtrees, polluant):
    """G9 : une zone = un point, densité de population contre concentration
    moyenne de ses stations de fond."""
    fond = donnees_filtrees[donnees_filtrees["type d'influence"] == 'Fond']
    par_station = moyennes_stations(fond, ['Zas', 'type zone', 'densite'])
    par_zone = par_station.groupby(['Zas', 'type zone', 'densite'], as_index=False)['moyenne'].mean()
    par_zone['moyenne'] = par_zone['moyenne'].round(1)
    fig = px.scatter(par_zone, x='densite', y='moyenne', color='type zone', hover_name='Zas',
                     title=f"{polluant} : concentration des stations de fond selon la densité de la zone",
                     labels={'densite': 'Densité de population (hab/km2)', 'moyenne': UNITE,
                             'type zone': 'Type de zone'})
    return fig


def sunburst_stations(donnees):
    """G13 : composition du réseau de mesure : territoire, puis typologie.
    La taille de chaque part = nombre de stations."""
    stations = donnees[['code site', 'territoire', 'typologie']].drop_duplicates()
    fig = px.sunburst(stations, path=['territoire', 'typologie'],
                      title="Stations de mesure : territoire et typologie")
    return fig


# seuils français d'information et d'alerte (docs/variables_et_graphiques.md)
# (nom du seuil, colonne à comparer, valeur en µg/m3)
# "moyenne" = moyenne du jour ; "max horaire" = au moins une heure au-dessus ce jour-là
SEUILS_FRANCE = {
    'PM10': [('information (moyenne du jour)', 'moyenne', 50),
             ('alerte (moyenne du jour)', 'moyenne', 80)],
    'NO2': [('information (au moins 1 h)', 'max horaire', 200)],
    'O3': [('information (au moins 1 h)', 'max horaire', 180),
           ('alerte (au moins 1 h)', 'max horaire', 240)],
    'SO2': [('information (au moins 1 h)', 'max horaire', 300)],
}


def tableau_seuils(donnees_filtrees, polluant):
    """G10 : nombre de jours au-dessus de chaque seuil du polluant.
    Renvoie None si le polluant n'a aucun seuil dans notre document."""
    liste_seuils = []
    if polluant in SEUILS_OMS_JOUR:
        liste_seuils.append(('OMS 24 h', 'moyenne', SEUILS_OMS_JOUR[polluant]))
    if polluant in SEUILS_FRANCE:
        liste_seuils = liste_seuils + SEUILS_FRANCE[polluant]
    if len(liste_seuils) == 0:
        return None

    lignes = []
    for nom, colonne, valeur in liste_seuils:
        au_dessus = donnees_filtrees[donnees_filtrees[colonne] > valeur]
        lignes.append({'seuil': nom,
                       'valeur (µg/m3)': valeur,
                       'jours au-dessus': len(au_dessus),
                       '% des jours': round(100 * len(au_dessus) / len(donnees_filtrees), 2),
                       'stations concernées': len(au_dessus['code site'].unique())})
    return pd.DataFrame(lignes)


def tableau_contingence(donnees_filtrees, polluant):
    """G11 : tableau de contingence type d'influence × dépassement du seuil OMS 24 h.
    Renvoie None si le polluant n'a pas de seuil OMS sur 24 h."""
    if polluant not in SEUILS_OMS_JOUR:
        return None
    donnees_p = donnees_filtrees.copy()
    au_dessus = donnees_p['moyenne'] > SEUILS_OMS_JOUR[polluant]
    donnees_p['depassement'] = au_dessus.map({True: 'au-dessus OMS', False: 'sous OMS'})
    contingence = donnees_p.pivot_table(index="type d'influence", columns='depassement',
                                        values='moyenne', aggfunc='count')
    # si une case n'existe pas (aucun jour au-dessus par exemple), on met 0
    for colonne in ['au-dessus OMS', 'sous OMS']:
        if colonne not in contingence.columns:
            contingence[colonne] = 0
    contingence = contingence.fillna(0)
    total = contingence['au-dessus OMS'] + contingence['sous OMS']
    contingence['% au-dessus'] = (100 * contingence['au-dessus OMS'] / total).round(1)
    return contingence


def afficher(donnees_filtrees, polluant):
    """Page « Lieux et seuils » du dashboard (appelée par app.py)."""
    st.subheader("Où la pollution est-elle la plus forte ?")
    colonne1, colonne2 = st.columns(2)
    colonne1.plotly_chart(barres_regions(donnees_filtrees, polluant), use_container_width=True)
    colonne2.plotly_chart(boxplot_influence(donnees_filtrees, polluant), use_container_width=True)
    colonne1.plotly_chart(nuage_densite(donnees_filtrees, polluant), use_container_width=True)
    colonne2.plotly_chart(histogramme(donnees_filtrees, polluant), use_container_width=True)

    st.subheader("Dépassements des seuils")
    tableau = tableau_seuils(donnees_filtrees, polluant)
    if tableau is None:
        st.write(f"Pas de seuil sur 24 h ni de seuil d'alerte pour {polluant} dans notre document C2.")
    else:
        st.write("Nombre de jours au-dessus des seuils (un jour = une station un jour donné) :")
        st.write(tableau)

    colonne1, colonne2 = st.columns(2)
    fig = camembert_oms(donnees_filtrees, polluant)
    if fig is not None:
        colonne1.plotly_chart(fig, use_container_width=True)
    contingence = tableau_contingence(donnees_filtrees, polluant)
    if contingence is not None:
        colonne2.write("Tableau de contingence : type de station × dépassement du seuil OMS 24 h (nombre de jours)")
        colonne2.write(contingence)

    st.plotly_chart(courbe_jours(donnees_filtrees, polluant), use_container_width=True)

    with st.expander("Le réseau de stations"):
        st.plotly_chart(sunburst_stations(donnees_filtrees), use_container_width=True)

    st.caption("Seuils : recommandations OMS 2021 et seuils français d'information / d'alerte "
               "(sources dans docs/variables_et_graphiques.md). Une partie des données ne sont "
               "pas encore vérifiées : ce sont des dépassements observés, pas des infractions officielles.")


# Partie test : ne s'exécute que si on lance ce fichier directement
if __name__ == "__main__":
    donnees = charger_donnees()

    fig = sunburst_stations(donnees)
    fig.write_html("resultats/graph_sunburst_stations.html")

    for polluant in ['NO2', 'PM2.5', 'O3']:
        donnees_polluant = filtrer(donnees, polluant)
        print(polluant, ":", len(donnees_polluant), "lignes")
        histogramme(donnees_polluant, polluant).write_html(f"resultats/graph_histogramme_{polluant}.html")
        courbe_jours(donnees_polluant, polluant).write_html(f"resultats/graph_courbe_{polluant}.html")
        boxplot_influence(donnees_polluant, polluant).write_html(f"resultats/graph_box_influence_{polluant}.html")
        barres_regions(donnees_polluant, polluant).write_html(f"resultats/graph_regions_{polluant}.html")
        nuage_densite(donnees_polluant, polluant).write_html(f"resultats/graph_densite_{polluant}.html")
        fig = camembert_oms(donnees_polluant, polluant)
        if fig is None:
            print("  pas de seuil OMS sur 24 h : pas de camembert")
        else:
            fig.write_html(f"resultats/graph_camembert_{polluant}.html")
        print(tableau_seuils(donnees_polluant, polluant))
        print(tableau_contingence(donnees_polluant, polluant))

    # exemple avec une période : l'été seulement
    donnees_ete = filtrer(donnees, 'O3', mois_debut=6, mois_fin=8)
    courbe_jours(donnees_ete, 'O3 (juin-août)').write_html("resultats/graph_courbe_O3_ete.html")

    print("Graphiques enregistrés dans resultats/ (fichiers graph_*.html)")

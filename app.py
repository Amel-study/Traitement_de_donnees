# A5 - Dashboard Streamlit : la pollution de l'air en France en 2025
# Lancement, depuis le dossier du projet :  streamlit run app.py
# (dans Spyder : ! streamlit run app.py), puis ouvrir http://localhost:8501
# Il faut avoir lancé avant : 04_annee_complete.py, 03_metadonnees.py
# et 05_fusion.py (fichiers dans data_clean/).

import pandas as pd
import streamlit as st

import carte
import graphiques_temps as gt

# les graphiques de Coura (C5) : s'ils ne sont pas encore prêts,
# le dashboard marche quand même
try:
    import graphiques
    GRAPHIQUES_COURA = True
except ImportError:
    GRAPHIQUES_COURA = False

POLLUANTS = ['NO2', 'PM10', 'PM2.5', 'O3', 'SO2', 'CO', 'NO', 'NOX as NO2', 'C6H6']
NOMS_POLLUANTS = {'NO2': 'dioxyde d\'azote', 'PM10': 'particules < 10 µm',
                  'PM2.5': 'particules < 2,5 µm', 'O3': 'ozone',
                  'SO2': 'dioxyde de soufre', 'CO': 'monoxyde de carbone',
                  'NO': 'monoxyde d\'azote', 'NOX as NO2': 'oxydes d\'azote',
                  'C6H6': 'benzène'}
LISTE_MOIS = list(gt.NOMS_MOIS.values())

st.set_page_config(page_title="Pollution de l'air 2025", layout='wide')


# ---------------------------------------------------------------
# Chargement des données
# @st.cache_data : Streamlit relance tout le script à chaque clic ;
# grâce à cette ligne, les fichiers ne sont lus qu'une seule fois
# ---------------------------------------------------------------
@st.cache_data
def charger_donnees():
    return carte.charger_donnees()


@st.cache_data
def charger_regions():
    return carte.charger_regions()


@st.cache_data
def charger_horaire(stations_outre_mer):
    horaire = pd.read_csv("data_clean/mesures_horaires_janvier_juillet_2025.csv",
                          sep=';', encoding='utf-8-sig')
    return gt.preparer_horaire(horaire, stations_outre_mer)


donnees = charger_donnees()
regions_geo = charger_regions()

# ---------------------------------------------------------------
# Barre de gauche : navigation et filtres
# ---------------------------------------------------------------
st.sidebar.title("Pollution de l'air 2025")
page = st.sidebar.selectbox("Page", ['Accueil', 'Carte', 'Évolution dans le temps',
                                     'Lieux et seuils', 'Données et méthode'])

st.sidebar.header("Filtres")
polluant = st.sidebar.selectbox("Polluant", POLLUANTS,
                                format_func=lambda p: f"{p} ({NOMS_POLLUANTS[p]})")
mois_debut_nom, mois_fin_nom = st.sidebar.select_slider(
    "Période", options=LISTE_MOIS, value=('janvier', 'décembre'))
# position dans la liste + 1 = numéro du mois
mois_debut = LISTE_MOIS.index(mois_debut_nom) + 1
mois_fin = LISTE_MOIS.index(mois_fin_nom) + 1

toutes_regions = sorted(donnees['region'].unique())
regions_choisies = st.sidebar.multiselect("Régions (vide = toutes)", toutes_regions)

# application des filtres
donnees_filtrees = carte.filtrer(donnees, polluant, mois_debut, mois_fin)
if len(regions_choisies) > 0:
    donnees_filtrees = donnees_filtrees[donnees_filtrees['region'].isin(regions_choisies)]

st.sidebar.write(f"**{len(donnees_filtrees)}** moyennes journalières, "
                 f"**{len(donnees_filtrees['code site'].unique())}** stations")

# ---------------------------------------------------------------
# Pages
# ---------------------------------------------------------------
if len(donnees_filtrees) == 0:
    st.warning("Aucune mesure pour ce choix de filtres (ce polluant n'est "
               "peut-être pas mesuré dans ces régions).")

elif page == 'Accueil':
    st.title("La pollution de l'air en France en 2025")
    st.write("Concentrations de polluants mesurées heure par heure par les "
             "stations de surveillance de la qualité de l'air (source : "
             "data.gouv.fr, LCSQA), nettoyées puis réduites à une moyenne "
             "par jour et par station.")

    colonne1, colonne2, colonne3, colonne4 = st.columns(4)
    colonne1.write(f"### {len(donnees['code site'].unique())}\nstations")
    colonne2.write(f"### {len(donnees['region'].unique())}\nrégions")
    colonne3.write(f"### {len(donnees['Polluant'].unique())}\npolluants")
    colonne4.write(f"### {len(donnees)}\nmoyennes journalières")

    st.subheader(f"{polluant} sur la période choisie")
    moyenne = donnees_filtrees['moyenne'].mean()
    mediane = donnees_filtrees['moyenne'].median()
    st.write(f"Moyenne : **{moyenne:.1f} µg/m3** — médiane : **{mediane:.1f} µg/m3**")
    if polluant in carte.SEUILS_OMS_JOUR:
        seuil = carte.SEUILS_OMS_JOUR[polluant]
        nb_au_dessus = len(donnees_filtrees[donnees_filtrees['moyenne'] > seuil])
        part = 100 * nb_au_dessus / len(donnees_filtrees)
        st.write(f"Seuil OMS sur 24 h : {seuil} µg/m3 — dépassé dans "
                 f"**{part:.1f} %** des mesures journalières.")
    st.write("Utilisez le menu à gauche pour changer de page et de filtres.")

elif page == 'Carte':
    st.title("Carte")
    territoires = ['metropole'] + sorted(donnees[donnees['territoire'] == 'outre-mer']['region'].unique())
    territoire = st.selectbox("Territoire", territoires)

    par_station = carte.moyennes_par_station(donnees_filtrees, polluant)
    st.plotly_chart(carte.carte_stations(par_station, polluant, territoire),
                    use_container_width=True)
    if territoire == 'metropole':
        st.plotly_chart(carte.carte_regions(donnees_filtrees, polluant, regions_geo),
                        use_container_width=True)

    with st.expander("Stations les plus touchées"):
        st.write(par_station.sort_values('moyenne', ascending=False).head(10))

elif page == 'Évolution dans le temps':
    st.title("Évolution dans le temps")
    colonne1, colonne2 = st.columns(2)
    colonne1.plotly_chart(gt.graphique_mois(donnees_filtrees, polluant),
                          use_container_width=True)
    colonne2.plotly_chart(gt.graphique_saisons(donnees_filtrees, polluant),
                          use_container_width=True)
    colonne1.plotly_chart(gt.graphique_jour_semaine(donnees_filtrees, polluant),
                          use_container_width=True)

    # profil horaire : métropole seulement, données de janvier et juillet
    outre_mer = donnees[donnees['territoire'] == 'outre-mer']
    horaire = charger_horaire(outre_mer['code site'].unique().tolist())
    stations_choisies = donnees_filtrees['code site'].unique()
    horaire_filtre = horaire[(horaire['Polluant'] == polluant)
                             & (horaire['code site'].isin(stations_choisies))]
    if len(horaire_filtre) > 0:
        colonne2.plotly_chart(gt.graphique_profil_horaire(horaire_filtre, polluant),
                              use_container_width=True)
        colonne2.caption("Profil calculé sur janvier et juillet (métropole).")

    st.subheader("Statistiques des moyennes journalières")
    st.write(gt.tableau_stats(donnees_filtrees))

elif page == 'Lieux et seuils':
    st.title("Lieux et seuils")
    if GRAPHIQUES_COURA:
        graphiques.afficher(donnees_filtrees, polluant)
    else:
        st.info("Page en cours de préparation (graphiques de Coura, tâches C4 et C5).")

elif page == 'Données et méthode':
    st.title("Données et méthode")
    st.markdown("""
**Source** : données « temps réel » de mesure des polluants réglementés,
data.gouv.fr (LCSQA), année 2025 : 365 fichiers, 17,6 millions de lignes.

**Nettoyage (pour chaque jour)**
1. suppression des mesures invalides (validité = -1, 4 % des lignes) ;
2. suppression des doublons cachés (même mesure envoyée deux fois) ;
3. suppression de 8 colonnes inutiles (vides ou toujours identiques) ;
4. espaces en trop enlevés dans les noms de stations ;
5. CO converti de mg/m3 en µg/m3, une seule écriture de l'unité ;
6. valeurs négatives mises à 0 ;
7. dates converties en vraies dates.

**Réduction** : une moyenne par jour, par station et par polluant, gardée
seulement si au moins 18 heures sur 24 ont été mesurées (règle européenne).

**Fusion** avec les métadonnées des stations (position GPS) et des zones
(population), puis ajout de la région, du mois, de la saison et du jour.

**Limites** : une partie des données sont « brutes » (pas encore vérifiées
par les organismes) ; on parle donc de dépassements observés, pas de
non-respect officiel de la réglementation.
""")
    st.subheader("Aperçu des données filtrées")
    st.write(donnees_filtrees.head(100))

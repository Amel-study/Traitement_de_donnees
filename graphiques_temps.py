# Graphiques "dans le temps" pour le dashboard (Amel)
# Mêmes analyses que scripts/06_analyse_temps.py, mais sous forme de
# fonctions : elles reçoivent les données déjà filtrées par le dashboard
# (un polluant, une période, des régions) et renvoient une figure plotly.

import pandas as pd
import plotly.express as px

NOMS_MOIS = {1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai',
             6: 'juin', 7: 'juillet', 8: 'août', 9: 'septembre',
             10: 'octobre', 11: 'novembre', 12: 'décembre'}
NOMS_JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
              'samedi', 'dimanche']
ORDRE_SAISONS = ['hiver', 'printemps', 'été', 'automne']


def tableau_stats(donnees):
    """Statistiques des moyennes journalières selon le type d'influence."""
    stats = donnees.groupby("type d'influence")['moyenne'].describe().round(1)
    stats = stats.rename(columns={'count': 'nb jours', 'mean': 'moyenne',
                                  'std': 'écart type', '50%': 'médiane'})
    return stats


def graphique_mois(donnees, polluant):
    """Moyenne par mois, une courbe par type d'influence."""
    par_mois = donnees.groupby(['mois', "type d'influence"],
                               as_index=False)['moyenne'].mean()
    par_mois['moyenne'] = par_mois['moyenne'].round(1)
    par_mois['nom du mois'] = par_mois['mois'].map(NOMS_MOIS)
    fig = px.line(par_mois, x='nom du mois', y='moyenne',
                  color="type d'influence", markers=True,
                  title=f"{polluant} : moyenne par mois",
                  labels={'nom du mois': 'Mois',
                          'moyenne': 'Concentration (µg/m3)'})
    return fig


def graphique_jour_semaine(donnees, polluant):
    """Moyenne selon le jour de la semaine."""
    par_jour = donnees.groupby('jour semaine', as_index=False)['moyenne'].mean()
    par_jour['moyenne'] = par_jour['moyenne'].round(1)
    fig = px.bar(par_jour, x='jour semaine', y='moyenne',
                 category_orders={'jour semaine': NOMS_JOURS},
                 title=f"{polluant} : moyenne selon le jour de la semaine",
                 labels={'jour semaine': 'Jour',
                         'moyenne': 'Concentration (µg/m3)'})
    return fig


def graphique_saisons(donnees, polluant):
    """Boxplot : moyenne de chaque station sur chaque saison."""
    par_saison = donnees.groupby(['code site', 'saison'],
                                 as_index=False)['moyenne'].mean()
    fig = px.box(par_saison, x='saison', y='moyenne', color='saison',
                 category_orders={'saison': ORDRE_SAISONS},
                 title=f"{polluant} : moyenne des stations par saison",
                 labels={'moyenne': 'Moyenne sur la saison (µg/m3)'})
    return fig


def preparer_horaire(horaire, stations_outre_mer):
    """Données horaires de janvier et juillet : garde la métropole et
    passe en heure française (+1 h en janvier, +2 h en juillet)."""
    horaire = horaire[~horaire['code site'].isin(stations_outre_mer)].copy()
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
    return horaire


def graphique_profil_horaire(horaire, polluant):
    """Moyenne heure par heure, janvier contre juillet."""
    profil = horaire.groupby(['nom du mois', 'heure'],
                             as_index=False)['valeur'].mean()
    profil['valeur'] = profil['valeur'].round(1)
    fig = px.line(profil, x='heure', y='valeur', color='nom du mois',
                  markers=True,
                  title=f"{polluant} : profil d'une journée (heure française)",
                  labels={'heure': 'Heure', 'valeur': 'Concentration (µg/m3)',
                          'nom du mois': 'Mois'})
    return fig

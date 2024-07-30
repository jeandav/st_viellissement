import streamlit as st
import pandas as pd
import math
from pathlib import Path

import plotly.express as px
import numpy as np

# -----------------------------------------------------------------------------


st.set_page_config(
    page_title='Evolution du vieillissement',
    page_icon=':chart_with_upwards_trend:',
    layout="centered"
)

# -----------------------------------------------------------------------------

@st.cache_data
def get_cluster_data():
    DATA_FILENAME = Path(__file__).parent/'../data/df_cluster_complete.csv'
    df = pd.read_csv(DATA_FILENAME, encoding='latin-1', sep=';', decimal=".")


    decimals = 2    
    df['interdecile'] = df['interdecile'].apply(lambda x: round(x, decimals))
    
    return df

def get_menage_data():
    DATA_FILENAME = Path(__file__).parent/'../data/caisse_dep/caisse_dep_menage.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df

def get_intens_pauv_data():
    DATA_FILENAME = Path(__file__).parent/'../data/caisse_dep/caisse_dep_intens_pauv.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=",")

    return df

def get_rev_disp_data():
    DATA_FILENAME = Path(__file__).parent/'../data/caisse_dep/caisse_dep_rev_disp.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=",")

    return df

def get_drees_data():
    DATA_FILENAME = Path(__file__).parent/'../data/traitement_drees/livia_lieux_vie_sc1.csv'
    df = pd.read_csv(DATA_FILENAME, encoding='latin-1', sep=';')

    # df = df[df['genre'] == 'HOMMES']
    # df = df[df['tranche_age'] == '75 ans et plus']
    df = df[df['hyp_evol_dependance'] == 'intermediaire']
    df = df[df['hyp_evol_demo'] == 'central']
    df = df[['ca', 'tranche_age', 'genre', 'annee', 'nb_proj_seniors']]
    df = df.groupby(['ca', 'tranche_age', 'genre', 'annee'])['nb_proj_seniors'].sum()
    df = df.reset_index()
    # return df




def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'../data/traitement_drees/livia_lieux_vie_sc1.csv'
    df = pd.read_csv(DATA_FILENAME, encoding='latin-1', sep=';')

    # df = df[df['genre'] == 'HOMMES']
    # df = df[df['tranche_age'] == '75 ans et plus']
    df = df[df['hyp_evol_dependance'] == 'intermediaire']
    df = df[df['hyp_evol_demo'] == 'central']
    df = df[['ca', 'tranche_age', 'genre', 'annee', 'nb_proj_seniors']]
    df = df.groupby(['ca', 'tranche_age', 'genre', 'annee'])['nb_proj_seniors'].sum()
    df = df.reset_index()


    return df


def get_persagees_data():
    DATA_FILENAME = Path(__file__).parent/'../data/PERSAGEES/PERSAGEES_TRAITE.csv'
    df = pd.read_csv(DATA_FILENAME, sep=',', encoding='latin-1')

    df = df[['CA','SEXE','TRANCHAGE','ANNEE','value']]
    df = df.groupby(['CA','SEXE','TRANCHAGE','ANNEE']).sum().reset_index()

    df['ANEE'] = pd.to_numeric(df['ANNEE'])

    return df



df_cluster = get_cluster_data()
# df_menage = get_menage_data()
df_intens_pauv = get_intens_pauv_data()
df_rev_disp = get_rev_disp_data()
# df_drees = get_drees_data()
# gdp_df = get_gdp_data()
# df_persagees = get_persagees_data()



# -----------------------------------------------------------------------------






liste_ca = df_cluster['ressort_ca'].unique()

# with st.sidebar:
#     selected_ca = st.multiselect(
#         "Cour d\'appel :",
#         liste_ca,
#         ['CAEN', 'RENNES', 'LIMOGES', 'REIMS', 'BESANCON'])

with st.sidebar:



    cluster_options = {
        "Groupe A" : ['VERSAILLES', 'PARIS'],
        "Groupe B" : ['ANGERS', 'DIJON', 'CAEN', 'POITIERS', 'RIOM', 'BOURGES', 'LIMOGES', 'AGEN'],
        "Groupe C" : ['DOUAI', 'AMIENS', 'CHAMBERY', 'ROUEN', 'GRENOBLE', 'COLMAR', 'LYON', 'REIMS', 'METZ', 'TOULOUSE'],
        "Groupe D" : ['RENNES', 'ORLEANS', 'NANCY', 'BESANCON', 'NIMES', 'AIX EN PROVENCE', 'MONTPELLIER', 'BORDEAUX', 'PAU'],
    }

    chosen_cluster = st.radio(
        "Groupe :",
        cluster_options.keys(),
        horizontal=True
    )

    selected_ca = st.multiselect(
        'Cour d\'appel :',
        liste_ca,
        cluster_options[chosen_cluster])

    # st.write(selected_ca)
    '''
    ---
    '''

    '''
    Ministère de la Justice  \nPôle de l'Evaluation et de la Prospective
    '''



filtered_df_cluster = df_cluster[df_cluster['ressort_ca'].isin(selected_ca)]

# st.table(df_menage)



st.image('https://upload.wikimedia.org/wikipedia/commons/0/06/Minist%C3%A8re_de_la_Justice.svg', width=100)

'''
# Vulnérabilité financière
'''


'''
### Médiane du revenu disponible par unité de consommation (€)
'''
# st.bar_chart(df_rev_disp[df_rev_disp['ca'].isin(selected_ca)], x="ca", y="med_rev_disp", horizontal=True)

fig = px.bar(df_rev_disp[df_rev_disp['ca'].isin(selected_ca)], x="med_rev_disp", y="ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Revenu médian disponible"
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

'''
### Bénéficiaires du minimum vieillesse
'''
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_min_vie", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_min_vie", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires du minimum vieillesse (en milliers)"
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

'''
### Intensité de la pauvreté au seuil de 60%
'''
# st.bar_chart(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="ca", y="intens_pauv", horizontal=True)

fig = px.bar(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="intens_pauv", y="ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Intensité de la pauvreté des personnes agées (0 à 1)"
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

'''
### Interdécile
'''
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="interdecile", horizontal=True)

fig = px.bar(filtered_df_cluster, x="interdecile", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Interdécile"
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


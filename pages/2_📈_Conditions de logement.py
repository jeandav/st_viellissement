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

def get_popglobale_data():
    DATA_FILENAME = Path(__file__).parent/'../data/pop_globale_ressort.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df


df_cluster = get_cluster_data()
df_menage = get_menage_data()
# df_intens_pauv = get_intens_pauv_data()
# df_rev_disp = get_rev_disp_data()
# df_drees = get_drees_data()
# df_persagees = get_persagees_data()
# gdp_df = get_gdp_data()
df_popglobale = get_popglobale_data()

df_cluster = pd.merge(df_cluster, df_popglobale, left_on='ressort_ca', right_on='pop')
df_cluster['N_x60_ans_et_plus_isoles_pop'] = (df_cluster['N_x60_ans_et_plus_isoles'] / df_cluster['pop_2024'])*100


df_menage = pd.merge(df_menage, df_popglobale, left_on='CA', right_on='pop')

df_menage['X60_ANS_ET_PLUS_APPART_AV_ASC_pop'] = (df_menage['X60_ANS_ET_PLUS_APPART_AV_ASC'] / df_menage['pop_2024'])*100
df_menage['X60_ANS_ET_PLUS_APPART_SS_ASC_pop'] = (df_menage['X60_ANS_ET_PLUS_APPART_SS_ASC'] / df_menage['pop_2024'])*100


# -----------------------------------------------------------------------------




# st.write(df_menage)

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
        "Choix du groupe :",
        cluster_options.keys(),
        horizontal=True
    )
    '''
    ---
    '''
    selected_ca = st.multiselect(
        'Choix de la cour d\'appel :',
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

# st.table(df_cluster)



st.image('img/logo_minjus.svg', width=100)


'''
# Conditions de logement
'''


'''
---
### Population des 60 ans et plus isolées
_Rapporté à la population du ressort de cour d'appel en 2024_
'''
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_x60_ans_et_plus_isoles", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_x60_ans_et_plus_isoles_pop", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de 60 ans et plus isolés (en milliers)"
)
fig.add_vline(x=filtered_df_cluster.N_x60_ans_et_plus_isoles_pop.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

'''
---
### Population des 60 ans et plus dans un appartement sans ascenceur :
_Rapporté à la population du ressort de cour d'appel en 2024_

'''




fig = px.bar(df_menage[df_menage['CA'].isin(selected_ca)], x="X60_ANS_ET_PLUS_APPART_SS_ASC_pop", y="CA", orientation='h', height=300)
fig.add_vline(x=df_menage.X60_ANS_ET_PLUS_APPART_SS_ASC_pop.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
'''
---
### Population des 60 ans et plus dans un appartement avec ascenceur :
_Rapporté à la population du ressort de cour d'appel en 2024_

'''


fig = px.bar(df_menage[df_menage['CA'].isin(selected_ca)], x="X60_ANS_ET_PLUS_APPART_AV_ASC_pop", y="CA", orientation='h', height=300)
fig.add_vline(x=df_menage.X60_ANS_ET_PLUS_APPART_AV_ASC_pop.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
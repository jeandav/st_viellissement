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
df_menage = get_menage_data()
# df_intens_pauv = get_intens_pauv_data()
# df_rev_disp = get_rev_disp_data()
# df_drees = get_drees_data()
# df_persagees = get_persagees_data()
# gdp_df = get_gdp_data()


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
# Conditions de logement lié à l’isolement de la personne âgée
'''


'''
### 60 ans et plus isolés
'''
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_x60_ans_et_plus_isoles", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_x60_ans_et_plus_isoles", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de 60 ans et plus isolés (en milliers)"
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

'''
### Population des 60 ans et plus dans un ménage
'''

# st.bar_chart(df_menage[df_menage['CA'].isin(selected_ca)], x="CA", y=["X60_ANS_ET_PLUS_APPART_AV_ASC","X60_ANS_ET_PLUS_APPART_SS_ASC","X60_ANS_ET_PLUS_AUT_LOGT","X60_ANS_ET_PLUS_EMMENAGT_2","X60_ANS_ET_PLUS_EMMENAGT_30","X60_ANS_ET_PLUS_EN_MAISON","X60_ANS_ET_PLUS_ISOLES","X60_ANS_ET_PLUS_LOC_PARC_PRIVE","X60_ANS_ET_PLUS_LOC_PARC_SOCIAL","X60_ANS_ET_PLUS_LOGT_1970","X60_ANS_ET_PLUS_PROPRIETAIRES","X60_ANS_ET_PLUS_SANS_VOITURE"], horizontal=True)

fig = px.bar(df_menage[df_menage['CA'].isin(selected_ca)], x=["X60_ANS_ET_PLUS_APPART_AV_ASC","X60_ANS_ET_PLUS_APPART_SS_ASC"], y="CA", orientation='h', height=300)
newnames = {'X60_ANS_ET_PLUS_APPART_AV_ASC':'Appartements avec ascenceur', 'X60_ANS_ET_PLUS_APPART_SS_ASC': 'Appartements sans ascenceur'}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
fig.update_layout(
    yaxis_title='',
    xaxis_title='Année',
    legend_title=None,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        )
    )
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de 60 ans et plus dans un ménage"
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

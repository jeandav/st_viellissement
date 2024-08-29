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

def get_popglobale_data():
    DATA_FILENAME = Path(__file__).parent/'../data/pop_globale_ressort.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df


df_cluster = get_cluster_data()
df_menage = get_menage_data()
df_popglobale = get_popglobale_data()

df_cluster = pd.merge(df_cluster, df_popglobale, left_on='ressort_ca', right_on='pop')


df_menage = pd.merge(df_menage, df_popglobale, left_on='CA', right_on='pop')

df_menage['pop_2016'] = df_menage['pop_2016'].astype(float)
df_menage['X60_ANS_ET_PLUS_APPART_AV_ASC_pop'] = (df_menage['X60_ANS_ET_PLUS_APPART_AV_ASC'] / df_menage['pop_2016'])*100
df_menage['X60_ANS_ET_PLUS_APPART_SS_ASC_pop'] = (df_menage['X60_ANS_ET_PLUS_APPART_SS_ASC'] / df_menage['pop_2016'])*100


# -----------------------------------------------------------------------------




# st.write(df_menage)

liste_ca = df_cluster['ressort_ca'].unique()


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

# st.write(df_menage)

# ===========================
# MARK: Population des 60 ans et plus isolés
# ===========================

'''
---
### Population des 60 ans et plus isolés
_Rapporté par la population totale en 2016_
'''

st.write('✅')

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_x60_ans_et_plus_isoles", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_x60_ans_et_plus_isoles", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de 60 ans et plus isolés (en milliers)"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_x60_ans_et_plus_isoles.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ===========================
# MARK: Population des 60 ans et plus dans un appartement sans ascenceur
# ===========================


'''
---
### Population des 60 ans et plus dans un appartement _sans ascenceur_ :
_Rapporté à la population du ressort de cour d'appel en 2016_
'''

st.write('✅')



fig = px.bar(df_menage[df_menage['CA'].isin(selected_ca)], x="X60_ANS_ET_PLUS_APPART_SS_ASC_pop", y="CA", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Population des 60 ans et plus dans un appartement sans ascenceur"
)
fig.add_vline(x=df_menage[df_menage['CA'].isin(liste_ca)].X60_ANS_ET_PLUS_APPART_SS_ASC_pop.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===========================
# MARK: Population des 60 ans et plus dans un appartement avec ascenceur
# ===========================


'''
---
### Population des 60 ans et plus dans un appartement _avec ascenceur_ :
_Rapporté à la population du ressort de cour d'appel en 2016_
'''

st.write('✅')



fig = px.bar(df_menage[df_menage['CA'].isin(selected_ca)], x="X60_ANS_ET_PLUS_APPART_AV_ASC_pop", y="CA", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Population des 60 ans et plus dans un appartement avec ascenceur"
)
fig.add_vline(x=df_menage[df_menage['CA'].isin(liste_ca)].X60_ANS_ET_PLUS_APPART_AV_ASC_pop.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
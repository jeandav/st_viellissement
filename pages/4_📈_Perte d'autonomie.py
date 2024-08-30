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

def get_popglobale_data():
    DATA_FILENAME = Path(__file__).parent/'../data/pop_globale_ressort.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df

# df_persagees = get_persagees_data()
df_cluster = get_cluster_data()
df_popglobale = get_popglobale_data()

df_cluster = pd.merge(df_cluster, df_popglobale, left_on='ressort_ca', right_on='pop')
df_cluster['ind_vie_pop'] = df_cluster['ind_vie'] / df_cluster['pop_2024']


# -----------------------------------------------------------------------------






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
    Ministère de la Justice  \nDirection des services judiciaires   \nPôle de l'Evaluation et de la Prospective
    '''



filtered_df_cluster = df_cluster[df_cluster['ressort_ca'].isin(selected_ca)]

# st.table(df_menage)

st.image('img/logo_minjus.svg', width=100)


'''
# Perte d'autonomie
'''
# ===========================
# MARK: Nombre de bénéficiaires de l'APA à domicile
# ===========================
'''
---
### Nombre de bénéficiaires de l'APA* _à domicile_
Payés au titre du mois de décembre 2022, rapporté par la population totale en 2022

_*Allocation personnalisée d'autonomie_
'''
# st.write('✅')

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y=["N_apa_dom","N_apa_etab"], horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_apa_dom", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de l'APA à domicile"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_dom.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



# ===========================
# MARK: Nombre de bénéficiaires de l'APA en établissement
# ===========================
'''
### Nombre de bénéficiaires de l'APA* _en établissement_
Payés au titre du mois de décembre 2022, rapporté par la population totale en 2022

_*Allocation personnalisée d'autonomie_

'''
# st.write('✅')

fig = px.bar(filtered_df_cluster, x="N_apa_etab", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de l'APA en établissement"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_etab.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})




# ===========================
# MARK: Nombre de bénéficiaires de la PCH de 60 ans et plus
# ===========================
'''
---
### Nombre de bénéficiaires de la PCH* de 60 ans et plus
_*Prestation de compensation du handicap_

_Rapporté par la population totale en 2022_
'''
# st.write('✅')

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_pch", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_pch", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de la PCH (en milliers)"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_pch.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

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

def get_intens_pauv_data():
    DATA_FILENAME = Path(__file__).parent/'../data/caisse_dep/caisse_dep_intens_pauv.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=",")

    return df

def get_rev_disp_data():
    DATA_FILENAME = Path(__file__).parent/'../data/caisse_dep/caisse_dep_rev_disp.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=",")

    return df


def get_popglobale_data():
    DATA_FILENAME = Path(__file__).parent/'../data/pop_globale_ressort.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df



df_cluster = get_cluster_data()
df_intens_pauv = get_intens_pauv_data()
df_rev_disp = get_rev_disp_data()
df_popglobale = get_popglobale_data()

df_cluster = pd.merge(df_cluster, df_popglobale, left_on='ressort_ca', right_on='pop')
df_cluster['ind_vie_pop'] = df_cluster['ind_vie'] / df_cluster['pop_2024']

df_rev_disp = pd.merge(df_rev_disp, df_popglobale, left_on='ca', right_on='pop')
df_rev_disp['med_rev_disp_pop'] = (df_rev_disp['med_rev_disp'] / df_rev_disp['pop_2024'])*100


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
    Ministère de la Justice  \nPôle de l'Evaluation et de la Prospective
    '''



filtered_df_cluster = df_cluster[df_cluster['ressort_ca'].isin(selected_ca)]

# st.table(df_rev_disp)



st.image('img/logo_minjus.svg', width=100)

'''
# Vulnérabilité financière
'''

# ===========================
# MARK: Médiane du revenu disponible par unité de consommation
# ===========================


'''
---
### Médiane du revenu disponible par unité de consommation
'''
st.write('✅')

pop_options = {
    "Population globale" : "med_rev_disp",
    "60-74 ans" : "n_vie_60_74",
    "Plus de 75 ans" : "n_vie_75",
}
selected_pop = st.selectbox(
        "Population :",
        pop_options.keys())

# st.bar_chart(df_rev_disp[df_rev_disp['ca'].isin(selected_ca)], x="ca", y="med_rev_disp", horizontal=True)
# st.write(df_rev_disp[df_rev_disp['ca'].isin(liste_ca)].med_rev_disp.mean())

# st.write(df_rev_disp)
# st.write(pop_options[selected_pop])

fig = px.bar(df_rev_disp[df_rev_disp['ca'].isin(selected_ca)], x=pop_options[selected_pop], y="ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Revenu médian disponible (€)"
)
fig.add_vline(x=df_rev_disp[df_rev_disp['ca'].isin(liste_ca)][pop_options[selected_pop]].mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})





# ===========================
# MARK: Bénéficiaires du minimum vieillesse
# ===========================

'''
---
### Bénéficiaires du minimum vieillesse
_Rapporté par la population totale en 2022_
'''
st.write('✅')
# st.write(filtered_df_cluster)
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_min_vie", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_min_vie", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires du minimum vieillesse (en milliers)"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_min_vie.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===========================
# MARK: Intensité de la pauvreté au seuil de 60%
# ===========================


'''
---
### Intensité de la pauvreté au seuil de 60%
'''
# st.bar_chart(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="ca", y="intens_pauv", horizontal=True)

fig = px.bar(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="intens_pauv", y="ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Intensité de la pauvreté des personnes agées (0 à 1)"
)
fig.add_vline(x=df_intens_pauv[df_intens_pauv['ca'].isin(liste_ca)].intens_pauv.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



# ===========================
# MARK: Interdécile
# ===========================


'''
---
### Interdécile*
_Relation le 1er et le 9e déciles de la distribution de l'indice de pauvreté_
'''

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="interdecile", horizontal=True)

fig = px.bar(filtered_df_cluster, x="interdecile", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Interdécile"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].interdecile.mean(), line_width=1, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


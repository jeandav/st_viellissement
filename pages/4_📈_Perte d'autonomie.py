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

    st.write("""
    <b>Réalisation</b><br>
    Ministère de la Justice<br>
    Direction des services judiciaires <br>
    Pôle de l'Evaluation et de la Prospective
    """, unsafe_allow_html=True)



filtered_df_cluster = df_cluster[df_cluster['ressort_ca'].isin(selected_ca)]

# st.table(df_menage)

st.image('img/logo_minjus.svg', width=100)


'''
# Perte d'autonomie
---
'''
# ===========================
# MARK: Nombre de bénéficiaires de l'APA à domicile
# ===========================

st.write("""
<h3>Nombre de bénéficiaires de l'APA* <em>à domicile</em></h3>
Payés au titre du mois de décembre 2022, pour 100.000 habitants
<br>
<em>*Allocation personnalisée d'autonomie</em>
""", unsafe_allow_html=True)

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y=["N_apa_dom","N_apa_etab"], horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_apa_dom", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de l'APA à domicile pour 100.000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_dom.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_apa_dom'].iloc[0]),' personnes sur 100.000 sont bénéficiaires de l’APA <i>à domicile</i>. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_dom.mean()),'personnes sur 100.000.',unsafe_allow_html=True)

# ===========================
# MARK: Nombre de bénéficiaires de l'APA en établissement
# ===========================

st.write("""
<h3>Nombre de bénéficiaires de l'APA* <em>en établissement</em></h3>
Payés au titre du mois de décembre 2022, pour 100.000 habitants
<br>
<em>*Allocation personnalisée d'autonomie</em>
""", unsafe_allow_html=True)
# st.write('✅')

fig = px.bar(filtered_df_cluster, x="N_apa_etab", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de l'APA en établissement pour 100.000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_etab.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_apa_etab'].iloc[0]),' personnes sur 100.000 sont bénéficiaires de l’APA <i>en établissement</i>. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_etab.mean()),'personnes sur 100.000.',unsafe_allow_html=True)
st.markdown(':grey[Source : _DREES; exploitation PEP/DSJ_]')


# ===========================
# MARK: Nombre de bénéficiaires de la PCH de 60 ans et plus
# ===========================

st.write("""
<hr>
<h3>Nombre de bénéficiaires de la PCH* de 60 ans et plus</h3>
Pour 100.000 habitants<br>
<em>*Prestation de compensation du handicap</em>
""", unsafe_allow_html=True)

# st.write('✅')

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_pch", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_pch", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de la PCH pour 100.000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_pch.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})




st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_pch'].iloc[0]),'personnes sur 100.000 de 60 ans ou plus est bénéficiaire de la PCH. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_pch.mean()),'personnes sur 100.000.',unsafe_allow_html=True)
st.markdown(':grey[Source : _DREES; exploitation PEP/DSJ_]')

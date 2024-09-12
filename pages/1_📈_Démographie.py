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
gdp_df = get_gdp_data()
df_persagees = get_persagees_data()
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

# st.write(df_cluster)


st.image('img/logo_minjus.svg', width=100)


'''
# Démographie
---
'''

min_value = gdp_df['annee'].min()
max_value = gdp_df['annee'].max()

from_year = min_value
to_year = max_value

liste_ca = gdp_df['ca'].unique()


genre_options = {
    "Femmes" : "FEMMES",
    "Hommes" : "HOMMES",
}

col1, col2 = st.columns(2)

with col1:
    selected_genre = st.selectbox(
        "Sexe :",
        genre_options.keys())

with col2:
    selected_trancheage = st.selectbox(
        "Tranche d\'age :",
        ("75 ans et plus", "60-74 ans"))

# st.write(selected_genre)
# st.write(selected_trancheage)

# ===========================
# MARK: Nombre projeté de seniors
# ===========================


if selected_genre == 'Femmes' and selected_trancheage == '75 ans et plus': st.write('### Nombre projeté de seniors de femmes de 75 ans ou plus en 2040')
if selected_genre == 'Femmes' and selected_trancheage == '60-74 ans': st.write('### Nombre projeté de femmes de 60-74 ans en 2040')
if selected_genre == 'Hommes' and selected_trancheage == '75 ans et plus': st.write('### Nombre projeté de seniors d’hommes de 75 ans ou plus en 2040')
if selected_genre == 'Hommes' and selected_trancheage == '60-74 ans': st.write('### Nombre projeté d’hommes de 60-74 ans en 2040')
# st.write('✅')

# st.write(selected_ca.append('FRANCE'))
filtered_gdp_df = gdp_df[
    # (gdp_df['dep2'].isin(selected_countries))
    (gdp_df['ca'].isin(selected_ca))
    & (gdp_df['genre'] == genre_options[selected_genre])
    & (gdp_df['tranche_age'] == selected_trancheage)
    & (gdp_df['annee'] <= to_year)
    & (from_year <= gdp_df['annee'])
]


filtered_df_persagees = df_persagees[
    (df_persagees['CA'].isin(selected_ca))
    & (df_persagees['SEXE'] == genre_options[selected_genre])
    & (df_persagees['TRANCHAGE'] == selected_trancheage)
    & (df_persagees['ANNEE'] <= 2040)
]
# st.write(filtered_df_persagees)
fig = px.line(filtered_df_persagees, x="ANNEE", y="value", color='CA', markers=True)
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

# fig.add_vline(x=2024, line_width=1, line_color="lightgrey")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ===========================
# MARK: Nombre projeté de seniors
# ===========================


if selected_genre == 'Femmes' and selected_trancheage == '75 ans et plus': st.write('### Nombre projeté de seniors de femmes de 75 ans ou plus en en établissement en situation de dépendance en 2040')
if selected_genre == 'Femmes' and selected_trancheage == '60-74 ans': st.write('### Nombre projeté de femmes de 60-74 ans en en établissement en situation de dépendance en 2040')
if selected_genre == 'Hommes' and selected_trancheage == '75 ans et plus': st.write('### Nombre projeté de seniors d’hommes de 75 ans ou plus en en établissement en situation de dépendance en 2040')
if selected_genre == 'Hommes' and selected_trancheage == '60-74 ans': st.write('### Nombre projeté d’hommes de 60-74 ans en en établissement en situation de dépendance en 2040')

# st.table(filtered_df_persagees)
filtered_gdp_df = filtered_gdp_df[filtered_gdp_df['annee'] <= 2040]

fig = px.line(filtered_gdp_df, x="annee", y="nb_proj_seniors", color='ca', markers=True)
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
# fig.add_vline(x=2024, line_width=1, line_color="lightgrey")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


st.markdown(':grey[Source : _Modèle LIVIA (DREES)_]')


# ===========================
# MARK: Indice de vieillissement
# ===========================
'''
---
### Indice de vieillissement
'''
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="ind_vie", horizontal=True)

fig = px.bar(filtered_df_cluster, x="ind_vie", y="ressort_ca", orientation='h', height=300)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Indice de vieillissement"
)
# fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].ind_vie.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")
fig.add_vline(x=86, line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


st.write('<b><u>Note de lecture :</b></u> L’indice de vieillissement est le rapport de la population des 65 ans et plus sur celle des moins de 20 ans. Plus l’indice est faible, plus le rapport est favorable aux jeunes; plus il est élevé plus il est favorable aux personnes âgées.', unsafe_allow_html=True)
st.markdown(':grey[Source : _Insee, Recensement de la population (RP), exploitation principale_]')

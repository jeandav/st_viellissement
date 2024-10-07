import streamlit as st
import pandas as pd
import math
from pathlib import Path

import plotly.express as px
import numpy as np

from pages.jd_functions.jd_func import select_graph_height
from pages.jd_functions.jd_func import liste_cluster_options
from pages.jd_functions.jd_func import sidebar_signature

from pages.jd_functions.jd_func_import import get_cluster_data


# -----------------------------------------------------------------------------

st.set_page_config(
    page_title='Evolution du vieillissement',
    page_icon=':chart_with_upwards_trend:',
    layout="centered"
)

# -----------------------------------------------------------------------------

# @st.cache_data

df_cluster = get_cluster_data()

# -----------------------------------------------------------------------------

liste_ca = df_cluster['ressort_ca'].unique()

with st.sidebar:
    cluster_options = liste_cluster_options()
    chosen_cluster = st.radio("Choix du groupe :", cluster_options.keys(),horizontal=True, index=3)
    '''---'''
    selected_ca = st.multiselect('Choix de la cour d\'appel :', liste_ca, cluster_options[chosen_cluster])
    '''---'''
    st.write(sidebar_signature(), unsafe_allow_html=True)

jd_graph_height = select_graph_height(len(selected_ca))
filtered_df_cluster = df_cluster[df_cluster['ressort_ca'].isin(selected_ca)]

# -----------------------------------------------------------------------------

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
Payés au titre du mois de décembre 2022, pour 1000 habitants
<br>
<em>*Allocation personnalisée d'autonomie</em>
""", unsafe_allow_html=True)

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y=["N_apa_dom","N_apa_etab"], horizontal=True)

fig = px.bar(filtered_df_cluster, x=filtered_df_cluster.N_apa_dom/100, y="ressort_ca", orientation='h', height=jd_graph_height, text=filtered_df_cluster.N_apa_dom/100)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de l'APA à domicile pour 1000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_dom.mean()/100, line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_apa_dom'].iloc[0]/100,2),' personnes sur 1000 sont bénéficiaires de l’APA <i>à domicile</i>. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_dom.mean()/100,2),'personnes sur 1000.',unsafe_allow_html=True)

# ===========================
# MARK: Nombre de bénéficiaires de l'APA en établissement
# ===========================

st.write("""
<h3>Nombre de bénéficiaires de l'APA* <em>en établissement</em></h3>
Payés au titre du mois de décembre 2022, pour 1000 habitants
<br>
<em>*Allocation personnalisée d'autonomie</em>
""", unsafe_allow_html=True)
# st.write('✅')

fig = px.bar(filtered_df_cluster, x=filtered_df_cluster.N_apa_etab/100, y="ressort_ca", orientation='h', height=jd_graph_height, text=filtered_df_cluster.N_apa_etab/100)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de l'APA en établissement pour 1000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_etab.mean()/100, line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_apa_etab'].iloc[0]/100,2),' personnes sur 1000 sont bénéficiaires de l’APA <i>en établissement</i>. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_apa_etab.mean()/100,2),'personnes sur 1000.',unsafe_allow_html=True)
st.markdown(':grey[Source : _DREES; exploitation PEP/DSJ_]')


# ===========================
# MARK: Nombre de bénéficiaires de la PCH de 60 ans et plus
# ===========================

st.write("""
<hr>
<h3>Nombre de bénéficiaires de la PCH* de 60 ans et plus</h3>
Pour 1000 habitants<br>
<em>*Prestation de compensation du handicap</em>
""", unsafe_allow_html=True)


fig = px.bar(filtered_df_cluster, x=filtered_df_cluster.N_pch/100, y="ressort_ca", orientation='h', height=jd_graph_height, text=filtered_df_cluster.N_pch/100)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires de la PCH pour 100 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_pch.mean()/100, line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_pch'].iloc[0]/100,2),'personnes sur 1000 de 60 ans ou plus est bénéficiaire de la PCH. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_pch.mean()/100,2),'personnes sur 1000.',unsafe_allow_html=True)
st.markdown(':grey[Source : _DREES; exploitation PEP/DSJ_]')

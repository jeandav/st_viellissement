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
from pages.jd_functions.jd_func_import import get_intens_pauv_data
from pages.jd_functions.jd_func_import import get_rev_disp_data



# -----------------------------------------------------------------------------

st.set_page_config(
    page_title='Evolution du vieillissement',
    page_icon=':chart_with_upwards_trend:',
    layout="centered"
)

# -----------------------------------------------------------------------------

# @st.cache_data

df_cluster = get_cluster_data()
df_intens_pauv = get_intens_pauv_data()
df_rev_disp = get_rev_disp_data()


# -----------------------------------------------------------------------------

liste_ca = df_cluster['ressort_ca'].unique()

with st.sidebar:
    cluster_options = liste_cluster_options()
    chosen_cluster = st.radio("Choix du groupe :", cluster_options.keys(),horizontal=True)
    '''---'''
    selected_ca = st.multiselect('Choix de la cour d\'appel :', liste_ca, cluster_options[chosen_cluster])
    '''---'''
    st.write(sidebar_signature(), unsafe_allow_html=True)

jd_graph_height = select_graph_height(len(selected_ca))
filtered_df_cluster = df_cluster[df_cluster['ressort_ca'].isin(selected_ca)]

# -----------------------------------------------------------------------------

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

pop_options = {
    "Population globale" : "med_rev_disp",
    "60-74 ans" : "n_vie_60_74",
    "Plus de 75 ans" : "n_vie_75",
}
selected_pop = st.selectbox(
        "Population :",
        pop_options.keys())

fig = px.bar(df_rev_disp[df_rev_disp['ca'].isin(selected_ca)], x=pop_options[selected_pop], y="ca", orientation='h', height=jd_graph_height, text=pop_options[selected_pop])
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Revenu médian disponible (€)"
)
fig.add_vline(x=df_rev_disp[df_rev_disp['ca'].isin(liste_ca)][pop_options[selected_pop]].mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

data_med_disp = df_rev_disp[df_rev_disp['ca'] == selected_ca[0]]

# st.write('Le revenu disponible par uniré de consommation correspond au niveau de vie d un ménage')

st.write('<b><u>Note de lecture : </b></u>Le revenu disponible par unité de consommation correspond au niveau de vie d’un ménage. Au sein du ressort de la cour d’appel de ', data_med_disp['ca'].iloc[0].title(),', dans la catégorie \"',selected_pop,'\" le revenu disponible par unité de consommation est de ',round(data_med_disp[pop_options[selected_pop]].iloc[0]),'€, contre ',round(df_rev_disp[df_rev_disp['ca'].isin(liste_ca)][pop_options[selected_pop]].mean()),'€ sur l’ensemble de la France.', unsafe_allow_html=True)







# ===========================
# MARK: Bénéficiaires du minimum vieillesse
# ===========================

'''
---
### Bénéficiaires du minimum vieillesse
_Pour 1000 habitants._
'''


fig = px.bar(filtered_df_cluster, x=filtered_df_cluster.N_min_vie/100, y="ressort_ca", orientation='h', height=jd_graph_height, text=filtered_df_cluster.N_min_vie/100)
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires du minimum vieillesse pour 1000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_min_vie.mean()/100, line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})




st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_min_vie'].iloc[0]/100,2),'personnes sur 1000 bénéficient du minimum vieillesse. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_min_vie.mean()/100,2),'personnes sur 1000.', unsafe_allow_html=True)

st.markdown(':grey[Source : _Drees ; Insee, Estimations de population; exploitation PEP/DSJ_]')



# ===========================
# MARK: Intensité de la pauvreté au seuil de 60%
# ===========================


'''
---
### Intensité de la pauvreté au seuil de 60%
'''
# st.bar_chart(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="ca", y="intens_pauv", horizontal=True)

fig = px.bar(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="intens_pauv", y="ca", orientation='h', height=jd_graph_height, text=round(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)].intens_pauv,3))
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Intensité de la pauvreté des personnes agées"
)
fig.add_vline(x=df_intens_pauv[df_intens_pauv['ca'].isin(liste_ca)].intens_pauv.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.write('<b><u>Note de lecture :</b></u> L’intensité de la pauvreté est définie comme étant l’écart relatif entre le revenu moyen des personnes pauvres et le seuil de pauvreté. En France et en Europe, le seuil est le plus souvent fixé à 60% du niveau de vie médian. Plus cet indicateur est élevé et plus la pauvreté est dite intense. Au sein du ressort de la cour d’appel de ',df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)].iloc[0].ca.title(),', ce seuil est de ', round(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)].iloc[0].intens_pauv, 3),', contre',round(df_intens_pauv[df_intens_pauv['ca'].isin(liste_ca)].intens_pauv.mean(), 3),'dans l’ensemble de la population Française.',unsafe_allow_html=True)


# ===========================
# MARK: Interdécile
# ===========================

'''
---
### Interdécile
'''

# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="interdecile", horizontal=True)

fig = px.bar(filtered_df_cluster, x="interdecile", y="ressort_ca", orientation='h', height=jd_graph_height, text="interdecile")
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Interdécile"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].interdecile.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


st.write('<b><u>Note de lecture :</b></u> L’interdécile est une mesure de l’inégalité des revenus. Il rapporte le niveau de vie minimum des 10% les plus riches et le niveau de vie maximum des 10% les plus modestes. Au sein du ressort de la d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),', l’interdécile est de',filtered_df_cluster['interdecile'].iloc[0],'contre',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].interdecile.mean(),2),'dans l’ensemble de la population Française.', unsafe_allow_html=True)
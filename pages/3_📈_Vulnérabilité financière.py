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


# def get_popglobale_data():
#     DATA_FILENAME = Path(__file__).parent/'../data/pop_globale_ressort.csv'
#     df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

#     return df



df_cluster = get_cluster_data()
df_intens_pauv = get_intens_pauv_data()
df_rev_disp = get_rev_disp_data()
# df_popglobale = get_popglobale_data()

# df_cluster = pd.merge(df_cluster, df_popglobale, left_on='ressort_ca', right_on='pop')
# df_cluster['ind_vie_pop'] = df_cluster['ind_vie'] / df_cluster['pop_2024']

# df_rev_disp = pd.merge(df_rev_disp, df_popglobale, left_on='ca', right_on='pop')
# df_rev_disp['med_rev_disp_pop'] = (df_rev_disp['med_rev_disp'] / df_rev_disp['pop_2024'])*100


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

jd_graph_height = 300
if len(selected_ca) > 3:
    jd_graph_height = 500
else:
    jd_graph_height = 300

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
# st.write('✅')

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

fig = px.bar(df_rev_disp[df_rev_disp['ca'].isin(selected_ca)], x=pop_options[selected_pop], y="ca", orientation='h', height=jd_graph_height, text=pop_options[selected_pop])
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Revenu médian disponible (€)"
)
fig.add_vline(x=df_rev_disp[df_rev_disp['ca'].isin(liste_ca)][pop_options[selected_pop]].mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

data_med_disp = df_rev_disp[df_rev_disp['ca'] == selected_ca[0]]

# st.write('Le revenu disponible par uniré de consommation correspond au niveau de vie d un ménage')

st.write('<b><u>Note de lecture : </b></u>Le revenu disponible par unité de consommation correspond au niveau de vie d’un ménage. Au sein du ressort de la cour d’appel de ', data_med_disp['ca'].iloc[0].title(),', le revenu disponible par unité de consommation est de ',round(data_med_disp[pop_options[selected_pop]].iloc[0]),'€, contre ',round(df_rev_disp[df_rev_disp['ca'].isin(liste_ca)][pop_options[selected_pop]].mean()),'€ dans la population Française.', unsafe_allow_html=True)

# st.markdown(':grey[Source : _Insee, Revenus localisés sociaux et fiscaux (Filosofi); exploitation PEP/DSJ_]')

# st.write(round(df_rev_disp[df_rev_disp['ca'].isin(liste_ca)][pop_options[selected_pop]].mean()))
# st.write(data_med_disp['ca'].iloc[0].title())
# st.write(data_med_disp)

# st.write('Par exemple, pour la population \"',pop_options[selected_pop],'la médiane du niveau de vie moyen est de ',)
# st.write(data_iv)







# ===========================
# MARK: Bénéficiaires du minimum vieillesse
# ===========================

'''
---
### Bénéficiaires du minimum vieillesse
_Pour 100.000 habitants._
'''

# st.write('✅')
# st.write(filtered_df_cluster)
# st.bar_chart(filtered_df_cluster, x="ressort_ca", y="N_min_vie", horizontal=True)

fig = px.bar(filtered_df_cluster, x="N_min_vie", y="ressort_ca", orientation='h', height=jd_graph_height, text='N_min_vie')
fig.update_layout(
    yaxis_title="Cour d\'appel", xaxis_title="Nombre de bénéficiaires du minimum vieillesse pour 100.000 habitants"
)
fig.add_vline(x=df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_min_vie.mean(), line_width=1.5, line_color="lightgrey", annotation_text="France", annotation_position="top")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})




st.write('<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),',', round(filtered_df_cluster['N_min_vie'].iloc[0]),'personnes sur 100.000 bénéficient du minimum vieillesse. Sur l’ensemble de la population Française, ce ratio est de',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].N_min_vie.mean()),'personnes sur 100.000.', unsafe_allow_html=True)

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


st.write('<b><u>Note de lecture :</b></u> L’interdécile est une mesure de l’inégalité des revenus. Il rapporte le niveau de vie minimum des 10 % les plus riches et le niveau de vie maximum des 10% les plus pauvres. Au sein du ressort de la d’appel de',filtered_df_cluster['ressort_ca'].iloc[0].title(),', l’interdécile est de',filtered_df_cluster['interdecile'].iloc[0],'contre',round(df_cluster[df_cluster['ressort_ca'].isin(liste_ca)].interdecile.mean(),2),'dans l’ensemble de la population Française.', unsafe_allow_html=True)
import streamlit as st
import pandas as pd

import plotly.express as px

from pages.jd_functions.jd_func import select_graph_height
from pages.jd_functions.jd_func import format_float
from pages.jd_functions.jd_func import is_list_in_dict

import pages.jd_functions.constants as constants

from pages.jd_functions.jd_func_import import get_cluster_data
from pages.jd_functions.jd_func_import import get_menage_data
from pages.jd_functions.jd_func_import import get_popglobale_data


# -----------------------------------------------------------------------------

st.set_page_config(
    page_title=constants.config_page_title,
    page_icon=constants.config_page_icon,
    layout=constants.config_layout,
)

# -----------------------------------------------------------------------------

df_cluster = get_cluster_data()
df_menage = get_menage_data()
df_popglobale = get_popglobale_data()

df_cluster = pd.merge(df_cluster, df_popglobale, left_on="ressort_ca", right_on="pop")
df_menage = pd.merge(df_menage, df_popglobale, left_on="CA", right_on="pop")

df_menage["pop_2016"] = df_menage["pop_2016"].astype(float)
df_menage["X60_ANS_ET_PLUS_APPART_AV_ASC_pop"] = (
    df_menage["X60_ANS_ET_PLUS_APPART_AV_ASC"] / df_menage["pop_2016"]
) * 100
df_menage["X60_ANS_ET_PLUS_APPART_SS_ASC_pop"] = (
    df_menage["X60_ANS_ET_PLUS_APPART_SS_ASC"] / df_menage["pop_2016"]
) * 100

# -----------------------------------------------------------------------------

liste_ca = df_cluster["ressort_ca"].unique()


liste_ca = df_cluster["ressort_ca"].unique()

with st.sidebar:
    cluster_options = constants.cluster_options
    chosen_cluster = st.radio(
        "Choix du groupe :", cluster_options.keys(), horizontal=True, index=3
    )
    """---"""
    selected_ca = st.multiselect(
        "Choix de la cour d'appel :", liste_ca, cluster_options[chosen_cluster]
    )
    # """---"""
    # chosen_mean = st.checkbox("Afficher la moyenne du groupe", True)
    chosen_mean = is_list_in_dict(cluster_options, selected_ca)
    # st.write(chosen_mean)
    """---"""
    st.write(constants.pep_signature, unsafe_allow_html=True)

jd_graph_height = select_graph_height(len(selected_ca))
filtered_df_cluster = df_cluster[df_cluster["ressort_ca"].isin(selected_ca)]


df_menage_filtered = df_menage[df_menage["CA"].isin(selected_ca)]
first_ca = df_menage_filtered["CA"].iloc[0]

# -----------------------------------------------------------------------------

st.image(constants.img_logo, width=constants.img_width)


"""
# Conditions de logement
"""

# ===========================
# MARK: Population des 60 ans et plus isolés
# ===========================

"""
---
### Population des 60 ans et plus isolés
_Pour 100 habitants_
"""

fig = px.bar(
    filtered_df_cluster,
    x=(filtered_df_cluster.N_x60_ans_et_plus_isoles) / 1000,
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text=round((filtered_df_cluster.N_x60_ans_et_plus_isoles) / 1000,2),
)

fig.update_layout(
    yaxis_title="Cour d'appel",
    xaxis_title="Nombre de 60 ans et plus isolés pour 100 habitants",
    # hovermode=False,
    margin_pad=constants.margin_pad
)

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Nombre de 60 ans et plus<br>isolés pour 100 habitants: %{x}") #


# ========== Moyenne France ==========
fig.add_vline(
    x=df_cluster[
        df_cluster["ressort_ca"].isin(liste_ca)
    ].N_x60_ans_et_plus_isoles.mean()
    / 1000,
    line_width=constants.line_france_width,
    line_color=constants.line_france_color,
    annotation_text=constants.line_france_text,
    annotation_position=constants.line_france_annotation_position,
)

# ========== Moyenne cour ==========
if chosen_mean:
    fig.add_vline(
        x=df_cluster[
            df_cluster["ressort_ca"].isin(cluster_options[chosen_cluster])
        ].N_x60_ans_et_plus_isoles.mean()
        / 1000,
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(round((filtered_df_cluster["N_x60_ans_et_plus_isoles"].iloc[0]) / 1000,2)),
    "personnes sur 100 sont des personnes de plus de 60 ans isolée. Sur l’ensemble de la population française, ce ratio est de ",
    format_float(
        round(
            df_cluster[
                df_cluster["ressort_ca"].isin(liste_ca)
            ].N_x60_ans_et_plus_isoles.mean()
            / 1000,
            2,
        )
    ),
    "personnes sur 100.",
    unsafe_allow_html=True,
)

st.markdown(":grey[Source : _Insee ; exploitation PEP/DSJ_]")


# ===========================
# MARK: Population des 60 ans et plus dans un appartement sans ascenseur
# ===========================


"""
---
### Population des 60 ans et plus dans un appartement _sans ascenseur_
_Pour 100 habitants_
"""


fig = px.bar(
    df_menage_filtered,
    x="X60_ANS_ET_PLUS_APPART_SS_ASC_pop",
    y="CA",
    orientation="h",
    height=jd_graph_height,
    text=round(df_menage_filtered["X60_ANS_ET_PLUS_APPART_SS_ASC_pop"], 2),
)
fig.update_layout(
    yaxis_title="Cour d'appel",
    xaxis_title="Population des 60 ans et plus dans un appartement sans ascenseur pour 100 habitants",
    # hovermode=False,
    margin_pad=constants.margin_pad
)

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Population des 60 ans et plus<br>dans un appartement sans ascenseur<br>pour 100 habitants: %{x}") #

# ========== Moyenne France ==========
fig.add_vline(
    x=df_menage[
        df_menage["CA"].isin(liste_ca)
    ].X60_ANS_ET_PLUS_APPART_SS_ASC_pop.mean(),
    line_width=constants.line_france_width,
    line_color=constants.line_france_color,
    annotation_text=constants.line_france_text,
    annotation_position=constants.line_france_annotation_position,
)

# ========== Moyenne cour ==========
if chosen_mean:
    fig.add_vline(
        x=df_menage[
            df_menage["CA"].isin(cluster_options[chosen_cluster])
        ].X60_ANS_ET_PLUS_APPART_SS_ASC_pop.mean(),
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(
        round(df_menage_filtered["X60_ANS_ET_PLUS_APPART_SS_ASC_pop"].iloc[0], 2)
    ),
    "personnes sur 100 sont des personnes âgées vivant dans un appartement <i>sans ascenceur</i>. Sur l’ensemble de la population française, ce ratio est de",
    format_float(
        round(
            df_menage[
                df_menage["CA"].isin(liste_ca)
            ].X60_ANS_ET_PLUS_APPART_SS_ASC_pop.mean(),
            2,
        )
    ),
    "personnes sur 100.",
    unsafe_allow_html=True,
)

st.markdown(":grey[Source : _Insee; exploitation PEP/DSJ_]")

# ===========================
# MARK: Population des 60 ans et plus dans un appartement avec ascenseur
# ===========================


"""
---
### Population des 60 ans et plus dans un appartement _avec ascenseur_
_Pour 100 habitants_
"""

fig = px.bar(
    df_menage[df_menage["CA"].isin(selected_ca)],
    x="X60_ANS_ET_PLUS_APPART_AV_ASC_pop",
    y="CA",
    orientation="h",
    height=jd_graph_height,
    text=round(df_menage_filtered["X60_ANS_ET_PLUS_APPART_AV_ASC_pop"], 2),
)
fig.update_layout(
    yaxis_title="Cour d'appel",
    xaxis_title="Population des 60 ans et plus dans un appartement avec ascenseur pour 100 habitants",
    # hovermode=False,
    margin_pad=constants.margin_pad
)

# ========== Moyenne France ==========
fig.add_vline(
    x=df_menage[
        df_menage["CA"].isin(liste_ca)
    ].X60_ANS_ET_PLUS_APPART_AV_ASC_pop.mean(),
    line_width=constants.line_france_width,
    line_color=constants.line_france_color,
    annotation_text=constants.line_france_text,
    annotation_position=constants.line_france_annotation_position,
)

# ========== Moyenne cour ==========
if chosen_mean:
    fig.add_vline(
        x=df_menage[
            df_menage["CA"].isin(cluster_options[chosen_cluster])
        ].X60_ANS_ET_PLUS_APPART_AV_ASC_pop.mean(),
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Population des 60 ans et plus<br>dans un appartement avec ascenseur<br>pour 100 habitants: %{x}") #

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(
        round(df_menage_filtered[df_menage_filtered["CA"] == first_ca].X60_ANS_ET_PLUS_APPART_AV_ASC_pop.iloc[0], 2)
    ),
    "personnes sur 100 sont des personnes âgées vivant dans un appartement <i>avec ascenceur</i>. Sur l’ensemble de la population française, ce ratio est de",
    format_float(
        round(
            df_menage[
                df_menage["CA"].isin(liste_ca)
            ].X60_ANS_ET_PLUS_APPART_AV_ASC_pop.mean(),
            2,
        )
    ),
    "personnes sur 100.",
    unsafe_allow_html=True,
)

st.markdown(":grey[Source : _Insee; exploitation PEP/DSJ_]")
import streamlit as st

import plotly.express as px

from pages.jd_functions.jd_func import select_graph_height
from pages.jd_functions.jd_func import format_float

import pages.jd_functions.constants as constants

from pages.jd_functions.jd_func_import import get_cluster_data


# -----------------------------------------------------------------------------

st.set_page_config(
    page_title=constants.config_page_title,
    page_icon=constants.config_page_icon,
    layout=constants.config_layout,
)

# -----------------------------------------------------------------------------

df_cluster = get_cluster_data()

# -----------------------------------------------------------------------------

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
    """---"""
    chosen_mean = st.checkbox("Afficher la moyenne du groupe", True)
    """---"""
    st.write(constants.pep_signature, unsafe_allow_html=True)

jd_graph_height = select_graph_height(len(selected_ca))
filtered_df_cluster = df_cluster[df_cluster["ressort_ca"].isin(selected_ca)]
filtered_df_liste_ca = df_cluster[df_cluster["ressort_ca"].isin(liste_ca)]

first_ca = filtered_df_cluster["ressort_ca"].iloc[0]

# -----------------------------------------------------------------------------


st.image(constants.img_logo, width=constants.img_width)


"""
# Perte d'autonomie
---
"""
# ===========================
# MARK: Nombre de bénéficiaires de l'APA à domicile
# ===========================

st.write(
    """
    <h3>Nombre de bénéficiaires de l'APA <em>à domicile</em></h3>
    Payés au titre du mois de décembre 2022, pour 1&nbsp;000 habitants
    <br>
    """,
    unsafe_allow_html=True,
)

fig = px.bar(
    filtered_df_cluster,
    x=filtered_df_cluster.N_apa_dom / 100,
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text=filtered_df_cluster.N_apa_dom / 100,
)
fig.update_layout(
    yaxis_title="Cour d'appel",
    xaxis_title="Nombre de bénéficiaires de l'APA à domicile pour 1&nbsp;000 habitants",
    margin_pad=constants.margin_pad
)

# ========== Moyenne France ==========
fig.add_vline(
    x=filtered_df_liste_ca.N_apa_dom.mean() / 100,
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
        ].N_apa_dom.mean()
        / 100,
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>%{x} bénéficiaires de l'APA<br>à domicile pour 1&nbsp;000 habitants") #

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(round(filtered_df_cluster["N_apa_dom"].iloc[0] / 100, 2)),
    " personnes sur 1&nbsp;000 sont bénéficiaires de l’APA (Allocation personnalisée d’autonomie) <i>à domicile</i>. Sur l’ensemble de la population française, ce ratio est de",
    format_float(
        round(
            filtered_df_liste_ca.N_apa_dom.mean() / 100,
            2,
        )
    ),
    "personnes sur 1&nbsp;000.",
    unsafe_allow_html=True,
)

# ===========================
# MARK: Nombre de bénéficiaires de l'APA en établissement
# ===========================

st.write(
    """
    <h3>Nombre de bénéficiaires de l'APA <em>en établissement</em></h3>
    Payés au titre du mois de décembre 2022, pour 1&nbsp;000 habitants
    <br>
    """,
    unsafe_allow_html=True,
)

fig = px.bar(
    filtered_df_cluster,
    x=filtered_df_cluster.N_apa_etab / 100,
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text=filtered_df_cluster.N_apa_etab / 100,
)
fig.update_layout(
    yaxis_title="Cour d'appel",
    xaxis_title="Nombre de bénéficiaires de l'APA en établissement pour 1&nbsp;000 habitants",
    margin_pad=constants.margin_pad
)
# ========== Moyenne France ==========
fig.add_vline(
    x=filtered_df_liste_ca.N_apa_etab.mean() / 100,
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
        ].N_apa_etab.mean()
        / 100,
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>%{x} bénéficiaires de l'APA<br>en établissement pour 1&nbsp;000 habitants") #

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(round(filtered_df_cluster["N_apa_etab"].iloc[0] / 100, 2)),
    " personnes sur 1&nbsp;000 sont bénéficiaires de l’APA (Allocation personnalisée d’autonomie) <i>en établissement</i>. Sur l’ensemble de la population française, ce ratio est de",
    format_float(
        round(
            filtered_df_liste_ca.N_apa_etab.mean() / 100,
            2,
        )
    ),
    "personnes sur 1&nbsp;000.",
    unsafe_allow_html=True,
)
st.markdown(":grey[Source : _DREES; exploitation PEP/DSJ_]")


# ===========================
# MARK: Nombre de bénéficiaires de la PCH de 60 ans et plus
# ===========================

st.write(
    """
    <hr>
    <h3>Nombre de bénéficiaires de la PCH de 60 ans et plus</h3>
    Pour 1&nbsp;000 habitants<br>
    """,
    unsafe_allow_html=True,
)


fig = px.bar(
    filtered_df_cluster,
    x=filtered_df_cluster.N_pch / 100,
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text=filtered_df_cluster.N_pch / 100,
)
fig.update_layout(
    yaxis_title="Cour d'appel",
    xaxis_title="Nombre de bénéficiaires de la PCH pour 1&nbsp;000 habitants",
    margin_pad=constants.margin_pad
)

# ========== Moyenne France ==========
fig.add_vline(
    x=filtered_df_liste_ca.N_pch.mean() / 100,
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
        ].N_pch.mean()
        / 100,
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>%{x} bénéficiaires de la<br>PCH pour 1&nbsp;000 habitants") #

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(round(filtered_df_cluster["N_pch"].iloc[0] / 100, 2)),
    "personnes sur 1&nbsp;000 de 60 ans ou plus est bénéficiaire de la PCH (Prestation de compensation du handicap). Sur l’ensemble de la population française, ce ratio est de",
    format_float(
        round(filtered_df_liste_ca.N_pch.mean() / 100, 2)
    ),
    "personnes sur 1&nbsp;000.",
    unsafe_allow_html=True,
)
st.markdown(":grey[Source : _DREES; exploitation PEP/DSJ_]")
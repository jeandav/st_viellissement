import streamlit as st

import plotly.express as px

from pages.jd_functions.jd_func import select_graph_height
from pages.jd_functions.jd_func import format_float
from pages.jd_functions.jd_func import format_thousands
from pages.jd_functions.jd_func import is_list_in_dict

import pages.jd_functions.constants as constants

from pages.jd_functions.jd_func_import import get_cluster_data
from pages.jd_functions.jd_func_import import get_intens_pauv_data
from pages.jd_functions.jd_func_import import get_rev_disp_data


# -----------------------------------------------------------------------------

st.set_page_config(
    page_title=constants.config_page_title,
    page_icon=constants.config_page_icon,
    layout=constants.config_layout,
)

# -----------------------------------------------------------------------------

df_cluster = get_cluster_data()
df_intens_pauv = get_intens_pauv_data()
df_rev_disp = get_rev_disp_data()

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
    # """---"""
    # chosen_mean = st.checkbox("Afficher la moyenne du groupe", True)
    chosen_mean = is_list_in_dict(cluster_options, selected_ca)
    # st.write(chosen_mean)
    """---"""
    st.write(constants.pep_signature, unsafe_allow_html=True)

jd_graph_height = select_graph_height(len(selected_ca))
filtered_df_cluster = df_cluster[df_cluster["ressort_ca"].isin(selected_ca)]

first_ca = filtered_df_cluster["ressort_ca"].iloc[0]

# -----------------------------------------------------------------------------

st.image(constants.img_logo, width=constants.img_width)

"""
# Vulnérabilité financière
"""

# ===========================
# MARK: Médiane du revenu disponible par unité de consommation
# ===========================


"""
---
### Médiane du revenu disponible par unité de consommation
"""

pop_options = {
    "Population globale": "med_rev_disp",
    "60-74 ans": "n_vie_60_74",
    "Plus de 75 ans": "n_vie_75",
}
selected_pop = st.selectbox("Population :", pop_options.keys())
pop_options_verbatim = {
    "Population globale": "il est de",
    "60-74 ans": "pour les 60-74 ans, il est de",
    "Plus de 75 ans": "pour les plus de 75 ans, il est",
}
fig = px.bar(
    df_rev_disp[df_rev_disp["ca"].isin(selected_ca)],
    x=pop_options[selected_pop],
    y="ca",
    orientation="h",
    height=jd_graph_height,
    text=pop_options[selected_pop],
)
fig.update_layout(
    yaxis_title="cour d'appel", xaxis_title="Revenu médian disponible (€)",
    margin_pad=constants.margin_pad
)

# ========== Moyenne France ==========
fig.add_vline(
    x=df_rev_disp[df_rev_disp["ca"].isin(liste_ca)][pop_options[selected_pop]].mean(),
    line_width=constants.line_france_width,
    line_color=constants.line_france_color,
    annotation_text=constants.line_france_text,
    annotation_position=constants.line_france_annotation_position,
)

# ========== Moyenne cour ==========
if chosen_mean:
    fig.add_vline(
        x=df_rev_disp[df_rev_disp["ca"].isin(cluster_options[chosen_cluster])][
            pop_options[selected_pop]
        ].mean(),
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Revenu médian disponible: %{x}€") #

fig.update_traces(hovertemplate=None)
fig.update_layout(hovermode=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
data_med_disp = df_rev_disp[df_rev_disp["ca"] == selected_ca[0]]
st.write(
    "<b><u>Note de lecture : </b></u>Le revenu disponible par unité de consommation correspond au niveau de vie d’un ménage. Au sein du ressort de la cour d’appel de ",
    data_med_disp["ca"].iloc[0].title() + ",",
    pop_options_verbatim[selected_pop],
    "est de ",
    format_thousands(round(data_med_disp[pop_options[selected_pop]].iloc[0])),
    "€, contre ",
    format_thousands(
        round(
            df_rev_disp[df_rev_disp["ca"].isin(liste_ca)][
                pop_options[selected_pop]
            ].mean()
        )
    ),
    "€ au national.",
    unsafe_allow_html=True,
)

st.info("Le revenu disponible par unité de consommation (UC), également appelé 'niveau de vie', est le revenu disponible par 'équivalent adulte'. Il est calculé en rapportant le revenu disponible du ménage au nombre d'unités de consommation qui le composent. Toutes les personnes rattachées au même ménage fiscal ont le même revenu disponible par UC (ou niveau de vie).", icon='📌')

# ===========================
# MARK: Bénéficiaires du minimum vieillesse
# ===========================

"""
---
### Bénéficiaires du minimum vieillesse
_Pour 1&nbsp;000 habitants_
"""


fig = px.bar(
    filtered_df_cluster,
    x=filtered_df_cluster.N_min_vie / 100,
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text=filtered_df_cluster.N_min_vie / 100,
)
fig.update_layout(
    yaxis_title="cour d'appel",
    xaxis_title="Nombre de bénéficiaires du minimum vieillesse pour 1&nbsp;000 habitants",
    margin_pad=constants.margin_pad
)

# ========== Moyenne France ==========
fig.add_vline(
    x=df_cluster[df_cluster["ressort_ca"].isin(liste_ca)].N_min_vie.mean() / 100,
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
        ].N_min_vie.mean()
        / 100,
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>%{x} bénéficiaires du minimum<br>vieillesse pour 1 000 habitants") #

fig.update_traces(hovertemplate=None)
fig.update_layout(hovermode=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel ",
    constants.noms_apostrophe[first_ca] + ",",
    format_float(round(filtered_df_cluster["N_min_vie"].iloc[0] / 100, 2)),
    "personnes sur 1&nbsp;000 bénéficient du minimum vieillesse. Au niveau national, ce ratio est de",
    format_float(
        round(
            df_cluster[df_cluster["ressort_ca"].isin(liste_ca)].N_min_vie.mean() / 100,
            2,
        )
    ),
    "personnes sur 1&nbsp;000.",
    unsafe_allow_html=True,
)

st.markdown(
    ":grey[Source : _DREES - Insee, Estimations de population - exploitation PEP/DSJ_]"
)


# ===========================
# MARK: Intensité de la pauvreté au seuil de 60%
# ===========================


"""
---
### Intensité de la pauvreté au seuil de 60%
"""
# st.bar_chart(df_intens_pauv[df_intens_pauv['ca'].isin(selected_ca)], x="ca", y="intens_pauv", horizontal=True)

fig = px.bar(
    df_intens_pauv[df_intens_pauv["ca"].isin(selected_ca)],
    x="intens_pauv",
    y="ca",
    orientation="h",
    height=jd_graph_height,
    text=round(df_intens_pauv[df_intens_pauv["ca"].isin(selected_ca)].intens_pauv, 2),
)
fig.update_layout(
    yaxis_title="cour d'appel",
    xaxis_title="Intensité de la pauvreté des personnes agées",
    margin_pad=constants.margin_pad
)

# ========== Moyenne France ==========
fig.add_vline(
    x=df_intens_pauv[df_intens_pauv["ca"].isin(liste_ca)].intens_pauv.mean(),
    line_width=constants.line_france_width,
    line_color=constants.line_france_color,
    annotation_text=constants.line_france_text,
    annotation_position=constants.line_france_annotation_position,
)

# ========== Moyenne cour ==========
if chosen_mean:
    fig.add_vline(
        x=df_intens_pauv[
            df_intens_pauv["ca"].isin(cluster_options[chosen_cluster])
        ].intens_pauv.mean(),
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Intensité de la pauvreté des personnes agées: %{x}") #

fig.update_traces(hovertemplate=None)
fig.update_layout(hovermode=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    '<b><u>Note de lecture :</b></u> Au sein du ressort de la cour d’appel ',
    constants.noms_apostrophe[first_ca],
    ", ce seuil est de ",
    format_float(
        round(
            df_intens_pauv[df_intens_pauv["ca"].isin(selected_ca)].iloc[0].intens_pauv,
            2,
        )
    ),
    ", contre",
    format_float(
        round(df_intens_pauv[df_intens_pauv["ca"].isin(liste_ca)].intens_pauv.mean(), 2)
    ),
    "dans l’ensemble de la population française.",
    unsafe_allow_html=True,
)
st.markdown(
    ":grey[Source : _Insee - exploitation PEP/DSJ_]"
)
st.info("L’intensité de la pauvreté est définie comme étant l’écart relatif entre le revenu moyen des personnes pauvres et le seuil de pauvreté. En France, le seuil est en règle générale fixé à 60% du niveau de vie médian. Plus cet indicateur est élevé et plus la pauvreté est dite \"intense\".", icon='📌')


# ===========================
# MARK: Interdécile
# ===========================

"""
---
### Interdécile
"""

fig = px.bar(
    filtered_df_cluster,
    x="interdecile",
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text="interdecile",
)
fig.update_layout(yaxis_title="cour d'appel", xaxis_title="Interdécile",
    margin_pad=constants.margin_pad)

# ========== Moyenne France ==========
fig.add_vline(
    x=df_cluster[df_cluster["ressort_ca"].isin(liste_ca)].interdecile.mean(),
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
        ].interdecile.mean(),
        line_width=constants.line_cour_width,
        line_color=constants.line_cour_color,
        annotation_text=chosen_cluster,
        annotation_position=constants.line_cour_annotation_position,
        annotation_font_color=constants.line_cour_color,
    )

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Interdécile: %{x}") #

fig.update_traces(hovertemplate=None)
fig.update_layout(hovermode=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> Au sein du ressort de la d’appel ",
    constants.noms_apostrophe[first_ca],
    ", l’interdécile est de",
    format_float(filtered_df_cluster["interdecile"].iloc[0]),
    "contre",
    format_float(
        round(df_cluster[df_cluster["ressort_ca"].isin(liste_ca)].interdecile.mean(), 2)
    ),
    "dans l’ensemble de la population française.",
    unsafe_allow_html=True,
)
st.markdown(
    ":grey[Source : _Insee - exploitation PEP/DSJ_]"
)
st.info("L’interdécile est une mesure de l’inégalité des revenus. Il rapporte le niveau de vie minimum des 10% les plus riches au niveau de vie maximum des 10% les plus modestes.", icon='📌')

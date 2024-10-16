import streamlit as st

import plotly.express as px

from pages.jd_functions.jd_func import select_graph_height
from pages.jd_functions.jd_func import format_float
from pages.jd_functions.jd_func import format_thousands

import pages.jd_functions.constants as constants

from pages.jd_functions.jd_func_import import get_cluster_data
from pages.jd_functions.jd_func_import import get_gdp_data
from pages.jd_functions.jd_func_import import get_persagees_data


# -----------------------------------------------------------------------------

st.set_page_config(
    page_title=constants.config_page_title,
    page_icon=constants.config_page_icon,
    layout=constants.config_layout,
)

# -----------------------------------------------------------------------------

df_cluster = get_cluster_data()
gdp_df = get_gdp_data()
df_persagees = get_persagees_data()

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
    # chosen_mean = st.checkbox("Afficher la moyenne du groupe", True)
    # """---"""
    st.write(constants.pep_signature, unsafe_allow_html=True)

jd_graph_height = select_graph_height(len(selected_ca))
filtered_df_cluster = df_cluster[df_cluster["ressort_ca"].isin(selected_ca)]

# -----------------------------------------------------------------------------

st.image(constants.img_logo, width=constants.img_width)

"""
# Démographie
---
"""

from_year = gdp_df["annee"].min()
to_year = gdp_df["annee"].max()

liste_ca = gdp_df["ca"].unique()

genre_options = {
    "Femmes": "FEMMES",
    "Hommes": "HOMMES",
}

col1, col2 = st.columns(2)

with col1:
    selected_genre = st.selectbox("Sexe :", genre_options.keys())

with col2:
    selected_trancheage = st.selectbox(
        "Tranche d'age :", ("75 ans et plus", "60-74 ans")
    )


# ===========================
# MARK: Nombre projeté de seniors d’ici 2040
# ===========================


if selected_genre == "Femmes" and selected_trancheage == "75 ans et plus":
    st.write("### Nombre projeté de femmes de 75 ans ou plus d’ici 2040")
if selected_genre == "Femmes" and selected_trancheage == "60-74 ans":
    st.write("### Nombre projeté de femmes de 60-74 ans d’ici 2040")
if selected_genre == "Hommes" and selected_trancheage == "75 ans et plus":
    st.write("### Nombre projeté d’hommes de 75 ans ou plus d’ici 2040")
if selected_genre == "Hommes" and selected_trancheage == "60-74 ans":
    st.write("### Nombre projeté d’hommes de 60-74 ans d’ici 2040")

filtered_gdp_df = gdp_df[
    # (gdp_df['dep2'].isin(selected_countries))
    (gdp_df["ca"].isin(selected_ca))
    & (gdp_df["genre"] == genre_options[selected_genre])
    & (gdp_df["tranche_age"] == selected_trancheage)
    & (gdp_df["annee"] <= to_year)
    & (from_year <= gdp_df["annee"])
]


filtered_df_persagees = df_persagees[
    (df_persagees["CA"].isin(selected_ca))
    & (df_persagees["SEXE"] == genre_options[selected_genre])
    & (df_persagees["TRANCHAGE"] == selected_trancheage)
    & (df_persagees["ANNEE"] <= 2040)
]

fig = px.line(filtered_df_persagees, x="ANNEE", y="value", color="CA", markers=True)
fig.update_layout(
    yaxis_title="",
    xaxis_title="Année",
    legend_title=None,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    # margin_pad=constants.margin_pad,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ===========================
# MARK: Nombre projeté de seniors en situation de dépendance d’ici 2040
# ===========================


if selected_genre == "Femmes" and selected_trancheage == "75 ans et plus":
    st.write("### Nombre projeté de femmes de 75 ans ou plus en établissement en situation de dépendance d’ici 2040")
if selected_genre == "Femmes" and selected_trancheage == "60-74 ans":
    st.write("### Nombre projeté de femmes de 60-74 ans en établissement en situation de dépendance d’ici 2040")
if selected_genre == "Hommes" and selected_trancheage == "75 ans et plus":
    st.write("### Nombre projeté d’hommes de 75 ans ou plus en établissement en situation de dépendance d’ici 2040")
if selected_genre == "Hommes" and selected_trancheage == "60-74 ans":
    st.write("### Nombre projeté d’hommes de 60-74 ans en établissement en situation de dépendance d’ici 2040")

filtered_gdp_df = filtered_gdp_df[filtered_gdp_df["annee"] <= 2040]

fig = px.line(filtered_gdp_df, x="annee", y="nb_proj_seniors", color="ca", markers=True)
fig.update_layout(
    yaxis_title="",
    xaxis_title="Année",
    legend_title=None,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    # margin_pad=constants.margin_pad,
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

data_2040 = filtered_df_persagees[
    (filtered_df_persagees["CA"] == selected_ca[0])
    & (filtered_df_persagees["ANNEE"] == 2040)
]

data_2024 = filtered_df_persagees[
    (filtered_df_persagees["CA"] == selected_ca[0])
    & (filtered_df_persagees["ANNEE"] == 2024)
]

def pourcentage_evolution(valeur_initiale, valeur_finale):
    evolution = valeur_finale / valeur_initiale - 1
    pourcentage = evolution * 100
    return pourcentage

evolution = round(
    pourcentage_evolution(data_2024["value"].iloc[0], data_2040["value"].iloc[0])
)

data_2024_dep = filtered_gdp_df[
    (filtered_gdp_df["ca"] == selected_ca[0]) & (filtered_gdp_df["annee"] == 2024)
]
data_2040_dep = filtered_gdp_df[
    (filtered_gdp_df["ca"] == selected_ca[0]) & (filtered_gdp_df["annee"] == 2040)
]

augm2 = ""
if round(pourcentage_evolution(data_2024["value"].iloc[0], data_2040["value"].iloc[0])):
    augm2 = "+"
else:
    augm2 = ""

augm1 = ""
if (
    round(
        pourcentage_evolution(
            data_2024_dep["nb_proj_seniors"].iloc[0],
            data_2040_dep["nb_proj_seniors"].iloc[0],
        )
    )
    > 0
):
    augm1 = "+"
else:
    augm1 = ""


# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> En 2040, la DRESS estime à près de ",
    format_thousands(int(data_2040["value"].iloc[0])),
    " ",
    data_2040["SEXE"].iloc[0].lower(),
    " de ",
    data_2040["TRANCHAGE"].iloc[0].lower(),
    " au sein du ressort de la cour d’appel de ",
    data_2040["CA"].iloc[0].title() + ",",
    " contre ",
    format_thousands(int(data_2024["value"].iloc[0])),
    " en 2024, soit une évolution de ",
    augm2,
    format_float(
        round(
            pourcentage_evolution(
                data_2024["value"].iloc[0], data_2040["value"].iloc[0]
            )
        )
    ),
    "%. S’agissant des ",
    data_2024_dep["genre"].iloc[0].lower(),
    "de ",
    data_2040["TRANCHAGE"].iloc[0].lower(),
    " en établissement en situation de dépendance, le total est de ",
    format_thousands(data_2024_dep["nb_proj_seniors"].iloc[0]),
    " en 2024 contre ",
    format_thousands(data_2040_dep["nb_proj_seniors"].iloc[0]),
    " en 2040, ce qui représente",
    augm1,
    format_float(
        round(
            pourcentage_evolution(
                data_2024_dep["nb_proj_seniors"].iloc[0],
                data_2040_dep["nb_proj_seniors"].iloc[0],
            )
        )
    ),
    "%.",
    unsafe_allow_html=True,
)

st.markdown(":grey[Source : _Modèle LIVIA (DREES); exploitation PEP/DSJ_]")


# ===========================
# MARK: Indice de vieillissement
# ===========================
"""
---
### Indice de vieillissement
"""

fig = px.bar(
    filtered_df_cluster,
    x="ind_vie",
    y="ressort_ca",
    orientation="h",
    height=jd_graph_height,
    text="ind_vie",
)
fig.update_layout(yaxis_title="Cour d'appel", xaxis_title="Indice de vieillissement",
    margin_pad=constants.margin_pad)

fig.update_traces(hovertemplate="Cour d’appel: %{y}<br>Indice de vieillissement: %{x}") #

# ========== Moyenne France ==========
fig.add_vline(
    x=86,
    line_width=constants.line_france_width,
    line_color=constants.line_france_color,
    annotation_text=constants.line_france_text,
    annotation_position=constants.line_france_annotation_position,
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

data_iv = filtered_df_cluster[filtered_df_cluster["ressort_ca"] == selected_ca[0]]

# ========== Note de lecture ==========
st.write(
    "<b><u>Note de lecture :</b></u> L’indice de vieillissement est le rapport de la population des 65 ans et plus sur celle des moins de 20 ans. Plus l’indice est faible, plus le rapport est favorable aux jeunes; plus il est élevé plus il est favorable aux personnes âgées. Par exemple, au sein du ressort de la cour d’appel de",
    data_2040["CA"].iloc[0].title() + ", ",
    "on dénombre ",
    format_float(data_iv["ind_vie"].iloc[0]),
    " seniors de plus de 65 ans pour 100 jeunes de moins de 20 ans. Au niveau national, ce chiffre s’élève à 86.",
    unsafe_allow_html=True,
)
st.markdown(
    ":grey[Source : _Insee, Recensement de la population (RP); exploitation PEP/DSJ_]"
)
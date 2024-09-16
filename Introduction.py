import streamlit as st

st.set_page_config(
    page_title="Tableau de bord du vieillissement démographique",
    # page_icon="👋",
)
st.image('img/logo_minjus.svg', width=100)

st.write("# Tableau de bord du vieillissement démographique")

st.sidebar.success("Sélectionner une thématique ci-dessus.")


st.markdown(
    """
    Le tableau de bord du vieillissement compile des données publiques à l'échelle des ressorts des cours d'appel sur le territoire français.

    **👈 Sélectionnez un thème dans le volet ci-contre** pour les visualiser.
"""
)

st.markdown("")
st.markdown("")
st.markdown("")


st.markdown(
    """
    ### Sources des données utilisées
    - [Ministère de la Justice](https://www.data.gouv.fr/fr/datasets/liste-des-juridictions-competentes-pour-les-communes-de-france/) : Liste des juridictions compétentes pour les communes de France
    - [INSEE/OMPHALE](https://www.insee.fr/fr/information/1303412) : Projections démographiques Omphale
    - [DREES](https://drees.solidarites-sante.gouv.fr/ressources-et-methodes/projection-de-personnes-agees-dependantes-par-lieu-de-vie-le-modele-livia) : Projection de personnes âgées dépendantes par lieu de vie
        - [Modèle Lieux de vie et autonomie (LIVIA)](https://drees.solidarites-sante.gouv.fr/ressources-et-methodes/projection-de-personnes-agees-dependantes-par-lieu-de-vie-le-modele-livia) : ¨Projections du nombre de personnes âgées de plus de 60 ans entre 2015 et 2050 et répartitions par sexe, tranche d’âge, niveau de perte d’autonomie et lieu de vie.
        - [Caisse des dépôts : 60 ans et plus : revenus et aides financières par département](https://opendata.caissedesdepots.fr/explore/dataset/60ans_et_plus_revenu/information/#60-ans-et-plus-population-en-2013-et-en-2050), pré-traitement des données.
    """
)

# st.markdown(
#     """
#     ### Réalisation

#     - Ministère de la Justice
#     - Pôle de l'Evaluation et de la Prospective - Direction des Services Judiciaires
#     """
# )
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
    - INSEE :
        - Projections démographiques Omphale
        - Recensement de la population (RP)
        - Dispositif sur les revenus localisés sociaux et Fiscaux (FILOSOFI)
    - DREES (Direction de la recherche, des études, de l’évaluation et des statistiques)
        - Modèle Lieux de vie et autonomie (LIVIA) : Projections du nombre de personnes âgées de plus de 60 ans entre 2015 et 2050 et répartitions par sexe, tranche d’âge, niveau de perte d’autonomie et lieu de vie.
        - Allocation personnalisée d’autonomie (APA)
        """
)

# st.markdown(
#     """
#     ### Réalisation

#     - Ministère de la Justice
#     - Pôle de l'Evaluation et de la Prospective - Direction des Services Judiciaires
#     """
# )
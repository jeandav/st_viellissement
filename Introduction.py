import streamlit as st

import pages.jd_functions.constants as constants

# -----------------------------------------------------------------------------

st.set_page_config(
    page_title=constants.config_page_title,
    page_icon=constants.config_page_icon,
    layout=constants.config_layout,
)

# -----------------------------------------------------------------------------

st.image(constants.img_logo, width=constants.img_width)

st.write("# Baromètre du vieillissement démographique")

st.sidebar.success("Sélectionner une thématique ci-dessus.")

st.markdown(
    """
    Elaboré par le PEP de la DSJ, il compile les données publiques à l'échelle des ressorts des cours d'appel sur le territoire français.

    **👈 Sélectionnez un thème dans le volet ci-contre** pour les visualiser.
    """
)

for _ in range(0):
    st.markdown("")

st.markdown(
    """
    ### Sources des données utilisées
    - [Ministère de la Justice](https://www.data.gouv.fr/fr/datasets/liste-des-juridictions-competentes-pour-les-communes-de-france/) : Liste des juridictions compétentes pour les communes de France
    - INSEE :
        - Projections démographiques OMPHALE : (Outil méthodologique de projection d'habitants, d'actifs, de logements et d'élèves) 
        - Recensement de la population (RP)
        - Dispositif sur les revenus localisés sociaux et Fiscaux (FILOSOFI)
    - DREES (Direction de la recherche, des études, de l’évaluation et des statistiques)
        - Modèle Lieux de vie et autonomie (LIVIA) : projections du nombre de personnes âgées de plus de 60 ans entre 2015 et 2050 et répartitions par sexe, tranche d’âge, niveau de perte d’autonomie et lieu de vie.
        - Allocation personnalisée d’autonomie (APA)
        """
)

for _ in range(0):
    st.markdown("")

st.markdown(
    """
    ### Glossaire
|  | Définition   |
|----------|-------------|
| APA | Allocation personnalisée d’autonomie   |
| PCH | Prestation de compensation du handicap   |
        """
)
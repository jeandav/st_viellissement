import streamlit as st

st.set_page_config(
    page_title="Tableau de bord du vieillissement démographique",
    # page_icon="👋",
)

st.write("# Tableau de bord du vieillissement démographique")

st.sidebar.success("Sélectionner une thématique ci-dessus.")

st.markdown(
    """
    Le tableau de bord du vieillissement compile des données publiques à l'échelle des ressorts de cour d'appel sur le territoire Français.

    **👈 Sélectionnez un thème dans le volet ci-contre** pour les visualiser.

    ### Source des données utilisées
    - [Ministère de la Justice](https://www.data.gouv.fr/fr/datasets/liste-des-juridictions-competentes-pour-les-communes-de-france/) : Liste des juridictions compétentes pour les communes de France
    - [INSEE/OMPHALE](https://www.insee.fr/fr/information/1303412) : Projections démographiques Omphale
    - [DREES](https://drees.solidarites-sante.gouv.fr/ressources-et-methodes/projection-de-personnes-agees-dependantes-par-lieu-de-vie-le-modele-livia) : Projection de personnes âgées dépendantes par lieu de vie
"""
)

st.markdown(
    """
    ### Réalisation

    - Ministère de la Justice
    - Pôle de l'Evaluation et de la Prospective - Direction des Services Judiciaires
    """
)
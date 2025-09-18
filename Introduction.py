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

st.title("Baromètre du vieillissement démographique", anchor=False)

st.sidebar.success("Sélectionner une thématique ci-dessus.")

st.markdown(
    """
    Elaboré par le PEP de la DSJ, il compile les données publiques à l'échelle des ressorts des cours d'appel sur le territoire français.

    **👈 Sélectionnez une thématique dans le volet ci-contre.**
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
        - Recensement de la population (RP) : Indice de vieillissement
        - Dispositif sur les revenus localisés sociaux et Fiscaux (FILOSOFI)
        - Traitement caisse des dépôts:
            - Population des 60-74 ans et plus isolés
            - Population des 75 ans et plus en appartement avec ou sans ascenseur
    - DREES (Direction de la recherche, des études, de l’évaluation et des statistiques)
        - Modèle Lieux de vie et autonomie (LIVIA) : projections du nombre de personnes âgées de plus de 60 ans entre 2015 et 2050 et répartitions par sexe, tranche d’âge, niveau de perte d’autonomie et lieu de vie.
        - Nombre de bénéficiaires de l'APA (Allocation personnalisée d’autonomie), payés au titre du mois de décembre 2022 à domicile et en établissement.
        - Nombre de bénéficiaires de la PCH (Prestation de compensation du handicap) de 60 ans et plus
        - Nombre de bénéficiaires du minimum vieillesse
        """
)
import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data

def get_cluster_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/df_cluster_complete.csv'
    df = pd.read_csv(DATA_FILENAME, encoding='latin-1', sep=';', decimal=".")


    decimals = 2    
    df['interdecile'] = df['interdecile'].apply(lambda x: round(x, decimals))
    
    return df

def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/traitement_drees/livia_lieux_vie_sc1.csv'
    df = pd.read_csv(DATA_FILENAME, encoding='latin-1', sep=';')

    # df = df[df['genre'] == 'HOMMES']
    # df = df[df['tranche_age'] == '75 ans et plus']
    df = df[df['hyp_evol_dependance'] == 'intermediaire']
    df = df[df['hyp_evol_demo'] == 'central']
    df = df[['ca', 'tranche_age', 'genre', 'annee', 'nb_proj_seniors']]
    df = df.groupby(['ca', 'tranche_age', 'genre', 'annee'])['nb_proj_seniors'].sum()
    df = df.reset_index()

    return df


def get_persagees_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/PERSAGEES/PERSAGEES_TRAITE.csv'
    df = pd.read_csv(DATA_FILENAME, sep=',', encoding='latin-1')

    df = df[['CA','SEXE','TRANCHAGE','ANNEE','value']]
    df = df.groupby(['CA','SEXE','TRANCHAGE','ANNEE']).sum().reset_index()

    df['ANEE'] = pd.to_numeric(df['ANNEE'])

    return df

def get_menage_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/caisse_dep/caisse_dep_menage.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df

def get_popglobale_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/pop_globale_ressort.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=".")

    return df

def get_intens_pauv_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/caisse_dep/caisse_dep_intens_pauv.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=",")

    return df

def get_rev_disp_data():
    DATA_FILENAME = Path(__file__).parent/'../../data/caisse_dep/caisse_dep_rev_disp.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', decimal=",")

    return df
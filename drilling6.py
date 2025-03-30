import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import interp1d
import time
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Analyse de Forages",
    page_icon="⛏️",
    layout="wide"
)

# Suppression du menu hamburger et du footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Initialisation du session state
if 'data' not in st.session_state:
    st.session_state.data = {
        'collars': None,
        'survey': None,
        'lithology': None,
        'assays': None,
        'columns_mapping': {},
        'desurvey_result': None,
        'composite_result': None
    }

# Fonction pour charger et mettre en cache les données
@st.cache_data
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return None

# Création des onglets
tabs = st.tabs(["Chargement", "Aperçu", "Desurvey", "Composites", "Statistiques", "Visualisation 3D"])

# Barre latérale avec progression
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Onglet Chargement
with tabs[0]:
    st.header("Chargement des Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        collars_file = st.file_uploader("Fichier Collars", type=['csv'])
        if collars_file:
            st.session_state.data['collars'] = load_data(collars_file)
            
        survey_file = st.file_uploader("Fichier Survey", type=['csv'])
        if survey_file:
            st.session_state.data['survey'] = load_data(survey_file)
    
    with col2:
        litho_file = st.file_uploader("Fichier Lithology", type=['csv'])
        if litho_file:
            st.session_state.data['lithology'] = load_data(litho_file)
            
        assays_file = st.file_uploader("Fichier Assays", type=['csv'])
        if assays_file:
            st.session_state.data['assays'] = load_data(assays_file)

    # Configuration des colonnes
    if st.session_state.data['collars'] is not None:
        st.subheader("Configuration des colonnes")
        cols = st.columns(4)
        with cols[0]:
            st.session_state.data['columns_mapping']['hole_id'] = st.selectbox(
                "HOLE_ID", st.session_state.data['collars'].columns)
        with cols[1]:
            st.session_state.data['columns_mapping']['east'] = st.selectbox(
                "EAST", st.session_state.data['collars'].columns)
        with cols[2]:
            st.session_state.data['columns_mapping']['north'] = st.selectbox(
                "NORTH", st.session_state.data['collars'].columns)
        with cols[3]:
            st.session_state.data['columns_mapping']['elevation'] = st.selectbox(
                "ELEVATION", st.session_state.data['collars'].columns)

# Les autres onglets restent identiques...

# Ajout d'un bouton de téléchargement pour chaque résultat
def download_button(data, name):
    if data is not None:
        csv = data.to_csv(index=False)
        st.download_button(
            label=f"Télécharger {name}",
            data=csv,
            file_name=f"{name}.csv",
            mime='text/csv'
        )

# Simulation de chargement
for i in range(100):
    status_text.text(f"Chargement: {i+1}%")
    progress_bar.progress(i + 1)
    time.sleep(0.01)

progress_bar.empty()
status_text.empty()

# Bouton de rafraîchissement dans la barre latérale
if st.sidebar.button("Rafraîchir"):
    st.experimental_rerun()
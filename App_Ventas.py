import streamlit as st
import sys
from pathlib import Path

# Configurar path para imports relativos
sys.path.insert(0, str(Path(__file__).parent))

# Configuración de Página Global (Debe ser lo primero)
st.set_page_config(
    page_title="Viajes Cusco Perú - Constructor de Itinerarios",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar Estilos Globales
def load_css():
    css_path = Path("assets/css/app_style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Importar y renderizar el módulo de ventas
from modules.ventas.ui import render_ventas_ui

render_ventas_ui()

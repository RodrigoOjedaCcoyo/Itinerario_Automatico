import streamlit as st
import sys
from pathlib import Path

# Configurar path para imports relativos si es necesario
sys.path.append(str(Path(__file__).parent))

# Configuración de Página Global (Debe ser lo primero)
st.set_page_config(
    page_title="Viajes Cusco Perú - Sistema Integral",
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

# Importar Módulos
from modules.ventas.ui import render_ventas_ui

# --- NAVIGATOR ---
# En un futuro, aquí se añade el Sidebar de Navegación entre Ventas | Operaciones | Contabilidad
# Por ahora, renderizamos Ventas directamente como módulo principal

def main():
    render_ventas_ui()

if __name__ == "__main__":
    main()

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

# --- SEGURIDAD ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    from modules.auth.ui import render_login_ui
    render_login_ui()
else:
    # Sidebar de Usuario Autenticado
    with st.sidebar:
        user_email = st.session_state.get("user_email", "desconocido")
        user_rol = st.session_state.get("user_rol", "VENTAS")
        st.write(f"👤 **Usuario:** {user_email}")
        st.write(f"🛡️ **Rol:** {user_rol}")
        if st.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.rerun()
        st.divider()
        st.caption("v2.3 - Estabilidad Reforzada 🟢")

    # Importar y renderizar el módulo de ventas
    from modules.ventas.ui import render_ventas_ui
    render_ventas_ui()

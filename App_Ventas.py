import streamlit as st
import sys
import datetime
from pathlib import Path
import extra_streamlit_components as nsc

# Configurar path para imports relativos
sys.path.insert(0, str(Path(__file__).parent))

# Configuración de Página Global (Debe ser lo primero)
st.set_page_config(
    page_title="Constructor de Itinerarios",
    page_icon="assets/images/logo_background.ico",
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

# --- GESTIÓN DE COOKIES (PERSISTENCIA 24H) ---
def get_manager():
    return nsc.CookieManager()

cookie_manager = get_manager()

# --- SEGURIDAD ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Intentar auto-login si no está autenticado
if not st.session_state.authenticated:
    existing_cookie = cookie_manager.get(cookie="latitud_session_token")
    if existing_cookie:
        # Recuperar datos del token (es un dict guardado en la cookie)
        try:
            st.session_state.authenticated = True
            st.session_state.user_email = existing_cookie.get("email")
            st.session_state.user_rol = existing_cookie.get("rol")
            st.session_state.vendedor_name = existing_cookie.get("nombre")
        except:
            pass

if not st.session_state.authenticated:
    from modules.auth.ui import render_login_ui
    render_login_ui(cookie_manager=cookie_manager)
else:
    # Sidebar de Usuario Autenticado
    with st.sidebar:
        user_email = st.session_state.get("user_email", "desconocido")
        user_rol = st.session_state.get("user_rol", "VENTAS")
        st.write(f"👤 **Usuario:** {user_email}")
        st.write(f"🛡️ **Rol:** {user_rol}")
        if st.button("Cerrar Sesión"):
            cookie_manager.delete("latitud_session_token")
            st.session_state.authenticated = False
            st.rerun()
        st.divider()
        
        # Módulos Disponibles según Rol
        active_tab = "Itinerarios"
        if user_rol in ["GERENCIA", "OPERACIONES"]:
            st.markdown("### ⚙️ Administración")
            active_tab = st.radio("Selector de Módulo:", ["Itinerarios", "Catálogo Maestro"], index=0, help="Elige la herramienta a usar.")
            st.divider()
            
        st.caption("v2.5 - Catálogo Integrado 🚀")

    # Renderizar el módulo seleccionado
    if active_tab == "Catálogo Maestro":
        from modules.admin.ui_precios import render_admin_precios_ui
        render_admin_precios_ui()
    else:
        # Importar y renderizar el módulo de ventas
        from modules.ventas.ui import render_ventas_ui
        render_ventas_ui()

import streamlit as st
import sys
import datetime
import base64
from pathlib import Path
import extra_streamlit_components as nsc

# Configurar path para imports relativos
sys.path.insert(0, str(Path(__file__).parent))

# Helper para cargar imágenes en Base64 en Streamlit
def get_base64_image(img_path):
    p = Path(img_path)
    if not p.exists():
        return ""
    try:
        with open(p, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        ext = p.suffix[1:].lower()
        mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
        return f"data:{mime};base64,{encoded_string}"
    except Exception as e:
        return ""

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
        
        # Módulos Disponibles para Todos
        st.markdown("### ⚙️ Administración")
        active_tab = st.radio("Selector de Módulo:", ["Itinerarios", "Catálogo Maestro"], index=0, help="Elige la herramienta a usar.")
        st.divider()
            
        st.caption("v2.5 - Catálogo Integrado 🚀")
        
        # Redes Sociales en Sidebar
        st.divider()
        st.markdown("### 📱 Síguenos en Redes")
        
        fb_b64 = get_base64_image("assets/Logo de Redes Sociales/Logo de Facebook.png")
        ig_b64 = get_base64_image("assets/Logo de Redes Sociales/Logo de Instagram.webp")
        tt_b64 = get_base64_image("assets/Logo de Redes Sociales/Logo de Tik Tok.webp")
        yt_b64 = get_base64_image("assets/Logo de Redes Sociales/Logo de Youtube.webp")
        ta_b64 = get_base64_image("assets/Logo de Redes Sociales/Logo de Tripadvisor.png")
        
        html_social = f"""
        <div style="display: flex; gap: 12px; justify-content: center; align-items: center; padding: 10px 0;">
            <a href="https://www.facebook.com/ViajesCuscoPeruSalkantay" target="_blank" title="Facebook">
                <img src="{fb_b64}" width="30" height="30" style="border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />
            </a>
            <a href="https://www.instagram.com/viajescuscoperu" target="_blank" title="Instagram">
                <img src="{ig_b64}" width="30" height="30" style="border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />
            </a>
            <a href="https://www.tiktok.com/@viajescuscoperu1" target="_blank" title="TikTok">
                <img src="{tt_b64}" width="30" height="30" style="border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />
            </a>
            <a href="https://www.youtube.com/@viajescuscoperu" target="_blank" title="YouTube">
                <img src="{yt_b64}" width="30" height="30" style="border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />
            </a>
            <a href="https://www.tripadvisor.com.pe/Attraction_Review-g294314-d7777014-Reviews-Viajes_Cusco_Peru-Cusco_Cusco_Region.html" target="_blank" title="TripAdvisor">
                <img src="{ta_b64}" width="30" height="30" style="border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />
            </a>
        </div>
        """
        st.markdown(html_social, unsafe_allow_html=True)

    # Renderizar el módulo seleccionado
    if active_tab == "Catálogo Maestro":
        from modules.admin.ui_precios import render_admin_precios_ui
        render_admin_precios_ui()
    else:
        # Importar y renderizar el módulo de ventas
        from modules.ventas.ui import render_ventas_ui
        render_ventas_ui()

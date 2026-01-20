import streamlit as st
from utils.supabase_db import verify_user

def render_login_ui():
    """Renderiza una interfaz de inicio de sesión elegante."""
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='font-size: 3rem;'>🏔️</h1>
            <h2 style='color: #2d3436;'>Viajes Cusco Perú</h2>
            <p style='color: #636e72;'>Sistema Interno de Itinerarios</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input("Correo Electrónico Autorizado", placeholder="tu_correo@agencia.com")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Ingresar al Portal", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("Por favor, ingresa tu correo y contraseña.")
                else:
                    user_data = verify_user(email.strip().lower(), password)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_rol = user_data.get("rol", "VENTAS")
                        st.success(f"¡Bienvenido, acceso concedido como {st.session_state.user_rol}!")
                        st.rerun()
                    else:
                        st.error("Acceso denegado. Este correo no está en la lista blanca.")
                        st.info("Contacta al administrador para que añada tu correo a la tabla `usuarios_app`.")

    st.markdown("---")
    st.caption("Protegido por Supabase Auth & RLS")

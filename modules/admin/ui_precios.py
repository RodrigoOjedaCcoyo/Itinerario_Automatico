import streamlit as st
from utils.supabase_db import get_available_tours, update_tour_prices, create_new_tour

def render_admin_precios_ui():
    st.markdown("## ⚙️ Configuración Maestra de Catálogo")
    st.markdown("Gestiona los precios base de los tours. **Los cambios afectarán a todas las nuevas cotizaciones.**")
    st.divider()

    # Obtener tours
    with st.spinner("Cargando catálogo..."):
        tours_db = get_available_tours()

    tab1, tab2 = st.tabs(["✏️ Editar Precios Actuales", "➕ Crear Nuevo Tour"])

    with tab1:
        if not tours_db:
            st.warning("No hay tours disponibles o hubo un error al cargar el catálogo.")
            return

        st.markdown("### 🏷️ Lista de Tours Básico")

    # Controles de filtrado visual (opcional)
    search = st.text_input("🔍 Buscar Tour", "").lower()

    for idx, t in enumerate(tours_db):
        if search and search not in t['titulo'].lower():
            continue

        id_tour = t.get('id_tour')
        if not id_tour:
            continue # Saltar si no tiene ID

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
            
            with col1:
                st.markdown(f"**{t['titulo']}**")
                # Se podría poner última actualización aquí si tuvieramos el campo
            
            with col2:
                # Precio Nacional
                key_nac = f"nac_{id_tour}_{idx}"
                if key_nac not in st.session_state:
                    st.session_state[key_nac] = t.get('costo_nacional', 0.0)
                val_nac = st.number_input("Precio Nacional (S/)", value=float(st.session_state[key_nac]), step=1.0, key=f"in_{key_nac}")

            with col3:
                # Precio Extranjero
                key_ext = f"ext_{id_tour}_{idx}"
                if key_ext not in st.session_state:
                    st.session_state[key_ext] = t.get('costo_extranjero', 0.0)
                val_ext = st.number_input("Precio Extranjero (USD)", value=float(st.session_state[key_ext]), step=1.0, key=f"in_{key_ext}")

            with col4:
                # Precio CAN
                key_can = f"can_{id_tour}_{idx}"
                if key_can not in st.session_state:
                    st.session_state[key_can] = t.get('costo_can', 0.0)
                val_can = st.number_input("Precio CAN (USD)", value=float(st.session_state[key_can]), step=1.0, key=f"in_{key_can}")

            with col5:
                st.write("") # Espaciador
                if st.button("💾 Guardar", key=f"btn_save_{id_tour}_{idx}", use_container_width=True):
                    with st.spinner("Guardando..."):
                        success, msg = update_tour_prices(id_tour, val_nac, val_ext, val_can)
                        if success:
                            st.toast(f"✅ {t['titulo']} actualizado.", icon="🚀")
                            st.session_state[key_nac] = val_nac
                            st.session_state[key_ext] = val_ext
                            st.session_state[key_can] = val_can
                        else:
                            st.error(f"Error al guardar: {msg}")
            
            st.divider()

    with tab2:
        st.markdown("### 🆕 Ingresar un Tour a la Base de Datos")
        st.info("Al crear un tour, este estará inmediatamente disponible para los vendedores.")
        
        with st.form("form_crear_tour", clear_on_submit=True):
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                f_nombre = st.text_input("Nombre del Tour *", placeholder="Ej: City Tour Gastronómico")
                f_desc = st.text_area("Descripción Principal", placeholder="Escribe un resumen del tour...")
            with col_t2:
                f_dias = st.number_input("Días", min_value=1, value=1, step=1)
                f_horas = st.number_input("Horas (Opcional)", min_value=0, value=0, step=1)
            
            st.markdown("**Precios Base (Adultos)**")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                f_p_nac = st.number_input("Precio Perú (S/) *", min_value=0.0, value=0.0, step=1.0)
            with col_p2:
                f_p_ext = st.number_input("Precio Extranjero (USD) *", min_value=0.0, value=0.0, step=1.0)
            with col_p3:
                f_p_can = st.number_input("Precio Comunidad Andina (USD)", min_value=0.0, value=0.0, step=1.0)
            
            st.markdown("**Detalles (Separados por comas)**")
            f_high = st.text_input("Lugares a visitar", placeholder="Ej: Plaza Mayor, Catacumbas, Museo de Osma")
            f_inc = st.text_input("Qué incluye", placeholder="Ej: Transporte, Guía español, Tickets")
            f_no_inc = st.text_input("Qué NO incluye", placeholder="Ej: Alimentación, Propinas")
            
            submit_btn = st.form_submit_button("Guardar en Base de Datos", type="primary", use_container_width=True)

            if submit_btn:
                if not f_nombre or (f_p_nac == 0 and f_p_ext == 0):
                    st.error("❌ El nombre y al menos un precio base son obligatorios.")
                else:
                    success, msg = create_new_tour(
                        nombre=f_nombre, descripcion=f_desc, highlights_text=f_high,
                        precio_nac=f_p_nac, precio_ext=f_p_ext, precio_can=f_p_can,
                        incluye_text=f_inc, no_incluye_text=f_no_inc,
                        duracion_dias=f_dias, duracion_horas=f_horas
                    )
                    if success:
                        st.success(f"✅ Tour '{f_nombre}' enlazado a la matriz de precios.", icon="✨")
                    else:
                        st.error(f"Fallo en inserción: {msg}")

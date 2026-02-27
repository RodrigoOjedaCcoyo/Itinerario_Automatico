import streamlit as st
from utils.supabase_db import get_available_tours, update_tour_master, create_new_tour, create_master_package

def render_admin_precios_ui():
    st.markdown("## ⚙️ Configuración Maestra de Catálogo")
    st.markdown("Gestiona los tours y paquetes. **Los cambios afectarán a todas las nuevas cotizaciones.**")
    st.divider()

    # Obtener tours
    with st.spinner("Cargando catálogo..."):
        tours_db = get_available_tours()

    tab1, tab2, tab3 = st.tabs(["✏️ Editar Catálogo Existente", "➕ Crear Nuevo Tour", "📦 Crear Nuevo Paquete"])

    with tab1:
        if not tours_db:
            st.warning("No hay tours disponibles o hubo un error al cargar el catálogo.")
        else:
            st.markdown("### 🏷️ Gestión de Tours")
            search = st.text_input("🔍 Buscar por nombre", "").lower()

            for idx, t in enumerate(tours_db):
                if search and search not in t['titulo'].lower():
                    continue

                id_tour = t.get('id_tour')
                if not id_tour: continue

                with st.expander(f"📦 {t['titulo']}"):
                    with st.form(f"form_edit_{id_tour}_{idx}"):
                        col_e1, col_e2 = st.columns([2, 1])
                        with col_e1:
                            new_nombre = st.text_input("Nombre del Tour", value=t['titulo'])
                            new_desc = st.text_area("Descripción", value=t.get('descripcion', ""), height=150)
                        with col_e2:
                            st.markdown("**Precios Base**")
                            new_p_nac = st.number_input("Nacional (S/)", value=float(t.get('costo_nacional', 0.0)), step=1.0)
                            new_p_ext = st.number_input("Extranjero (USD)", value=float(t.get('costo_extranjero', 0.0)), step=1.0)
                            new_p_can = st.number_input("CAN (USD)", value=float(t.get('costo_can', 0.0)), step=1.0)

                        st.markdown("**Detalles Detallados (Separados por comas)**")
                        # Pre-procesar listas para el input de texto
                        high_str = ", ".join(t.get('highlights', [])) if isinstance(t.get('highlights'), list) else ""
                        inc_str = ", ".join(t.get('servicios', [])) if isinstance(t.get('servicios'), list) else ""
                        no_inc_str = ", ".join(t.get('servicios_no_incluye', [])) if isinstance(t.get('servicios_no_incluye'), list) else ""

                        new_high = st.text_input("Highlights / Lugares", value=high_str)
                        new_inc = st.text_input("Incluye", value=inc_str)
                        new_no_inc = st.text_input("No Incluye", value=no_inc_str)

                        if st.form_submit_button("💾 Guardar Cambios Totales", type="primary", use_container_width=True):
                            # Estructurar data para update_tour_master
                            # Convertir strings de vuelta a JSONB para mantener compatibilidad con el ecosistema
                            update_data = {
                                "nombre": new_nombre,
                                "descripcion": new_desc,
                                "precio_adulto_nacional": new_p_nac,
                                "precio_adulto_extranjero": new_p_ext,
                                "precio_adulto_can": new_p_can,
                                "highlights": {"itinerario": new_desc, "lugares": [h.strip() for h in new_high.split(",") if h.strip()]},
                                "servicios_incluidos": {"incluye": [i.strip() for i in new_inc.split(",") if i.strip()]},
                                "servicios_no_incluidos": {"no_incluye": [n.strip() for n in new_no_inc.split(",") if n.strip()]}
                            }
                            
                            with st.spinner("Actualizando base de datos..."):
                                success, msg = update_tour_master(id_tour, update_data)
                                if success:
                                    st.success(f"✅ '{new_nombre}' actualizado correctamente.")
                                    # Opcional: st.rerun() para refrescar la lista
                                else:
                                    st.error(f"Error: {msg}")

    with tab2:
        st.markdown("### 🆕 Ingresar un Tour a la Base de Datos")
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
                        st.success(f"✅ Tour '{f_nombre}' guardado exitosamente.")
                    else:
                        st.error(f"Fallo en inserción: {msg}")

    with tab3:
        st.markdown("### 📦 Armar Nuevo Paquete Maestro")
        st.info("Un paquete es un conjunto de tours ordenados por días. Los vendedores podrán cargarlo de un solo clic.")
        
        with st.form("form_crear_paquete", clear_on_submit=True):
            col_p1, col_p2 = st.columns([2, 1])
            with col_p1:
                p_nombre = st.text_input("Nombre del Paquete *", placeholder="Ej: Cusco Mágico Tradicional")
                p_desc = st.text_area("Descripción General (Opcional)", placeholder="Resumen para el itinerario...")
            with col_p2:
                p_dias = st.number_input("Total Días", min_value=1, value=3, step=1)
                p_noches = st.number_input("Total Noches", min_value=0, value=2, step=1)
            
            col_p3, col_p4 = st.columns(2)
            with col_p3:
                p_destino = st.text_input("Destino Principal", placeholder="Ej: Cusco")
            with col_p4:
                p_temporada = st.text_input("Temporada sugerida", placeholder="Ej: Todo el año")

            st.markdown("---")
            st.markdown("**Selección de Tours para el Itinerario**")
            
            # Selector de múltiples tours del catálogo
            st.write("Elige los tours que componen este paquete:")
            opciones_tours = {t['titulo']: t['id_tour'] for t in tours_db}
            seleccionados = st.multiselect("Seleccionar Tours *", options=list(opciones_tours.keys()))
            
            tours_vinculados = []
            if seleccionados:
                st.write("Asigna el Día y el Orden para cada tour:")
                for i, nombre_t in enumerate(seleccionados):
                    id_t = opciones_tours[nombre_t]
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1: st.write(f"🔹 {nombre_t}")
                    with c2: v_dia = st.number_input(f"Día", min_value=1, max_value=p_dias, value=1, key=f"d_{id_t}_{i}")
                    with c3: v_ord = st.number_input(f"Orden", min_value=1, value=i+1, key=f"o_{id_t}_{i}")
                    tours_vinculados.append({"id_tour": id_t, "dia": v_dia, "orden": v_ord})

            st.divider()
            submit_pkg = st.form_submit_button("🔨 Crear Paquete Maestro", type="primary", use_container_width=True)

            if submit_pkg:
                if not p_nombre or not tours_vinculados:
                    st.error("❌ El nombre y al menos un tour son obligatorios.")
                else:
                    with st.spinner("Creando paquete y vinculando tours..."):
                        success, msg = create_master_package(
                            nombre=p_nombre, descripcion=p_desc,
                            dias=p_dias, noches=p_noches,
                            tours_vinculados=tours_vinculados,
                            destino=p_destino, temporada=p_temporada
                        )
                        if success:
                            st.success(f"✅ Paquete '{p_nombre}' disponible en el catálogo maestro.")
                        else:
                            st.error(f"Error: {msg}")

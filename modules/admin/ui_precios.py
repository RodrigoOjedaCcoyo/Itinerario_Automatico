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
                            st.markdown("**💰 Precios Base (Adulto)**")
                            new_p_nac = st.number_input("Nacional (S/)", value=float(t.get('costo_nacional', 0.0)), step=1.0, key=f"ed_nac_{id_tour}")
                            new_p_ext = st.number_input("Extranjero (USD)", value=float(t.get('costo_extranjero', 0.0)), step=1.0, key=f"ed_ext_{id_tour}")
                            new_p_can = st.number_input("CAN (USD)", value=float(t.get('costo_can', 0.0)), step=1.0, key=f"ed_can_{id_tour}")

                        with st.expander("⭐ Configuración de Precios Avanzada (Niños, Estudiantes, PCD)"):
                            st.caption("Si dejas estos campos en 0, se usarán los descuentos automáticos del sistema.")
                            c_adv1, c_adv2, c_adv3 = st.columns(3)
                            with c_adv1:
                                st.markdown("**Niños**")
                                n_nino_nac = st.number_input("Niño Nac (S/)", value=float(t.get('costo_nac_nino', 0.0)), key=f"ed_nnn_{id_tour}")
                                n_nino_ext = st.number_input("Niño Ext (USD)", value=float(t.get('costo_ext_nino', 0.0)), key=f"ed_nne_{id_tour}")
                                n_nino_can = st.number_input("Niño CAN (USD)", value=float(t.get('costo_can_nino', 0.0)), key=f"ed_nnc_{id_tour}")
                            with c_adv2:
                                st.markdown("**Estudiantes**")
                                n_est_nac = st.number_input("Est Nac (S/)", value=float(t.get('costo_nac_est', 0.0)), key=f"ed_nen_{id_tour}")
                                n_est_ext = st.number_input("Est Ext (USD)", value=float(t.get('costo_ext_est', 0.0)), key=f"ed_nee_{id_tour}")
                                n_est_can = st.number_input("Est CAN (USD)", value=float(t.get('costo_can_est', 0.0)), key=f"ed_nec_{id_tour}")
                            with c_adv3:
                                st.markdown("**Invalidez (PCD)**")
                                # Nota: En el cargado actual de tours, no extraemos estos campos, así que usamos 0 por defecto
                                n_pcd_nac = st.number_input("PCD Nac (S/)", value=0.0, key=f"ed_npn_{id_tour}")
                                n_pcd_ext = st.number_input("PCD Ext (USD)", value=0.0, key=f"ed_npe_{id_tour}")
                                n_pcd_can = st.number_input("PCD CAN (USD)", value=0.0, key=f"ed_npc_{id_tour}")

                        st.markdown("**📝 Detalles del Itinerario (Separados por comas)**")
                        # Pre-procesar listas para el input de texto
                        high_str = ", ".join(t.get('highlights', [])) if isinstance(t.get('highlights'), list) else ""
                        inc_str = ", ".join(t.get('servicios', [])) if isinstance(t.get('servicios'), list) else ""
                        no_inc_str = ", ".join(t.get('servicios_no_incluye', [])) if isinstance(t.get('servicios_no_incluye'), list) else ""

                        new_high = st.text_input("Highlights / Atractivos", value=high_str, key=f"ed_high_{id_tour}")
                        new_inc = st.text_input("Incluye", value=inc_str, key=f"ed_inc_{id_tour}")
                        new_no_inc = st.text_input("No Incluye", value=no_inc_str, key=f"ed_noinc_{id_tour}")

                        if st.form_submit_button("💾 Guardar Cambios Totales", type="primary", use_container_width=True):
                            # Estructurar data para update_tour_master
                            # Convertir strings de vuelta a JSONB para mantener compatibilidad con el ecosistema
                            update_data = {
                                "nombre": new_nombre,
                                "descripcion": new_desc,
                                "precio_adulto_nacional": new_p_nac,
                                "precio_adulto_extranjero": new_p_ext,
                                "precio_adulto_can": new_p_can,
                                # Precios avanzados
                                "precio_nino_nacional": n_nino_nac,
                                "precio_nino_extranjero": n_nino_ext,
                                "precio_nino_can": n_nino_can,
                                "precio_estudiante_nacional": n_est_nac,
                                "precio_estudiante_extranjero": n_est_ext,
                                "precio_estudiante_can": n_est_can,
                                "precio_pcd_nacional": n_pcd_nac,
                                "precio_pcd_extranjero": n_pcd_ext,
                                "precio_pcd_can": n_pcd_can,
                                # JSONs
                                "highlights": {"itinerario": new_desc, "lugares": [h.strip() for h in new_high.split(",") if h.strip()]},
                                "servicios_incluidos": {"incluye": [i.strip() for i in new_inc.split(",") if i.strip()]},
                                "servicios_no_incluidos": {"no_incluye": [n.strip() for n in new_no_inc.split(",") if n.strip()]}
                            }
                            
                            with st.spinner("Actualizando base de datos..."):
                                success, msg = update_tour_master(id_tour, update_data)
                                if success:
                                    st.success(f"✅ '{new_nombre}' actualizado correctamente.")
                                    st.rerun()
                                else:
                                    st.error(f"Error: {msg}")

    with tab2:
        st.markdown("### ➕ Ingresar Nuevo Tour al Catálogo")
        with st.form("form_crear_tour", clear_on_submit=True):
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                f_nombre = st.text_input("Nombre del Tour *", placeholder="Ej: Full Day Paracas e Ica")
                f_desc = st.text_area("Descripción Principal", placeholder="Escribe el itinerario o resumen...")
            with col_t2:
                f_dias = st.number_input("Días", min_value=1, value=1, step=1)
                f_horas = st.number_input("Horas", min_value=0, value=0, step=1)
            
            st.markdown("**💰 Precios Base (Adultos)**")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                f_p_nac = st.number_input("Precio Perú (S/) *", min_value=0.0, value=0.0, step=1.0)
            with col_p2:
                f_p_ext = st.number_input("Precio Extranjero (USD) *", min_value=0.0, value=0.0, step=1.0)
            with col_p3:
                f_p_can = st.number_input("Precio Comunidad Andina (USD)", min_value=0.0, value=0.0, step=1.0)

            with st.expander("⭐ Configuración de Precios Avanzada (Niños, Estudiantes, PCD)"):
                st.caption("Opcional: Si los dejas en 0, el sistema calculará los descuentos automáticamente.")
                coa1, coa2, coa3 = st.columns(3)
                with coa1:
                    st.markdown("**Niños**")
                    f_nnn = st.number_input("Niño Nac (S/)", min_value=0.0, value=0.0)
                    f_nne = st.number_input("Niño Ext (USD)", min_value=0.0, value=0.0)
                    f_nnc = st.number_input("Niño CAN (USD)", min_value=0.0, value=0.0)
                with coa2:
                    st.markdown("**Estudiantes**")
                    f_nen = st.number_input("Est Nac (S/)", min_value=0.0, value=0.0)
                    f_nee = st.number_input("Est Ext (USD)", min_value=0.0, value=0.0)
                    f_nec = st.number_input("Est CAN (USD)", min_value=0.0, value=0.0)
                with coa3:
                    st.markdown("**Invalidez (PCD)**")
                    f_npn = st.number_input("PCD Nac (S/)", min_value=0.0, value=0.0)
                    f_npe = st.number_input("PCD Ext (USD)", min_value=0.0, value=0.0)
                    f_npc = st.number_input("PCD CAN (USD)", min_value=0.0, value=0.0)
            
            st.markdown("**📝 Detalles (Separados por comas)**")
            f_high = st.text_input("Highlights / Atractivos", placeholder="Ej: Islas Ballestas, Huacachina, Bodegas")
            f_inc = st.text_input("Qué incluye", placeholder="Ej: Movilidad, Guía, Almuerzo")
            f_no_inc = st.text_input("Qué NO incluye", placeholder="Ej: Tasa Sernanp, Vuelos")
            
            submit_btn = st.form_submit_button("🔨 Crear Tour Oficial", type="primary", use_container_width=True)

            if submit_btn:
                if not f_nombre or (f_p_nac == 0 and f_p_ext == 0):
                    st.error("❌ El nombre y al menos un precio de adulto son obligatorios.")
                else:
                    success, msg = create_new_tour(
                        nombre=f_nombre, descripcion=f_desc, highlights_text=f_high,
                        precio_nac=f_p_nac, precio_ext=f_p_ext, precio_can=f_p_can,
                        incluye_text=f_inc, no_incluye_text=f_no_inc,
                        duracion_dias=f_dias, duracion_horas=f_horas,
                        # Valores avanzados (pasamos None si son 0 para que use el default)
                        precio_nino_nac=f_nnn if f_nnn > 0 else None,
                        precio_nino_ext=f_nne if f_nne > 0 else None,
                        precio_nino_can=f_nnc if f_nnc > 0 else None,
                        precio_est_nac=f_nen if f_nen > 0 else None,
                        precio_est_ext=f_nee if f_nee > 0 else None,
                        precio_est_can=f_nec if f_nec > 0 else None,
                        precio_pcd_nac=f_npn, precio_pcd_ext=f_npe, precio_pcd_can=f_npc
                    )
                    if success:
                        st.success(f"✅ Tour '{f_nombre}' guardado exitosamente.")
                        st.rerun()
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

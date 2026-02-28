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
                            
                            # Validación de palabras en descripción
                            current_desc = t.get('description', t.get('descripcion', ""))
                            word_count = len(current_desc.split())
                            desc_label = f"Descripción (Itinerario) - {word_count}/100 palabras"
                            
                            new_desc = st.text_area(desc_label, value=current_desc, height=150)
                            
                            new_word_count = len(new_desc.split())
                            if new_word_count > 100:
                                st.error(f"⚠️ ¡Atención! La descripción tiene {new_word_count} palabras. El límite para el PDF es de 100.")
                        with col_e2:
                            st.markdown("**💰 Precios Base (Adulto)**")
                            new_p_nac = st.number_input("Nacional (S/)", value=float(t.get('costo_nacional', 0.0)), step=1.0, key=f"ed_nac_{id_tour}")
                            new_p_ext = st.number_input("Extranjero (USD)", value=float(t.get('costo_extranjero', 0.0)), step=1.0, key=f"ed_ext_{id_tour}")
                            new_p_can = st.number_input("CAN (USD)", value=float(t.get('costo_can', 0.0)), step=1.0, key=f"ed_can_{id_tour}")

                        # --- DETALLES AVANZADOS ---
                        c_adv_main1, c_adv_main2 = st.columns(2)
                        with c_adv_main1:
                            with st.expander("⭐ Precios Niños, Estudiantes, PCD"):
                                st.caption("Configuración manual por categoría:")
                                c_adv1, c_adv2, c_adv3 = st.columns(3)
                                with c_adv1:
                                    st.markdown("**Niños**")
                                    n_nino_nac = st.number_input("Nac (S/)", value=float(t.get('costo_nac_nino', 0.0)), key=f"ed_nnn_{id_tour}")
                                    n_nino_ext = st.number_input("Ext (USD)", value=float(t.get('costo_ext_nino', 0.0)), key=f"ed_nne_{id_tour}")
                                    n_nino_can = st.number_input("CAN (USD)", value=float(t.get('costo_can_nino', 0.0)), key=f"ed_nnc_{id_tour}")
                                with c_adv2:
                                    st.markdown("**Estudiantes**")
                                    n_est_nac = st.number_input("Nac (S/)", value=float(t.get('costo_nac_est', 0.0)), key=f"ed_nen_{id_tour}")
                                    n_est_ext = st.number_input("Ext (USD)", value=float(t.get('costo_ext_est', 0.0)), key=f"ed_nee_{id_tour}")
                                    n_est_can = st.number_input("CAN (USD)", value=float(t.get('costo_can_est', 0.0)), key=f"ed_nec_{id_tour}")
                                with c_adv3:
                                    st.markdown("**PCD**")
                                    n_pcd_nac = st.number_input("Nac (S/)", value=float(t.get('costo_nac_pcd', 0.0)), key=f"ed_npn_{id_tour}")
                                    n_pcd_ext = st.number_input("Ext (USD)", value=float(t.get('costo_ext_pcd', 0.0)), key=f"ed_npe_{id_tour}")
                                    n_pcd_can = st.number_input("CAN (USD)", value=float(t.get('costo_can_pcd', 0.0)), key=f"ed_npc_{id_tour}")
                        
                        with c_adv_main2:
                            with st.expander("🛠️ Configuración Técnica"):
                                st.caption("Metadatos y duración:")
                                c_tech1, c_tech2 = st.columns(2)
                                with c_tech1:
                                    n_dias = st.number_input("Días", min_value=1, value=int(t.get('duracion_dias', 1)), key=f"ed_dias_{id_tour}")
                                    n_horas = st.number_input("Horas", min_value=0, value=int(t.get('duracion_horas', 0)), key=f"ed_hr_{id_tour}")
                                with c_tech2:
                                    n_dificultad = st.selectbox("Dificultad", options=["FACIL", "MODERADO", "DIFICIL", "EXTREMO"], index=["FACIL", "MODERADO", "DIFICIL", "EXTREMO"].index(t.get('dificultad', 'FACIL')), key=f"ed_dif_{id_tour}")
                                    n_categoria = st.text_input("Categoría", value=t.get('categoria', 'General'), key=f"ed_cat_{id_tour}")
                                
                                n_img = st.text_input("Carpeta Imágenes", value=t.get('carpeta_img', 'general'), key=f"ed_img_{id_tour}")
                                n_hora = st.text_input("Hora Inicio (HH:MM)", value=t.get('hora_inicio', '08:00:00')[:8], key=f"ed_hora_{id_tour}")

                        st.markdown("**📝 Textos del Itinerario**")
                        # Pre-procesar listas para el input de texto
                        raw_h = t.get('highlights', [])
                        # Si es el nuevo formato dict {"itinerario":..., "lugares":...}
                        if isinstance(raw_h, dict):
                            high_list = raw_h.get('lugares', raw_h.get('highlights', raw_h.get('itinerario_lista', [])))
                        else:
                            high_list = raw_h if isinstance(raw_h, list) else []
                            
                        high_str = ", ".join(high_list) if isinstance(high_list, list) else ""
                        
                        raw_i = t.get('servicios', []) # Clave en el dict devuelto por get_available_tours
                        inc_str = ", ".join(raw_i) if isinstance(raw_i, list) else ""
                        
                        raw_ni = t.get('servicios_no_incluye', [])
                        no_inc_str = ", ".join(raw_ni) if isinstance(raw_ni, list) else ""

                        new_high = st.text_input("Highlights / Atractivos", value=high_str, key=f"ed_high_{id_tour}")
                        new_inc = st.text_input("Incluye", value=inc_str, key=f"ed_inc_{id_tour}")
                        new_no_inc = st.text_input("No Incluye", value=no_inc_str, key=f"ed_noinc_{id_tour}")

                        if st.form_submit_button("💾 Guardar Cambios Totales", type="primary", use_container_width=True):
                            update_data = {
                                "nombre": new_nombre,
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
                                "duracion_dias": n_dias,
                                "duracion_horas": n_horas,
                                "dificultad": n_dificultad,
                                "categoria": n_categoria,
                                "carpeta_img": n_img,
                                "hora_inicio": n_hora.split()[0] if " " in n_hora else n_hora, # Quitar AM/PM si existe
                                "highlights": {"itinerario": new_desc, "lugares": [h.strip() for h in new_high.split(",") if h.strip()]},
                                "servicios_incluidos": {"incluye": [i.strip() for i in new_inc.split(",") if i.strip()]},
                                "servicios_no_incluidos": {"no_incluye": [n.strip() for n in new_no_inc.split(",") if n.strip()]}
                            }
                            
                            with st.spinner("Actualizando base de datos..."):
                                if len(new_desc.split()) > 100:
                                    st.error("❌ No se puede guardar: La descripción excede las 100 palabras.")
                                else:
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
                f_desc = st.text_area("Descripción Principal (Máx 100 palabras) *", placeholder="Escribe el itinerario o resumen...")
                
                f_word_count = len(f_desc.split())
                if f_word_count > 0:
                    st.caption(f"Palabras: {f_word_count}/100")
                if f_word_count > 100:
                    st.error(f"⚠️ Has excedido el límite ({f_word_count}/100).")
            with col_t2:
                f_dias = st.number_input("Días", min_value=1, value=1, step=1)
                f_horas = st.number_input("Horas", min_value=0, value=0, step=1)
            
            st.markdown("**💰 Precios Base (Adultos)**")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1: f_p_nac = st.number_input("Precio Perú (S/) *", min_value=0.0, value=0.0)
            with col_p2: f_p_ext = st.number_input("Precio Extranjero (USD) *", min_value=0.0, value=0.0)
            with col_p3: f_p_can = st.number_input("Precio CAN (USD)", min_value=0.0, value=0.0)

            c_adv_c1, c_adv_c2 = st.columns(2)
            with c_adv_c1:
                with st.expander("⭐ Precios Niños, Estudiantes, PCD"):
                    st.caption("Opcional: Si dejas 0, el sistema calcula automáticamente.")
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
                        st.markdown("**PCD**")
                        f_npn = st.number_input("PCD Nac (S/)", value=0.0)
                        f_npe = st.number_input("PCD Ext (USD)", value=0.0)
                        f_npc = st.number_input("PCD CAN (USD)", value=0.0)
            
            with c_adv_c2:
                with st.expander("🛠️ Información Técnica"):
                    f_dificultad = st.selectbox("Dificultad", options=["FACIL", "MODERADO", "DIFICIL", "EXTREMO"])
                    f_categoria = st.text_input("Categoría", value="General")
                    f_img = st.text_input("Carpeta Imágenes", value="general")
                    f_hora = st.text_input("Hora Inicio", value="08:00:00")

            st.markdown("**📝 Textos (Separados por comas)**")
            f_high = st.text_input("Highlights / Atractivos")
            f_inc = st.text_input("Qué incluye")
            f_no_inc = st.text_input("Qué NO incluye")
            
            if st.form_submit_button("🔨 Crear Tour Oficial", type="primary", use_container_width=True):
                if not f_nombre:
                    st.error("❌ El nombre es obligatorio.")
                elif len(f_desc.split()) > 100:
                    st.error(f"❌ La descripción es muy larga ({len(f_desc.split())} palabras). Máximo 100.")
                else:
                    success, msg = create_new_tour(
                        nombre=f_nombre, descripcion=f_desc, highlights_text=f_high,
                        precio_nac=f_p_nac, precio_ext=f_p_ext, precio_can=f_p_can,
                        incluye_text=f_inc, no_incluye_text=f_no_inc,
                        duracion_dias=f_dias, duracion_horas=f_horas,
                        precio_nino_nac=f_nnn if f_nnn > 0 else None,
                        precio_nino_ext=f_nne if f_nne > 0 else None,
                        precio_nino_can=f_nnc if f_nnc > 0 else None,
                        precio_est_nac=f_nen if f_nen > 0 else None,
                        precio_est_ext=f_nee if f_nee > 0 else None,
                        precio_est_can=f_nec if f_nec > 0 else None,
                        precio_pcd_nac=f_npn, precio_pcd_ext=f_npe, precio_pcd_can=f_npc,
                        categoria=f_categoria, dificultad=f_dificultad, 
                        carpeta_img=f_img, hora_inicio=f_hora
                    )
                    if success:
                        st.success(f"✅ Tour '{f_nombre}' creado.")
                        st.rerun()
                    else: st.error(f"Error: {msg}")

    with tab3:
        st.markdown("### 📦 Armar Nuevo Paquete Maestro")
        with st.form("form_crear_paquete", clear_on_submit=True):
            col_p1, col_p2 = st.columns([2, 1])
            with col_p1:
                p_nombre = st.text_input("Nombre del Paquete *")
                p_desc = st.text_area("Descripción General")
            with col_p2:
                p_dias = st.number_input("Total Días", min_value=1, value=3)
                p_noches = st.number_input("Total Noches", min_value=0, value=2)
            
            col_p3, col_p4, col_p5 = st.columns(3)
            with col_p3:
                p_destino = st.text_input("Destino Principal", placeholder="Ej: Cusco")
            with col_p4:
                p_temporada = st.text_input("Temporada sugerida", placeholder="Ej: Todo el año")
            with col_p5:
                p_precio_sug = st.number_input("Precio Sugerido (Opcional)", min_value=0.0, value=0.0)
            
            st.write("Selecciona los tours:")
            opciones_tours = {t['titulo']: t['id_tour'] for t in tours_db}
            seleccionados = st.multiselect("Tours del Catálogo", options=list(opciones_tours.keys()))
            
            tours_vinculados = []
            if seleccionados:
                for i, nt in enumerate(seleccionados):
                    id_t = opciones_tours[nt]
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1: st.caption(nt)
                    with c2: vd = st.number_input("Día", 1, p_dias, 1, key=f"pd_{id_t}_{i}")
                    with c3: vo = st.number_input("Ord", 1, 99, i+1, key=f"po_{id_t}_{i}")
                    tours_vinculados.append({"id_tour": id_t, "dia": vd, "orden": vo})

            if st.form_submit_button("🔨 Crear Paquete Maestro", type="primary", use_container_width=True):
                if p_nombre and tours_vinculados:
                    success, msg = create_master_package(
                        nombre=p_nombre, descripcion=p_desc,
                        dias=p_dias, noches=p_noches,
                        tours_vinculados=tours_vinculados,
                        precio_sugerido=p_precio_sug,
                        destino=p_destino, temporada=p_temporada
                    )
                    if success: st.success("✅ Paquete guardado."); st.rerun()
                    else: st.error(msg)
                else: st.error("Faltan datos.")

import streamlit as st
import os
import json
from datetime import datetime
from data.tours_db import tours_db, paquetes_db
from utils.pdf_generator import generate_pdf

# --- CONSTANTS ---
PACKAGES_FILE = 'data/paquetes_guardados.json'

# --- PERSISTENCE HELPERS ---
def load_saved_packages():
    if os.path.exists(PACKAGES_FILE):
        try:
            with open(PACKAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_package(name, itinerary):
    data = load_saved_packages()
    data[name] = itinerary
    
    # Create dir if not exists
    os.makedirs(os.path.dirname(PACKAGES_FILE), exist_ok=True)
    
    with open(PACKAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- MAIN UI RENDERER ---
def render_ventas_ui():
    st.title("🛡️ Constructor de Itinerarios Premium")
    st.caption("Módulo de Ventas v2.0 - Arquitectura Modular")
    
    # Ensure Session State
    if 'itinerario' not in st.session_state:
        st.session_state.itinerario = []
    if 'origen_previo' not in st.session_state:
        st.session_state.origen_previo = "Nacional/Chileno"

    # Layout
    col1, col2 = st.columns([1, 2])

    # --- COLUMNA 1: CONFIGURACIÓN ---
    with col1:
        st.subheader("👤 Datos del Pasajero")
        nombre = st.text_input("Nombre Completo del Cliente", placeholder="Ej: Juan Pérez")
        
        cv1, cv2 = st.columns(2)
        vendedor = cv1.text_input("Vendedor", placeholder="Nombre Agente")
        celular = cv2.text_input("Celular", placeholder="+51 9XX...")
        
        t_col1, t_col2 = st.columns(2)
        tipo_t = t_col1.radio("Origen", ["Nacional/Chileno", "Extranjero"])
        modo_s = t_col2.radio("Servicio", ["Sistema Pool", "Servicio Privado"])

        # Auto-update Prices logic
        if tipo_t != st.session_state.origen_previo:
            for tour in st.session_state.itinerario:
                t_base = next((t for t in tours_db if t['titulo'] == tour['titulo']), None)
                if t_base:
                    tour['costo'] = t_base['costo_nacional'] if "Nacional" in tipo_t else t_base['costo_extranjero']
            st.session_state.origen_previo = tipo_t
            st.rerun()

        st.markdown("#### 👥 Pasajeros")
        p_c1, p_c2, p_c3 = st.columns(3)
        n_adultos_nac = p_c1.number_input("Ad. Nac", 0, value=1 if "Nacional" in tipo_t else 0)
        n_ninos_nac = p_c1.number_input("Niñ. Nac", 0)
        n_adultos_ext = p_c2.number_input("Ad. Ext", 0, value=1 if "Extranjero" in tipo_t else 0)
        n_ninos_ext = p_c2.number_input("Niñ. Ext", 0)
        n_adultos_can = p_c3.number_input("Ad. CAN", 0)
        n_ninos_can = p_c3.number_input("Niñ. CAN", 0)
        
        col_f1, col_f2 = st.columns(2)
        fecha_inicio = col_f1.date_input("Inicio", datetime.now())
        fecha_fin = col_f2.date_input("Fin", datetime.now())

        st.divider()
        
        # --- CARGA DE PAQUETES ---
        st.subheader("📦 Cargar Paquete")
        cat_sel = st.selectbox("Línea de Producto", ["-- Seleccione --", "Cusco Tradicional", "Perú para el Mundo"])
        
        if cat_sel != "-- Seleccione --":
            pkgs_filtered = [p for p in paquetes_db if cat_sel.upper() in p['nombre'].upper()]
            dias_disponibles = [p['nombre'].split(" ")[-1] for p in pkgs_filtered]
            dia_sel = st.selectbox("Duración", dias_disponibles)
            
            if st.button("🚀 Cargar"):
                pkg_final = next(p for p in pkgs_filtered if dia_sel in p['nombre'])
                st.session_state.itinerario = []
                for t_n in pkg_final['tours']:
                    t_f = next((t for t in tours_db if t['titulo'] == t_n), None)
                    if t_f:
                        nuevo_t = t_f.copy()
                        # Init prices
                        nuevo_t['costo_nac'] = t_f.get('costo_nacional', 0)
                        nuevo_t['costo_ext'] = t_f.get('costo_extranjero', 0)
                        if "MACHU PICCHU" in t_f['titulo'].upper():
                            nuevo_t['costo_can'] = nuevo_t['costo_ext'] - 20
                        else:
                            nuevo_t['costo_can'] = nuevo_t['costo_ext']
                        st.session_state.itinerario.append(nuevo_t)
                st.success("Cargado")
                st.rerun()

        st.subheader("📍 Individual")
        tour_nombres = [t['titulo'] for t in tours_db]
        tour_sel = st.selectbox("Tour Individual", ["-- Seleccione --"] + tour_nombres)
        if st.button("Agregar +"):
            if tour_sel != "-- Seleccione --":
                t_data = next(t for t in tours_db if t['titulo'] == tour_sel)
                nuevo_t = t_data.copy()
                nuevo_t['costo_nac'] = t_data.get('costo_nacional', 0)
                nuevo_t['costo_ext'] = t_data.get('costo_extranjero', 0)
                if "MACHU PICCHU" in t_data['titulo'].upper():
                    nuevo_t['costo_can'] = nuevo_t['costo_ext'] - 20
                else:
                    nuevo_t['costo_can'] = nuevo_t['costo_ext']
                st.session_state.itinerario.append(nuevo_t)
                st.rerun()

    # --- COLUMNA 2: ITINERARIO ---
    with col2:
        st.subheader("📋 Detalle del Itinerario")
        
        # Totals calc
        total_nac_pp = 0
        total_ext_pp = 0
        total_can_pp = 0
        es_pool = (modo_s == "Sistema Pool")
        
        if not st.session_state.itinerario:
            st.info("Itinerario vacío.")
        else:
            for i, tour in enumerate(st.session_state.itinerario):
                total_nac_pp += tour.get('costo_nac', 0)
                total_ext_pp += tour.get('costo_ext', 0)
                total_can_pp += tour.get('costo_can', 0)
                
                with st.expander(f"DÍA {i+1}: {tour['titulo']}", expanded=False):
                    c_edit, c_ctrl = st.columns([6, 1])
                    with c_edit:
                         # Edit Prices
                        col_n, col_e, col_c = st.columns(3)
                        tour['costo_nac'] = col_n.number_input(f"S/ Nac", value=float(tour.get('costo_nac', 0)), key=f"cn_{i}", disabled=es_pool)
                        tour['costo_ext'] = col_e.number_input(f"$ Ext", value=float(tour.get('costo_ext', 0)), key=f"ce_{i}", disabled=es_pool)
                        
                        if "MACHU PICCHU" in tour['titulo'].upper():
                            tour['costo_can'] = col_c.number_input(f"$ CAN", value=float(tour.get('costo_can', 0)), key=f"cc_{i}", disabled=es_pool)
                        else:
                            st.write("") # Spacer
                            tour['costo_can'] = tour['costo_ext']

                        # Edit Content
                        tour['titulo'] = st.text_input("Título", tour['titulo'], key=f"tt_{i}", disabled=es_pool)
                        tour['descripcion'] = st.text_area("Desc", tour['descripcion'], key=f"desc_{i}", height=70, disabled=es_pool)
                    
                    with c_ctrl:
                         if st.button("🗑️", key=f"del_{i}"):
                            st.session_state.itinerario.pop(i)
                            st.rerun()
                         if i > 0 and st.button("🔼", key=f"up_{i}"):
                            st.session_state.itinerario.insert(i-1, st.session_state.itinerario.pop(i))
                            st.rerun()

            # --- TOTALES ---
            st.divider()
            pas_nac = n_adultos_nac + n_ninos_nac
            pas_ext = n_adultos_ext + n_ninos_ext
            pas_can = n_adultos_can + n_ninos_can
            
            c_r1, c_r2, c_r3 = st.columns(3)
            c_r1.metric("Total Nacional (S/)", f"{total_nac_pp * pas_nac:,.2f}")
            c_r2.metric("Total Extranjero ($)", f"{total_ext_pp * pas_ext:,.2f}")
            c_r3.metric("Total CAN ($)", f"{total_can_pp * pas_can:,.2f}")
            
            # --- GENERAR PDF ---
            if st.button("🔥 GENERAR PDF PREMIUM", use_container_width=True):
                if nombre:
                    # Prepare Data for Generator
                    
                    # Logic for cover image
                    cover = "portada_peru.png" if cat_sel == "Perú para el Mundo" else "portada_cusco.png"
                    # Resolve absolute path for cover
                    cover_path = os.path.abspath(cover).replace('\\', '/')
                    logo_path = os.path.abspath("logo_viajes.png").replace('\\', '/')
                    # Check if exists, else use placeholder logic in generator can handle, but better here
                    
                    pdf_data = {
                        'pasajero': nombre.upper(),
                        'fechas': f"Del {fecha_inicio.strftime('%d/%m')} al {fecha_fin.strftime('%d/%m')}",
                        'duracion': f"{len(st.session_state.itinerario)}D/{(len(st.session_state.itinerario)-1)}N",
                        'cover_img': cover_path,
                        'title_1': "PERÚ" if cat_sel == "Perú para el Mundo" else "CUSCO",
                        'title_2': "PARA EL MUNDO" if cat_sel == "Perú para el Mundo" else "TRADICIONAL",
                        'vendedor': vendedor,
                        'celular': celular,
                        'logo_url': logo_path,
                        'logo_cover_url': os.path.abspath("Fondo.png").replace('\\', '/'),
                        'llama_img': os.path.abspath("Fondo.png").replace('\\', '/'),
                        'precios': {
                            'nac': {'monto': f"{total_nac_pp:,.2f}"} if pas_nac > 0 else None,
                            'ext': {'monto': f"{total_ext_pp:,.2f}"} if pas_ext > 0 else None,
                            'can': {'monto': f"{total_can_pp:,.2f}"} if pas_can > 0 else None
                        },
                        'days': st.session_state.itinerario
                    }
                    
                    with st.spinner("Diseñando PDF..."):
                        pdf_file = generate_pdf(pdf_data, f"Itinerario_{nombre}.pdf")
                        
                    with open(pdf_file, "rb") as f:
                        st.download_button("📥 DESCARGAR PDF", f, file_name=f"Itinerario_{nombre}.pdf", mime="application/pdf", type="primary")
                else:
                    st.error("Falta Nombre del Pasajero")

    # Sidebar: Saved Packages
    with st.sidebar:
        st.header("💾 Guardados")
        p_name = st.text_input("Nombre Paquete")
        if st.button("Guardar"):
            if p_name and st.session_state.itinerario:
                save_package(p_name, st.session_state.itinerario)
                st.success("Guardado!")
                
        saved = load_saved_packages()
        if saved:
            sel_s = st.selectbox("Cargar", ["--"] + list(saved.keys()))
            if sel_s != "--":
                if st.button("Cargar "):
                    st.session_state.itinerario = saved[sel_s]
                    st.rerun()


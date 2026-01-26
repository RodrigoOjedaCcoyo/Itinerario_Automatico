import streamlit as st
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from utils.pdf_generator import generate_pdf
from utils.supabase_db import (
    save_itinerary_v2, 
    get_last_itinerary_v3, 
    get_available_tours, 
    get_available_packages,
    get_vendedores,
    populate_catalog
)

# --- CONSTANTS ---
PACKAGES_FILE = 'paquetes_personalizados.json'

# --- FUNCIONES DE PERSISTENCIA ---
def guardar_paquete(nombre, itinerario):
    data = {}
    if os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    data[nombre] = itinerario
    with open(PACKAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_paquetes():
    if os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# --- DICCIONARIO DE ICONOS SVG ---
ICON_MAP = {
    'transporte': '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle>',
    'traslado': '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle>',
    'guía': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
    'asistencia': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle>',
    'almuerzo': '<path d="M3 2v7c0 1.1.9 2 2 2h4V2"></path><path d="M7 2v20"></path><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>',
    'alimentación': '<path d="M3 2v7c0 1.1.9 2 2 2h4V2"></path><path d="M7 2v20"></path><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>',
    'ingreso': '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"></path><path d="M13 5v2"></path><path d="M13 17v2"></path><path d="M13 11v2"></path>',
    'boleto': '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"></path><path d="M13 5v2"></path><path d="M13 17v2"></path><path d="M13 11v2"></path>',
    'vuelo': '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path>',
    'botiquín': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M9 12h6"/><path d="M12 9v6"/>',
    'oxígeno': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M9 12h6"/><path d="M12 9v6"/>',
    'propinas': '<line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    'default_in': '<polyline points="20 6 9 17 4 12"></polyline>',
    'default_out': '<line x1="5" y1="12" x2="19" y2="12"></line>'
}

def get_svg_icon(text, default_key='default_in'):
    text_lower = text.lower()
    for key, svg in ICON_MAP.items():
        if key in text_lower:
            return svg
    return ICON_MAP[default_key]

def obtener_imagenes_tour(nombre_carpeta):
    """Obtiene las imágenes de un tour desde la carpeta assets/img/tours/"""
    base_path = Path(os.getcwd()) / 'assets' / 'img' / 'tours' / nombre_carpeta
    
    if not base_path.exists():
        # Fallback a carpeta general si existe
        general_path = Path(os.getcwd()) / 'assets' / 'img' / 'tours' / 'general'
        if general_path.exists():
            base_path = general_path
        else:
            return ["https://via.placeholder.com/400x300?text=Foto+Tour"] * 5
    
    imagenes = []
    if base_path.exists():
        for f in base_path.iterdir():
            if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                imagenes.append(str(f.absolute()))
    
    while len(imagenes) < 5:
        imagenes.append("https://via.placeholder.com/400x300?text=Foto+Tour")
        
    return imagenes[:5]

# --- UI PRINCIPAL ---
def render_ventas_ui():
    """Renderiza la interfaz de ventas"""
    
    # Esconder elementos de Streamlit (Header, Menu, Footer)
    st.markdown("""
        <style>
            [data-testid="stHeader"], header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display: none;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """, unsafe_allow_html=True)
    
    # Estado de sesión
    if 'itinerario' not in st.session_state:
        st.session_state.itinerario = []
    if 'origen_previo' not in st.session_state:
        st.session_state.origen_previo = "Nacional"
    
    # Campos del formulario controlados
    if 'f_vendedor' not in st.session_state: st.session_state.f_vendedor = ""
    if 'f_celular' not in st.session_state: st.session_state.f_celular = ""
    if 'f_fuente' not in st.session_state: st.session_state.f_fuente = "WhatsApp"
    if 'f_estado' not in st.session_state: st.session_state.f_estado = "Frío"
    if 'f_origen' not in st.session_state: st.session_state.f_origen = "Nacional"
    if 'f_categoria' not in st.session_state: st.session_state.f_categoria = "Cusco Tradicional"
    if 'f_tipo_cliente' not in st.session_state: st.session_state.f_tipo_cliente = "B2C"
    if 'f_nota_precio' not in st.session_state: st.session_state.f_nota_precio = "INCLUYE TOUR Y ALOJAMIENTO"
    if 'f_estrategia' not in st.session_state: st.session_state.f_estrategia = "Opciones"
    if 'u_h2' not in st.session_state: st.session_state.u_h2 = 40.0
    if 'u_h3' not in st.session_state: st.session_state.u_h3 = 70.0
    if 'u_h4' not in st.session_state: st.session_state.u_h4 = 110.0
    if 'u_t_v' not in st.session_state: st.session_state.u_t_v = 90.0
    if 'u_t_o' not in st.session_state: st.session_state.u_t_o = 140.0
    # Verificar Conexión
    from utils.supabase_db import get_supabase_client
    if get_supabase_client() is None:
        st.warning("⚠️ El sistema no está conectado a Supabase (El Cerebro). Configura el archivo .env para habilitar el seguimiento de leads.")

    st.title("🏔️ Constructor de Itinerarios Premium")
    st.write("Interfaz exclusiva para el equipo de ventas de Viajes Cusco Perú.")
    
    # 0. Cargar Catálogo desde Supabase (Cacheado en sesión)
    if not st.session_state.get('catalogo_tours') or not st.session_state.get('catalogo_paquetes') or not st.session_state.get('lista_vendedores') or st.sidebar.button("🔄 Refrescar Catálogo"):
        with st.spinner("Cargando catálogo desde el Cerebro..."):
            st.session_state.catalogo_tours = get_available_tours()
            st.session_state.catalogo_paquetes = get_available_packages()
            st.session_state.lista_vendedores = get_vendedores()
            
            nt = len(st.session_state.catalogo_tours) if st.session_state.catalogo_tours else 0
            np = len(st.session_state.catalogo_paquetes) if st.session_state.catalogo_paquetes else 0
            nv = len(st.session_state.lista_vendedores) if st.session_state.lista_vendedores else 0
            
            if nt == 0:
                st.sidebar.error("⚠️ No hay tours en Supabase.")
            else:
                st.sidebar.success(f"✅ {nt} tours, {np} paquetes y {nv} vendedores listos.")
    
    tours_db = st.session_state.get('catalogo_tours', [])
    paquetes_db = st.session_state.get('catalogo_paquetes', [])
    vendedores_db = st.session_state.get('lista_vendedores', [])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("👤 Datos del Pasajero")
        
        nc1, nc2 = st.columns([5, 1])
        nombre = nc1.text_input("Nombre Completo del Cliente", placeholder="Ej: Juan Pérez")
        nc2.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) # Espaciador para alinear con input
        if nc2.button("🔍", help="Buscar cliente"):
            if nombre:
                nombre_clean = nombre.strip().upper() # Limpiamos espacios y estandarizamos
                with st.spinner(f"Buscando a {nombre_clean}..."):
                    st.toast(f"🔎 Buscando '{nombre_clean}' en Base de Datos (v3)...", icon="😎")
                    last_data = get_last_itinerary_v3(nombre_clean)
                    if last_data:
                        # Auto-llenar campos desde el nuevo esquema
                        datos_completos = last_data.get("datos_render", {})
                        st.session_state.f_vendedor = datos_completos.get("vendedor", "")
                        st.session_state.f_celular = datos_completos.get("celular_cliente", "")
                        st.session_state.f_fuente = datos_completos.get("fuente", "WhatsApp")
                        st.session_state.f_estrategia = datos_completos.get("estrategia", "Opciones")
                        st.session_state.f_origen = datos_completos.get("categoria", "Nacional")
                        
                        if datos_completos and 'days' in datos_completos:
                             # Re-construir itinerario simplificado para el editor
                             new_it = []
                             for d in datos_completos['days']:
                                 t_original = next((t for t in tours_db if t['titulo'] == d['titulo']), None)
                                 if t_original:
                                     new_it.append(t_original.copy())
                             st.session_state.itinerario = new_it
                        
                        st.success(f"¡Datos cargados para {nombre}!")
                        st.rerun()
                    else:
                        st.warning("No se encontraron registros previos.")

        ld_col1, ld_col2 = st.columns([1, 1])
        
        with ld_col1:
            # Canal
            idx_t = 0 if st.session_state.f_tipo_cliente == "B2C" else 1
            tipo_c = st.selectbox("Canal de Venta", ["B2C (Directo)", "B2B (Agencia)"], index=idx_t)
            st.session_state.f_tipo_cliente = "B2C" if "B2C" in tipo_c else "B2B"

            # Fuente
            fuente_list = ["WhatsApp", "Facebook Ads", "Instagram Ads", "Google Ads", "Web Site", "Recomendado", "Otros"]
            idx_f = fuente_list.index(st.session_state.f_fuente) if st.session_state.f_fuente in fuente_list else 0
            origen_lead = st.selectbox("Fuente del Lead", fuente_list, index=idx_f)
            
        with ld_col2:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) # Espaciado 
            estrategias = ["Opciones", "Matriz", "General"]
            idx_e = estrategias.index(st.session_state.f_estrategia) if st.session_state.f_estrategia in estrategias else 0
            estrategia_v = st.radio("Estrategia de Venta", estrategias, index=idx_e, horizontal=True)
            st.session_state.f_estrategia = estrategia_v

        cv1, cv2 = st.columns(2)
        # Buscar índice del vendedor actual
        vendedor_actual = st.session_state.f_vendedor
        idx_v = 0
        if vendedor_actual in vendedores_db:
            idx_v = vendedores_db.index(vendedor_actual)
        
        vendedor = cv1.selectbox("Vendedor", vendedores_db, index=idx_v if vendedores_db else 0)
        celular = cv2.text_input("Celular del Cliente *", value=st.session_state.f_celular, placeholder="Ej: +51 9XX XXX XXX")
        
        t_col1, t_col2 = st.columns(2)
        idx_o = 0 if "Nacional" in st.session_state.f_origen else (1 if "Extranjero" in st.session_state.f_origen else 2)
        tipo_t = t_col1.radio("Origen", ["Nacional", "Extranjero", "Mixto"], index=idx_o)
        modo_s = "Sistema Pool" # Definimos por defecto para evitar errores en el PDF
        # es_pool = (modo_s == "Sistema Pool") # Mantenemos modo_edicion individual
        
        # Actualizar precios al cambiar origen
        if tipo_t != st.session_state.origen_previo:
            for tour in st.session_state.itinerario:
                t_base = next((t for t in tours_db if t['titulo'] == tour['titulo']), None)
                if t_base:
                    tour['costo'] = t_base['costo_nacional'] if "Nacional" in tipo_t else t_base['costo_extranjero']
            st.session_state.origen_previo = tipo_t
            st.rerun()
        
        st.markdown("#### 👥 Pasajeros")
        # Mostrar columnas solo según el origen seleccionado para limpiar la UI
        if tipo_t == "Nacional":
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                st.caption("🇵🇪 NACIONALES")
                n_adultos_nac = st.number_input("👤 Adultos", min_value=0, value=1, step=1, key="an_nac")
                n_estud_nac = st.number_input("🎓 Estudiantes", min_value=0, value=0, step=1, key="es_nac")
                n_pcd_nac = st.number_input("♿ PcD", min_value=0, value=0, step=1, key="pcd_nac")
                n_ninos_nac = st.number_input("👶 Niños", min_value=0, value=0, step=1, key="ni_nac")
            # Forzamos los otros a 0 para que no afecten cálculos
            n_adultos_ext = n_estud_ext = n_pcd_ext = n_ninos_ext = 0
            n_adultos_can = n_estud_can = n_pcd_can = n_ninos_can = 0
            with p_col2: st.empty() # Espaciador
        elif tipo_t == "Extranjero":
            p_col1, p_col2, p_col3 = st.columns([1, 1, 1])
            with p_col1:
                st.caption("🌎 EXTRANJEROS")
                n_adultos_ext = st.number_input("👤 Adultos", min_value=0, value=1, step=1, key="an_ext")
                n_estud_ext = st.number_input("🎓 Estudiantes", min_value=0, value=0, step=1, key="es_ext")
                n_pcd_ext = st.number_input("♿ PcD", min_value=0, value=0, step=1, key="pcd_ext")
                n_ninos_ext = st.number_input("👶 Niños", min_value=0, value=0, step=1, key="ni_ext")
            with p_col2:
                st.caption("🤝 COMUNIDAD ANDINA (CAN)")
                n_adultos_can = st.number_input("👤 Adultos ", min_value=0, value=0, step=1, key="an_can")
                n_estud_can = st.number_input("🎓 Estudiantes ", min_value=0, value=0, step=1, key="es_can")
                n_pcd_can = st.number_input("♿ PcD ", min_value=0, value=0, step=1, key="pcd_can")
                n_ninos_can = st.number_input("👶 Niños ", min_value=0, value=0, step=1, key="ni_can")
            # Forzamos nacionales a 0
            n_adultos_nac = n_estud_nac = n_pcd_nac = n_ninos_nac = 0
            with p_col3: st.empty() # Espaciador
        else: # MODO MIXTO: Muestra TODO
            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1:
                st.caption("🇵🇪 NACIONALES")
                n_adultos_nac = st.number_input("👤 Adultos ", min_value=0, value=0, step=1, key="an_nac_m")
                n_estud_nac = st.number_input("🎓 Estudiantes ", min_value=0, value=0, step=1, key="es_nac_m")
                n_pcd_nac = st.number_input("♿ PcD ", min_value=0, value=0, step=1, key="pcd_nac_m")
                n_ninos_nac = st.number_input("👶 Niños ", min_value=0, value=0, step=1, key="ni_nac_m")
            with p_col2:
                st.caption("🌎 EXTRANJEROS")
                n_adultos_ext = st.number_input("👤 Adultos", min_value=0, value=0, step=1, key="an_ext_m")
                n_estud_ext = st.number_input("🎓 Estudiantes", min_value=0, value=0, step=1, key="es_ext_m")
                n_pcd_ext = st.number_input("♿ PcD", min_value=0, value=0, step=1, key="pcd_ext_m")
                n_ninos_ext = st.number_input("👶 Niños", min_value=0, value=0, step=1, key="ni_ext_m")
            with p_col3:
                st.caption("🤝 CAN")
                n_adultos_can = st.number_input("👤 Adultos  ", min_value=0, value=0, step=1, key="an_can_m")
                n_estud_can = st.number_input("🎓 Estudiantes  ", min_value=0, value=0, step=1, key="es_can_m")
                n_pcd_can = st.number_input("♿ PcD  ", min_value=0, value=0, step=1, key="pcd_can_m")
                n_ninos_can = st.number_input("👶 Niños  ", min_value=0, value=0, step=1, key="ni_can_m")

        
        total_pasajeros = (n_adultos_nac + n_estud_nac + n_pcd_nac + n_ninos_nac + 
                           n_adultos_ext + n_estud_ext + n_pcd_ext + n_ninos_ext + 
                           n_adultos_can + n_estud_can + n_pcd_can + n_ninos_can)
        st.info(f"Total personas: {total_pasajeros}")
        
        col_date1, col_date2 = st.columns([2, 1])
        fecha_inicio = col_date1.date_input("📅 Fecha de Inicio del Viaje", datetime.now())
        usa_fechas = col_date2.checkbox("¿Ver fechas?", value=st.session_state.get('f_usa_fechas', True), key="f_usa_fechas", help="Si se desactiva, el PDF dirá 'DÍA 1' en lugar de fechas exactas.")
        
        # Calculamos la fecha fin automáticamente basada en el número de días
        num_dias = len(st.session_state.itinerario)
        fecha_fin = fecha_inicio + timedelta(days=max(0, num_dias - 1))
        # Rango para la portada
        if usa_fechas:
            rango_fechas = f"Del {fecha_inicio.strftime('%d/%m')} al {fecha_fin.strftime('%d/%m, %Y')}"
        else:
            rango_fechas = f"{num_dias} DÍAS / {max(0, num_dias-1)} NOCHES"

        # Sidebar para paquetes guardados
        with st.sidebar:
            st.header("💾 Mis Paquetes Guardados")
            
            with st.expander("➕ Guardar Itinerario Actual", expanded=False):
                nombre_p = st.text_input("Nombre de tu paquete", placeholder="Ej: Machu Picchu VIP 3D")
                if st.button("💾 Confirmar Guardado"):
                    if nombre_p and st.session_state.itinerario:
                        guardar_paquete(nombre_p, st.session_state.itinerario)
                        st.success(f"¡'{nombre_p}' guardado!")
                        st.rerun()
                    else:
                        st.warning("Ponle un nombre y agrega tours primero.")
            
            st.divider()
            
            paquetes_c = cargar_paquetes()
            if paquetes_c:
                p_sel = st.selectbox("📂 Selecciona uno de tus paquetes", ["-- Seleccione --"] + list(paquetes_c.keys()))
                if p_sel != "-- Seleccione --":
                    if st.button("🚀 Cargar mi Paquete"):
                        st.session_state.itinerario = paquetes_c[p_sel]
                        st.success(f"Paquete '{p_sel}' cargado.")
                        st.rerun()
            else:
                st.caption("No tienes paquetes guardados aún.")
        
        st.divider()
        
        st.subheader("🎁 Cargar Paquete Sugerido")
        # Sincronizar selectbox con session_state
        lineas = ["Cusco Tradicional", "Perú para el Mundo"]
        idx_cat = lineas.index(st.session_state.f_categoria) if st.session_state.f_categoria in lineas else 0
        cat_sel = st.selectbox("Elija Línea de Producto", lineas, index=idx_cat)
        st.session_state.f_categoria = cat_sel
        
        if cat_sel != "-- Seleccione --":
            pkgs_filtered = [p for p in paquetes_db if cat_sel.upper() in p['nombre'].upper()]
            dias_disponibles = [p['nombre'].split(" ")[-1] for p in pkgs_filtered]
            dia_sel = st.selectbox("Seleccione Duración", dias_disponibles)
            
            if pkgs_filtered and st.button("🚀 Cargar Itinerario", use_container_width=True):
                pkg_final = next((p for p in pkgs_filtered if dia_sel in p['nombre']), None)
                if pkg_final:
                    found_tours = []
                    missing_tours = []
                    for t_n in pkg_final['tours']:
                        # Búsqueda robusta (sin espacios, sin mayúsculas/minúsculas)
                        t_f = next((t for t in tours_db if t['titulo'].strip().upper() == t_n.strip().upper()), None)
                        if t_f:
                            nuevo_t = t_f.copy()
                            nuevo_t['costo_nac'] = t_f.get('costo_nacional', 0)
                            nuevo_t['costo_ext'] = t_f.get('costo_extranjero', 0)
                            if "MACHU PICCHU" in t_f['titulo'].upper():
                                nuevo_t['costo_can'] = nuevo_t['costo_ext'] - 20
                            else:
                                nuevo_t['costo_can'] = nuevo_t['costo_ext']
                            found_tours.append(nuevo_t)
                        else:
                            missing_tours.append(t_n)
                    
                    if found_tours:
                        st.session_state.itinerario = found_tours
                        st.session_state.f_categoria = cat_sel # Asegurar categoría al cargar
                        if missing_tours:
                            st.warning(f"⚠️ Algunos tours no se encontraron en el catálogo general: {', '.join(missing_tours)}")
                        st.success(f"✅ Paquete '{pkg_final['nombre']}' cargado con {len(found_tours)} tours.")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: El paquete '{pkg_final['nombre']}' quiere cargar estos tours: {pkg_final['tours']}, pero ninguno coincide con los {len(tours_db)} tours que hay en la base de datos.")
                        if st.button("🔧 Forzar Sincronización"):
                            st.session_state.catalogo_tours = None
                            st.rerun()
                else:
                    st.error("❌ Error al identificar el paquete seleccionado.")
        
        st.subheader("📍 Agregar Tour Individual")
        tour_nombres = [t['titulo'] for t in tours_db]
        tour_sel = st.selectbox("Seleccione un tour", ["-- Seleccione --"] + tour_nombres)
        if tour_sel != "-- Seleccione --" and st.button("Agregar Tour"):
            t_data = next((t for t in tours_db if t['titulo'] == tour_sel), None)
            if t_data:
                nuevo_t = t_data.copy()
                nuevo_t['costo_nac'] = t_data.get('costo_nacional', 0)
                nuevo_t['costo_ext'] = t_data.get('costo_extranjero', 0)
                if "MACHU PICCHU" in t_data['titulo'].upper():
                    nuevo_t['costo_can'] = nuevo_t['costo_ext'] - 20
                else:
                    nuevo_t['costo_can'] = nuevo_t['costo_ext']
                st.session_state.itinerario.append(nuevo_t)
                st.rerun()
    
    with col2:
        st.subheader("📋 Plan de Viaje Actual")
        
        total_nac_pp = 0
        total_ext_pp = 0
        total_can_pp = 0
        
        # El modo de edición ahora es individual por cada tour
        
        if not st.session_state.itinerario:
            st.info("El itinerario está vacío. Comienza cargando un paquete o un tour individual.")
        else:
            for i, tour in enumerate(st.session_state.itinerario):
                total_nac_pp += tour.get('costo_nac', 0)
                total_ext_pp += tour.get('costo_ext', 0)
                total_can_pp += tour.get('costo_can', 0)
                
                c_content, c_btns = st.columns([0.88, 0.12])
                
                with c_content:
                    es_mp = "MACHU PICCHU" in tour['titulo'].upper()
                    
                    current_date = fecha_inicio + timedelta(days=i)
                    date_str = current_date.strftime('%d/%m/%Y')
                    header_text = f"🗓️ {date_str} - DÍA {i+1}: {tour['titulo']} - (S/ {tour.get('costo_nac', 0)} | $ {tour.get('costo_ext', 0)})"
                    if es_mp:
                        header_text = f"🗓️ {date_str} - DÍA {i+1}: {tour['titulo']} - (S/ {tour.get('costo_nac', 0)} | $ {tour.get('costo_ext', 0)} | CAN $ {tour.get('costo_can', 0)})"
                    
                    with st.expander(header_text, expanded=False):
                        # Control de edición manual para este día específico
                        modo_edicion = st.toggle("🔧 Modificar datos de este día", key=f"mod_edit_{i}")
                        is_disabled = not modo_edicion
                        
                        if es_mp:
                            col_t1, col_n, col_e, col_c, col_h = st.columns([1.5, 0.6, 0.6, 0.6, 0.6])
                            tour['titulo'] = col_t1.text_input(f"Título día {i+1}", tour['titulo'], key=f"title_{i}", disabled=is_disabled)
                            tour['hora_inicio'] = col_h.text_input(f"⏰ Hora", value=tour.get('hora_inicio', '08:00 AM'), key=f"hi_{i}", disabled=is_disabled)
                            tour['costo_nac'] = col_n.number_input(f"Nac (S/)", value=float(tour.get('costo_nac', 0)), key=f"cn_{i}", disabled=is_disabled)
                            tour['costo_ext'] = col_e.number_input(f"Ext ($)", value=float(tour.get('costo_ext', 0)), key=f"ce_{i}", disabled=is_disabled)
                            tour['costo_can'] = col_c.number_input(f"CAN ($)", value=float(tour.get('costo_can', 0)), key=f"cc_{i}", disabled=is_disabled)
                        else:
                            col_t1, col_n, col_e, col_h = st.columns([2, 0.8, 0.8, 0.8])
                            tour['titulo'] = col_t1.text_input(f"Título día {i+1}", tour['titulo'], key=f"title_{i}", disabled=is_disabled)
                            tour['hora_inicio'] = col_h.text_input(f"⏰ Hora", value=tour.get('hora_inicio', '08:00 AM'), key=f"hi_{i}", disabled=is_disabled)
                            tour['costo_nac'] = col_n.number_input(f"Nac (S/)", value=float(tour.get('costo_nac', 0)), key=f"cn_{i}", disabled=is_disabled)
                            tour['costo_ext'] = col_e.number_input(f"Ext ($)", value=float(tour.get('costo_ext', 0)), key=f"ce_{i}", disabled=is_disabled)
                            tour['costo_can'] = tour['costo_ext']
                        
                        st.divider()
                        
                        desc_key = f"desc_{i}"
                        raw_desc = st.text_area(f"Descripción día {i+1}", tour.get('descripcion', ""), key=desc_key, height=100, disabled=is_disabled)
                        tour['descripcion'] = raw_desc
                        words_count = len(raw_desc.split())
                        st.caption(f"📝 {words_count} palabras")
                        
                        col_ex1, col_ex2 = st.columns(2)
                        h_text = col_ex1.text_area(f"📍 Atractivos", "\n".join(tour.get('highlights', [])), key=f"h_{i}", height=120, disabled=is_disabled)
                        tour['highlights'] = [line.strip() for line in h_text.split("\n") if line.strip()]
                        
                        s_text = col_ex2.text_area(f"✅ Incluye", "\n".join(tour.get('servicios', [])), key=f"s_{i}", height=120, disabled=is_disabled)
                        tour['servicios'] = [line.strip() for line in s_text.split("\n") if line.strip()]

                        sn_text = st.text_area(f"❌ No Incluye", "\n".join(tour.get('servicios_no_incluye', [])), key=f"sn_{i}", height=80, disabled=is_disabled)
                        tour['servicios_no_incluye'] = [line.strip() for line in sn_text.split("\n") if line.strip()]
                        
                        if is_disabled:
                            st.caption("💡 Haz clic en 'Modificar datos de este día' arriba para editar precios o textos.")
                
                with c_btns:
                    st.write('<div style="margin-top: 4px;"></div>', unsafe_allow_html=True)
                    # Usamos columnas para el control de orden y borrado
                    b_col1, b_col2 = st.columns([2, 1])
                    
                    # Selector de posición numérica
                    new_pos = b_col1.number_input("Orden", 
                                                 min_value=1, 
                                                 max_value=len(st.session_state.itinerario), 
                                                 value=i+1, 
                                                 key=f"new_pos_{i}",
                                                 on_change=None) # Podríamos usar on_change pero el flujo actual usa rerun
                    
                    # Si el número cambia, movemos el tour
                    if new_pos != i+1:
                        st.session_state.itinerario.insert(new_pos-1, st.session_state.itinerario.pop(i))
                        st.rerun()

                    if b_col2.button("🗑️", key=f"del_{i}"):
                        st.session_state.itinerario.pop(i)
                        st.rerun()
                
                st.markdown('<div style="margin-top: -15px;"></div>', unsafe_allow_html=True)
            
            st.divider()
            
            
            st.markdown("#### 💰 Margen Extra / Ajuste Global (Opcional)")
            ma1, ma2, ma3, ma4 = st.columns(4)
            extra_nac = ma1.number_input("S/ Extra (Nac)", value=float(st.session_state.get('f_extra_nac', 0.0)), step=10.0)
            extra_ext = ma2.number_input("$ Extra (Ext)", value=float(st.session_state.get('f_extra_ext', 0.0)), step=5.0)
            extra_can = ma3.number_input("$ Extra (CAN)", value=float(st.session_state.get('f_extra_can', 0.0)), step=5.0)
            
            # Cálculo automático base de noches
            auto_noches = max(0, len(st.session_state.itinerario) - 1)
            num_noches = ma4.number_input("🌙 Noches Hotel", value=int(st.session_state.get('f_num_noches', auto_noches)), min_value=0, step=1)
            
            st.session_state.f_extra_nac = extra_nac
            st.session_state.f_extra_ext = extra_ext
            st.session_state.f_extra_can = extra_can
            st.session_state.f_num_noches = num_noches

            # --- CONFIGURACIÓN DE UPGRADES (HOTEL Y TREN) ---
            u_h2, u_h3, u_h4 = 0, 0, 0
            u_t_v, u_t_o = 0, 0
            precio_cierre_over = None

            with st.expander("🏨 Configuración de Costos de Upgrades", expanded=(estrategia_v in ["Matriz", "Opciones"])):
                st.caption("Define el costo ADICIONAL por noche para hoteles y el total por el tren (se usa para cálculos automáticos).")
                ch1, ch2, ch3 = st.columns(3)
                curr = "S/" if tipo_t == "Nacional" else "$"
                u_h2 = ch1.number_input(f"Hotel 2* ({curr}/noche)", value=float(st.session_state.get('u_h2', 40.0)), key="uh2")
                u_h3 = ch2.number_input(f"Hotel 3* ({curr}/noche)", value=float(st.session_state.get('u_h3', 70.0)), key="uh3")
                u_h4 = ch3.number_input(f"Hotel 4* ({curr}/noche)", value=float(st.session_state.get('u_h4', 110.0)), key="uh4")
                
                st.divider()
                ct1, ct2 = st.columns(2)
                u_t_v = ct1.number_input("Extra Tren Vistadome ($)", value=float(st.session_state.get('u_t_v', 90.0)), key="utv")
                u_t_o = ct2.number_input("Extra Tren Observatory ($)", value=float(st.session_state.get('u_t_o', 140.0)), key="uto")
                
                st.session_state.u_h2 = u_h2
                st.session_state.u_h3 = u_h3
                st.session_state.u_h4 = u_h4
                st.session_state.u_t_v = u_t_v
                st.session_state.u_t_o = u_t_o

            sel_hotel_gen = "Sin Hotel"
            sel_tren_gen = "Expedition"

            if estrategia_v == "General":
                with st.container(border=True):
                    st.markdown("🎯 **Configuración del Paquete (Modo General)**")
                    cg1, cg2 = st.columns(2)
                    sel_hotel_gen = cg1.selectbox("Categoría de Hotel", ["Sin Hotel", "Hotel 2*", "Hotel 3*", "Hotel 4*"], key="sel_h_gen")
                    sel_tren_gen = cg2.selectbox("Tipo de Tren", ["Expedition", "Vistadome", "Observatory"], key="sel_t_gen")
                    
                    curr_c = "S/" if tipo_t == "Nacional" else "$"
                    precio_cierre_over = st.number_input(f"Monto Total Final Manual ({curr_c})", value=0.0, help="Si dejas en 0, se usará el precio calculado automáticamente con los upgrades seleccionados.")
                    if precio_cierre_over > 0:
                        st.info(f"Se usará {curr_c} {precio_cierre_over:,.2f} como precio final en el PDF.")
                    else:
                        st.caption("Se calculará el precio base + upgrades seleccionados.")

            st.divider()
            
            pasajeros_nac = n_adultos_nac + n_estud_nac + n_pcd_nac + n_ninos_nac
            pasajeros_ext = n_adultos_ext + n_estud_ext + n_pcd_ext + n_ninos_ext
            pasajeros_can = n_adultos_can + n_estud_can + n_pcd_can + n_ninos_can
            
            # --- LÓGICA DE DESCUENTOS AUTOMÁTICOS ---
            # Nacionales: Niño -S/ 40, Estudiante/PcD -S/ 70
            desc_nac = (n_ninos_nac * 40.0) + (n_estud_nac * 70.0) + (n_pcd_nac * 70.0)
            # Extranjeros/CAN: Niño -$15, Estudiante/PcD -$20
            desc_ext = (n_ninos_ext * 15.0) + (n_estud_ext * 20.0) + (n_pcd_ext * 20.0)
            desc_can = (n_ninos_can * 15.0) + (n_estud_can * 20.0) + (n_pcd_can * 20.0)

            real_nac = (total_nac_pp * pasajeros_nac) + extra_nac - desc_nac
            real_ext = (total_ext_pp * pasajeros_ext) + extra_ext - desc_ext
            real_can = (total_can_pp * pasajeros_can) + extra_can - desc_can
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.markdown("### 🇵🇪 Nacionales")
                st.markdown(f"## S/ {real_nac:,.2f}")
                if desc_nac > 0:
                    st.success(f"📉 Ahorro Aplicado: S/ {desc_nac:,.2f}")
                st.caption(f"({pasajeros_nac} pas x S/ {total_nac_pp:,.2f} p/p)")
            
            with col_res2:
                st.markdown("### 🌎 Extranjeros")
                st.markdown(f"## $ {real_ext:,.2f}")
                if desc_ext > 0:
                    st.success(f"📉 Ahorro Aplicado: $ {desc_ext:,.2f}")
                st.caption(f"({pasajeros_ext} pas x $ {total_ext_pp:,.2f} p/p)")
            
            with col_res3:
                st.markdown("### 🤝 CAN")
                st.markdown(f"## $ {real_can:,.2f}")
                if desc_can > 0:
                    st.success(f"📉 Ahorro Aplicado: $ {desc_can:,.2f}")
                st.caption(f"({pasajeros_can} pas x $ {total_can_pp:,.2f} p/p)")
            
            nota_p = st.text_input("📝 Nota de Precio (Aparece en el PDF)", value=st.session_state.f_nota_precio, placeholder="Ej: INCLUYE HOTEL EN HAB. DOBLE")
            st.session_state.f_nota_precio = nota_p
            
            st.divider()
            
            c_btn1, c_btn2 = st.columns(2)
            if c_btn2.button("🧹 Limpiar Todo"):
                st.session_state.itinerario = []
                st.rerun()
            
            if c_btn1.button("🔥 GENERAR ITINERARIO PDF"):
                if nombre and celular and st.session_state.itinerario:
                    with st.spinner("Generando PDF con Edge..."):
                        # Determinar portada y títulos desde el ESTADO DE SESIÓN
                        base_dir = os.getcwd()
                        cover_1 = os.path.join(base_dir, "assets", "images", "covers", "peru_mundo.jpg")
                        cover_2 = os.path.join(base_dir, "assets", "images", "covers", "cusco_tradicional.jpg")
                        fallback_cover = os.path.join(base_dir, "Approaching-Salkantay-Mountain-peru.jpg")
                        
                        target_cat = st.session_state.get('f_categoria', 'Cusco Tradicional')
                        
                        if target_cat == "Perú para el Mundo":
                            cover_img = cover_1 if os.path.exists(cover_1) else fallback_cover
                            t1, t2 = "PERÚ", "PARA EL MUNDO"
                        else:
                            cover_img = cover_2 if os.path.exists(cover_2) else fallback_cover
                            t1, t2 = "CUSCO", "TRADICIONAL"
                        
                        # Logo
                        logo_orig = "Captura de pantalla 2026-01-05 102612.png"
                        logo_path = os.path.abspath(logo_orig if os.path.exists(logo_orig) else "Fondo.png")
                        
                        # Preparar días con imágenes
                        days_data = []
                        for i, tour in enumerate(st.session_state.itinerario):
                            carpeta = tour.get('carpeta_img', 'general')
                            imgs = obtener_imagenes_tour(carpeta)
                            
                            # Preparar servicios con iconos SVG
                            servicios_html = []
                            for s in tour.get('servicios', []):
                                svg_content = get_svg_icon(s, 'default_in')
                                servicios_html.append({'texto': s, 'svg': svg_content})
                            
                            servicios_no_html = []
                            for s in tour.get('servicios_no_incluye', []):
                                svg_content = get_svg_icon(s, 'default_out')
                                servicios_no_html.append({'texto': s, 'svg': svg_content})
                            
                            current_date = fecha_inicio + timedelta(days=i)
                            days_data.append({
                                'numero': i + 1,
                                'fecha': current_date.strftime('%d / %m / %Y') if usa_fechas else "",
                                'titulo': tour['titulo'],
                                'hora_inicio': tour.get('hora_inicio') or '08:00 AM',
                                'descripcion': tour.get('descripcion', ''),
                                'highlights': tour.get('highlights', []),
                                'servicios': servicios_html,
                                'servicios_no': servicios_no_html,
                                'images': imgs
                            })
                        
                        try:
                            # 1. Preparar data completa
                            # USAR EL VALOR MANUAL DE NOCHES RECIÉN DEFINIDO
                            # num_noches ya fue definido arriba en la UI
                            curr_sym = "S/" if tipo_t == "Nacional" else "$"
                            
                            # Base Price calculation for the primary category
                            if tipo_t == "Nacional":
                                base_raw = total_nac_pp + (extra_nac/max(1, pasajeros_nac))
                            elif tipo_t == "Extranjero":
                                base_raw = total_ext_pp + (extra_ext/max(1, pasajeros_ext))
                            else: # Mixto
                                base_raw = total_ext_pp + (extra_ext/max(1, pasajeros_ext))

                            # Aplicar Upgrades si estamos en modo General
                            base_final = base_raw
                            if estrategia_v == "General":
                                # Sumar Hotel
                                if sel_hotel_gen == "Hotel 2*": base_final += (u_h2 * num_noches)
                                elif sel_hotel_gen == "Hotel 3*": base_final += (u_h3 * num_noches)
                                elif sel_hotel_gen == "Hotel 4*": base_final += (u_h4 * num_noches)
                                
                                # Sumar Tren
                                if sel_tren_gen == "Vistadome": base_final += u_t_v
                                elif sel_tren_gen == "Observatory": base_final += u_t_o

                            # Matrix Calculation
                            def calc_m(base, extra_t, extra_h_n):
                                return base + extra_t + (extra_h_n * num_noches)

                            pricing_matrix = {
                                'expedition': {
                                    'sin': f"{calc_m(base_final, 0, 0):,.2f}",
                                    'h2': f"{calc_m(base_final, 0, u_h2):,.2f}",
                                    'h3': f"{calc_m(base_final, 0, u_h3):,.2f}",
                                    'h4': f"{calc_m(base_final, 0, u_h4):,.2f}"
                                },
                                'vistadome': {
                                    'sin': f"{calc_m(base_final, u_t_v, 0):,.2f}",
                                    'h2': f"{calc_m(base_final, u_t_v, u_h2):,.2f}",
                                    'h3': f"{calc_m(base_final, u_t_v, u_h3):,.2f}",
                                    'h4': f"{calc_m(base_final, u_t_v, u_h4):,.2f}"
                                },
                                'observatory': {
                                    'sin': f"{calc_m(base_final, u_t_o, 0):,.2f}",
                                    'h2': f"{calc_m(base_final, u_t_o, u_h2):,.2f}",
                                    'h3': f"{calc_m(base_final, u_t_o, u_h3):,.2f}",
                                    'h4': f"{calc_m(base_final, u_t_o, u_h4):,.2f}"
                                }
                            }

                            full_itinerary_data = {
                                'title_1': t1,
                                'title_2': t2,
                                'pasajero': nombre.upper(),
                                'fechas': rango_fechas.upper(),
                                'usa_fechas': usa_fechas,
                                'categoria': target_cat.upper(),
                                'modo': modo_s.upper(),
                                'estrategia': estrategia_v,
                                'simbolo_moneda': curr_sym,
                                'duracion': f"{len(st.session_state.itinerario)}D / {num_noches}N",
                                'cover_url': os.path.abspath(cover_img),
                                'vendedor': vendedor,
                                'celular_cliente': celular,
                                'fuente': origen_lead,
                                'estado': "Cotización", # Valor fijo ya que usamos estrategia
                                'logo_url': logo_path,
                                'logo_cover_url': logo_path,
                                'llama_img': os.path.abspath("Fondo.png"),
                                'precios': {
                                    'nac': {'monto': f"{total_nac_pp + (extra_nac/max(1, pasajeros_nac)):,.2f}"} if (total_nac_pp > 0) else None,
                                    'ext': {'monto': f"{total_ext_pp + (extra_ext/max(1, pasajeros_ext)):,.2f}"} if (total_ext_pp > 0) else None,
                                    'can': {'monto': f"{total_can_pp + (extra_can/max(1, pasajeros_can)):,.2f}"} if (total_can_pp > 0) else None,
                                },
                                'precio_cierre': f"{precio_cierre_over:,.2f}" if (precio_cierre_over and precio_cierre_over > 0) else f"{base_final:,.2f}",
                                'matriz': pricing_matrix,
                                'precio_nota': nota_p.upper(),
                                'canal': st.session_state.f_tipo_cliente,
                                'days': days_data
                            }

                            # 2. Guardar en Supabase y obtener ID de vinculación
                            itinerary_id = None
                            with st.spinner("Sincronizando con el Cerebro (Leads e Itinerario)..."):
                                itinerary_id = save_itinerary_v2(full_itinerary_data)
                                if itinerary_id:
                                    st.toast("✅ Lead e Itinerario sincronizados", icon="🧠")
                            
                            # 3. Generar PDF
                            pdf_path = generate_pdf(full_itinerary_data)
                            
                            if itinerary_id:
                                st.info(f"🔑 **CÓDIGO DE VINCULACIÓN:** `{itinerary_id}`")
                                st.caption("Copia este ID y pégalo en el Registro de Venta para importar toda la información automáticamente.")

                            with open(pdf_path, "rb") as file:
                                st.download_button(
                                    label="📥 Descargar PDF Final",
                                    data=file,
                                    file_name=f"Itinerario_{nombre.replace(' ', '_')}.pdf",
                                    mime="application/pdf"
                                )
                            st.success(f"¡Itinerario listo para {nombre}!")
                        except Exception as e:
                            st.error(f"Error procesando: {e}")
                else:
                    st.warning("⚠️ Asegúrate de poner el Nombre, el Celular y tener al menos un tour en el plan.")
    
    # Pie de página
    st.markdown("---")
    st.caption("v2.0 - Sistema de Gestión de Itinerarios con Edge PDF | Viajes Cusco Perú")

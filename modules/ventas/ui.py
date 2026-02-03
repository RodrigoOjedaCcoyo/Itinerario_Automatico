import streamlit as st
import os
import uuid
import json
from datetime import datetime, timedelta
from pathlib import Path
from utils.pdf_generator import generate_pdf
from utils.supabase_db import (
    save_itinerary_v2, 
    get_last_itinerary_by_phone, 
    get_available_tours, 
    get_available_packages,
    get_vendedores,
    populate_catalog,
    save_custom_package,
    get_custom_packages,
    delete_custom_package,
    get_service_templates
)

# --- ELIMINADAS FUNCIONES DE PERSISTENCIA LOCAL (AHORA ES CLOUD) ---

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

def format_tour_time(raw_time):
    """Convierte un string de tiempo técnico (ej. 08:00:00) a un formato amigable (ej. 08:00 AM)"""
    if not raw_time:
        return "08:00 AM"
    
    raw_str = str(raw_time).strip()
    if ':' in raw_str:
        try:
            parts = raw_str.split(':')
            h = int(parts[0])
            m = int(parts[1]) if len(parts) > 1 else 0
            
            # Si ya tiene AM o PM, lo dejamos tal cual
            if 'AM' in raw_str.upper() or 'PM' in raw_str.upper():
                return raw_str
                
            if h >= 12:
                h_12 = h - 12 if h > 12 else 12
                return f"{h_12:02d}:{m:02d} PM"
            else:
                h_12 = h if h > 0 else 12
                return f"{h_12:02d}:{m:02d} AM"
        except:
            return raw_str
    return raw_str

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

def crear_dia_base(titulo="Día Personalizado", desc="", servicios=None, icons=None):
    """Crea la estructura base para un día manual o personalizado."""
    return {
        "id": str(uuid.uuid4()),
        "titulo": titulo,
        "descripcion": desc,
        "highlights": [titulo],
        "servicios": servicios if servicios else ["Asistencia personalizada"],
        "servicios_no_incluye": ["Gastos extras", "Propinas"],
        "costo_nac": 0.0,
        "costo_ext": 0.0,
        "costo_can": 0.0,
        "hora_inicio": "08:00 AM",
        "carpeta_img": "general"
    }

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
    if 'f_monto_adelanto' not in st.session_state: st.session_state.f_monto_adelanto = 0.0
    if 'f_monto_pendiente' not in st.session_state: st.session_state.f_monto_pendiente = 0.0
    if 'f_estrategia' not in st.session_state: st.session_state.f_estrategia = "Opciones"
    if 'u_h2' not in st.session_state: st.session_state.u_h2 = 40.0
    if 'u_h3' not in st.session_state: st.session_state.u_h3 = 70.0
    if 'u_h4' not in st.session_state: st.session_state.u_h4 = 110.0
    if 'u_t_v' not in st.session_state: st.session_state.u_t_v = 90.0
    if 'u_t_o' not in st.session_state: st.session_state.u_t_o = 140.0
    # Inicialización de Ajuste Global
    if 'f_extra_nac' not in st.session_state: st.session_state.f_extra_nac = 0.0
    if 'f_extra_ext' not in st.session_state: st.session_state.f_extra_ext = 0.0
    if 'f_extra_can' not in st.session_state: st.session_state.f_extra_can = 0.0
    if 'f_num_noches' not in st.session_state: st.session_state.f_num_noches = 0
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

    # SIDEBAR: PAQUETES CLOUD (Mejorado y Visible)
    with st.sidebar:
        st.header("☁️ Mis Paquetes en la Nube")
        
        with st.expander("✨ Guardar Itinerario Actual", expanded=True):
            nombre_p = st.text_input("Nombre del paquete", key="cloud_pkg_name", placeholder="Ej: Machu Picchu VIP 3D")
            es_pub = st.toggle("Compartir con el equipo", value=True, help="Si se activa, otros vendedores podrán ver y usar este paquete.")
            if st.button("💾 Guardar en la Nube", use_container_width=True):
                if nombre_p and st.session_state.itinerario:
                    with st.spinner("Guardando..."):
                        success = save_custom_package(nombre_p, st.session_state.itinerario, st.session_state.get("user_email"), es_pub)
                        if success:
                            st.success(f"¡'{nombre_p}' guardado exitosamente!")
                            st.rerun()
                        else:
                            st.error("Hubo un error al guardar en la nube.")
                else:
                    st.warning("Escribe un nombre y agrega tours primero.")
        
        st.divider()
        
        cloud_pkgs = get_custom_packages()
        if cloud_pkgs:
            st.subheader("📂 Paquetes del Equipo")
            for cp in cloud_pkgs:
                with st.container(border=True):
                    col_p1, col_p2 = st.columns([4, 1])
                    with col_p1:
                        st.markdown(f"**{cp['nombre']}**")
                        st.caption(f"Por: {cp['creado_por'].split('@')[0] if cp['creado_por'] else 'Anon'}")
                    with col_p2:
                        # Botón cargar
                        if st.button("🚀", key=f"load_{cp['id_paquete_personalizado']}", help="Cargar este paquete"):
                            st.session_state.itinerario = cp['itinerario']
                            st.success(f"Cargado: {cp['nombre']}")
                            st.rerun()
                        # Botón eliminar (solo si es el creador o admin)
                        is_owner = cp['creado_por'] == st.session_state.get("user_email")
                        is_admin = st.session_state.get("user_rol") == "ADMIN"
                        if is_owner or is_admin:
                            if st.button("🗑️", key=f"del_{cp['id_paquete_personalizado']}", help="Eliminar paquete"):
                                if delete_custom_package(cp['id_paquete_personalizado']):
                                    st.success("Paquete eliminado.")
                                    st.rerun()
        else:
            st.caption("No hay paquetes guardados en la nube aún.")
        
        st.divider()

    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("👤 Datos del Pasajero")
        
        nombre = st.text_input("Nombre Completo del Cliente", value=st.session_state.get('f_nombre', ''), placeholder="Ej: Juan Pérez")
        st.session_state.f_nombre = nombre

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

        # El vendedor se obtiene automáticamente de la sesión
        vendedor = st.session_state.get("vendedor_name", "Anonimo")
        
        cel1, cel2 = st.columns([4, 1])
        celular = cel1.text_input("Celular del Cliente *", value=st.session_state.f_celular, placeholder="Ej: 9XX XXX XXX")
        st.session_state.f_celular = celular
        
        cel2.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if cel2.button("🔍", key="search_phone"):
            if celular:
                with st.spinner("Buscando por celular..."):
                    last_data = get_last_itinerary_by_phone(celular)
                    if last_data:
                        datos_completos = last_data.get("datos_render", {})
                        st.session_state.f_nombre = datos_completos.get("pasajero", "")
                        st.session_state.f_vendedor = datos_completos.get("vendedor", "")
                        st.session_state.f_fuente = datos_completos.get("fuente", "WhatsApp")
                        st.session_state.f_estrategia = datos_completos.get("estrategia", "Opciones")
                        st.session_state.f_origen = datos_completos.get("categoria", "Nacional")
                        
                        if datos_completos and 'days' in datos_completos:
                             new_it = []
                             for d in datos_completos['days']:
                                 # 1. Intentar buscar metadatos en el catálogo oficial (como la carpeta_img)
                                 t_catalog = next((t for t in tours_db if t.get('titulo') == d.get('titulo')), None)
                                 
                                 # 2. Reconstruir con PRIORIDAD a lo guardado en el PDF (lo que el vendedor editó)
                                 tour_obj = {
                                     "id": d.get('id_original', str(uuid.uuid4())),
                                     "titulo": d.get('titulo', 'Día Cargado'),
                                     "descripcion": d.get('descripcion', ''),
                                     # Convertir servicios de [{texto, svg}] a lista simple de textos
                                     "servicios": [s['texto'] for s in d.get('servicios', [])] if isinstance(d.get('servicios'), list) and d.get('servicios') and isinstance(d.get('servicios')[0], dict) else d.get('servicios', []),
                                     "servicios_no_incluye": d.get('servicios_no_incluye', [s['texto'] for s in d.get('servicios_no', [])] if d.get('servicios_no') else []),
                                     "costo_nac": float(d.get('costo_nac', 0)),
                                     "costo_ext": float(d.get('costo_ext', 0)),
                                     "costo_can": float(d.get('costo_can', 0)),
                                     "costo_nac_est": float(d.get('costo_nac_est', float(d.get('costo_nac', 0))-70)),
                                     "costo_nac_nino": float(d.get('costo_nac_nino', float(d.get('costo_nac', 0))-40)),
                                     "costo_ext_est": float(d.get('costo_ext_est', float(d.get('costo_ext', 0))-20)),
                                     "costo_ext_nino": float(d.get('costo_ext_nino', float(d.get('costo_ext', 0))-15)),
                                     "costo_can_est": float(d.get('costo_can_est', float(d.get('costo_can', 0))-20)),
                                     "costo_can_nino": float(d.get('costo_can_nino', float(d.get('costo_can', 0))-15)),
                                     "hora_inicio": d.get('hora_inicio', '08:00 AM'),
                                     "carpeta_img": t_catalog.get('carpeta_img', 'general') if t_catalog else 'general'
                                 }
                                 new_it.append(tour_obj)
                                     
                             st.session_state.itinerario = new_it
                        
                        st.success(f"¡Datos de {st.session_state.f_nombre} cargados!")
                        st.rerun()
                    else:
                        st.warning("No se encontraron registros previos.")
        
        t_col1, t_col2 = st.columns(2)
        idx_o = 0 if "Nacional" in st.session_state.f_origen else 1
        tipo_t = t_col1.radio("Origen", ["Nacional", "Extranjero"], index=idx_o)
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
        
        st.markdown("#### 👥 Composición del Grupo")
        
        if tipo_t == "Nacional":
            # Caso simple: Solo nacionales
            p_col_n = st.columns([1, 2])[0]
            with p_col_n:
                st.caption("🇵🇪 NACIONALES")
                n_adultos_nac = st.number_input("👤 Adultos", min_value=0, value=int(st.session_state.get('n_adultos_nac', 1)), step=1, key="an_nac_uni")
                n_estud_nac = st.number_input("🎓 Estudiantes", min_value=0, value=int(st.session_state.get('n_estud_nac', 0)), step=1, key="es_nac_uni")
                n_pcd_nac = st.number_input("♿ PcD", min_value=0, value=int(st.session_state.get('n_pcd_nac', 0)), step=1, key="pcd_nac_uni")
                n_ninos_nac = st.number_input("👶 Niños", min_value=0, value=int(st.session_state.get('n_ninos_nac', 0)), step=1, key="ni_nac_uni")
            
            # Los otros se quedan con lo que tenían en la sesión o en 0 si no existen
            n_adultos_ext = int(st.session_state.get('n_adultos_ext', 0))
            n_estud_ext = int(st.session_state.get('n_estud_ext', 0))
            n_pcd_ext = int(st.session_state.get('n_pcd_ext', 0))
            n_ninos_ext = int(st.session_state.get('n_ninos_ext', 0))
            
            n_adultos_can = int(st.session_state.get('n_adultos_can', 0))
            n_estud_can = int(st.session_state.get('n_estud_can', 0))
            n_pcd_can = int(st.session_state.get('n_pcd_can', 0))
            n_ninos_can = int(st.session_state.get('n_ninos_can', 0))
            
        else:
            # Caso "Extranjero": Muestra solo Extranjeros y CAN
            p_col1, p_col2 = st.columns(2)
            
            with p_col1:
                st.caption("🌎 EXTRANJEROS")
                n_adultos_ext = st.number_input("👤 Adultos", min_value=0, value=int(st.session_state.get('n_adultos_ext', 1)), step=1, key="an_ext_uni")
                n_estud_ext = st.number_input("🎓 Estudiantes", min_value=0, value=int(st.session_state.get('n_estud_ext', 0)), step=1, key="es_ext_uni")
                n_pcd_ext = st.number_input("♿ PcD", min_value=0, value=int(st.session_state.get('n_pcd_ext', 0)), step=1, key="pcd_ext_uni")
                n_ninos_ext = st.number_input("👶 Niños", min_value=0, value=int(st.session_state.get('n_ninos_ext', 0)), step=1, key="ni_ext_uni")

            with p_col2:
                st.caption("🤝 CAN")
                n_adultos_can = st.number_input("👤 Adultos ", min_value=0, value=int(st.session_state.get('n_adultos_can', 0)), step=1, key="an_can_uni")
                n_estud_can = st.number_input("🎓 Estudiantes ", min_value=0, value=int(st.session_state.get('n_estud_can', 0)), step=1, key="es_can_uni")
                n_pcd_can = st.number_input("♿ PcD ", min_value=0, value=int(st.session_state.get('n_pcd_can', 0)), step=1, key="pcd_can_uni")
                n_ninos_can = st.number_input("👶 Niños ", min_value=0, value=int(st.session_state.get('n_ninos_can', 0)), step=1, key="ni_can_uni")
            
            # Los nacionales se quedan con lo que tenían en la sesión
            n_adultos_nac = int(st.session_state.get('n_adultos_nac', 0))
            n_estud_nac = int(st.session_state.get('n_estud_nac', 0))
            n_pcd_nac = int(st.session_state.get('n_pcd_nac', 0))
            n_ninos_nac = int(st.session_state.get('n_ninos_nac', 0))

        # Persistencia obligatoria de todos los valores para el cálculo en página
        st.session_state.n_adultos_nac = n_adultos_nac
        st.session_state.n_estud_nac = n_estud_nac
        st.session_state.n_pcd_nac = n_pcd_nac
        st.session_state.n_ninos_nac = n_ninos_nac
        
        st.session_state.n_adultos_ext = n_adultos_ext
        st.session_state.n_estud_ext = n_estud_ext
        st.session_state.n_pcd_ext = n_pcd_ext
        st.session_state.n_ninos_ext = n_ninos_ext
        
        st.session_state.n_adultos_can = n_adultos_can
        st.session_state.n_estud_can = n_estud_can
        st.session_state.n_pcd_can = n_pcd_can
        st.session_state.n_ninos_can = n_ninos_can

        
        total_pasajeros = (n_adultos_nac + n_estud_nac + n_pcd_nac + n_ninos_nac + 
                           n_adultos_ext + n_estud_ext + n_pcd_ext + n_ninos_ext + 
                           n_adultos_can + n_estud_can + n_pcd_can + n_ninos_can)
        st.info(f"Total personas: {total_pasajeros}")
        
        # --- NUEVA SECCIÓN: DISTRIBUCIÓN DE HABITACIONES ---
        with st.expander("🛏️ Distribución de Habitaciones", expanded=total_pasajeros > 0):
            st.caption("Define cómo se distribuirá el grupo en las habitaciones.")
            rdr1_1, rdr1_2, rdr1_3 = st.columns(3)
            n_sgl = rdr1_1.number_input("Simple (1p)", min_value=0, value=int(st.session_state.get('f_n_sgl', 0)), step=1, key="f_n_sgl")
            n_dbl = rdr1_2.number_input("Doble Twin (2p)", min_value=0, value=int(st.session_state.get('f_n_dbl', 0)), step=1, key="f_n_dbl")
            n_mat = rdr1_3.number_input("Matrimonial (2p)", min_value=0, value=int(st.session_state.get('f_n_mat', 0)), step=1, key="f_n_mat")
            
            rdr2_1, rdr2_2, _ = st.columns(3)
            n_tpl = rdr2_1.number_input("Triple (3p)", min_value=0, value=int(st.session_state.get('f_n_tpl', 0)), step=1, key="f_n_tpl")
            n_cua = rdr2_2.number_input("Cuádruple (4p)", min_value=0, value=int(st.session_state.get('f_n_cua', 0)), step=1, key="f_n_cua")
            
            pax_en_habitaciones = (n_sgl * 1) + (n_dbl * 2) + (n_mat * 2) + (n_tpl * 3) + (n_cua * 4)
            if pax_en_habitaciones != total_pasajeros:
                st.warning(f"⚠️ La distribución ({pax_en_habitaciones} pax) no coincide con el total de pasajeros ({total_pasajeros} pax).")
            else:
                st.success(f"✅ Distribución correcta para {total_pasajeros} pasajeros.")
        
        
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

        # --- ELIMINADA SECCIÓN ANTIGUA DE PAQUETES LOCALES ---
        
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
                            cn = float(t_f.get('costo_nacional', 0))
                            ce = float(t_f.get('costo_extranjero', 0))
                            nuevo_t['costo_nac'] = cn
                            nuevo_t['costo_nac_est'] = cn - 70.0
                            nuevo_t['costo_nac_nino'] = cn - 40.0
                            nuevo_t['costo_ext'] = ce
                            nuevo_t['costo_ext_est'] = ce - 20.0
                            nuevo_t['costo_ext_nino'] = ce - 15.0

                            if "MACHU PICCHU" in t_f['titulo'].upper():
                                cc = ce - 20.0
                            else:
                                cc = ce
                            
                            nuevo_t['costo_can'] = cc
                            nuevo_t['costo_can_est'] = cc - 20.0
                            nuevo_t['costo_can_nino'] = cc - 15.0
                            
                            # ID único para persistencia de widgets
                            if 'id' not in nuevo_t:
                                nuevo_t['id'] = str(uuid.uuid4())
                                
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
                cn = float(t_data.get('costo_nacional', 0))
                ce = float(t_data.get('costo_extranjero', 0))
                nuevo_t['costo_nac'] = cn
                nuevo_t['costo_nac_est'] = cn - 70.0
                nuevo_t['costo_nac_nino'] = cn - 40.0
                nuevo_t['costo_ext'] = ce
                nuevo_t['costo_ext_est'] = ce - 20.0
                nuevo_t['costo_ext_nino'] = ce - 15.0

                if "MACHU PICCHU" in t_data['titulo'].upper():
                    cc = ce - 20.0
                else:
                    cc = ce
                
                nuevo_t['costo_can'] = cc
                nuevo_t['costo_can_est'] = cc - 20.0
                nuevo_t['costo_can_nino'] = cc - 15.0
                
                # ID único para persistencia de widgets
                nuevo_t['id'] = str(uuid.uuid4())
                
                st.session_state.itinerario.append(nuevo_t)
                st.rerun()
        
        st.subheader("✨ Servicios Rápidos / Personalizados")
        
        c_p1, c_p2 = st.columns([1, 1])
        
        with c_p1:
            if st.button("➕ Agregar Día en Blanco", use_container_width=True, help="Añade un día vacío para que escribas lo que quieras."):
                nuevo_d = crear_dia_base()
                st.session_state.itinerario.append(nuevo_d)
                # Activar edición para el nuevo día
                st.session_state[f"mod_edit_{nuevo_d['id']}"] = True
                st.rerun()
        
        with c_p2:
            db_templates = get_service_templates()
            quick_opt_map = {t['titulo']: t for t in db_templates}
            quick_names = ["-- Seleccione Plantilla --"] + list(quick_opt_map.keys())
            
            q_sel = st.selectbox("Plantillas Rápidas", quick_names, label_visibility="collapsed")
            
            if q_sel != "-- Seleccione Plantilla --":
                if st.button("⚡ Aplicar Plantilla", use_container_width=True):
                    template_data = quick_opt_map[q_sel]
                    
                    nuevo_d = crear_dia_base(
                        titulo=template_data['titulo'],
                        desc=template_data.get('descripcion', "")
                    )
                    # Opcional: Si la plantilla tiene precios, podrías asignarlos aquí
                    nuevo_d['costo_nac'] = float(template_data.get('costo_nac', 0.0))
                    nuevo_d['costo_ext'] = float(template_data.get('costo_ext', 0.0))
                    
                    st.session_state.itinerario.append(nuevo_d)
                    st.session_state[f"mod_edit_{nuevo_d['id']}"] = True
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
                
                tour_id = tour.get('id', str(uuid.uuid4()))
                tour['id'] = tour_id # Asegurar que esté guardado
                
                c_content, c_btns = st.columns([0.88, 0.12])
                
                with c_content:
                    es_mp = "MACHU PICCHU" in tour['titulo'].upper()
                    
                    current_date = fecha_inicio + timedelta(days=i)
                    date_str = current_date.strftime('%d/%m/%Y')
                    header_icon = "⭐" if modo_s == "B2B" else "📍" 
                    header_text = f"✨ {date_str} - DÍA {i+1}: {tour['titulo']} - (S/ {tour.get('costo_nac', 0)} | $ {tour.get('costo_ext', 0)})"
                    if es_mp:
                        header_text = f"✨ {date_str} - DÍA {i+1}: {tour['titulo']} - (S/ {tour.get('costo_nac', 0)} | $ {tour.get('costo_ext', 0)} | CAN $ {tour.get('costo_can', 0)})"
                    
                    with st.expander(header_text, expanded=False):
                        # Control de edición manual para este día específico
                        modo_edicion = st.toggle("🔧 Modificar datos de este día", key=f"mod_edit_{tour_id}")
                        is_disabled = not modo_edicion
                        
                        if es_mp:
                            col_t1, col_n, col_e, col_c, col_h = st.columns([1.5, 0.6, 0.6, 0.6, 0.6])
                            tour['titulo'] = col_t1.text_input(f"Título día {i+1}", tour['titulo'], key=f"title_{tour_id}", disabled=is_disabled)
                            tour['hora_inicio'] = col_h.text_input(f"⏰ Hora", value=tour.get('hora_inicio', '08:00 AM'), key=f"hi_{tour_id}", disabled=is_disabled)
                            tour['costo_nac'] = col_n.number_input(f"Nac (S/)", value=float(tour.get('costo_nac', 0)), key=f"cn_{tour_id}", disabled=is_disabled)
                            tour['costo_ext'] = col_e.number_input(f"Ext ($)", value=float(tour.get('costo_ext', 0)), key=f"ce_{tour_id}", disabled=is_disabled)
                            tour['costo_can'] = col_c.number_input(f"CAN ($)", value=float(tour.get('costo_can', 0)), key=f"cc_{tour_id}", disabled=is_disabled)
                        else:
                            col_t1, col_n, col_e, col_h = st.columns([2, 0.8, 0.8, 0.8])
                            tour['titulo'] = col_t1.text_input(f"Título día {i+1}", tour['titulo'], key=f"title_{tour_id}", disabled=is_disabled)
                            tour['hora_inicio'] = col_h.text_input(f"⏰ Hora", value=tour.get('hora_inicio', '08:00 AM'), key=f"hi_{tour_id}", disabled=is_disabled)
                            tour['costo_nac'] = col_n.number_input(f"Nac (S/)", value=float(tour.get('costo_nac', 0)), key=f"cn_{tour_id}", disabled=is_disabled)
                            tour['costo_ext'] = col_e.number_input(f"Ext ($)", value=float(tour.get('costo_ext', 0)), key=f"ce_{tour_id}", disabled=is_disabled)
                            tour['costo_can'] = tour['costo_ext']
                        
                        # --- MEJORA: Tarifas por Categoría (Ahora más visible) ---
                        if modo_edicion:
                            with st.container(border=True):
                                st.markdown("##### 👥 Edición de Tarifas por Categoría (Estudiantes/Niños)")
                                ec1, ec2, ec3 = st.columns(3)
                                # Nacionales
                                ec1.markdown("**🇵🇪 Nac**")
                                tour['costo_nac_est'] = ec1.number_input(f"Estud/PcD (S/)", value=float(tour.get('costo_nac_est', tour['costo_nac']-70)), key=f"cn_e_{tour_id}")
                                tour['costo_nac_nino'] = ec1.number_input(f"Niño (S/)", value=float(tour.get('costo_nac_nino', tour['costo_nac']-40)), key=f"cn_n_{tour_id}")
                                # Extranjeros
                                ec2.markdown("**🌎 Ext**")
                                tour['costo_ext_est'] = ec2.number_input(f"Estud/PcD ($)", value=float(tour.get('costo_ext_est', tour['costo_ext']-20)), key=f"ce_e_{tour_id}")
                                tour['costo_ext_nino'] = ec2.number_input(f"Niño ($)", value=float(tour.get('costo_ext_nino', tour['costo_ext']-15)), key=f"ce_n_{tour_id}")
                                # CAN
                                ec3.markdown("**🤝 CAN**")
                                tour['costo_can_est'] = ec3.number_input(f"Estud/PcD ($)", value=float(tour.get('costo_can_est', tour['costo_can']-20)), key=f"cc_e_{tour_id}")
                                tour['costo_can_nino'] = ec3.number_input(f"Niño ($)", value=float(tour.get('costo_can_nino', tour['costo_can']-15)), key=f"cc_n_{tour_id}")
                        else:
                            with st.expander("👥 Ver Tarifas por Categoría"):
                                st.write(f"**Nac:** Estud S/ {tour.get('costo_nac_est',0)} | Niño S/ {tour.get('costo_nac_nino',0)}")
                                st.write(f"**Ext:** Estud $ {tour.get('costo_ext_est',0)} | Niño $ {tour.get('costo_ext_nino',0)}")

                        st.divider()
                        
                        desc_key = f"desc_{tour_id}"
                        raw_desc = st.text_area(f"Descripción día {i+1}", tour.get('descripcion', ""), key=desc_key, height=100, disabled=is_disabled)
                        tour['descripcion'] = raw_desc
                        st.caption("💡 **Tips:** `**Negrita**`, `*Cursiva*`, `[Enter]` para nuevo párrafo.")
                        words_count = len(raw_desc.split())
                        st.caption(f"📝 {words_count} palabras")
                        
                        # Atractivos eliminados por pedido del usuario - Simplificación
                        
                        s_text = st.text_area(f"✅ Incluye", "\n".join(tour.get('servicios', [])), key=f"s_{tour_id}", height=120, disabled=is_disabled)
                        tour['servicios'] = [line.strip() for line in s_text.split("\n") if line.strip()]

                        sn_text = st.text_area(f"❌ No Incluye", "\n".join(tour.get('servicios_no_incluye', [])), key=f"sn_{tour_id}", height=80, disabled=is_disabled)
                        tour['servicios_no_incluye'] = [line.strip() for line in sn_text.split("\n") if line.strip()]
                        
                        if is_disabled:
                            st.caption("💡 Haz clic en 'Modificar datos de este día' arriba para editar precios o textos.")
                
                with c_btns:
                    st.write('<div style="margin-top: 4px;"></div>', unsafe_allow_html=True)
                    # Usamos el ID único para que los botones sean estables al moverse
                    tour_id = tour.get('id', str(i))
                    b1, b2, b3 = st.columns(3)
                    
                    if b1.button("🔼", key=f"up_{tour_id}"):
                        if i > 0:
                            item = st.session_state.itinerario.pop(i)
                            st.session_state.itinerario.insert(i-1, item)
                            st.rerun()
                            
                    if b2.button("🔽", key=f"down_{tour_id}"):
                        if i < len(st.session_state.itinerario)-1:
                            item = st.session_state.itinerario.pop(i)
                            st.session_state.itinerario.insert(i+1, item)
                            st.rerun()
                            
                    if b3.button("🗑️", key=f"del_{tour_id}"):
                        st.session_state.itinerario.pop(i)
                        st.rerun()
                
                st.markdown('<div style="margin-top: -15px;"></div>', unsafe_allow_html=True)
            
            st.divider()
            
            
            st.markdown("#### 💰 Margen Extra / Ajuste Global (Opcional)")
            ma1, ma2, ma3, ma4 = st.columns(4)
            # Usar keys permite que el valor se mantenga estable aunque la app se refresque por otras razones
            extra_nac = ma1.number_input("S/ Extra (Nac)", step=10.0, key="f_extra_nac")
            extra_ext = ma2.number_input("$ Extra (Ext)", step=5.0, key="f_extra_ext")
            extra_can = ma3.number_input("$ Extra (CAN)", step=5.0, key="f_extra_can")
            
            # Cálculo automático base de noches si el valor es 0 o el estado no existe
            auto_noches = max(0, len(st.session_state.itinerario) - 1)
            # Solo forzar auto_noches si el usuario no ha tocado el campo (valor en 0)
            if st.session_state.f_num_noches == 0 and auto_noches > 0:
                st.session_state.f_num_noches = auto_noches

            num_noches = ma4.number_input("🌙 Noches Hotel", min_value=0, step=1, key="f_num_noches")

            # --- CONFIGURACIÓN DE UPGRADES (HOTEL Y TREN) ---
            u_h2, u_h3, u_h4 = 0, 0, 0
            u_t_v, u_t_o = 0, 0
            precio_cierre_over = 0.0

            with st.expander("🏨 Configuración de Costos de Upgrades", expanded=(estrategia_v in ["Matriz", "Opciones"])):
                st.caption("Define el costo por persona/noche según el tipo de habitación para cada categoría.")
                
                curr = "S/" if tipo_t == "Nacional" else "$"
                
                # Definir Pestañas por Categoría para que sea más limpio
                tab2, tab3, tab4 = st.tabs(["Hotel 2*", "Hotel 3*", "Hotel 4*"])
                
                with tab2:
                    cc2_1, cc2_2, cc2_3 = st.columns(3)
                    u_h2_sgl = cc2_1.number_input(f"Simple ({curr})", value=float(st.session_state.get('u_h2_sgl', 60.0)), key="uh2_sgl")
                    u_h2_dbl = cc2_2.number_input(f"Doble ({curr})", value=float(st.session_state.get('u_h2_dbl', 40.0)), key="uh2_dbl")
                    u_h2_mat = cc2_3.number_input(f"Matrim. ({curr})", value=float(st.session_state.get('u_h2_mat', 40.0)), key="uh2_mat")
                    cc2_4, cc2_5, _ = st.columns(3)
                    u_h2_tpl = cc2_4.number_input(f"Triple ({curr})", value=float(st.session_state.get('u_h2_tpl', 35.0)), key="uh2_tpl")
                    u_h2_cua = cc2_5.number_input(f"Cuádruple ({curr})", value=float(st.session_state.get('u_h2_cua', 30.0)), key="uh2_cua")
                
                with tab3:
                    cc3_1, cc3_2, cc3_3 = st.columns(3)
                    u_h3_sgl = cc3_1.number_input(f"Simple ({curr})", value=float(st.session_state.get('u_h3_sgl', 100.0)), key="uh3_sgl")
                    u_h3_dbl = cc3_2.number_input(f"Doble ({curr})", value=float(st.session_state.get('u_h3_dbl', 70.0)), key="uh3_dbl")
                    u_h3_mat = cc3_3.number_input(f"Matrim. ({curr})", value=float(st.session_state.get('u_h3_mat', 70.0)), key="uh3_mat")
                    cc3_4, cc3_5, _ = st.columns(3)
                    u_h3_tpl = cc3_4.number_input(f"Triple ({curr})", value=float(st.session_state.get('u_h3_tpl', 65.0)), key="uh3_tpl")
                    u_h3_cua = cc3_5.number_input(f"Cuádruple ({curr})", value=float(st.session_state.get('u_h3_cua', 60.0)), key="uh3_cua")

                with tab4:
                    cc4_1, cc4_2, cc4_3 = st.columns(3)
                    u_h4_sgl = cc4_1.number_input(f"Simple ({curr})", value=float(st.session_state.get('u_h4_sgl', 180.0)), key="uh4_sgl")
                    u_h4_dbl = cc4_2.number_input(f"Doble ({curr})", value=float(st.session_state.get('u_h4_dbl', 110.0)), key="uh4_dbl")
                    u_h4_mat = cc4_3.number_input(f"Matrim. ({curr})", value=float(st.session_state.get('u_h4_mat', 110.0)), key="uh4_mat")
                    cc4_4, cc4_5, _ = st.columns(3)
                    u_h4_tpl = cc4_4.number_input(f"Triple ({curr})", value=float(st.session_state.get('u_h4_tpl', 100.0)), key="uh4_tpl")
                    u_h4_cua = cc4_5.number_input(f"Cuádruple ({curr})", value=float(st.session_state.get('u_h4_cua', 90.0)), key="uh4_cua")

                st.session_state.u_h2_sgl = u_h2_sgl; st.session_state.u_h2_dbl = u_h2_dbl; st.session_state.u_h2_mat = u_h2_mat; st.session_state.u_h2_tpl = u_h2_tpl; st.session_state.u_h2_cua = u_h2_cua
                st.session_state.u_h3_sgl = u_h3_sgl; st.session_state.u_h3_dbl = u_h3_dbl; st.session_state.u_h3_mat = u_h3_mat; st.session_state.u_h3_tpl = u_h3_tpl; st.session_state.u_h3_cua = u_h3_cua
                st.session_state.u_h4_sgl = u_h4_sgl; st.session_state.u_h4_dbl = u_h4_dbl; st.session_state.u_h4_mat = u_h4_mat; st.session_state.u_h4_tpl = u_h4_tpl; st.session_state.u_h4_cua = u_h4_cua
                
                st.divider()
                st.markdown("🚅 **Suplementos de Tren**")
                ct1, ct2, ct3 = st.columns(3)
                u_t_v = ct1.number_input("Extra Tren Vistadome ($)", value=float(st.session_state.get('u_t_v', 90.0)), key="utv")
                u_t_o = ct2.number_input("Extra Tren Observatory ($)", value=float(st.session_state.get('u_t_o', 140.0)), key="uto")
                
                # Tren Local solo para Nacionales
                u_t_local = 0.0
                if tipo_t == "Nacional":
                    u_t_local = ct3.number_input("Costo Tren Local (S/)", value=float(st.session_state.get('u_t_local', 0.0)), key="utlocal", help="Costo fijo o diferencia por persona para el Tren Local")
                
                st.session_state.u_h2 = u_h2
                st.session_state.u_h3 = u_h3
                st.session_state.u_h4 = u_h4
                st.session_state.u_t_v = u_t_v
                st.session_state.u_t_o = u_t_o
                st.session_state.u_t_local = u_t_local

            sel_hotel_gen = "Sin Hotel"
            sel_tren_gen = "Expedition"

            if estrategia_v == "General":
                with st.container(border=True):
                    st.markdown("🎯 **Configuración del Paquete (Modo General)**")
                    cg1, cg2 = st.columns(2)
                    sel_hotel_gen = cg1.selectbox("Categoría de Hotel", ["Sin Hotel", "Hotel 2*", "Hotel 3*", "Hotel 4*"], key="sel_h_gen")
                    
                    opciones_tren = ["Expedition", "Vistadome", "Observatory"]
                    if tipo_t == "Nacional":
                        opciones_tren.insert(0, "Tren Local")
                    
                    sel_tren_gen = cg2.selectbox("Tipo de Tren", opciones_tren, key="sel_t_gen")
                    
                    curr_c = "S/" if tipo_t == "Nacional" else "$"
                    precio_cierre_over = st.number_input(f"Monto Total Final Manual ({curr_c})", value=0.0, help="Si dejas en 0, se usará el precio calculado automáticamente con los upgrades seleccionados.")
                    if precio_cierre_over > 0:
                        st.info(f"Se usará {curr_c} {precio_cierre_over:,.2f} como precio final en el PDF.")
                    else:
                        st.caption("Se calculará el precio base + upgrades seleccionados.")

            st.divider()
            
            # FILTRAR PASAJEROS Y MÁRGENES SEGÚN ORIGEN (Para evitar filtraciones de data oculta en la sesión)
            # Definimos variables locales de conteo para la lógica de cálculo
            c_ad_nac = n_adultos_nac; c_es_nac = n_estud_nac; c_pc_nac = n_pcd_nac; c_ni_nac = n_ninos_nac
            c_ad_ext = n_adultos_ext; c_es_ext = n_estud_ext; c_pc_ext = n_pcd_ext; c_ni_ext = n_ninos_ext
            c_ad_can = n_adultos_can; c_es_can = n_estud_can; c_pc_can = n_pcd_can; c_ni_can = n_ninos_can
            
            # Margen local para cálculo
            m_extra_nac = extra_nac
            m_extra_ext = extra_ext
            m_extra_can = extra_can

            if tipo_t == "Nacional":
                pasajeros_nac = c_ad_nac + c_es_nac + c_pc_nac + c_ni_nac
                pasajeros_ext = 0; pasajeros_can = 0
                # Zero out foreigners for calculation
                c_ad_ext = 0; c_es_ext = 0; c_pc_ext = 0; c_ni_ext = 0
                c_ad_can = 0; c_es_can = 0; c_pc_can = 0; c_ni_can = 0
                m_extra_ext = 0.0; m_extra_can = 0.0
            else:
                pasajeros_nac = 0
                pasajeros_ext = c_ad_ext + c_es_ext + c_pc_ext + c_ni_ext
                pasajeros_can = c_ad_can + c_es_can + c_pc_can + c_ni_can
                # Zero out nationals for calculation
                c_ad_nac = 0; c_es_nac = 0; c_pc_nac = 0; c_ni_nac = 0
                m_extra_nac = 0.0

            # Lógica de Upgrades
            calc_upgrades = 0.0
            calc_tren = 0.0
            tc = 3.8 # Tipo de cambio base para el sistema
            
            if estrategia_v == "General":
                # 🏨 Cálculo ponderado de Hotel según distribución de habitaciones
                if sel_hotel_gen != "Sin Hotel":
                    # Mapeo de tarifas según categoría seleccionada (2*, 3*, 4*)
                    cat_code = sel_hotel_gen.split(" ")[1].replace("*", "") # "2", "3" o "4"
                    t_sgl = st.session_state.get(f'u_h{cat_code}_sgl', 0.0)
                    t_dbl = st.session_state.get(f'u_h{cat_code}_dbl', 0.0)
                    t_mat = st.session_state.get(f'u_h{cat_code}_mat', 0.0)
                    t_tpl = st.session_state.get(f'u_h{cat_code}_tpl', 0.0)
                    t_cua = st.session_state.get(f'u_h{cat_code}_cua', 0.0)
                    
                    # Costo total del grupo = sum(pax * tarifa_pp) * num_noches
                    total_hotel_grupo = (n_sgl * 1 * t_sgl + 
                                         n_dbl * 2 * t_dbl + 
                                         n_mat * 2 * t_mat +
                                         n_tpl * 3 * t_tpl + 
                                         n_cua * 4 * t_cua) * num_noches
                    
                    # El 'upgrade' por persona que entra al cálculo general es el promedio ponderado
                    calc_upgrades = total_hotel_grupo / max(1, total_pasajeros)
                
                if sel_tren_gen == "Tren Local":
                    calc_tren = u_t_local
                elif sel_tren_gen == "Vistadome":
                    calc_tren = (u_t_v * tc) if tipo_t == "Nacional" else u_t_v
                elif sel_tren_gen == "Observatory":
                    calc_tren = (u_t_o * tc) if tipo_t == "Nacional" else u_t_o
                else:
                    calc_tren = 0
            
            # --- NUEVA LÓGICA DE CÁLCULO DETALLADO ---
            # Inicializar acumuladores por categoría
            total_nac = 0.0
            total_ext = 0.0
            total_can = 0.0

            for t in st.session_state.itinerario:
                # Nacionales
                total_nac += (t.get('costo_nac', 0) * c_ad_nac)
                total_nac += (t.get('costo_nac_est', t.get('costo_nac', 0)-70) * (c_es_nac + c_pc_nac))
                total_nac += (t.get('costo_nac_nino', t.get('costo_nac', 0)-40) * c_ni_nac)
                
                # Extranjeros
                total_ext += (t.get('costo_ext', 0) * c_ad_ext)
                total_ext += (t.get('costo_ext_est', t.get('costo_ext', 0)-20) * (c_es_ext + c_pc_ext))
                total_ext += (t.get('costo_ext_nino', t.get('costo_ext', 0)-15) * c_ni_ext)

                # CAN
                total_can += (t.get('costo_can', 0) * c_ad_can)
                total_can += (t.get('costo_can_est', t.get('costo_can', 0)-20) * (c_es_can + c_pc_can))
                total_can += (t.get('costo_can_nino', t.get('costo_can', 0)-15) * c_ni_can)

            real_nac = total_nac + m_extra_nac + (calc_upgrades + calc_tren) * pasajeros_nac
            real_ext = total_ext + m_extra_ext + (calc_upgrades + calc_tren) * pasajeros_ext
            real_can = total_can + m_extra_can + (calc_upgrades + calc_tren) * pasajeros_can
            
            # Variables base para el PDF y UI (sin extras ni upgrades iniciales, se añaden según modo)
            total_nac_pp = total_nac / max(1, pasajeros_nac)
            total_ext_pp = total_ext / max(1, pasajeros_ext)
            total_can_pp = total_can / max(1, pasajeros_can)

            # Para mostrar en la UI los precios promedio con todo incluido
            avg_nac_pp = real_nac / max(1, pasajeros_nac)
            avg_ext_pp = real_ext / max(1, pasajeros_ext)
            avg_can_pp = real_can / max(1, pasajeros_can)

            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.markdown("### 🇵🇪 Nacional")
                st.markdown(f"## S/ {real_nac:,.2f}")
                st.caption(f"**{pasajeros_nac}** pasajeros | Prom: **S/ {avg_nac_pp:,.2f}**")
            
            with col_res2:
                st.markdown("### 🌎 Extranjero")
                st.markdown(f"## USD {real_ext:,.2f}")
                st.caption(f"**{pasajeros_ext}** pasajeros | Prom: **USD {avg_ext_pp:,.2f}**")
            
            with col_res3:
                st.markdown("### 🤝 CAN")
                st.markdown(f"## USD {real_can:,.2f}")
                st.caption(f"**{pasajeros_can}** pasajeros | Prom: **USD {avg_can_pp:,.2f}**")
            
            # --- SECCIÓN FINANCIERA (MOVIDA AQUÍ PARA EVITAR ERRORES DE ORDEN) ---
            st.divider()
            st.markdown("### 💰 Control de Adelanto y Saldo")
            curr_c = "S/" if tipo_t == "Nacional" else "$"
            caf1, caf2 = st.columns(2)
            
            # El monto de referencia es el manual si existe, o la suma de TODOS los reales (Nac + Ext + CAN)
            monto_t_ref = precio_cierre_over if precio_cierre_over > 0 else (real_nac + real_ext + real_can)
            
            m_adelanto = caf1.number_input(f"Monto Pagado ({curr_c})", 
                                           value=float(st.session_state.get('f_monto_adelanto', 0.0)), 
                                           min_value=0.0,
                                           step=10.0,
                                           key="v_adelanto")
            st.session_state.f_monto_adelanto = m_adelanto
            
            s_pendiente = max(0.0, monto_t_ref - m_adelanto)
            caf2.metric("Saldo Pendiente", f"{curr_c} {s_pendiente:,.2f}")
            st.session_state.f_monto_pendiente = s_pendiente

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
                        fallback_cover = os.path.join(base_dir, "assets", "images", "fallback_cover.jpg")
                        
                        target_cat = st.session_state.get('f_categoria', 'Cusco Tradicional')
                        
                        if target_cat == "Perú para el Mundo":
                            cover_img = cover_1 if os.path.exists(cover_1) else fallback_cover
                            t1, t2 = "PERÚ", "PARA EL MUNDO"
                        else:
                            cover_img = cover_2 if os.path.exists(cover_2) else fallback_cover
                            t1, t2 = "CUSCO", "TRADICIONAL"
                        
                        # Logo
                        logo_orig = "Captura de pantalla 2026-01-05 102612.png"
                        logo_path = os.path.abspath(logo_orig if os.path.exists(logo_orig) else os.path.join("assets", "images", "logo_background.png"))
                        
                        # Preparar días con imágenes
                        days_data = []
                        for i, tour in enumerate(st.session_state.itinerario):
                            titulo_actual = tour.get('titulo', '').upper()
                            carpeta = tour.get('carpeta_img', 'general')
                            
                            # SINCRONIZACIÓN INTELIGENTE: 
                            # Si el usuario cambió el título manualmente, intentamos buscar la carpeta correcta
                            if tours_db:
                                match_t = next((t for t in tours_db if t['titulo'].upper() == titulo_actual), None)
                                if match_t:
                                    carpeta = match_t.get('carpeta_img', carpeta)

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
                                'hora_inicio': format_tour_time(tour.get('hora_inicio', '08:00 AM')),
                                'descripcion': tour.get('descripcion', ''),
                                'servicios': servicios_html,
                                'servicios_no': servicios_no_html,
                                'images': imgs,
                                # --- PERSISTENCIA DE DATOS DE EDICIÓN ---
                                'costo_nac': tour.get('costo_nac', 0),
                                'costo_ext': tour.get('costo_ext', 0),
                                'costo_can': tour.get('costo_can', 0),
                                'costo_nac_est': tour.get('costo_nac_est', 0),
                                'costo_nac_nino': tour.get('costo_nac_nino', 0),
                                'costo_ext_est': tour.get('costo_ext_est', 0),
                                'costo_ext_nino': tour.get('costo_ext_nino', 0),
                                'costo_can_est': tour.get('costo_can_est', 0),
                                'costo_can_nino': tour.get('costo_can_nino', 0),
                                'servicios_no_incluye': tour.get('servicios_no_incluye', []),
                                'id_original': tour.get('id', '')
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

                            # Lista de precios de cierre para el PDF
                            precios_cierre_list = []
                            
                            # FILTRAR POR ORIGEN: Solo mostrar lo que el usuario ha elegido como Origen principal
                            if tipo_t == "Nacional" and pasajeros_nac > 0:
                                b_nac = total_nac_pp + (extra_nac/max(1, pasajeros_nac))
                                if estrategia_v == "General": b_nac += (calc_upgrades + calc_tren)
                                precios_cierre_list.append({
                                    'label': 'TOTAL NACIONAL',
                                    'simbolo': 'S/',
                                    'monto_total': f"{b_nac * pasajeros_nac:,.2f}",
                                    'monto_pp': f"{b_nac:,.2f}"
                                })

                            if tipo_t == "Extranjero":
                                if pasajeros_ext > 0 or pasajeros_can > 0:
                                    b_ext = total_ext_pp + (extra_ext/max(1, pasajeros_ext))
                                    b_can = total_can_pp + (extra_can/max(1, pasajeros_can))
                                    
                                    if estrategia_v == "General":
                                        b_ext += (calc_upgrades + calc_tren)
                                        b_can += (calc_upgrades + calc_tren)
                                    
                                    total_combinado = (b_ext * pasajeros_ext) + (b_can * pasajeros_can)
                                    
                                    monto_pp_val = ""
                                    nota_breakdown = ""
                                    if pasajeros_ext > 0 and pasajeros_can > 0:
                                        monto_pp_val = "Ver desglose abajo"
                                        nota_breakdown = f"Incluye {pasajeros_ext} pas. Extranjero (USD {b_ext:,.2f} c/u) y {pasajeros_can} pas. CAN (USD {b_can:,.2f} c/u)"
                                    elif pasajeros_ext > 0:
                                        monto_pp_val = f"USD {b_ext:,.2f}"
                                        nota_breakdown = ""
                                    else:
                                        monto_pp_val = f"USD {b_can:,.2f}"
                                        nota_breakdown = ""

                                    precios_cierre_list.append({
                                        'label': 'TOTAL EXTRANJEROS / CAN',
                                        'simbolo': 'USD',
                                        'monto_total': f"{total_combinado:,.2f}",
                                        'monto_pp': monto_pp_val,
                                        'nota': nota_breakdown
                                    })
                            
                            # Fallback para base_final (usado en comparativas)
                            base_final = total_ext_pp + (extra_ext/max(1, pasajeros_ext))
                            if tipo_t == "Nacional": base_final = total_nac_pp + (extra_nac/max(1, pasajeros_nac))
                            if estrategia_v == "General": base_final += (calc_upgrades + calc_tren)

                            # Matrix Calculation
                            def calc_m(base, extra_t, extra_h_n):
                                return base + extra_t + (extra_h_n * num_noches)

                            pricing_matrix = {}


                            if tipo_t == "Nacional":


                                pricing_matrix['tren_local'] = {


                                    'sin': f"{calc_m(base_final, u_t_local, 0):,.2f}",


                                    'h2': f"{calc_m(base_final, u_t_local, u_h2):,.2f}",


                                    'h3': f"{calc_m(base_final, u_t_local, u_h3):,.2f}",


                                    'h4': f"{calc_m(base_final, u_t_local, u_h4):,.2f}"


                                }



                            pricing_matrix.update({


                                'expedition': {


                                    'sin': f"{calc_m(base_final, 0, 0):,.2f}",


                                    'h2': f"{calc_m(base_final, 0, u_h2):,.2f}",


                                    'h3': f"{calc_m(base_final, 0, u_h3):,.2f}",


                                    'h4': f"{calc_m(base_final, 0, u_h4):,.2f}"


                                },


                                'vistadome': {


                                    'sin': f"{calc_m(base_final, u_t_v * (tc if tipo_t == 'Nacional' else 1), 0):,.2f}",


                                    'h2': f"{calc_m(base_final, u_t_v * (tc if tipo_t == 'Nacional' else 1), u_h2):,.2f}",


                                    'h3': f"{calc_m(base_final, u_t_v * (tc if tipo_t == 'Nacional' else 1), u_h3):,.2f}",


                                    'h4': f"{calc_m(base_final, u_t_v * (tc if tipo_t == 'Nacional' else 1), u_h4):,.2f}"


                                },


                                'observatory': {


                                    'sin': f"{calc_m(base_final, u_t_o * (tc if tipo_t == 'Nacional' else 1), 0):,.2f}",


                                    'h2': f"{calc_m(base_final, u_t_o * (tc if tipo_t == 'Nacional' else 1), u_h2):,.2f}",


                                    'h3': f"{calc_m(base_final, u_t_o * (tc if tipo_t == 'Nacional' else 1), u_h3):,.2f}",


                                    'h4': f"{calc_m(base_final, u_t_o * (tc if tipo_t == 'Nacional' else 1), u_h4):,.2f}"


                                }


                            })


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
                                'llama_img': os.path.abspath(os.path.join("assets", "images", "logo_background.png")),
                                'llama_purchase_img': os.path.abspath(os.path.join("assets", "images", "llama_purchase.png")),
                                'train_exp_img': os.path.abspath(os.path.join("assets", "images", "train_expedition.png")),
                                'train_vis_img': os.path.abspath(os.path.join("assets", "images", "train_vistadome.png")),
                                'train_obs_img': os.path.abspath(os.path.join("assets", "images", "train_observatory.png")),
                                'es_nacional': (tipo_t == "Nacional"),
                                'precios': {
                                    'nac': {
                                        'monto': f"{total_nac_pp + (extra_nac/max(1, pasajeros_nac)):,.2f}",
                                        'total': f"{real_nac:,.2f}"
                                    } if (total_nac > 0) else None,
                                    'ext': {
                                        'monto': f"{total_ext_pp + (extra_ext/max(1, pasajeros_ext)):,.2f}",
                                        'total': f"{real_ext:,.2f}"
                                    } if (total_ext > 0) else None,
                                    'can': {
                                        'monto': f"{total_can_pp + (extra_can/max(1, pasajeros_can)):,.2f}",
                                        'total': f"{real_can:,.2f}"
                                    } if (total_can > 0) else None,
                                },
                                'total_pasajeros': pasajeros_nac if tipo_t == "Nacional" else (pasajeros_ext + pasajeros_can),
                                'precio_cierre': f"{precio_cierre_over:,.2f}" if (precio_cierre_over and precio_cierre_over > 0) else f"{real_nac if tipo_t == 'Nacional' else (real_ext + real_can):,.2f}",
                                'precio_cierre_pp': f"{(precio_cierre_over/max(1, pasajeros_nac if tipo_t == 'Nacional' else (pasajeros_ext + pasajeros_can))):,.2f}" if (precio_cierre_over and precio_cierre_over > 0) else f"{base_final:,.2f}",
                                'monto_adelanto': f"{st.session_state.get('f_monto_adelanto', 0.0):,.2f}",
                                'monto_pendiente': f"{st.session_state.get('f_monto_pendiente', 0.0):,.2f}",
                                'matriz': pricing_matrix,
                                'precio_nota': nota_p.upper(),
                                'canal': st.session_state.get('f_tipo_cliente', 'B2C'),
                                'days': days_data,
                                'precios_cierre': precios_cierre_list,
                                'manual_override': f"{precio_cierre_over:,.2f}" if (precio_cierre_over and precio_cierre_over > 0) else None
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

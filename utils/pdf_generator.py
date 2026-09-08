import os
import base64
import requests
import streamlit as st
from dotenv import load_dotenv
try:
    import markdown
except ImportError:
    markdown = None
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

load_dotenv()

PDFSHIFT_API_URL = "https://api.pdfshift.io/v3/convert/pdf"

# --- CONFIGURACIÓN ---
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "assets" / "templates"
CSS_FILE = BASE_DIR / "assets" / "css" / "report.css"
OUTPUT_FILENAME = "Itinerario_Ventas.pdf"

def find_image(path):
    """Busca la imagen en la ruta dada o en carpetas comunes si no se encuentra."""
    if not path: return None
    path_str = str(path)
    p = Path(path_str)
    
    # 1. Probar ruta tal cual
    if p.exists(): return p
    
    # 2. Probar ruta relativa al BASE_DIR
    # Limpiamos la ruta de posibles prefijos de Windows si estamos en Linux
    clean_filename = path_str.replace('\\', '/').split('/')[-1]
    p_rel = BASE_DIR / clean_filename
    if p_rel.exists(): return p_rel
    
    # 3. Buscar en todo el proyecto por nombre de archivo
    for root, dirs, files in os.walk(BASE_DIR):
        if clean_filename in files:
            return Path(root) / clean_filename
            
    return None

def get_image_as_base64(path):
    """Convierte imagen a Base64 asegurando compatibilidad total."""
    img_path = find_image(path)
    if not img_path:
        # Si no es un archivo local pero es una URL, devolverla tal cual
        if isinstance(path, str) and (path.startswith('http://') or path.startswith('https://')):
            return path
        return ""
    try:
        ext = img_path.suffix[1:].lower()
        mime = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"data:{mime};base64,{b64}"
    except Exception as e:
        print(f"Error procesando {path}: {e}")
        return ""

def get_pdfshift_api_key():
    """Obtiene la API key de PDFShift desde st.secrets (Streamlit Cloud) o .env (local)."""
    try:
        return st.secrets.get("PDFSHIFT_API_KEY") or os.getenv("PDFSHIFT_API_KEY")
    except Exception:
        return os.getenv("PDFSHIFT_API_KEY")

def render_html_preview(itinerary_data, is_preview=False):
    """Renderiza el itinerario a HTML con imágenes en Base64 para la vista previa."""
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # Cargar CSS
    css_content = ""
    if CSS_FILE.exists():
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()

    # Convertir TODAS las imágenes a Base64
    itinerary_data['logo_url'] = get_image_as_base64(itinerary_data.get('logo_url'))
    itinerary_data['logo_cover_url'] = get_image_as_base64(itinerary_data.get('logo_cover_url'))
    itinerary_data['cover_url'] = get_image_as_base64(itinerary_data.get('cover_url'))
    itinerary_data['llama_img'] = get_image_as_base64(itinerary_data.get('llama_img'))
    itinerary_data['llama_purchase_img'] = get_image_as_base64(itinerary_data.get('llama_purchase_img'))
    itinerary_data['train_exp_img'] = get_image_as_base64(itinerary_data.get('train_exp_img'))
    itinerary_data['train_vis_img'] = get_image_as_base64(itinerary_data.get('train_vis_img'))
    itinerary_data['train_obs_img'] = get_image_as_base64(itinerary_data.get('train_obs_img'))

    # Imágenes de Acreditación Legal (Método Directo Robusto)
    def load_direct_b64(rel_path):
        abs_path = BASE_DIR / rel_path
        if abs_path.exists():
            try:
                ext = abs_path.suffix[1:].lower()
                mime = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
                with open(abs_path, "rb") as f:
                    content = f.read()
                    b64 = base64.b64encode(content).decode('utf-8')
                    return f"data:{mime};base64,{b64}"
            except Exception as e:
                return ""
        return ""

    itinerary_data['ruc_img_url'] = load_direct_b64("assets/img/accreditations/ruc_sunat.png")
    itinerary_data['constancia_img_url'] = load_direct_b64("assets/img/accreditations/constancia_gercetur.png")
    
    # Redes Sociales
    itinerary_data['fb_icon'] = load_direct_b64("assets/Logo de Redes Sociales/Logo de Facebook.png")
    itinerary_data['ig_icon'] = load_direct_b64("assets/Logo de Redes Sociales/Logo de Instagram.webp")
    itinerary_data['tt_icon'] = load_direct_b64("assets/Logo de Redes Sociales/Logo de Tik Tok.webp")
    itinerary_data['yt_icon'] = load_direct_b64("assets/Logo de Redes Sociales/Logo de Youtube.webp")
    itinerary_data['ta_icon'] = load_direct_b64("assets/Logo de Redes Sociales/Logo de Tripadvisor.png")

    # Intentar importar markdown aquí por si se instaló después del arranque
    global markdown
    if markdown is None:
        try:
            import markdown as md
            markdown = md
        except ImportError:
            pass

    for day in itinerary_data.get('days', []):
        day['images'] = [get_image_as_base64(img) for img in day.get('images', [])]
        # Convertir descripción de Markdown a HTML si el import fue exitoso
        if markdown and day.get('descripcion'):
            # Usamos una conversión más robusta
            day['descripcion'] = markdown.markdown(str(day['descripcion']), extensions=['nl2br', 'sane_lists'])

    html_content = template.render(**itinerary_data)
    
    # Inyectar CSS directamente en el HTML
    if css_content:
        # Reset básico y forzado de márgenes y tamaños SVG, aplicable TANTO en PDF como web
        extra_css = """
        html, body { margin: 0 !important; padding: 0 !important; }
        .service-icon, .service-icon svg { width: 35px !important; height: 35px !important; } 
        .pin-icon { width: 45px !important; height: 45px !important; }
        """
        
        # Inyectar variables de escala adaptativa solo si es modo vista previa web (Simulador PDF)
        if is_preview:
            # Simulamos un visor de PDF separando A4 con fondo gris y eliminando márgenes de body
            viewer_css = """
            html, body {
                margin: 0 !important;
                padding: 20px 0 !important;
                background-color: #525659 !important; /* Gris típico de PDF */
                display: flex !important;
                flex-direction: column;
                align-items: center;
                gap: 40px !important; /* Separación entre cada página web = hojas separadas */
                overflow-x: hidden;
            }
            .cover-container, .page-container, .premium-appendix-page {
                box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important; /* Sombra de la hoja */
                margin: 0 !important;
                page-break-after: avoid !important; /* Elimina hojas blancas extra en el renderizado web */
                flex-shrink: 0;
            }
            """
            extra_css += viewer_css
            
        style_tag = f"<style>{css_content}\n{extra_css}</style>"
        html_content = html_content.replace('</head>', f'{style_tag}\n</head>')

    return html_content, css_content

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """Genera el PDF llamando a la API de PDFShift (sin depender de Chromium local)."""
    api_key = get_pdfshift_api_key()
    if not api_key:
        raise Exception(
            "No se encontró la API KEY de PDFShift (configura PDFSHIFT_API_KEY en st.secrets o .env)."
        )

    html_content, _ = render_html_preview(itinerary_data, is_preview=False)

    response = requests.post(
        PDFSHIFT_API_URL,
        auth=(api_key, ""),
        json={
            "source": html_content,
            "format": "A4",
            "margin": "0",
            "print_media_type": True,
        },
        timeout=120,
    )

    if response.status_code != 200:
        raise Exception(f"PDFShift falló ({response.status_code}): {response.text}")

    output_path = BASE_DIR / output_filename
    with open(output_path, "wb") as f:
        f.write(response.content)

    return str(output_path)

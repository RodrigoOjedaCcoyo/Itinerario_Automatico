import jinja2
import pdfkit
import os
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / 'assets' / 'templates'
CSS_FILE = BASE_DIR / 'assets' / 'css' / 'report.css'

# Mapas de iconos SVG (Hardcoded for portabilidad, se podría mover a un JSON)
ICON_MAP = {
    'transporte': '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle>',
    'traslado': '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle>',
    'guía': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
    'asistencia': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
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

def get_svg(text, default_key):
    text_lower = text.lower()
    for key, svg in ICON_MAP.items():
        if key in text_lower:
            return svg
    return ICON_MAP[default_key]

def obtener_imagenes_tour(nombre_carpeta):
    base_path = BASE_DIR / 'assets' / 'img' / 'tours' / nombre_carpeta
    if not base_path.exists():
        base_path = BASE_DIR / 'assets' / 'img' / 'tours' / 'general'
    
    imagenes = []
    if base_path.exists():
        for f in base_path.iterdir():
            if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                # Convertimos a ruta absoluta para wkhtmltopdf
                imagenes.append(str(f.absolute()).replace('\\', '/'))
    
    while len(imagenes) < 5:
        imagenes.append("https://via.placeholder.com/400x300?text=Foto+Tour")
        
    return imagenes[:5]

import base64
import mimetypes

def image_to_base64(image_path):
    """Convierte una imagen local a string Base64 para incrustar en HTML."""
    path = Path(image_path)
    if not path.exists():
        return ""
    
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = 'image/png'
        
    try:
        with open(path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{b64_str}"
    except Exception as e:
        print(f"Error al convertir imagen {image_path}: {e}")
        return ""

def generate_pdf(itinerary_data, output_filename="Itinerario_Generado.pdf"):
    """
    Genera un PDF a partir de los datos del itinerario.
    """
    
    # 1. Prepare Environment
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template('report.html')
    
    # 1.5. Convert Critical Images to Base64 (Robustez para Cloud)
    # Convertimos las imágenes principales si son rutas locales
    if 'cover_img' in itinerary_data and os.path.exists(itinerary_data['cover_img']):
        itinerary_data['cover_img'] = image_to_base64(itinerary_data['cover_img'])
        
    if 'logo_url' in itinerary_data and os.path.exists(itinerary_data['logo_url']):
        itinerary_data['logo_url'] = image_to_base64(itinerary_data['logo_url'])

    if 'logo_cover_url' in itinerary_data and os.path.exists(itinerary_data['logo_cover_url']):
        itinerary_data['logo_cover_url'] = image_to_base64(itinerary_data['logo_cover_url'])
        
    if 'llama_img' in itinerary_data and os.path.exists(itinerary_data['llama_img']):
        itinerary_data['llama_img'] = image_to_base64(itinerary_data['llama_img'])

    # 2. Prepare Data Enrichment (SVG, Images)
    enriched_days = []
    for day in itinerary_data['days']:
        # Process Services SVG
        s_incluye = []
        for s in day.get('servicios', []):
            s_incluye.append({'text': s, 'svg': get_svg(s, 'default_in')})
            
        s_no = []
        for s in day.get('servicios_no_incluye', []):
            s_no.append({'text': s, 'svg': get_svg(s, 'default_out')})
            
        # Process Images (Convert to Base64 as well)
        imgs_paths = obtener_imagenes_tour(day.get('carpeta_img', 'general'))
        imgs_b64 = []
        for img_p in imgs_paths:
            if img_p.startswith('http'):
                imgs_b64.append(img_p)
            else:
                imgs_b64.append(image_to_base64(img_p))
        
        day_new = day.copy()
        day_new['servicios_incluye_svg'] = s_incluye
        day_new['servicios_no_svg'] = s_no
        day_new['images'] = imgs_b64
        enriched_days.append(day_new)
        
    itinerary_data['days'] = enriched_days
    
    # 3. Handle CSS (External File Strategy for Robustness)
    # We write the CSS to a temp file alongside the HTML so wkhtmltopdf resolves it naturally
    temp_css = BASE_DIR / "temp_style.css"
    with open(CSS_FILE, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    with open(temp_css, 'w', encoding='utf-8') as f:
        f.write(css_content)

    # 4. Render HTML
    # We pass css_url relative to the HTML file
    print(f"DEBUG: Linking CSS from {temp_css}")
    html_content = template.render(**itinerary_data, css_url="temp_style.css")
    
    # 5. Generate PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'disable-smart-shrinking': '', 
        'zoom': '1.33', # 1.33 = 1280px / 960px approx ratio to fill A4 width on standard DPI
        'dpi': '96',
        'viewport-size': '1280x1024',
        'quiet': '',
        'print-media-type': '' 
    }
    
    temp_html = BASE_DIR / "temp_report.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    output_path = BASE_DIR / output_filename
    
    try:
        pdfkit.from_file(str(temp_html), str(output_path), options=options)
    except Exception as e:
        print(f"Error generando PDF: {e}")
        # Even if it fails, sometimes it generates.
        pass
        
    # Cleanup
    if temp_html.exists():
        temp_html.unlink()
    if temp_css.exists():
        temp_css.unlink()
        
    return str(output_path)

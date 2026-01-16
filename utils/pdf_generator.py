import os
import subprocess
import base64
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- CONFIGURACIÓN ---
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "assets" / "templates"
CSS_FILE = BASE_DIR / "assets" / "css" / "report.css"
OUTPUT_FILENAME = "Itinerario_Ventas.pdf"

# Ruta de Edge (Verificada)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def image_to_base64(image_path):
    """Convierte una imagen local a cadena Base64."""
    try:
        with open(image_path, "rb") as img_file:
            return f"data:image/{Path(image_path).suffix[1:]};base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    except Exception as e:
        print(f"Error convirtiendo imagen {image_path}: {e}")
        return ""

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Genera un PDF usando Microsoft Edge en modo headless (motor Chromium).
    Esto garantiza que el diseño sea idéntico al navegador.
    """
    
    # 1. Configurar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Procesar imágenes del itinerario (Base64)
    # Convertimos logos generales
    if 'logo_url' in itinerary_data and os.path.exists(itinerary_data['logo_url']):
        itinerary_data['logo_url'] = image_to_base64(itinerary_data['logo_url'])

    if 'logo_cover_url' in itinerary_data and os.path.exists(itinerary_data['logo_cover_url']):
        itinerary_data['logo_cover_url'] = image_to_base64(itinerary_data['logo_cover_url'])
        
    if 'llama_img' in itinerary_data and os.path.exists(itinerary_data['llama_img']):
        itinerary_data['llama_img'] = image_to_base64(itinerary_data['llama_img'])
        
    # Procesar imágenes de cada día
    enriched_days = []
    for day in itinerary_data.get('days', []):
        processed_images = []
        for img_path in day.get('images', []):
            # Las imágenes vienen como File URIs o rutas, aseguramos formato
            clean_path = img_path.replace('file:///', '')
            # En Windows a veces pythen devuelve /C:/...
            if os.name == 'nt' and clean_path.startswith('/') and ':' in clean_path:
                 clean_path = clean_path.lstrip('/')
                 
            if os.path.exists(clean_path):
                processed_images.append(image_to_base64(clean_path))
            else:
                # Si es una URL remota o placeholder, dejarla tal cual
                processed_images.append(img_path)
        
        day['images'] = processed_images
        enriched_days.append(day)
        
    itinerary_data['days'] = enriched_days
    
    # 3. Leer CSS e inyectarlo (Para Edge, mejor inyectar directo o usar archivo local)
    # Vamos a usar archivo temporal para el HTML completo
    # NOTA: Edge renderiza mejor si el CSS está inline o linkeado localmente.
    # Usaremos link relativo para mantenerlo simple.
    
    # 4. Renderizar HTML
    # Pasamos el CSS como URL relativa para que el HTML temporal lo encuentre
    # Aseguramos que el CSS esté junto al HTML
    
    html_content = template.render(**itinerary_data, css_url="../css/report.css")
    
    # Guardamos en la raíz para que las rutas relativas funcionen (assets/...)
    temp_html_path = BASE_DIR / "temp_report.html"
    
    # Hack: Para asegurar que cargue el CSS si está en assets/css/
    # Modificamos la ruta en el HTML renderizado si es necesario, 
    # pero como guardamos temp_report.html en BASE_DIR, la ruta assets/css/report.css es válida.
    html_content = html_content.replace('../css/report.css', 'assets/css/report.css')
    
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    
    # 5. Ejecutar Edge Headless
    # Comando: msedge --headless --print-to-pdf=output.pdf --no-pdf-header-footer input.html
    # Agregamos --disable-gpu y --run-all-compositor-stages-before-draw para asegurar renderizado completo
    
    cmd = [
        str(EDGE_PATH),
        '--headless',
        f'--print-to-pdf={str(output_path)}',
        '--no-pdf-header-footer',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw', # Esperar a que carguen imágenes
        f'file:///{str(temp_html_path)}'
    ]
    
    print(f"Generando PDF con Edge: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"PDF generado exitosamente en: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando Edge: {e}")
        # Fallback o notificación de error
        raise e
    finally:
        # Limpieza
        if temp_html_path.exists():
            temp_html_path.unlink()

    return str(output_path)

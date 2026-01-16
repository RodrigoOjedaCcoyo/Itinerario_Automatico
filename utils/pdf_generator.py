import os
import base64
import subprocess
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- CONFIGURACIÓN ---
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "assets" / "templates"
CSS_FILE = BASE_DIR / "assets" / "css" / "report.css"
OUTPUT_FILENAME = "Itinerario_Ventas.pdf"

def image_to_base64(image_path):
    """Convierte una imagen local a cadena Base64."""
    try:
        ext = Path(image_path).suffix[1:].lower()
        mime = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
        with open(image_path, "rb") as img_file:
            return f"data:{mime};base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    except Exception as e:
        print(f"Error convirtiendo imagen {image_path}: {e}")
        return ""

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Genera un PDF usando Playwright CLI.
    Funciona en local Y en Streamlit Cloud.
    """
    
    # 1. Configurar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Procesar imágenes del itinerario (Base64)
    if 'logo_url' in itinerary_data and os.path.exists(itinerary_data['logo_url']):
        itinerary_data['logo_url'] = image_to_base64(itinerary_data['logo_url'])

    if 'logo_cover_url' in itinerary_data and os.path.exists(itinerary_data['logo_cover_url']):
        itinerary_data['logo_cover_url'] = image_to_base64(itinerary_data['logo_cover_url'])
        
    if 'llama_img' in itinerary_data and os.path.exists(itinerary_data['llama_img']):
        itinerary_data['llama_img'] = image_to_base64(itinerary_data['llama_img'])
    
    if 'cover_url' in itinerary_data and os.path.exists(itinerary_data['cover_url']):
        itinerary_data['cover_url'] = image_to_base64(itinerary_data['cover_url'])
        
    # Procesar imágenes de cada día
    enriched_days = []
    for day in itinerary_data.get('days', []):
        processed_images = []
        for img_path in day.get('images', []):
            if isinstance(img_path, str) and os.path.exists(img_path):
                processed_images.append(image_to_base64(img_path))
            else:
                processed_images.append(img_path)
        
        day['images'] = processed_images
        enriched_days.append(day)
        
    itinerary_data['days'] = enriched_days
    
    # 3. Renderizar HTML
    html_content = template.render(**itinerary_data, css_url="assets/css/report.css")
    
    # Guardamos el HTML temporal
    temp_html_path = BASE_DIR / "temp_report.html"
    
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    
    # 4. Generar PDF con Playwright via script externo
    print("Generando PDF con Playwright...")
    
    # Crear script temporal de Python para ejecutar Playwright fuera del loop de Streamlit
    script_content = f'''
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('file:///{str(temp_html_path).replace(chr(92), "/")}', wait_until='networkidle')
        await page.pdf(
            path='{str(output_path).replace(chr(92), "/")}',
            format='A4',
            margin={{'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}},
            print_background=True,
            prefer_css_page_size=True
        )
        await browser.close()
        print("PDF generado exitosamente")

asyncio.run(main())
'''
    
    script_path = BASE_DIR / "temp_pdf_script.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    try:
        # Ejecutar el script en un proceso separado usando el mismo ejecutable de python
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(BASE_DIR)
        )
        
        if result.returncode != 0:
            print(f"Error Playwright: {result.stderr}")
            # Si el error es que no está instalado en linux/cloud, intentamos instalarlo
            if "browser has been closed" in result.stderr or "Executable doesn't exist" in result.stderr:
                subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
                # Re-intentar
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=60, cwd=str(BASE_DIR))
                if result.returncode != 0:
                     raise Exception(f"Error tras re-instalacion: {result.stderr}")
            else:
                raise Exception(f"Error generando PDF: {result.stderr}")
        
        print(f"PDF generado en: {output_path}")
        
    except subprocess.TimeoutExpired:
        raise Exception("Tiempo de espera agotado generando el PDF")
    except Exception as e:
        print(f"Error: {e}")
        raise e
    finally:
        # Limpieza
        if temp_html_path.exists():
            temp_html_path.unlink()
        if script_path.exists():
            script_path.unlink()

    return str(output_path)

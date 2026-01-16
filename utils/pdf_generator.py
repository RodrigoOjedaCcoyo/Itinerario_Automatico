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
        # Si ya es base64 o URL, retornar tal cual
        if isinstance(image_path, str) and (image_path.startswith('data:image') or image_path.startswith('http')):
            return image_path
            
        path = Path(image_path)
        if not path.exists():
            print(f"Advertencia: Imagen no encontrada en {image_path}")
            return ""
            
        ext = path.suffix[1:].lower()
        mime = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
        with open(path, "rb") as img_file:
            return f"data:{mime};base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    except Exception as e:
        print(f"Error convirtiendo imagen {image_path}: {e}")
        return ""

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Genera un PDF inyectando TODO (CSS e Imágenes) directamente en el HTML.
    Esto garantiza que las imágenes aparezcan en cualquier entorno (Local/Cloud).
    """
    
    # 1. Configurar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Procesar TODAS las imágenes a Base64
    itinerary_data['logo_url'] = image_to_base64(itinerary_data.get('logo_url', ''))
    itinerary_data['logo_cover_url'] = image_to_base64(itinerary_data.get('logo_cover_url', ''))
    itinerary_data['llama_img'] = image_to_base64(itinerary_data.get('llama_img', ''))
    itinerary_data['cover_url'] = image_to_base64(itinerary_data.get('cover_url', ''))
        
    for day in itinerary_data.get('days', []):
        day['images'] = [image_to_base64(img) for img in day.get('images', [])]
    
    # 3. Leer CSS e inyectarlo directamente
    css_content = ""
    if CSS_FILE.exists():
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()
    
    # 4. Renderizar HTML (Pasamos el CSS como texto para ponerlo en <style>)
    html_content = template.render(**itinerary_data, inline_css=css_content)
    
    # Guardamos el HTML temporal
    temp_html_path = BASE_DIR / "temp_report.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    script_path = BASE_DIR / "temp_pdf_script.py"
    
    # 5. Script de Playwright (asegurando rutas compatibles)
    script_content = f'''
import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            # Cargar HTML
            await page.goto('file:///{str(temp_html_path).replace(chr(92), "/")}', wait_until='networkidle')
            # Esperar un poco extra para que el renderizado de base64 termine
            await asyncio.sleep(1)
            await page.pdf(
                path='{str(output_path).replace(chr(92), "/")}',
                format='A4',
                margin={{'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}},
                print_background=True,
                prefer_css_page_size=True
            )
            await browser.close()
    except Exception as e:
        print(f"Error en script: {{e}}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
'''
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(BASE_DIR)
        )
        
        if result.returncode != 0:
            # Si falta el navegador, intentar instalarlo
            if "Executable doesn't exist" in result.stderr:
                subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                raise Exception(f"Playwright Error: {result.stderr}")
        
    finally:
        if temp_html_path.exists(): temp_html_path.unlink()
        if script_path.exists(): script_path.unlink()

    return str(output_path)

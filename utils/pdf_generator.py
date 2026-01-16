import os
import subprocess
import sys
import base64
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- CONFIGURACIÓN ---
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "assets" / "templates"
CSS_FILE = BASE_DIR / "assets" / "css" / "report.css"
OUTPUT_FILENAME = "Itinerario_Ventas.pdf"

def get_image_as_base64(path):
    """Convierte una imagen a Base64 para asegurar que se vea en el PDF."""
    try:
        if not path: return ""
        p = Path(path)
        if not p.exists():
            # Intentar ruta relativa si la absoluta falla
            p = BASE_DIR / path
            if not p.exists(): return ""
            
        ext = p.suffix[1:].lower()
        mime = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
        with open(p, "rb") as f:
            return f"data:{mime};base64,{base64.encodebytes(f.read()).decode('utf-8')}"
    except:
        return ""

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Versión ROBUSTA:
    1. Inyecta el CSS directamente (Cero iconos gigantes).
    2. Convierte portadas y logos a Base64 (Cero fotos faltantes en piezas clave).
    3. Usa rutas de archivo directas para fotos de tours.
    """
    
    # 1. Preparar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Leer CSS e inyectarlo (SOLUCIÓN DEFINITIVA A ICONOS GIGANTES)
    css_content = ""
    if CSS_FILE.exists():
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()

    # 3. Convertir elementos CRÍTICOS a Base64
    itinerary_data['logo_url'] = get_image_as_base64(itinerary_data.get('logo_url'))
    itinerary_data['logo_cover_url'] = get_image_as_base64(itinerary_data.get('logo_cover_url'))
    itinerary_data['cover_url'] = get_image_as_base64(itinerary_data.get('cover_url'))
    itinerary_data['llama_img'] = get_image_as_base64(itinerary_data.get('llama_img'))

    # 4. Fotos de los días como URI de archivo (Más rápido que base64 para muchas fotos)
    for day in itinerary_data.get('days', []):
        new_imgs = []
        for img in day.get('images', []):
            if isinstance(img, str) and os.path.exists(img):
                new_imgs.append(Path(img).absolute().as_uri())
            else:
                new_imgs.append(img)
        day['images'] = new_imgs

    # 5. Renderizar HTML
    html_content = template.render(**itinerary_data, inline_css=css_content)
    
    temp_html_path = BASE_DIR / "temp_report.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    script_path = BASE_DIR / "temp_pdf_script.py"
    
    # 6. Script Playwright Ultra-Seguro
    script_content = f'''
import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            # Cargar HTML local
            await page.goto(r'file:///{str(temp_html_path).replace(chr(92), "/")}', wait_until='networkidle')
            # Esperar carga de imágenes
            await asyncio.sleep(2) 
            await page.pdf(
                path=r'{str(output_path).replace(chr(92), "/")}',
                format='A4',
                print_background=True,
                margin={{'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}},
                prefer_css_page_size=True
            )
            await browser.close()
    except Exception as e:
        print(f"ERROR: {{e}}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
'''
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    try:
        subprocess.run([sys.executable, str(script_path)], check=True, timeout=60)
    finally:
        if temp_html_path.exists(): temp_html_path.unlink()
        if script_path.exists(): script_path.unlink()

    return str(output_path)

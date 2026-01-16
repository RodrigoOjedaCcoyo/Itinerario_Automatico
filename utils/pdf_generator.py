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
    if not path:
        return ""
    try:
        p = Path(path)
        if not p.is_absolute():
            p = BASE_DIR / path
            
        if not p.exists():
            print(f"ERROR: No existe la imagen en {p}")
            return ""
            
        ext = p.suffix[1:].lower()
        mime = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
        with open(p, "rb") as f:
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    except Exception as e:
        print(f"Error convirtiendo {path} a base64: {e}")
        return ""

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Versión ULTRA-ROBUSTA para Cloud y Local:
    1. Inyecta el CSS directamente (Sin archivos externos).
    2. Convierte ABSOLUTAMENTE TODAS las imágenes a Base64.
    3. Ejecuta Playwright en proceso separado.
    """
    
    # 1. Preparar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Leer CSS e inyectarlo
    css_content = ""
    if CSS_FILE.exists():
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()

    # 3. Convertir TODO a Base64 (Única forma 100% segura en la nube)
    itinerary_data['logo_url'] = get_image_as_base64(itinerary_data.get('logo_url'))
    itinerary_data['logo_cover_url'] = get_image_as_base64(itinerary_data.get('logo_cover_url'))
    itinerary_data['cover_url'] = get_image_as_base64(itinerary_data.get('cover_url'))
    itinerary_data['llama_img'] = get_image_as_base64(itinerary_data.get('llama_img'))

    # Fotos de los días a Base64
    for day in itinerary_data.get('days', []):
        day['images'] = [get_image_as_base64(img) for img in day.get('images', [])]

    # 4. Renderizar HTML
    html_content = template.render(**itinerary_data, inline_css=css_content)
    
    # Guardar HTML temporal
    temp_html_path = BASE_DIR / "temp_report.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    script_path = BASE_DIR / "temp_pdf_script.py"
    
    # 5. Script Playwright
    # Usamos wait_until='load' porque 'networkidle' puede tardar mucho con base64 pesados
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
            await page.goto(r'file:///{str(temp_html_path).replace(chr(92), "/")}', wait_until='load', timeout=60000)
            # Pequeña espera para renderizado
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
        # Ejecutar el script
        subprocess.run([sys.executable, str(script_path)], check=True, timeout=90)
    finally:
        # Limpieza
        if temp_html_path.exists(): temp_html_path.unlink()
        if script_path.exists(): script_path.unlink()

    return str(output_path)

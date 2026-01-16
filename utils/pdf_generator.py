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

def find_image(path):
    """Busca la imagen en la ruta dada o en carpetas comunes si no se encuentra."""
    if not path: return None
    p = Path(path)
    
    # 1. Probar ruta tal cual
    if p.exists(): return p
    
    # 2. Probar ruta relativa al BASE_DIR
    p_rel = BASE_DIR / path.replace('\\', '/').split('/')[-1]
    if p_rel.exists(): return p_rel
    
    # 3. Buscar en todo el proyecto por nombre de archivo
    filename = os.path.basename(path)
    for root, dirs, files in os.walk(BASE_DIR):
        if filename in files:
            return Path(root) / filename
            
    return None

def get_image_as_base64(path):
    """Convierte imagen a Base64 asegurando compatibilidad total."""
    img_path = find_image(path)
    if not img_path:
        print(f"ADVERTENCIA: No se encontró la imagen: {path}")
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

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # Cargar CSS
    css_content = ""
    if CSS_FILE.exists():
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            # Escapar comillas para el script de JS
            css_content = f.read().replace('"', '\\"').replace('\n', ' ')

    # Convertir TODAS las imágenes a Base64
    itinerary_data['logo_url'] = get_image_as_base64(itinerary_data.get('logo_url'))
    itinerary_data['logo_cover_url'] = get_image_as_base64(itinerary_data.get('logo_cover_url'))
    itinerary_data['cover_url'] = get_image_as_base64(itinerary_data.get('cover_url'))
    itinerary_data['llama_img'] = get_image_as_base64(itinerary_data.get('llama_img'))

    for day in itinerary_data.get('days', []):
        day['images'] = [get_image_as_base64(img) for img in day.get('images', [])]

    html_content = template.render(**itinerary_data)
    
    temp_html_path = BASE_DIR / "temp_report.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    script_path = BASE_DIR / "temp_pdf_script.py"
    
    # Script Playwright
    script_content = f'''
import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(r'file:///{str(temp_html_path).replace(chr(92), "/")}', wait_until='load')
            
            # Inyectar CSS
            await page.add_style_tag(content="{css_content}")
            
            # Forzar iconos de nuevo (por si acaso)
            await page.add_style_tag(content=".service-icon, .service-icon svg {{ width: 32px !important; height: 32px !important; }} .pin-icon, .pin-icon svg {{ width: 45px !important; height: 45px !important; }}")
            
            await asyncio.sleep(3) # Esperar a que el navegador "digiera" el base64
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
        subprocess.run([sys.executable, str(script_path)], check=True, timeout=120)
    finally:
        if temp_html_path.exists(): temp_html_path.unlink()
        if script_path.exists(): script_path.unlink()

    return str(output_path)

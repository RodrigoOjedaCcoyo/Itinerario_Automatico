import os
import subprocess
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- CONFIGURACIÓN ---
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "assets" / "templates"
CSS_FILE = BASE_DIR / "assets" / "css" / "report.css"
OUTPUT_FILENAME = "Itinerario_Ventas.pdf"

# URL Base de tus imágenes en GitHub
GITHUB_BASE_URL = "https://raw.githubusercontent.com/RodrigoOjedaCcoyo/Itinerario_Automatico/main/"

def get_github_url(local_path):
    """Convierte una ruta local a una URL de GitHub."""
    if not local_path:
        return ""
    if str(local_path).startswith('http'):
        return local_path
        
    try:
        # Normalizar ruta para Windows/Linux
        clean_path = str(local_path).replace('\\', '/')
        if 'assets/' in clean_path:
            rel_path = clean_path.split('assets/')[-1]
            return f"{GITHUB_BASE_URL}assets/{rel_path}"
        # Si es un archivo en la raíz
        return f"{GITHUB_BASE_URL}{os.path.basename(clean_path)}"
    except:
        return local_path

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Genera un PDF inyectando el CSS local para asegurar diseño perfecto,
    pero cargando imágenes desde GitHub para ligereza.
    """
    
    # 1. Configurar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Convertir imágenes a GitHub URLs
    itinerary_data['logo_url'] = get_github_url(itinerary_data.get('logo_url'))
    itinerary_data['logo_cover_url'] = get_github_url(itinerary_data.get('logo_cover_url'))
    itinerary_data['llama_img'] = get_github_url(itinerary_data.get('llama_img'))
    itinerary_data['cover_url'] = get_github_url(itinerary_data.get('cover_url'))
        
    for day in itinerary_data.get('days', []):
        day['images'] = [get_github_url(img) for img in day.get('images', [])]
    
    # 3. Leer CSS local e inyectarlo (EVITA ICONOS GIGANTES)
    css_content = ""
    if CSS_FILE.exists():
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()
    
    # 4. Renderizar HTML
    html_content = template.render(**itinerary_data, inline_css=css_content)
    
    # Guardamos el HTML temporal
    temp_html_path = BASE_DIR / "temp_report.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    script_path = BASE_DIR / "temp_pdf_script.py"
    
    # 5. Script de Playwright (Chrome)
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
            # Esperar a que las fotos de GitHub terminen de bajar
            await asyncio.sleep(2) 
            await page.pdf(
                path='{str(output_path).replace(chr(92), "/")}',
                format='A4',
                margin={{'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}},
                print_background=True,
                prefer_css_page_size=True
            )
            await browser.close()
    except Exception as e:
        print(f"Error: {{e}}", file=sys.stderr)
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

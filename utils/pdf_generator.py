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

# URL Base de tus imágenes en GitHub (Para que la nube las vea siempre)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/RodrigoOjedaCcoyo/Itinerario_Automatico/main/"

def get_github_url(local_path):
    """Convierte una ruta local a una URL de GitHub."""
    if not local_path:
        return ""
    if str(local_path).startswith('http'):
        return local_path
        
    # Convertir a ruta relativa respecto a la raíz del proyecto
    try:
        rel_path = os.path.relpath(local_path, BASE_DIR).replace('\\', '/')
        # Si la imagen está en la raíz, rel_path será solo el nombre
        return f"{GITHUB_BASE_URL}{rel_path}"
    except:
        return local_path

def generate_pdf(itinerary_data, output_filename=OUTPUT_FILENAME):
    """
    Genera un PDF usando Playwright cargando recursos desde GitHub.
    """
    
    # 1. Configurar Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    
    # 2. Convertir rutas locales a URLs de GitHub
    itinerary_data['logo_url'] = get_github_url(itinerary_data.get('logo_url'))
    itinerary_data['logo_cover_url'] = get_github_url(itinerary_data.get('logo_cover_url'))
    itinerary_data['llama_img'] = get_github_url(itinerary_data.get('llama_img'))
    itinerary_data['cover_url'] = get_github_url(itinerary_data.get('cover_url'))
        
    for day in itinerary_data.get('days', []):
        day['images'] = [get_github_url(img) for img in day.get('images', [])]
    
    # 3. Renderizar HTML (Usamos enlace al CSS de GitHub para máxima compatibilidad)
    css_github_url = f"{GITHUB_BASE_URL}assets/css/report.css"
    html_content = template.render(**itinerary_data, css_url=css_github_url)
    
    # Guardamos el HTML temporal
    temp_html_path = BASE_DIR / "temp_report.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_path = BASE_DIR / output_filename
    script_path = BASE_DIR / "temp_pdf_script.py"
    
    # 4. Script de Playwright
    script_content = f'''
import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            # Cargar HTML desde el archivo temporal
            await page.goto('file:///{str(temp_html_path).replace(chr(92), "/")}', wait_until='networkidle')
            # Esperar a que carguen las fotos de GitHub
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

import os, sys
os.environ["PYTHONPATH"] = "c:/Itinerarios/Itinerario_Automatico"
sys.path.append("c:/Itinerarios/Itinerario_Automatico")

from utils.pdf_generator import render_html_preview

dummy_data = {
    'estrategia': 'General',
    'title_1': 'MOCK',
    'title_2': 'MOCK2',
    'cover_url': 'mock.jpg',
    'fechas': '12/12/26',
    'duracion': '3D',
    'days': [],
    'labels': {},
    'precios_cierre': []
}

html, css = render_html_preview(dummy_data, is_preview=True)
with open('c:/Itinerarios/Itinerario_Automatico/temp_debug.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")

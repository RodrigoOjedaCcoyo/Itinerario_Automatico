import os

file_path = r"c:\Itinerarios\Itinerario_Automatico\modules\ventas\ui.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_button_block = False
i = 0

while i < len(lines):
    line = lines[i]
    if 'if c_btn1.button("🔥 GENERAR ITINERARIO PDF"):' in line:
        indent = line.split('if')[0]
        
        # Inserciones:
        new_lines.append(f'{indent}preview_clicked = False\n')
        new_lines.append(f'{indent}gen_pdf_clicked = False\n')
        new_lines.append(f'{indent}tab_pdf, tab_prev = st.tabs(["📄 Generar PDF Final", "👁️ Vista Previa en Vivo"])\n')
        new_lines.append(f'{indent}with tab_pdf:\n')
        new_lines.append(f'{indent}    if st.button("🔥 GENERAR ITINERARIO PDF", use_container_width=True):\n')
        new_lines.append(f'{indent}        gen_pdf_clicked = True\n')
        new_lines.append(f'{indent}with tab_prev:\n')
        new_lines.append(f'{indent}    if st.button("🔄 Generar / Actualizar Vista Previa", type="primary", use_container_width=True):\n')
        new_lines.append(f'{indent}        preview_clicked = True\n')
        new_lines.append(f'\n{indent}if gen_pdf_clicked or preview_clicked:\n')
        i += 1
        continue

    if 'with st.spinner("Generando PDF con Edge..."):\n' in line:
        # Reemplazar spinner para que sea dinamico
        indent = line.split('with')[0]
        new_lines.append(f'{indent}with st.spinner("Procesando vista previa..." if preview_clicked else "Generando PDF con Edge..."):\n')
        i += 1
        continue
    
    if 'st.info("Generando Documento PDF final...")' in line:
        indent = line.split('st.info')[0]
        # Insertamos el bloque final:
        new_lines.append(f'{indent}if gen_pdf_clicked:\n')
        new_lines.append(f'{indent}    st.info("Generando Documento PDF final...")\n')
        
        # Debemos identar las siguientes lineas hasta el final del bloque
        i += 1
        while i < len(lines) and (lines[i].startswith(indent) or lines[i].strip() == ''):
            if lines[i].strip() == '':
                new_lines.append(lines[i])
            else:
                new_lines.append('    ' + lines[i])
            
            # Busquemos el final de la generacion de pdf. Es cuando los componentes de descarga terminan.
            # actually all remaining lines belong to pdf gen.
            i += 1
        
        # Ahora inyectamos la parte del preview
        new_lines.append(f'{indent}elif preview_clicked:\n')
        new_lines.append(f'{indent}    st.info("Renderizando Vista Previa...")\n')
        new_lines.append(f'{indent}    from utils.pdf_generator import render_html_preview\n')
        new_lines.append(f'{indent}    import streamlit.components.v1 as components\n')
        new_lines.append(f'{indent}    try:\n')
        new_lines.append(f'{indent}        html_str, _ = render_html_preview(itinerary_data)\n')
        new_lines.append(f'{indent}        with tab_prev:\n')
        new_lines.append(f'{indent}            components.html(html_str, height=1200, scrolling=True)\n')
        new_lines.append(f'{indent}    except Exception as e:\n')
        new_lines.append(f'{indent}        st.error(f"Error generando vista previa: {{e}}")\n')
        continue

    new_lines.append(line)
    i += 1

with open(r"c:\Itinerarios\Itinerario_Automatico\tmp\refactor_ui.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("ui.py refactored and saved as tmp/refactor_ui.py")

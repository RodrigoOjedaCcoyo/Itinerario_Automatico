
import re
import os

file_path = r'c:\Itinerarios\Itinerario_Automatico\Itinerarios\Datos.sql'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Esta es una técnica para encontrar los bloques de valores e INSERTs
# Buscamos el contenido dentro de los paréntesis de VALUES (...)
# y escapamos las comillas simples que están DENTRO de las comillas simples de SQL.

def escape_sql_quotes(match):
    values_part = match.group(1)
    # Buscamos strings de SQL: '...'
    # Usamos un regex para encontrar contenido entre comillas simples de forma no codiciosa
    def replace_internal_quotes(m):
        inner_content = m.group(1)
        # Escapamos ' por ''
        return "'" + inner_content.replace("'", "''") + "'"
    
    # Reemplazamos los strings que están entre comillas simples dentro de los valores
    fixed_values = re.sub(r"'((?:''|[^'])*)'", replace_internal_quotes, values_part)
    return f"VALUES ({fixed_values})"

# Buscamos VALUES ( ... ); de forma que abarque múltiples líneas
fixed_content = re.sub(r"(?i)VALUES\s*\((.*?)\)\s*;", escape_sql_quotes, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("¡Archivo Datos.sql corregido exitosamente!")

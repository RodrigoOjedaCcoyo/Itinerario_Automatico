from utils.supabase_db import get_last_itinerary_v2
import sys

# Forzamos codificación utf-8 para la consola
sys.stdout.reconfigure(encoding='utf-8')

print("--- INICIANDO DIAGNÓSTICO DE BÚSQUEDA ---")
nombre = "RODRIGO"
print(f"Buscando: '{nombre}'")

resultado = get_last_itinerary_v2(nombre)

if resultado:
    print("✅ ÉXITO: Se encontró el registro.")
    print(resultado)
else:
    print("❌ FALLO: No se encontró nada.")

print("--- FIN DEL DIAGNÓSTICO ---")

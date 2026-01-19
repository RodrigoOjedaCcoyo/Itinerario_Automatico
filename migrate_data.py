import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importar tours_db
sys.path.append(os.getcwd())
from data.tours_db import tours_db, paquetes_db

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL o SUPABASE_KEY no configurados en .env")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def migrate():
    supabase = get_supabase_client()
    if not supabase: return

    print("--- Iniciando migracion de datos al Cerebro ---")

    # 1. Migrar TOURS
    tours_map = {} # Para guardar correspondencia ID-Nombre para los paquetes
    
    for t in tours_db:
        print(f"Procesando tour: {t['titulo']}...")
        
        tour_data = {
            "nombre": t["titulo"],
            "descripcion": t["descripcion"],
            "duracion_horas": 10, # Valor por defecto si no existe
            "precio_base_usd": t["costo_extranjero"],
            "precio_nacional": t["costo_nacional"],
            "highlights": t["highlights"],
            "servicios_incluidos": t["servicios"],
            "servicios_no_incluidos": t["servicios_no_incluye"],
            "carpeta_img": t["carpeta_img"]
        }
        
        # Insertar tour
        res = supabase.table("tour").upsert(tour_data, on_conflict="nombre").execute()
        if res.data:
            tours_map[t["titulo"]] = res.data[0]["id_tour"]
            print(f"OK - Tour guardado: {t['titulo']}")

    # 2. Migrar PAQUETES
    for p in paquetes_db:
        print(f"Procesando paquete: {p['nombre']}...")
        
        paquete_data = {
            "nombre": p["nombre"],
            "descripcion": f"Paquete turístico completo: {p['nombre']}",
            "dias": len(p["tours"]),
            "noches": max(0, len(p["tours"]) - 1),
            "precio_sugerido": 0 # Se calcula dinámicamente o se pone manual luego
        }
        
        res_p = supabase.table("paquete").upsert(paquete_data, on_conflict="nombre").execute()
        
        if res_p.data:
            id_paquete = res_p.data[0]["id_paquete"]
            print(f"OK - Paquete guardado: {p['nombre']}")
            
            # 3. Vincular Paquete con Tours (paquete_tour)
            # Primero limpiamos vínculos viejos para este paquete
            supabase.table("paquete_tour").delete().eq("id_paquete", id_paquete).execute()
            
            vínculos = []
            for idx, tour_nombre in enumerate(p["tours"]):
                id_tour = tours_map.get(tour_nombre)
                if id_tour:
                    vínculos.append({
                        "id_paquete": id_paquete,
                        "id_tour": id_tour,
                        "orden": idx + 1
                    })
            
            if vínculos:
                supabase.table("paquete_tour").insert(vínculos).execute()
                print(f"Vinculados {len(vínculos)} tours al paquete {p['nombre']}")

    print("\n--- Migracion completada con exito ---")

if __name__ == "__main__":
    migrate()

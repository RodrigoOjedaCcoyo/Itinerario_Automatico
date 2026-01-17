import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    """Inicializa y retorna el cliente de Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ADVERTENCIA: SUPABASE_URL o SUPABASE_KEY no configurados.")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def save_itinerary(itinerary_data):
    """Guarda un itinerario en la tabla 'itinerarios' mapeando campos clave."""
    supabase = get_supabase_client()
    if not supabase: return False
    
    try:
        # Preparamos el registro mapeando los campos principales a columnas
        # y guardando el resto en un campo JSON llamado 'datos'
        record = {
            "pasajero": itinerary_data.get("pasajero"),
            "fechas": itinerary_data.get("fechas"),
            "categoria": itinerary_data.get("categoria"),
            "vendedor": itinerary_data.get("vendedor"),
            "fuente": itinerary_data.get("fuente"),
            "campana": itinerary_data.get("campana"),
            "estado": itinerary_data.get("estado"),
            "sucursal": itinerary_data.get("sucursal"),
            "celular": itinerary_data.get("celular_cliente"),
            "datos": itinerary_data
        }
        
        response = supabase.table("itinerarios").insert(record).execute()
        if response.data:
            return response.data[0].get("id")
        return None
    except Exception as e:
        print(f"Error guardando en Supabase: {e}")
        return None

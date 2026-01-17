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
    if not SUPABASE_URL or "your-project" in str(SUPABASE_URL) or not SUPABASE_KEY or "your-anon-key" in str(SUPABASE_KEY):
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

def save_itinerary_v2(itinerary_data):
    """
    Guarda un itinerario en 'itinerario_digital' y sincroniza con 'lead'.
    Versión adaptada al nuevo esquema maestro.
    """
    supabase = get_supabase_client()
    if not supabase: return None
    
    try:
        # 1. Primero manejamos el Lead (Buscamos por celular para evitar duplicados)
        celular = itinerary_data.get("celular_cliente")
        nombre = itinerary_data.get("pasajero")
        vendedor_id = itinerary_data.get("id_vendedor", 1) # Default al primer vendedor si no hay ID
        
        # Intentar buscar lead existente por celular
        lead_res = supabase.table("lead").select("id_lead").eq("numero_celular", celular).execute()
        
        id_lead = None
        if lead_res.data:
            id_lead = lead_res.data[0]["id_lead"]
        else:
            # Crear nuevo lead si no existe
            new_lead = {
                "numero_celular": celular,
                "nombre_pasajero": nombre,
                "id_vendedor": vendedor_id,
                "red_social": itinerary_data.get("fuente"),
                "estado_lead": itinerary_data.get("estado"),
                "whatsapp": True if itinerary_data.get("fuente") == "WhatsApp" else False
            }
            res_nl = supabase.table("lead").insert(new_lead).execute()
            if res_nl.data:
                id_lead = res_nl.data[0]["id_lead"]

        # 2. Guardar en itinerario_digital
        it_digital = {
            "id_lead": id_lead,
            "id_vendedor": vendedor_id,
            "nombre_pasajero_itinerario": nombre,
            "datos_render": itinerary_data
        }
        
        res_it = supabase.table("itinerario_digital").insert(it_digital).execute()
        
        if res_it.data:
            it_id = res_it.data[0]["id_itinerario_digital"]
            
            # 3. Actualizar el último itinerario en el Lead
            if id_lead:
                supabase.table("lead").update({"ultimo_itinerario_id": it_id}).eq("id_lead", id_lead).execute()
                
            return it_id
            
        return None
    except Exception as e:
        print(f"Error en Cerebro Supabase: {e}")
        return None

def get_last_itinerary_v2(name: str):
    """Busca el historial usando el nuevo esquema."""
    supabase = get_supabase_client()
    if not supabase or not name: return None
    
    try:
        response = supabase.table("itinerario_digital")\
            .select("*")\
            .ilike("nombre_pasajero_itinerario", f"%{name}%")\
            .order("fecha_generacion", descending=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error consultando Cerebro: {e}")
        return None

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
    Versión adaptada al ESQUEMA MAESTRO FINAL.
    """
    supabase = get_supabase_client()
    if not supabase: return None
    
    try:
        # 1. Resolver el id_vendedor por nombre
        vendedor_nombre = itinerary_data.get("vendedor", "Vendedor General")
        vendedor_res = supabase.table("vendedor").select("id_vendedor").ilike("nombre", f"%{vendedor_nombre}%").limit(1).execute()
        
        vendedor_id = 1 # Default
        if vendedor_res.data:
            vendedor_id = vendedor_res.data[0]["id_vendedor"]
        else:
            # Si no existe, creamos el vendedor para no romper la llave foránea
            new_vend = {"nombre": vendedor_nombre}
            res_v = supabase.table("vendedor").insert(new_vend).execute()
            if res_v.data:
                vendedor_id = res_v.data[0]["id_vendedor"]

        # 2. Manejar el Lead
        celular = itinerary_data.get("celular_cliente")
        nombre = itinerary_data.get("pasajero")
        fuente = itinerary_data.get("fuente")
        estado = itinerary_data.get("estado")
        
        # Buscar lead existente
        lead_res = supabase.table("lead").select("id_lead").eq("numero_celular", celular).execute()
        
        id_lead = None
        if lead_res.data:
            id_lead = lead_res.data[0]["id_lead"]
            # Actualizamos el estado del lead existente
            supabase.table("lead").update({
                "estado_lead": estado,
                "id_vendedor": vendedor_id,
                "nombre_pasajero": nombre
            }).eq("id_lead", id_lead).execute()
        else:
            # Crear nuevo lead
            new_lead = {
                "numero_celular": celular,
                "nombre_pasajero": nombre,
                "id_vendedor": vendedor_id,
                "red_social": fuente,
                "estado_lead": estado,
                "whatsapp": True if "WhatsApp" in fuente else False
            }
            res_nl = supabase.table("lead").insert(new_lead).execute()
            if res_nl.data:
                id_lead = res_nl.data[0]["id_lead"]

        # 3. Guardar en itinerario_digital
        it_digital = {
            "id_lead": id_lead,
            "id_vendedor": vendedor_id,
            "nombre_pasajero_itinerario": nombre,
            "datos_render": itinerary_data
        }
        
        res_it = supabase.table("itinerario_digital").insert(it_digital).execute()
        
        if res_it.data:
            it_id = res_it.data[0]["id_itinerario_digital"]
            
            # 4. Actualizar el último itinerario en el Lead para seguimiento rápido
            if id_lead:
                supabase.table("lead").update({"ultimo_itinerario_id": it_id}).eq("id_lead", id_lead).execute()
                
            return it_id
            
        return None
    except Exception as e:
        print(f"Error detallado en Cerebro Supabase: {e}")
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

def get_available_tours():
    """Obtiene el catálogo de tours desde Supabase."""
    supabase = get_supabase_client()
    if not supabase: return []
    try:
        res = supabase.table("tour").select("*").order("nombre").execute()
        # Adaptar nombres de columnas al formato que espera la UI si es necesario
        tours = []
        for t in res.data:
            tours.append({
                "titulo": t["nombre"],
                "descripcion": t["descripcion"],
                "highlights": t.get("highlights", []),
                "servicios": t.get("servicios_incluidos", []),
                "servicios_no_incluye": t.get("servicios_no_incluidos", []),
                "costo_nacional": float(t.get("precio_nacional", 0)),
                "costo_extranjero": float(t.get("precio_base_usd", 0)),
                "carpeta_img": t.get("carpeta_img", "general")
            })
        return tours
    except Exception:
        return []

def get_available_packages():
    """Obtiene el catálogo de paquetes desde Supabase."""
    supabase = get_supabase_client()
    if not supabase: return []
    try:
        res = supabase.table("paquete").select("*, paquete_tour(tour(nombre))").order("nombre").execute()
        packages = []
        for p in res.data:
            tours_names = [pt["tour"]["nombre"] for pt in p.get("paquete_tour", [])]
            packages.append({
                "nombre": p["nombre"],
                "tours": tours_names
            })
        return packages
    except Exception:
        return []

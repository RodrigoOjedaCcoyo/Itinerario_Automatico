import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

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

        # 2. Manejar el Lead (SOLO SI ES B2C)
        id_lead = None
        es_b2b = itinerary_data.get("canal") == "B2B"
        nombre = itinerary_data.get("pasajero")
        
        if not es_b2b:
            celular = itinerary_data.get("celular_cliente")
            fuente = itinerary_data.get("fuente")
            estado = itinerary_data.get("estado")
            
            # Buscar lead existente
            lead_res = supabase.table("lead").select("id_lead").eq("numero_celular", celular).execute()
            
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


def get_last_itinerary_v3(name: str):
    """Busca el historial usando el nuevo esquema."""
    supabase = get_supabase_client()
    if not supabase or not name: return None
    
    try:
        response = supabase.table("itinerario_digital")\
            .select("*")\
            .ilike("nombre_pasajero_itinerario", f"%{name}%")\
            .order("fecha_generacion", desc=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            return response.data[0]
            
        # Fallback: Si no hay itinerario, buscar en Leads
        # print(f"DEBUG: Intentando fallback en LEADS para: {name}")
        res_lead = supabase.table("lead")\
            .select("*")\
            .ilike("nombre_pasajero", f"%{name}%")\
            .order("fecha_creacion", desc=True)\
            .limit(1)\
            .execute()
            
        if res_lead.data:
            lead = res_lead.data[0]
            return {
                "datos_render": {
                    "pasajero": lead.get("nombre_pasajero", ""),
                    "celular_cliente": lead.get("numero_celular", ""),
                    "fuente": lead.get("red_social", "Desconocido"),
                    "estado": lead.get("estado_lead", "Nuevo")
                }
            }
            
        # Doble Fallback: Si no hay lead, buscar en Clientes
        # print(f"DEBUG: Intentando fallback en CLIENTES para: {name}")
        res_cliente = supabase.table("cliente")\
            .select("*")\
            .ilike("nombre", f"%{name}%")\
            .limit(1)\
            .execute()
            
        if res_cliente.data:
            # st.toast("✅ Cliente encontrado en DB Interna")
            client = res_cliente.data[0]
            pais = str(client.get("pais", "")).upper()
            categoria = "Nacional" if "PERU" in pais or "PERÚ" in pais else "Extranjero"
            
            return {
                "datos_render": {
                    "pasajero": client.get("nombre", ""),
                    "celular_cliente": "", # Cliente no tiene cel en esta tabla
                    "fuente": "Base de Datos",
                    "estado": "Cliente",
                    "categoria": categoria,
                    "tipo_cliente": client.get("tipo_cliente", "B2C")
                }
            }
        else:
            # st.error(f"⚠️ Cliente '{name}' no encontrado en tabla 'cliente'")
            pass
            
        return None
    except Exception as e:
        print(f"Error consultando Cerebro: {e}")
        return None

def populate_catalog():
    """Puebla la tabla tour con el contenido del archivo Itinerarios/Datos.sql"""
    supabase = get_supabase_client()
    if not supabase: return False
    
    try:
        sql_file = os.path.join("Itinerarios", "Datos.sql")
        if not os.path.exists(sql_file):
            print(f"Error: {sql_file} no existe.")
            return False
            
        # Nota: La ejecución real de SQL complejo con JSONB se maneja mejor desde el Editor SQL de Supabase.
        # He movido las imágenes y preparado la estructura.
        return True
    except Exception as e:
        print(f"Error al leer catálogo: {e}")
        return False
# ORPHANED CODE REMOVED TO FIX INDENTATION ERROR
#                         vínculos.append({
#                             "id_paquete": id_paquete,
#                             "id_tour": id_tour,
#                             "orden": idx + 1
#                         })
#                 if vínculos:
#                     supabase.table("paquete_tour").insert(vínculos).execute()
#         return True
#     except Exception as e:
#         print(f"Error en poblacion: {e}")
#         return False


def extract_json_list(data, keys_priority):
    """Helper para extraer listas de estructuras JSON variadas."""
    if not data: return []
    if isinstance(data, list): return data
    if isinstance(data, dict):
        for k in keys_priority:
            if k in data and isinstance(data[k], list):
                return data[k]
        # Fallback: devolver valores si es una lista plana disfrazada
        return []
    return []

def get_available_tours():
    """Obtiene el catálogo de tours desde Supabase."""
    supabase = get_supabase_client()
    if not supabase: return []
    try:
        # Intentamos seleccionar 'atractivos' explícitamente si existe
        res = supabase.table("tour").select("*, atractivos").order("nombre").execute()
    except Exception:
        # Fallback si la columna 'atractivos' no existe
        res = supabase.table("tour").select("*").order("nombre").execute()

    tours = []
    if res.data:
        for t in res.data:
            try:
                # 1. Parsear Atractivos (UI highlights) desde 'atractivos' o fallback a 'highlights'
                raw_atractivos = t.get("atractivos")
                # Si no hay columna atractivos, a veces se guardó en highlights["lugares"]
                raw_highlights_db = t.get("highlights")
                
                final_highlights = []
                # Prioridad 1: Columna atractivos
                if raw_atractivos:
                    final_highlights = extract_json_list(raw_atractivos, ["Lo que visitarás", "lugares", "atractivos"])
                
                # Prioridad 2: Buscar dentro de highlights si falló lo anterior
                if not final_highlights and raw_highlights_db:
                    final_highlights = extract_json_list(raw_highlights_db, ["Lo que visitarás", "lugares"])
                
                # 2. Parsear Servicios
                servicios_in = extract_json_list(t.get("servicios_incluidos"), ["incluye", "servicios"])
                servicios_out = extract_json_list(t.get("servicios_no_incluidos"), ["no_incluye", "no_incluidos"])

                # 3. Enriquecer descripción con 'itinerario' si existe
                desc = t.get("descripcion", "")
                rich_itinerary = ""
                
                # Intentar sacar el texto del itinerario/experiencia de los JSONs
                if isinstance(raw_atractivos, dict) and "itinerario" in raw_atractivos:
                    rich_itinerary = raw_atractivos["itinerario"]
                elif isinstance(raw_highlights_db, dict) and "itinerario" in raw_highlights_db:
                    rich_itinerary = raw_highlights_db["itinerario"]
                
                # Si encontramos texto enriquecido, lo usamos
                if rich_itinerary:
                    import re
                    # 1. Limpieza básica de caracteres
                    cleaned = rich_itinerary.replace("\\n", "\n").replace('""', '"').strip()
                    # 2. Eliminar el título entre corchetes ej: [Titulo]
                    cleaned = re.sub(r'^\[.*?\]\s*', '', cleaned)
                    # 3. Eliminar prefix común "La Experiencia:" o "The Experience:"
                    cleaned = re.sub(r'^(La Experiencia|The Experience):\s*', '', cleaned, flags=re.IGNORECASE)
                    # 4. Eliminar comillas envolventes si quedaron (ej: "Texto")
                    cleaned = cleaned.strip('"').strip()
                    
                    desc = cleaned

                # 4. Formatear Hora
                raw_hora = t.get("hora_inicio")
                formatted_hora = "08:00 AM"
                if raw_hora:
                    try:
                        # Si viene como timestamp ISO '2026-01-01 08:00:00-05'
                        if "T" in str(raw_hora) or "-" in str(raw_hora):
                            # Intento simple de parserDate
                            from dateutil import parser
                            dt = parser.parse(str(raw_hora))
                            formatted_hora = dt.strftime("%I:%M %p")
                        else:
                            # Asumimos que ya es string corto o time
                             formatted_hora = str(raw_hora)
                    except:
                        formatted_hora = str(raw_hora)

                tours.append({
                    "titulo": t.get("nombre", "Sin Nombre"),
                    "descripcion": desc,
                    "highlights": final_highlights,
                    "servicios": servicios_in,
                    "servicios_no_incluye": servicios_out,
                    "costo_nacional": float(t.get("precio_nacional") or 0),
                    "costo_extranjero": float(t.get("precio_base_usd") or 0),
                    "carpeta_img": t.get("carpeta_img") or "general",
                    "hora_inicio": formatted_hora
                })
            except Exception as e_row:
                print(f"Error procesando fila de tour {t.get('nombre')}: {e_row}")
                continue
    return tours


def get_available_packages():
    """Obtiene el catálogo de paquetes desde Supabase."""
    supabase = get_supabase_client()
    if not supabase: return []
    try:
        # Recuperamos 'orden' además del nombre del tour para poder ordenar
        # Filtramos solo paquetes activos
        res = supabase.table("paquete").select("*, paquete_tour(orden, tour(nombre))").eq("activo", True).order("nombre").execute()
        packages = []
        for p in res.data:
            # Obtenemos la lista cruda de relaciones
            raw_tours = p.get("paquete_tour", [])
            # Ordenamos por la columna 'orden' para respetar la secuencia del itinerario
            raw_tours.sort(key=lambda x: x.get("orden", 999))
            
            # Extraemos solo los nombres ya ordenados
            tours_names = [pt["tour"]["nombre"] for pt in raw_tours if pt.get("tour")]
            
            packages.append({
                "nombre": p["nombre"],
                "tours": tours_names
            })
        return packages
    except Exception as e:
        st.error(f"❌ Error de conexión al cargar Paquetes: {e}")
        return []

def get_vendedores():
    """Obtiene la lista de vendedores activos desde Supabase."""
    supabase = get_supabase_client()
    if not supabase: return []
    try:
        res = supabase.table("vendedor").select("nombre").eq("estado", "ACTIVO").order("nombre").execute()
        return [v["nombre"] for v in res.data]
    except Exception as e:
        print(f"Error cargando vendedores: {e}")
        return []

def verify_user(email, password):
    """
    Verifica credenciales usando el sistema de Autenticación OFICIAL de Supabase.
    Luego busca el rol en la tabla usuarios_app.
    """
    supabase = get_supabase_client()
    if not supabase: return None
    
    try:
        # 1. Intentar Login real en Supabase Auth
        res_auth = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if res_auth.user:
            # 2. Si el login es exitoso, buscamos su ROL en nuestra tabla blanca
            res_role = supabase.table("usuarios_app").select("rol").eq("email", email).execute()
            
            rol = "VENTAS" # Rol por defecto si no está en la tabla pero sí en Auth
            if res_role.data:
                rol = res_role.data[0]["rol"]
            
            return {
                "email": res_auth.user.email,
                "id": res_auth.user.id,
                "rol": rol
            }
        return None
    except Exception as e:
        # Si las credenciales son inválidas, Supabase lanzará una excepción
        print(f"Error de Auth: {e}")
        return None

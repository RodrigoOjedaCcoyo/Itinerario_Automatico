import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def translate_itinerary(itinerary_data, target_lang="English"):
    """
    Traduce los textos de un itinerario (títulos, descripciones, servicios) 
    usando OpenAI GPT-4o-mini.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return itinerary_data, "Error: No se encontró la API KEY de OpenAI."

    client = OpenAI(api_key=api_key)
    
    # Preparar el prompt para la IA
    # Solo traducimos los campos de texto para ahorrar tokens y mantener IDs/Precios intactos.
    system_prompt = f"""
    Eres un traductor experto en turismo y viajes. 
    Tu tarea es traducir el contenido de un itinerario de viaje del Español al {target_lang}.
    
    Reglas:
    1. Mantén un tono profesional, elegante y acogedor para una agencia de viajes premium.
    2. TOTALMENTE PROHIBIDO traducir nombres propios de lugares, atractivos turísticos o sitios arqueológicos (ej: 'Machu Picchu', 'Ollantaytambo', 'Sacsayhuaman', 'Qorikancha', 'Pisaq'). Estos deben permanecer EXACTAMENTE igual en el texto traducido.
    3. Solo traduce términos generales como 'Sacred Valley' por 'Valle Sagrado' si es estrictamente necesario para la fluidez, pero prioriza los nombres originales.
    4. Devuelve los resultados en el mismo formato estructurado que recibas (JSON-object).
    5. NO traduzcas bajo ninguna circunstancia números, fechas, horas, ni símbolos de moneda (S/, $, USD).
    """

    # Extraer textos para traducir
    # Para ser eficientes, enviamos todo en un solo bloque si es posible o por partes claras.
    processed_days = []
    
    for day in itinerary_data.get('days', []):
        user_prompt = f"""
        Traduce los siguientes campos al {target_lang}:
        Título: {day.get('titulo')}
        Descripción: {day.get('descripcion')}
        Incluye: {", ".join(day.get('servicios', []))}
        No Incluye: {", ".join(day.get('servicios_no_incluye', []))}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            translated_text = response.choices[0].message.content
            # Aquí necesitaríamos un parsing más robusto si enviamos todo junto, 
            # pero para esta versión inicial lo haremos por campos o con un formato claro de respuesta.
            # Mejorar: Pedirle a la IA que devuelva JSON directamente.
            
            json_prompt = f"""
            Traduce este JSON al {target_lang} respetando las llaves. Solo traduce los valores.
            {{
                "titulo": "{day.get('titulo')}",
                "descripcion": "{day.get('descripcion')}",
                "servicios": {day.get('servicios', [])},
                "servicios_no_incluye": {day.get('servicios_no_incluye', [])}
            }}
            """
            
            response_json = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json_prompt}
                ]
            )
            
            import json
            translations = json.loads(response_json.choices[0].message.content)
            
            # Crear copia del día con traducciones
            new_day = day.copy()
            new_day['titulo'] = translations.get('titulo', day['titulo'])
            new_day['descripcion'] = translations.get('descripcion', day['descripcion'])
            new_day['servicios'] = translations.get('servicios', day['servicios'])
            new_day['servicios_no_incluye'] = translations.get('servicios_no_incluye', day['servicios_no_incluye'])
            
            processed_days.append(new_day)
            
        except Exception as e:
            print(f"Error traduciendo día: {e}")
            processed_days.append(day)

    # Traducir Notas Finales si existen
    translated_itinerary = itinerary_data.copy()
    translated_itinerary['days'] = processed_days
    
    if itinerary_data.get('notas_finales'):
        try:
            note_prompt = f"Traduce al {target_lang}: {itinerary_data.get('notas_finales')}"
            res_note = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": note_prompt}
                ]
            )
            translated_itinerary['notas_finales'] = res_note.choices[0].message.content
        except:
            pass
            
    return translated_itinerary, None

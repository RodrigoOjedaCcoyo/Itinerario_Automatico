import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def translate_itinerary(itinerary_data, target_lang="English"):
    """
    Traduce los textos de un itinerario (títulos, descripciones, servicios) 
    usando OpenAI GPT-4o-mini.
    """
    try:
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    except:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return itinerary_data, "Error: No se encontró la API KEY de OpenAI (configura OPENAI_API_KEY en st.secrets o .env)."

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
            
            # Crear copia del día con todas las propiedades originales (incluyendo images, numero, fecha, etc.)
            new_day = day.copy()
            
            # Aplicar traducciones sobre la copia
            new_day['titulo'] = translations.get('titulo', day.get('titulo'))
            new_day['descripcion'] = translations.get('descripcion', day.get('descripcion'))
            new_day['servicios'] = translations.get('servicios', day.get('servicios'))
            new_day['servicios_no_incluye'] = translations.get('servicios_no_incluye', day.get('servicios_no_incluye', []))
            
            processed_days.append(new_day)
            
        except Exception as e:
            print(f"Error traduciendo día: {e}")
            processed_days.append(day)

    # 3. Traducir NOTA DE PRECIO
    if itinerary_data.get('nota_precio'):
        try:
            res_np = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Traduce al {target_lang}: {itinerary_data.get('nota_precio')}"}
                ]
            )
            itinerary_data['nota_precio'] = res_np.choices[0].message.content
        except: pass

    # 4. Traducir NOTAS FINALES (Personalizadas)
    if itinerary_data.get('notas_finales'):
        try:
            res_nf = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Traduce al {target_lang}: {itinerary_data.get('notas_finales')}"}
                ]
            )
            itinerary_data['notas_finales'] = res_nf.choices[0].message.content
        except: pass

    # 5. Traducir BLOQUES ESTÁTICOS (Guía y Políticas)
    # Definimos los bloques base en español si no vienen en el data
    guia_base = itinerary_data.get('guia_viajero', {
        "titulo": "Guía del Viajero",
        "subtitulo": "PREPARA TU AVENTURA",
        "secciones": [
            {"nombre": "SALUD Y PROTECCIÓN", "lista": ["BLOQUEADOR SOLAR SPF 50+", "REPELENTE DE INSECTOS", "MEDICACIÓN PERSONAL", "TOALLITAS HÚMEDAS"]}
        ],
        "secciones_extra": [
            {"nombre": "ROPA Y EQUIPO", "lista": ["CAMISAS DE MANGA LARGA", "PANTALONES CÓMODOS", "CHAQUETA DE LLUVIA / PONCHO", "MOCHILA LIGERA"]}
        ],
        "mensaje_final": "<p style='margin: 0; font-size: 1.1rem; color: #2d3436; font-weight: 600;'>✨ <strong>¡Prepárate para vivir una experiencia inolvidable!</strong> ✨</p><p style='margin: 10px 0 0 0; font-size: 0.9rem; color: #636e72;'>Cada detalle cuenta para que tu viaje sea perfecto. ¡Nos vemos pronto en Cusco!</p>"
    })

    politicas_base = itinerary_data.get('politicas', {
        "titulo_principal": "RESUMEN DE TÉRMINOS Y CONDICIONES",
        "secciones": [
            {
                "titulo": "1. Reservas y Pagos",
                "icon": "💳",
                "contenido": "<strong>Depósito inicial:</strong> Se requiere el 50% del total para confirmar la reserva del paquete turístico.<br><strong>Saldo restante:</strong> Debe liquidarse a más tardar 48 horas antes del inicio del primer tour o según lo acordado con su asesor.<br><strong>Métodos de pago:</strong> Transferencia bancaria, depósito, efectivo, PayPal y tarjetas (estas últimas con un recargo del 5%).<br><strong>Información requerida:</strong> El cliente debe facilitar datos reales (pasaporte/DNI, edad, restricciones médicas y alimentarias)."
            },
            {
                "titulo": "2. Políticas de Anulación",
                "icon": "🕒",
                "contenido": "<strong>Más de 15 días:</strong> Reembolso del 100% (menos 10% de gastos administrativos).<br><strong>Entre 8 y 14 días:</strong> Reembolso del 50%.<br><strong>Entre 4 y 7 días:</strong> Reembolso del 25%.<br><strong>Menos de 4 días:</strong> No hay devolución.<br><strong>Casos excepcionales:</strong> Ingresos a Machu Picchu o pasajes quedan sujetos a condiciones de los proveedores."
            },
            {
                "titulo": "3. Condiciones del Servicio",
                "icon": "📋",
                "contenido": "<strong>Documentación:</strong> Es obligatorio portar pasaporte o DNI original vigente.<br><strong>Infantes:</strong> Menores de 2 años viajan gratis.<br><strong>Habitaciones:</strong> El alojamiento individual (SGL) conlleva un suplemento adicional.<br><strong>Puntualidad:</strong> El cliente debe presentarse puntualmente en los puntos de encuentro.<br><strong>Seguro:</strong> Se recomienda contar con un seguro de viaje personal."
            },
            {
                "titulo": "4. Reglamento de Visita",
                "icon": "🏛️",
                "contenido": "<strong>Boletos:</strong> Son válidos para un solo ingreso a la Ciudadela de Machu Picchu.<br><strong>Permanencia:</strong> El tiempo promedio permitido es de 2 a 3 horas según circuito.<br><strong>Guía:</strong> El uso de guía oficial es obligatorio para el ingreso."
            },
            {
                "titulo": "5. Responsabilidades",
                "icon": "🛡️",
                "contenido": "<strong>La Agencia:</strong> Se compromete a brindar guías certificados y transporte autorizado.<br><strong>Eximentes:</strong> La agencia no se responsabiliza por robos, accidentes externos o cierres por causas de fuerza mayor (clima, huelgas, desastres).<br><strong>Jurisdicción:</strong> Controversias legales se resolverán bajo los tribunales de Cusco."
            },
            {
                "titulo": "6. Atención y Reclamos",
                "icon": "📱",
                "contenido": "<strong>Atención:</strong> Las consultas y reservas son 100% virtuales (WhatsApp/Email).<br><strong>Reclamos:</strong> Se dispone de un Libro de Reclamaciones (físico y virtual) conforme a la ley de INDECOPI."
            }
        ]
    })

    try:
        # Traducir Guía
        json_guia = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Traduce este objeto de guía al {target_lang}: {json.dumps(guia_base)}"}
            ]
        )
        itinerary_data['guia_viajero'] = json.loads(json_guia.choices[0].message.content)

        # Traducir Políticas
        json_pol = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Traduce este objeto de políticas al {target_lang}: {json.dumps(politicas_base)}"}
            ]
        )
        itinerary_data['politicas'] = json.loads(json_pol.choices[0].message.content)
    except:
        itinerary_data['guia_viajero'] = guia_base
        itinerary_data['politicas'] = politicas_base

    return itinerary_data, None

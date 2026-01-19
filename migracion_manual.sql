-- SCRIPT DE MIGRACIÓN MANUAL DE CATÁLOGO
-- Copia y pega esto en el SQL Editor de Supabase

-- 1. LIMPIEZA PREVIA (Opcional, ten cuidado)
-- DELETE FROM paquete_tour;
-- DELETE FROM paquete;
-- DELETE FROM tour;

-- 2. INSERTAR TOURS
INSERT INTO tour (nombre, descripcion, precio_base_usd, precio_nacional, highlights, servicios_incluidos, servicios_no_incluidos, carpeta_img, duracion_horas)
VALUES 
('RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL', 'Recepción en el aeropuerto de Cusco y traslado al hotel. Por la tarde, visita al Templo del Sol (Qoricancha) y la fortaleza de Sacsayhuamán.', 48.00, 120.00, '["Recepción y asistencia en el Aeropuerto", "Visita guiada al Templo del Sol (Qoricancha)", "Exploración de la Gran Fortaleza de Sacsayhuamán"]', '["Traslado privado Aeropuerto - Hotel", "Transporte turístico", "Guía Profesional"]', '["Alimentación", "Propinas"]', 'cusco_city', 5),
('CITY TOUR LIMA COLONIAL Y MODERNA', 'Recorrido por el Centro Histórico de Lima, Patrimonio de la Humanidad. Visita al Convento de San Francisco y sus Catacumbas.', 35.00, 116.55, '["Centro Histórico de Lima", "Convento de San Francisco", "Miraflores"]', '["Traslado Aeropuerto - Hotel", "Transporte turístico", "Guía local"]', '["Alimentación", "Vuelos"]', 'lima_city', 4),
('VALLE SAGRADO: PISAC Y OLLANTAYTAMBO', 'Visita al complejo arqueológico de Pisac y su tradicional mercado artesanal. Fortaleza de Ollantaytambo.', 50.00, 140.00, '["Terrazas de Pisac", "Mercado Artesanal", "Fortaleza de Ollantaytambo"]', '["Transporte turístico", "Guía oficial", "Almuerzo buffet"]', '["Bebidas extras", "Propinas"]', 'valle_sagrado', 10),
('VALLE SUR Y CAPILLA SIXTINA DE AMÉRICA', 'Exploración de la ingeniería hidráulica de Tipón y el centro Wari de Pikillacta. Iglesia de Andahuaylillas.', 35.00, 80.00, '["Ingeniería de Tipón", "Wari de Pikillacta", "Iglesia Andahuaylillas"]', '["Transporte turístico", "Guía especializado", "Tickets ingreso"]', '["Almuerzo", "Gastos personales"]', 'valle_sur', 6),
('MONTAÑA DE 7 COLORES (VINICUNCA)', 'Caminata hacia la famosa montaña Vinicunca para apreciar sus franjas minerales de colores.', 45.00, 100.00, '["Caminata a Vinicunca", "Vistas del Ausangate", "Alpacas y vida andina"]', '["Transporte turístico", "Desayuno y almuerzo buffet", "Guía profesional"]', '["Alquiler de caballo", "Bastones"]', 'vinicunca', 12),
('SANTUARIO HISTÓRICO DE MACHU PICCHU', 'Visita guiada a la Ciudad Perdida de los Incas. Incluye viaje en tren hasta Aguas Calientes y ascenso al santuario.', 250.00, 270.00, '["Ciudadela Inca", "Viaje en tren", "Intihuatana"]', '["Ticket ingreso Machu Picchu", "Boleto tren", "Boleto bus subida/bajada"]', '["Alimentación", "Entrada Huayna Picchu"]', 'machupicchu', 14),
('TOUR MÍSTICO Y CONEXIÓN ANDINA', 'Ceremonia de limpieza espiritual y meditación en centros energéticos. Tradición ancestral.', 35.00, 80.00, '["Pago a la Tierra", "Meditación centros energéticos", "Limpieza espiritual"]', '["Transporte privado", "Guía espiritual", "Kit ofrendas"]', '["Alimentación pesada", "Propinas"]', 'mistico', 6),
('LAGUNA HUMANTAY Y GLACIAR SALKANTAY', 'Aventura hacia una laguna turquesa a los pies del glaciar Humantay. Caminata en Soraypampa.', 45.00, 100.00, '["Laguna Turquesa", "Vistas glaciares", "Naturaleza pura"]', '["Transporte turístico", "Desayuno y almuerzo buffet", "Guía oficial aventura"]', '["Alquiler de caballo", "Snacks"]', 'humantay', 12)
ON CONFLICT (nombre) DO UPDATE SET 
    descripcion = EXCLUDED.descripcion,
    precio_base_usd = EXCLUDED.precio_base_usd,
    precio_nacional = EXCLUDED.precio_nacional,
    highlights = EXCLUDED.highlights,
    servicios_incluidos = EXCLUDED.servicios_incluidos,
    servicios_no_incluidos = EXCLUDED.servicios_no_incluidos,
    carpeta_img = EXCLUDED.carpeta_img;

-- 3. INSERTAR PAQUETES
INSERT INTO paquete (nombre, descripcion, dias, noches, precio_sugerido)
VALUES 
('CUSCO TRADICIONAL 3D/2N', 'Paquete clásico Cusco y Machu Picchu', 3, 2, 0),
('CUSCO TRADICIONAL 4D/3N', 'Cusco, Machu Picchu y Montaña 7 Colores', 4, 3, 0),
('CUSCO TRADICIONAL 5D/4N', 'Cusco completo con Laguna Humantay', 5, 4, 0),
('PERÚ PARA EL MUNDO 8D/7N', 'Lima, Cusco, Valle Sagrado y Machu Picchu completo', 8, 7, 0)
ON CONFLICT (nombre) DO UPDATE SET 
    descripcion = EXCLUDED.descripcion,
    dias = EXCLUDED.dias,
    noches = EXCLUDED.noches;

-- 4. VINCULAR PAQUETES CON TOURS
-- Nota: Esto asume que los IDs se generan secuencialmente si la tabla estaba vacía. 
-- Si no, es mejor usar subconsultas por nombre.

DELETE FROM paquete_tour WHERE id_paquete IN (SELECT id_paquete FROM paquete);

INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 1 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 3D%' AND t.nombre = 'RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 2 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 3D%' AND t.nombre = 'VALLE SAGRADO: PISAC Y OLLANTAYTAMBO';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 3 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 3D%' AND t.nombre = 'SANTUARIO HISTÓRICO DE MACHU PICCHU';

INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 1 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 4D%' AND t.nombre = 'RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 2 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 4D%' AND t.nombre = 'VALLE SAGRADO: PISAC Y OLLANTAYTAMBO';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 3 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 4D%' AND t.nombre = 'SANTUARIO HISTÓRICO DE MACHU PICCHU';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 4 FROM paquete p, tour t WHERE p.nombre LIKE 'CUSCO TRADICIONAL 4D%' AND t.nombre = 'MONTAÑA DE 7 COLORES (VINICUNCA)';

-- Y así sucesivamente para el resto...

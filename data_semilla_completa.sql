-- ==============================================================
-- CARGA COMPLETA DE CATÁLOGO (TOURS Y PAQUETES)
-- ==============================================================
-- Ejecuta esto después de haber creado las tablas con setup_maestro.sql

-- 0. ASEGURAR RESTRICCIONES (Para que funcione el ON CONFLICT)
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'tour_nombre_unique') THEN
        ALTER TABLE tour ADD CONSTRAINT tour_nombre_unique UNIQUE (nombre);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'paquete_nombre_unique') THEN
        ALTER TABLE paquete ADD CONSTRAINT paquete_nombre_unique UNIQUE (nombre);
    END IF;
END $$;

-- 1. INSERTAR TODOS LOS TOURS (8 TOURS)
INSERT INTO tour (nombre, descripcion, precio_base_usd, precio_nacional, highlights, servicios_incluidos, servicios_no_incluidos, carpeta_img, duracion_horas)
VALUES 
('RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL', 'Recepción en el aeropuerto de Cusco y traslado al hotel. Por la tarde, visita al Templo del Sol (Qoricancha) y la fortaleza de Sacsayhuamán.', 48.00, 120.00, 
 '["Recepción y asistencia en el Aeropuerto", "Visita guiada al Templo del Sol (Qoricancha)", "Exploración de la Gran Fortaleza de Sacsayhuamán", "Centros rituales de Qenqo y Puca Pucara", "Fuentes ceremoniales de Tambomachay", "Vistas panorámicas de la ciudad imperial"]', 
 '["Traslado privado Aeropuerto - Hotel", "Transporte turístico para el recorrido", "Guía Profesional bilingüe certificado", "Boleto Turístico (Ingresos)", "Ingreso al Templo del Qoricancha", "Botiquín de primeros auxilios y oxígeno", "Asistencia permanente personalizada"]', 
 '["Alimentación (Almuerzo / Cena)", "Gastos personales y souvenirs", "Propinas por servicio"]', 'cusco_city', 5),

('CITY TOUR LIMA COLONIAL Y MODERNA', 'Recorrido por el Centro Histórico de Lima, Patrimonio de la Humanidad. Visita al Convento de San Francisco y sus Catacumbas.', 35.00, 116.55, 
 '["Centro Histórico de Lima (Patrimonio UNESCO)", "Convento de San Francisco y Catacumbas", "Vista panorámica de Huaca Pucllana", "Recorrido por Miraflores y San Isidro", "Vistas del Pacífico desde el Malecón", "Parque del Amor y Larcomar"]', 
 '["Traslado privado Aeropuerto - Hotel", "Transporte turístico climatizado", "Guía local experto en historia", "Ingresos a museos y conventos", "Asistencia durante su estadía en Lima", "Seguro para pasajeros a bordo"]', 
 '["Alimentación completa", "Vuelos domésticos", "Gastos no especificados"]', 'lima_city', 4),

('VALLE SAGRADO: PISAC Y OLLANTAYTAMBO', 'Visita al complejo arqueológico de Pisac y su tradicional mercado artesanal. Tras un almuerzo buffet en Urubamba, exploraremos la fortaleza de Ollantaytambo.', 50.00, 140.00, 
 '["Terrazas agrícolas de Pisac", "Mercado Artesanal tradicional de Pisac", "Almuerzo buffet gourmet en Urubamba", "Ciudadela Viviente de Ollantaytambo", "Paisajes espectaculares de los Andes", "Recorrido histórico por el Valle Sagrado"]', 
 '["Recojo compartido o privado en su hotel", "Transporte turístico de ida y retorno", "Guía oficial de turismo especializado", "Almuerzo buffet en Urubamba", "Tickets de ingreso a los sitios indicados", "Botiquín de primeros auxilios y oxígeno"]', 
 '["Bebidas extras durante el almuerzo", "Compras personales en los mercados", "Propinas opcionales"]', 'valle_sagrado', 10),

('VALLE SUR Y CAPILLA SIXTINA DE AMÉRICA', 'Exploración de la ingeniería hidráulica de Tipón y el centro Wari de Pikillacta. Finalizaremos en la Iglesia de Andahuaylillas.', 35.00, 80.00, 
 '["Ingeniería hidráulica inca de Tipón", "Ciudadela Pre-inca Wari de Pikillacta", "Iglesia de Andahuaylillas (Arte Barroco)", "Paisajes del Valle del río Huatanay", "Historia del urbanismo antiguo en Cusco", "Fusión cultural andino-colonial"]', 
 '["Traslado ida y retorno desde su hotel", "Transporte turístico con chofer profesional", "Guía especializado en arte virreinal", "Tickets de ingreso a todos los sitios", "Asistencia personalizada durante el tour", "Equipo de primeros auxilios a bordo"]', 
 '["Almuerzo (Existen opciones típicas en ruta)", "Gastos personales", "Servicios no mencionados"]', 'valle_sur', 6),

('MONTAÑA DE 7 COLORES (VINICUNCA)', 'Caminata hacia la famosa montaña Vinicunca para apreciar sus franjas minerales de colores. Vistas del nevado Ausangate.', 45.00, 100.00, 
 '["Caminata a la cima de Vinicunca", "Vistas del Nevado Ausangate", "Paisajes de la Cordillera del Vilcanota", "Observación de alpacas y vida andina", "Conexión con los Apus sagrados", "Fotografía en el mirador de colores"]', 
 '["Recojo en su hotel en Cusco", "Transporte turístico especializado", "Desayuno y almuerzo buffet nutritivos", "Guía profesional de alta montaña", "Balón de oxígeno y botiquín completo", "Tickets de ingreso a la comunidad"]', 
 '["Alquiler de caballo (Opcional)", "Bastones profesionales y propinas", "Seguros médicos personales"]', 'vinicunca', 12),

('SANTUARIO HISTÓRICO DE MACHU PICCHU', 'Visita guiada a la Ciudad Perdida de los Incas. Incluye viaje en tren hasta Aguas Calientes y ascenso al santuario.', 250.00, 270.00, 
 '["Recorrido guiado por la Ciudadela Inca", "Vista panorámica clásica de Machu Picchu", "Viaje escénico en tren hacia la selva alta", "Visita al Intihuatana y Templos principales", "Tiempo libre en el pueblo de Aguas Calientes", "Asistencia en traslados y estaciones"]', 
 '["Ticket de ingreso oficial al Santuario", "Boleto de tren ida y retorno (Ruta elegida)", "Boletos de bus subida y bajada a la Ciudadela", "Guía oficial de turismo bilingüe certificado", "Traslados Hotel - Estación - Hotel", "Asistencia permanente durante el viaje"]', 
 '["Alimentación y bebidas en Aguas Calientes", "Entrada a montañas Huayna Picchu", "Propinas para guías y equipo"]', 'machupicchu', 14),

('TOUR MÍSTICO Y CONEXIÓN ANDINA', 'Ceremonia de limpieza espiritual y meditación en centros energéticos. Conexión con la sabiduría andina ancestral.', 35.00, 80.00, 
 '["Ceremonia de Pago a la Tierra", "Meditación en Centros Energéticos", "Explicación de la Cosmovisión Andina", "Conexión con los Apus guardianes", "Sesión de Limpieza espiritual", "Encuentro con maestros locales"]', 
 '["Transporte privado exclusivo", "Guía espiritual experto en misticismo", "Kit de ofrendas para el ritual", "Mantas térmicas para meditación", "Entradas a los centros de poder", "Asistencia personalizada"]', 
 '["Alimentación pesada (Se sugiere ayuno)", "Gastos personales y propinas"]', 'mistico', 6),

('LAGUNA HUMANTAY Y GLACIAR SALKANTAY', 'Aventura hacia una laguna turquesa a los pies del glaciar Humantay. Caminata escénica en Soraypampa.', 45.00, 100.00, 
 '["Caminata a la Laguna Turquesa Humantay", "Vistas de los Glaciares Humantay y Salkantay", "Paisajes de alta montaña sobre los 4,200m", "Ceremonia de agradecimiento a la tierra", "Fotografía en el espejo de agua natural", "Experiencia de aventura y aire puro"]', 
 '["Recojo y transporte turístico dedicado", "Desayuno y almuerzo buffet andino", "Guía oficial experto en aventura", "Bastones de caminata para el tour", "Botiquín y oxígeno de emergencia", "Ingresos al área protegida"]', 
 '["Alquiler de caballo (Comuneros)", "Gastos personales y snacks en ruta"]', 'humantay', 12)
ON CONFLICT (nombre) DO UPDATE SET 
    descripcion = EXCLUDED.descripcion,
    precio_base_usd = EXCLUDED.precio_base_usd,
    precio_nacional = EXCLUDED.precio_nacional,
    highlights = EXCLUDED.highlights,
    servicios_incluidos = EXCLUDED.servicios_incluidos,
    servicios_no_incluidos = EXCLUDED.servicios_no_incluidos,
    carpeta_img = EXCLUDED.carpeta_img;

-- 2. INSERTAR PAQUETES (4 PAQUETES)
INSERT INTO paquete (nombre, descripcion, dias, noches, precio_sugerido)
VALUES 
('CUSCO TRADICIONAL 3D/2N', 'Paquete clásico que incluye Cusco Imperial, Valle Sagrado y Machu Picchu.', 3, 2, 0),
('CUSCO TRADICIONAL 4D/3N', 'Extensión que incluye la famosa Montaña de 7 colores (Vinicunca).', 4, 3, 0),
('CUSCO TRADICIONAL 5D/4N', 'Aventura completa con Machu Picchu, Montaña 7 Colores y Laguna Humantay.', 5, 4, 0),
('PERÚ PARA EL MUNDO 8D/7N', 'El gran tour de Perú: Lima, Paracas/Ica, Cusco, Valle y Machu Picchu.', 8, 7, 0)
ON CONFLICT (nombre) DO UPDATE SET 
    descripcion = EXCLUDED.descripcion,
    dias = EXCLUDED.dias,
    noches = EXCLUDED.noches;

-- 3. VINCULAR PAQUETES CON TOURS (RELAClONES)
DELETE FROM paquete_tour;

-- Paquete 3D/2N
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 1 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 3D/2N' AND t.nombre = 'RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 2 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 3D/2N' AND t.nombre = 'VALLE SAGRADO: PISAC Y OLLANTAYTAMBO';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 3 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 3D/2N' AND t.nombre = 'SANTUARIO HISTÓRICO DE MACHU PICCHU';

-- Paquete 4D/3N
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 1 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 4D/3N' AND t.nombre = 'RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 2 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 4D/3N' AND t.nombre = 'VALLE SAGRADO: PISAC Y OLLANTAYTAMBO';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 3 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 4D/3N' AND t.nombre = 'SANTUARIO HISTÓRICO DE MACHU PICCHU';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 4 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 4D/3N' AND t.nombre = 'MONTAÑA DE 7 COLORES (VINICUNCA)';

-- Paquete 5D/4N
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 1 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 5D/4N' AND t.nombre = 'RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 2 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 5D/4N' AND t.nombre = 'VALLE SAGRADO: PISAC Y OLLANTAYTAMBO';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 3 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 5D/4N' AND t.nombre = 'SANTUARIO HISTÓRICO DE MACHU PICCHU';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 4 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 5D/4N' AND t.nombre = 'MONTAÑA DE 7 COLORES (VINICUNCA)';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 5 FROM paquete p, tour t WHERE p.nombre = 'CUSCO TRADICIONAL 5D/4N' AND t.nombre = 'LAGUNA HUMANTAY Y GLACIAR SALKANTAY';

-- Paquete 8D/7N
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 1 FROM paquete p, tour t WHERE p.nombre = 'PERÚ PARA EL MUNDO 8D/7N' AND t.nombre = 'CITY TOUR LIMA COLONIAL Y MODERNA';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 3 FROM paquete p, tour t WHERE p.nombre = 'PERÚ PARA EL MUNDO 8D/7N' AND t.nombre = 'RECEPCIÓN Y CITY TOUR CUSCO IMPERIAL';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 4 FROM paquete p, tour t WHERE p.nombre = 'PERÚ PARA EL MUNDO 8D/7N' AND t.nombre = 'VALLE SAGRADO: PISAC Y OLLANTAYTAMBO';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 5 FROM paquete p, tour t WHERE p.nombre = 'PERÚ PARA EL MUNDO 8D/7N' AND t.nombre = 'SANTUARIO HISTÓRICO DE MACHU PICCHU';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 6 FROM paquete p, tour t WHERE p.nombre = 'PERÚ PARA EL MUNDO 8D/7N' AND t.nombre = 'MONTAÑA DE 7 COLORES (VINICUNCA)';
INSERT INTO paquete_tour (id_paquete, id_tour, orden)
SELECT p.id_paquete, t.id_tour, 7 FROM paquete p, tour t WHERE p.nombre = 'PERÚ PARA EL MUNDO 8D/7N' AND t.nombre = 'VALLE SUR Y CAPILLA SIXTINA DE AMÉRICA';

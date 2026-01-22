-- ==============================================================
-- ACTUALIZACIÓN DE HORARIOS - CATÁLOGO DE TOURS
-- ==============================================================
-- Este script define las horas de inicio típicas para que el
-- Itinerario sea 100% automático al seleccionar un tour.

UPDATE tour SET hora_inicio = '06:00 AM' WHERE nombre ILIKE '%Machu Picchu%' OR nombre ILIKE '%Valle Sagrado%';
UPDATE tour SET hora_inicio = '01:00 PM' WHERE nombre ILIKE '%City Tour%';
UPDATE tour SET hora_inicio = '04:30 AM' WHERE nombre ILIKE '%7 Colores%' OR nombre ILIKE '%Humantay%';
UPDATE tour SET hora_inicio = '08:00 AM' WHERE hora_inicio IS NULL;

-- Verificar cambios
-- SELECT nombre, hora_inicio FROM tour;

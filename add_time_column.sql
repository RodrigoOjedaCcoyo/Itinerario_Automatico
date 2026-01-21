-- Agregando Columna de Hora de Inicio a los Tours
-- Ejecuta esto en Supabase SQL Editor para actualizar tu tabla

ALTER TABLE tour 
ADD COLUMN hora_inicio VARCHAR(20) DEFAULT '08:00 AM';

-- Opcional: Actualizar algunos tours conocidos con horas reales (Ejemplos)
UPDATE tour SET hora_inicio = '04:00 AM' WHERE nombre ILIKE '%Montaña%';
UPDATE tour SET hora_inicio = '04:30 AM' WHERE nombre ILIKE '%Laguna%';
UPDATE tour SET hora_inicio = '01:30 PM' WHERE nombre ILIKE '%City%';
UPDATE tour SET hora_inicio = '09:00 AM' WHERE nombre ILIKE '%Valle Sagrado%';
UPDATE tour SET hora_inicio = '06:00 AM' WHERE nombre ILIKE '%Machu Picchu%';

-- Verificación
SELECT nombre, hora_inicio FROM tour;

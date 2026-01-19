-- ==============================================================
-- PARCHE DE ESQUEMA: TABLA TOUR (PARA DISEÑO PREMIUM)
-- ==============================================================
-- Ejecuta esto en el SQL Editor de Supabase para habilitar 
-- las columnas que guardan los highlights y servicios.

ALTER TABLE tour 
ADD COLUMN IF NOT EXISTS highlights JSONB,
ADD COLUMN IF NOT EXISTS servicios_incluidos JSONB,
ADD COLUMN IF NOT EXISTS servicios_no_incluidos JSONB,
ADD COLUMN IF NOT EXISTS precio_nacional DECIMAL(10,2),
ADD COLUMN IF NOT EXISTS carpeta_img TEXT;

COMMENT ON COLUMN tour.highlights IS 'Puntos clave del tour para el PDF';
COMMENT ON COLUMN tour.servicios_incluidos IS 'Servicios con iconos para la culebrita';

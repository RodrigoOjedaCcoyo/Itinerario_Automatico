-- ==========================================
-- PARCHE DE SEGURIDAD: AÑADIR CONTRASEÑAS
-- ==========================================

-- 1. Añadir la columna password a la tabla usuarios_app
ALTER TABLE usuarios_app ADD COLUMN IF NOT EXISTS password VARCHAR(255);

-- 2. Establecer una contraseña temporal para los usuarios actuales
-- IMPORTANTE: Cambia 'Cusco2026' por la contraseña que tú quieras.
UPDATE usuarios_app SET password = '123' WHERE password IS NULL;

-- 3. Hacer que la columna sea obligatoria para el futuro
ALTER TABLE usuarios_app ALTER COLUMN password SET NOT NULL;

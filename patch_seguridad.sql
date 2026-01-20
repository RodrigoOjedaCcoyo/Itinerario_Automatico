-- ==========================================
-- PARCHE DE SEGURIDAD: AÑADIR CONTRASEÑAS
-- ==========================================

-- 1. Añadir la columna password a la tabla usuarios_app
ALTER TABLE usuarios_app ADD COLUMN IF NOT EXISTS password VARCHAR(255);

-- 2. Asegurarnos de que existan los usuarios base
INSERT INTO usuarios_app (email, password, rol) VALUES 
('ventas@agencia.com', '123', 'VENTAS'),
('gerencia@agencia.com', '123', 'GERENCIA')
ON CONFLICT (email) DO UPDATE SET password = '123';

-- 3. Establecer contraseña a cualquier otro usuario que haya quedado nulo
UPDATE usuarios_app SET password = '123' WHERE password IS NULL;

-- 4. Hacer que la columna sea obligatoria
ALTER TABLE usuarios_app ALTER COLUMN password SET NOT NULL;

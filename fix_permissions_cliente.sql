-- Script de Corrección de Permisos para Tabla CLIENTE
-- Ejecuta esto en el SQL Editor de Supabase para desbloquear la búsqueda

-- 1. Asegurar que RLS esté activo (por seguridad estándar)
ALTER TABLE cliente ENABLE ROW LEVEL SECURITY;

-- 2. Eliminar políticas antiguas para evitar conflictos
DROP POLICY IF EXISTS "Permiso Total Cliente" ON cliente;
DROP POLICY IF EXISTS "Acceso total" ON cliente;

-- 3. Crear una política permisiva para que la App pueda leer/escribir
-- IMPORTANTE: "USING (true)" significa que CUALQUIERA con acceso a la app puede leer/editar.
-- Dado que es una app interna de ventas, esto es aceptable y necesario para que el buscador funcione.
CREATE POLICY "Permiso Total Cliente"
ON cliente
FOR ALL
USING (true)
WITH CHECK (true);

-- Verificación (Opcional, solo para confirmar en la consola)
SELECT * FROM cliente LIMIT 1;

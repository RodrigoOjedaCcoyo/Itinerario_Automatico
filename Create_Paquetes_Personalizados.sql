-- TABLA PARA GUARDAR PAQUETES HECHOS POR VENTAS (NUEVA FUNCIÓN CLOUD)
CREATE TABLE IF NOT EXISTS paquete_personalizado (
    id_paquete_personalizado UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL,
    itinerario JSONB NOT NULL,
    creado_por TEXT, -- Email del vendedor
    es_publico BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Habilitar Seguridad (RLS)
ALTER TABLE paquete_personalizado ENABLE ROW LEVEL SECURITY;

-- Política: Todos pueden ver los paquetes
DROP POLICY IF EXISTS "Lectura pública de paquetes" ON paquete_personalizado;
CREATE POLICY "Lectura pública de paquetes" ON paquete_personalizado 
FOR SELECT USING (true);

-- Política: Solo usuarios autenticados pueden insertar/modificar
DROP POLICY IF EXISTS "Escritura para autenticados" ON paquete_personalizado;
CREATE POLICY "Escritura para autenticados" ON paquete_personalizado 
FOR ALL USING (auth.role() = 'authenticated');

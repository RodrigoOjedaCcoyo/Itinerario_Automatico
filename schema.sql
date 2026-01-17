-- TABLA PRINCIPAL PARA EL "CEREBRO" (SUPABASE)
-- Copia y pega esto en tu SQL Editor de Supabase

CREATE TABLE IF NOT EXISTS itinerarios (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Campos planos para búsqueda rápida y reportes
    pasajero TEXT,
    celular TEXT,
    vendedor TEXT,
    categoria TEXT, -- Nacional / Extranjero
    fuente TEXT,    -- WhatsApp, Facebook, etc.
    estado TEXT,    -- Frío, Tibio, Caliente
    
    -- El "Cerebro" de la data (Días, tours, imágenes, precios detallados)
    datos JSONB,
    
    -- Opcional: Para auditoría
    ultima_modificacion TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Índices para que las búsquedas por nombre sean instantáneas
CREATE INDEX IF NOT EXISTS idx_itinerarios_pasajero ON itinerarios (pasajero);
CREATE INDEX IF NOT EXISTS idx_itinerarios_vendedor ON itinerarios (vendedor);

-- Políticas de Seguridad (RLS) - Ajustar según necesidad
ALTER TABLE itinerarios ENABLE ROW LEVEL SECURITY;

-- Permitir que cualquier persona con la anon-key pueda insertar y leer (Ajustar para producción)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir todo a anon-key') THEN
        CREATE POLICY "Permitir todo a anon-key" ON itinerarios FOR ALL USING (true) WITH CHECK (true);
    END IF;
END $$;

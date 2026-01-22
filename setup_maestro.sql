-- ==============================================================
-- SETUP TOTAL (PULIDO Y BLINDADO): APP VIAJES CUSCO PERÚ
-- ==============================================================
-- Mejoras aplicadas: Restricciones de integridad, Índices de velocidad,
-- Valores JSONB por defecto y consistencia de Auditoría.
-- ==============================================================

-- 0. EXTENSIONES (Necesaria para UUIDs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. DEFINICIÓN DE TABLAS
-- --------------------------------------------------------------

-- ACCESO Y ROLES (Sincronizado con main.py: 'CONTABILIDAD')
CREATE TABLE usuarios_app (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Nueva columna de seguridad
    rol VARCHAR(50) NOT NULL -- 'VENTAS', 'OPERACIONES', 'CONTABILIDAD', 'GERENCIA'
);

-- NÚCLEO COMERCIAL
CREATE TABLE vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL, -- Blindado contra duplicados
    email VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);

CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo_cliente VARCHAR(50) DEFAULT 'B2C',
    pais VARCHAR(100),
    genero VARCHAR(20),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lead (
    id_lead SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor),
    numero_celular VARCHAR(20) NOT NULL,
    red_social VARCHAR(50),
    estado_lead VARCHAR(50) DEFAULT 'NUEVO',
    comentario TEXT,
    fecha_seguimiento DATE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    whatsapp BOOLEAN DEFAULT TRUE,
    nombre_pasajero VARCHAR(255),
    ultimo_itinerario_id UUID
);

-- CATÁLOGO
CREATE TABLE tour (
    id_tour SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    duracion_horas INTEGER,
    precio_base_usd DECIMAL(10,2),
    highlights JSONB DEFAULT '[]'::jsonb,          -- Default para evitar NoneType
    servicios_incluidos JSONB DEFAULT '[]'::jsonb,   -- Default para evitar NoneType
    servicios_no_incluidos JSONB DEFAULT '[]'::jsonb,-- Default para evitar NoneType
    precio_nacional DECIMAL(10,2),
    carpeta_img TEXT,
    hora_inicio VARCHAR(20) DEFAULT '08:00 AM'
);

CREATE TABLE paquete (
    id_paquete SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    dias INTEGER,
    noches INTEGER,
    precio_sugerido DECIMAL(10,2)
);

CREATE TABLE paquete_tour (
    id_paquete INTEGER REFERENCES paquete(id_paquete) ON DELETE CASCADE,
    id_tour INTEGER REFERENCES tour(id_tour),
    orden INTEGER NOT NULL,
    PRIMARY KEY (id_paquete, id_tour)
);

-- ITINERARIO DIGITAL
CREATE TABLE itinerario_digital (
    id_itinerario_digital UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_lead INTEGER REFERENCES lead(id_lead) ON DELETE SET NULL,
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor),
    nombre_pasajero_itinerario VARCHAR(255),
    datos_render JSONB DEFAULT '{}'::jsonb, -- Default para evitar KeyError
    fecha_generacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    url_pdf TEXT
);

-- VENTAS Y PAGOS
CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES cliente(id_cliente),
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor),
    id_itinerario_digital UUID REFERENCES itinerario_digital(id_itinerario_digital),
    id_paquete INTEGER REFERENCES paquete(id_paquete),
    fecha_venta DATE DEFAULT CURRENT_DATE,
    canal_venta VARCHAR(50),
    precio_total_cierre DECIMAL(10,2) NOT NULL,
    moneda VARCHAR(10) DEFAULT 'USD',
    estado_venta VARCHAR(50) DEFAULT 'CONFIRMADO',
    tour_nombre VARCHAR(255),
    url_itinerario TEXT,
    url_comprobante_pago TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- Auditoría
);

CREATE TABLE venta_tour (
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE CASCADE,
    n_linea INTEGER NOT NULL,
    id_tour INTEGER REFERENCES tour(id_tour),
    fecha_servicio DATE NOT NULL,
    precio_applied DECIMAL(10,2),
    costo_applied DECIMAL(10,2),
    cantidad_pasajeros INTEGER DEFAULT 1,
    hora_inicio VARCHAR(20) DEFAULT '08:00 AM',
    observaciones TEXT,
    id_itinerario_dia_index INTEGER,
    PRIMARY KEY (id_venta, n_linea)
);

CREATE TABLE pago (
    id_pago SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE CASCADE,
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto_pagado DECIMAL(10,2) NOT NULL,
    moneda VARCHAR(10) DEFAULT 'USD',
    metodo_pago VARCHAR(50),
    tipo_pago VARCHAR(50),
    observacion TEXT,
    url_comprobante TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- Auditoría
);

-- OPERACIONES
CREATE TABLE pasajero (
    id_pasajero SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE CASCADE,
    nombre_completo VARCHAR(255) NOT NULL,
    nacionalidad VARCHAR(100),
    numero_documento VARCHAR(50),
    tipo_documento VARCHAR(20),
    edad INTEGER,
    restricciones_alimentarias TEXT
);

CREATE TABLE guia (
    id_guia SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    idioma VARCHAR(100),
    telefono VARCHAR(20),
    estado VARCHAR(20) DEFAULT 'DISPONIBLE'
);

CREATE TABLE asignacion_guia (
    id_venta INTEGER,
    n_linea INTEGER,
    id_guia INTEGER REFERENCES guia(id_guia),
    fecha_servicio DATE NOT NULL,
    PRIMARY KEY (id_venta, n_linea, id_guia),
    FOREIGN KEY (id_venta, n_linea) REFERENCES venta_tour(id_venta, n_linea)
);

CREATE TABLE requerimiento (
    id SERIAL PRIMARY KEY,
    area_solicitante VARCHAR(50),
    descripcion TEXT,
    monto_estimado DECIMAL(10,2),
    estado VARCHAR(30) DEFAULT 'PENDIENTE',
    fecha_solicitud TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------
-- 2. ÍNDICES DE VELOCIDAD (MEJORA DE PERFORMANCE)
-- --------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_lead_celular ON lead(numero_celular);
CREATE INDEX IF NOT EXISTS idx_itinerary_search ON itinerario_digital(nombre_pasajero_itinerario);
CREATE INDEX IF NOT EXISTS idx_cliente_nombre ON cliente(nombre);
CREATE INDEX IF NOT EXISTS idx_venta_fecha ON venta(fecha_venta);

-- --------------------------------------------------------------
-- 3. DATOS INICIALES (SEMILLAS)
-- --------------------------------------------------------------
-- Limpieza preventiva para las semillas
DELETE FROM usuarios_app;
DELETE FROM vendedor;

INSERT INTO usuarios_app (email, password, rol) VALUES 
('TU_CORREO_MAESTRO@gmail.com', '123', 'GERENCIA'),
('ventas@agencia.com', '123', 'VENTAS'),
('operaciones@agencia.com', '123', 'OPERACIONES'),
('contabilidad@agencia.com', '123', 'CONTABILIDAD'),
('gerencia@agencia.com', '123', 'GERENCIA');

INSERT INTO vendedor (nombre, email) VALUES 
('Angel', 'angel@agencia.com'),
('Abel', 'abel@agencia.com'),
('Admin', 'admin@agencia.com');

-- --------------------------------------------------------------
-- 4. SEGURIDAD Y STORAGE (POLITICAS)
-- --------------------------------------------------------------
DO $$ 
DECLARE 
    t text;
BEGIN
    FOR t IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' 
    LOOP
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', t);
        -- Evitamos error si la política ya existe
        BEGIN
            EXECUTE format('CREATE POLICY "Acceso total" ON %I FOR ALL USING (true) WITH CHECK (true);', t);
        EXCEPTION WHEN others THEN
            NULL;
        END;
    END LOOP;
END $$;

-- Políticas de Storage
-- Nota: Asegúrate de crear los buckets 'itinerarios' y 'vouchers' en el Dashboard de Supabase primero.
DO $$ 
BEGIN
    BEGIN
        CREATE POLICY "Acceso Público Itinerarios" ON storage.objects FOR SELECT USING (bucket_id = 'itinerarios');
    EXCEPTION WHEN others THEN NULL; END;
    
    BEGIN
        CREATE POLICY "Subida Libre Itinerarios" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'itinerarios');
    EXCEPTION WHEN others THEN NULL; END;
    
    BEGIN
        CREATE POLICY "Acceso Público Vouchers" ON storage.objects FOR SELECT USING (bucket_id = 'vouchers');
    EXCEPTION WHEN others THEN NULL; END;
    
    BEGIN
        CREATE POLICY "Subida Libre Vouchers" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'vouchers');
    EXCEPTION WHEN others THEN NULL; END;
END $$;

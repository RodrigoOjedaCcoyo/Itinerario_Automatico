-- ==============================================================
-- ESQUEMA SQL DEFINITIVO - APP VIAJES CUSCO PERÚ v2.0
-- ==============================================================
-- Fecha de Creación: 22 de Enero 2026
-- Versión: 2.0 (Producción)
--
-- INSTRUCCIONES DE INSTALACIÓN:
-- 1. Respaldar base de datos actual (si existe)
-- 2. Limpiar esquema: DROP SCHEMA public CASCADE; CREATE SCHEMA public;
-- 3. Restaurar permisos del esquema (ver sección al final)
-- 4. Ejecutar este script completo en SQL Editor de Supabase
-- 5. Crear buckets en Storage: 'itinerarios' y 'vouchers' (Públicos)
-- 6. Actualizar TU_CORREO_MAESTRO@gmail.com con tu email real
-- ==============================================================


-- ==============================================================
-- SECCIÓN 1: TABLAS DE AUTENTICACIÓN Y ROLES
-- ==============================================================


CREATE TABLE usuarios_app (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK (rol IN ('VENTAS', 'OPERACIONES', 'CONTABILIDAD', 'GERENCIA')),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP WITH TIME ZONE
);


COMMENT ON TABLE usuarios_app IS 'Usuarios con acceso al sistema por email y rol';
COMMENT ON COLUMN usuarios_app.rol IS 'Rol del usuario: VENTAS, OPERACIONES, CONTABILIDAD o GERENCIA';


-- ==============================================================
-- SECCIÓN 2: NÚCLEO COMERCIAL
-- ==============================================================


CREATE TABLE vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    estado VARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'INACTIVO')),
    comision_pct DECIMAL(5,2) DEFAULT 0.00,
    fecha_ingreso DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE vendedor IS 'Vendedores de la agencia (para listas desplegables y asignaciones)';


CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(20),
    tipo_cliente VARCHAR(50) DEFAULT 'B2C' CHECK (tipo_cliente IN ('B2C', 'B2B', 'CORPORATIVO')),
    pais VARCHAR(100),
    ciudad VARCHAR(100),
    genero VARCHAR(20),
    fecha_nacimiento DATE,
    documento_identidad VARCHAR(50),
    preferencias_contacto TEXT,
    notas TEXT,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultima_compra DATE
);


COMMENT ON TABLE cliente IS 'Clientes de la agencia (B2C=Individual, B2B=Agencia, CORPORATIVO=Empresa)';


CREATE TABLE lead (
    id_lead SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor) ON DELETE SET NULL,
    numero_celular VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    red_social VARCHAR(50),
    estado_lead VARCHAR(50) DEFAULT 'NUEVO' CHECK (estado_lead IN ('NUEVO', 'CONTACTADO', 'COTIZADO', 'NEGOCIACION', 'GANADO', 'PERDIDO')),
    motivo_interes VARCHAR(100),
    comentario TEXT,
    fecha_seguimiento DATE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_conversion TIMESTAMP WITH TIME ZONE,
    whatsapp BOOLEAN DEFAULT TRUE,
    nombre_pasajero VARCHAR(255),
    pais_origen VARCHAR(100),
    presupuesto_estimado DECIMAL(10,2),
    ultimo_itinerario_id UUID
);


COMMENT ON TABLE lead IS 'Clientes potenciales en proceso de conversión';
COMMENT ON COLUMN lead.estado_lead IS 'Pipeline de ventas: NUEVO → CONTACTADO → COTIZADO → NEGOCIACION → GANADO/PERDIDO';


-- ==============================================================
-- SECCIÓN 3: CATÁLOGO DE PRODUCTOS
-- ==============================================================


CREATE TABLE tour (
    id_tour SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    duracion_horas INTEGER,
    duracion_dias INTEGER,
    precio_base_usd DECIMAL(10,2),
    precio_nacional DECIMAL(10,2),
    categoria VARCHAR(50),
    dificultad VARCHAR(20) CHECK (dificultad IN ('FACIL', 'MODERADO', 'DIFICIL', 'EXTREMO')),
    capacidad_max INTEGER,
    edad_minima INTEGER,
    temporada_recomendada VARCHAR(100),
    incluye TEXT,
    no_incluye TEXT,
    recomendaciones TEXT,
    highlights JSONB,
    servicios_incluidos JSONB,
    servicios_no_incluidos JSONB,
    carpeta_img TEXT,
    hora_inicio VARCHAR(20) DEFAULT '08:00 AM', -- ✅ AGREGADO PARA ITINERARIO AUTOMÁTICO
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE tour IS 'Catálogo de tours individuales ofrecidos por la agencia';
COMMENT ON COLUMN tour.highlights IS 'Puntos clave del tour en formato JSON para PDFs premium';
COMMENT ON COLUMN tour.servicios_incluidos IS 'Servicios con íconos SVG para diseño visual';


CREATE TABLE paquete (
    id_paquete SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    dias INTEGER NOT NULL,
    noches INTEGER NOT NULL,
    precio_sugerido DECIMAL(10,2),
    temporada VARCHAR(50),
    destino_principal VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE paquete IS 'Paquetes prediseñados (combinaciones de tours)';


CREATE TABLE paquete_tour (
    id_paquete INTEGER REFERENCES paquete(id_paquete) ON DELETE CASCADE,
    id_tour INTEGER REFERENCES tour(id_tour) ON DELETE RESTRICT,
    orden INTEGER NOT NULL,
    dia_del_paquete INTEGER,
    notas TEXT,
    PRIMARY KEY (id_paquete, id_tour, orden)
);


COMMENT ON TABLE paquete_tour IS 'Relación entre paquetes y tours (composición)';


CREATE TABLE catalogo_tours_imagenes (
    id_tour INTEGER REFERENCES tour(id_tour) ON DELETE CASCADE PRIMARY KEY,
    urls_imagenes JSONB DEFAULT '[]'::jsonb,
    url_principal TEXT,
    ultima_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE catalogo_tours_imagenes IS 'Galería de imágenes para cada tour del catálogo';


-- ==============================================================
-- SECCIÓN 4: ITINERARIOS DIGITALES
-- ==============================================================


CREATE TABLE itinerario_digital (
    id_itinerario_digital UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_lead INTEGER REFERENCES lead(id_lead) ON DELETE SET NULL,
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor) ON DELETE SET NULL,
    nombre_pasajero_itinerario VARCHAR(255),
    email_pasajero VARCHAR(255),
    telefono_pasajero VARCHAR(20),
    datos_render JSONB NOT NULL,
    version_constructor VARCHAR(20),
    fecha_generacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_envio TIMESTAMP WITH TIME ZONE,
    fecha_visto TIMESTAMP WITH TIME ZONE,
    url_pdf TEXT,
    estado VARCHAR(30) DEFAULT 'GENERADO' CHECK (estado IN ('GENERADO', 'ENVIADO', 'VISTO', 'ACEPTADO', 'RECHAZADO')),
    canal_envio VARCHAR(50),
    notas TEXT
);


COMMENT ON TABLE itinerario_digital IS 'Itinerarios personalizados generados para clientes (con UUID único)';
COMMENT ON COLUMN itinerario_digital.datos_render IS 'JSON completo para renderizar el PDF (days, servicios, precios, etc)';
COMMENT ON COLUMN itinerario_digital.version_constructor IS 'interno/externo para identificar estructura JSON';


-- ==============================================================
-- SECCIÓN 5: VENTAS Y PAGOS
-- ==============================================================


CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES cliente(id_cliente) ON DELETE RESTRICT,
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor) ON DELETE RESTRICT,
    id_itinerario_digital UUID REFERENCES itinerario_digital(id_itinerario_digital) ON DELETE SET NULL,
    id_paquete INTEGER REFERENCES paquete(id_paquete) ON DELETE SET NULL,
    fecha_venta DATE DEFAULT CURRENT_DATE NOT NULL,
    fecha_inicio DATE,                    
    fecha_fin DATE,                       
    canal_venta VARCHAR(50),
    precio_total_cierre DECIMAL(10,2) NOT NULL,
    costo_total DECIMAL(10,2),
    utilidad_bruta DECIMAL(10,2),
    moneda VARCHAR(10) DEFAULT 'USD' CHECK (moneda IN ('USD', 'PEN', 'EUR')),
    tipo_cambio DECIMAL(8,4),
    estado_venta VARCHAR(50) DEFAULT 'CONFIRMADO' CHECK (estado_venta IN ('COTIZADO', 'CONFIRMADO', 'EN_CURSO', 'COMPLETADO', 'CANCELADO')),
    tour_nombre VARCHAR(255),             
    num_pasajeros INTEGER DEFAULT 1,
    observaciones TEXT,
    url_itinerario TEXT,
    url_comprobante_pago TEXT,
    cancelada BOOLEAN DEFAULT FALSE,
    motivo_cancelacion TEXT,
    fecha_cancelacion TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE venta IS 'Ventas confirmadas de la agencia (convertidas desde leads o directas)';


CREATE TABLE venta_tour (
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE CASCADE,
    n_linea INTEGER NOT NULL,
    id_tour INTEGER REFERENCES tour(id_tour) ON DELETE RESTRICT,
    fecha_servicio DATE NOT NULL,
    hora_inicio VARCHAR(20) DEFAULT '08:00 AM', -- ✅ CAMBIADO A VARCHAR PARA COMPATIBILIDAD
    hora_fin TIME,
    precio_applied DECIMAL(10,2),
    costo_applied DECIMAL(10,2),
    cantidad_pasajeros INTEGER DEFAULT 1,
    punto_encuentro VARCHAR(255),
    observaciones TEXT,                   
    id_itinerario_dia_index INTEGER,
    estado_servicio VARCHAR(30) DEFAULT 'PENDIENTE' CHECK (estado_servicio IN ('PENDIENTE', 'CONFIRMADO', 'EN_CURSO', 'COMPLETADO', 'CANCELADO')),
    PRIMARY KEY (id_venta, n_linea)
);


CREATE TABLE pago (
    id_pago SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE CASCADE,
    fecha_pago DATE DEFAULT CURRENT_DATE NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL CHECK (monto_pagado > 0),
    moneda VARCHAR(10) DEFAULT 'USD' CHECK (moneda IN ('USD', 'PEN', 'EUR')),
    tipo_cambio DECIMAL(8,4),
    metodo_pago VARCHAR(50) CHECK (metodo_pago IN ('EFECTIVO', 'TRANSFERENCIA', 'TARJETA', 'PAYPAL', 'YAPE', 'PLIN', 'OTRO')),
    tipo_pago VARCHAR(50) CHECK (tipo_pago IN ('ADELANTO', 'SALDO', 'TOTAL', 'PARCIAL')),
    numero_operacion VARCHAR(100),
    banco VARCHAR(100),
    observacion TEXT,
    url_comprobante TEXT,
    verificado BOOLEAN DEFAULT FALSE,
    verificado_por INTEGER REFERENCES vendedor(id_vendedor),
    fecha_verificacion TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- ==============================================================
-- SECCIÓN 6: OPERACIONES Y LOGÍSTICA
-- ==============================================================


CREATE TABLE pasajero (
    id_pasajero SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE CASCADE,
    nombre_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(20),
    nacionalidad VARCHAR(100),
    numero_documento VARCHAR(50),
    tipo_documento VARCHAR(20) CHECK (tipo_documento IN ('DNI', 'PASAPORTE', 'CARNET_EXTRANJERIA', 'OTRO')),
    fecha_nacimiento DATE,
    edad INTEGER,
    genero VARCHAR(20),
    tipo_sangre VARCHAR(5),
    alergias TEXT,
    restricciones_alimentarias TEXT,
    condiciones_medicas TEXT,
    contacto_emergencia_nombre VARCHAR(255),
    contacto_emergencia_telefono VARCHAR(20),
    es_principal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE documentacion (
    id BIGSERIAL PRIMARY KEY,
    id_pasajero INTEGER REFERENCES pasajero(id_pasajero) ON DELETE CASCADE,
    tipo_documento VARCHAR(50) CHECK (tipo_documento IN ('PASAPORTE', 'VISA', 'SEGURO_VIAJE', 'CERTIFICADO_VACUNA', 'AUTORIZACION_MENOR', 'OTRO')),
    url_archivo TEXT,
    fecha_carga TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE,
    estado_entrega VARCHAR(30) DEFAULT 'PENDIENTE' CHECK (estado_entrega IN ('PENDIENTE', 'RECIBIDO', 'VERIFICADO', 'RECHAZADO')),
    es_critico BOOLEAN DEFAULT FALSE,
    notas TEXT
);


CREATE TABLE guia (
    id_guia SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    idiomas VARCHAR(200),
    especialidades VARCHAR(200),
    licencia VARCHAR(50),
    fecha_vencimiento_licencia DATE,
    calificacion DECIMAL(3,2),
    tarifa_dia DECIMAL(10,2),
    estado VARCHAR(20) DEFAULT 'DISPONIBLE' CHECK (estado IN ('DISPONIBLE', 'OCUPADO', 'VACACIONES', 'INACTIVO')),
    notas TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE asignacion_guia (
    id_venta INTEGER,
    n_linea INTEGER,
    id_guia INTEGER REFERENCES guia(id_guia) ON DELETE RESTRICT,
    fecha_servicio DATE NOT NULL,
    hora_inicio TIME,
    hora_fin TIME,
    tarifa_aplicada DECIMAL(10,2),
    confirmado BOOLEAN DEFAULT FALSE,
    notas TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_venta, n_linea, id_guia),
    FOREIGN KEY (id_venta, n_linea) REFERENCES venta_tour(id_venta, n_linea) ON DELETE CASCADE
);


CREATE TABLE requerimiento (
    id SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES venta(id_venta) ON DELETE SET NULL,
    tipo_requerimiento VARCHAR(50) CHECK (tipo_requerimiento IN ('TRANSPORTE', 'ALOJAMIENTO', 'ALIMENTACION', 'GUIA', 'TICKETS', 'OTRO')),
    proveedor VARCHAR(255),
    descripcion TEXT NOT NULL,
    monto_estimado DECIMAL(10,2),
    monto_real DECIMAL(10,2),
    moneda VARCHAR(10) DEFAULT 'USD',
    estado VARCHAR(30) DEFAULT 'PENDIENTE' CHECK (estado IN ('PENDIENTE', 'COTIZADO', 'APROBADO', 'PAGADO', 'COMPLETADO', 'CANCELADO')),
    fecha_necesidad DATE,
    fecha_solicitud TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    solicitado_por INTEGER REFERENCES vendedor(id_vendedor),
    aprobado_por INTEGER REFERENCES vendedor(id_vendedor),
    fecha_aprobacion TIMESTAMP WITH TIME ZONE,
    url_comprobante TEXT,
    notas TEXT
);


-- ==============================================================
-- SECCIÓN 7: ÍNDICES DE RENDIMIENTO
-- ==============================================================


CREATE INDEX idx_lead_celular ON lead(numero_celular);
CREATE INDEX idx_lead_vendedor ON lead(id_vendedor) WHERE estado_lead != 'PERDIDO';
CREATE INDEX idx_lead_estado ON lead(estado_lead);
CREATE INDEX idx_cliente_nombre ON cliente(nombre);
CREATE INDEX idx_venta_fecha ON venta(fecha_venta);
CREATE INDEX idx_venta_fechas_viaje ON venta(fecha_inicio, fecha_fin);
CREATE INDEX idx_venta_tour_fecha ON venta_tour(fecha_servicio);
CREATE INDEX idx_itinerario_pasajero ON itinerario_digital(nombre_pasajero_itinerario);


-- ==============================================================
-- SECCIÓN 8: DATOS INICIALES (SEMILLAS)
-- ==============================================================


INSERT INTO usuarios_app (email, rol) VALUES
('TU_CORREO_MAESTRO@gmail.com', 'GERENCIA'),
('ventas@agencia.com', 'VENTAS'),
('operaciones@agencia.com', 'OPERACIONES'),
('contabilidad@agencia.com', 'CONTABILIDAD');


INSERT INTO vendedor (nombre, email) VALUES
('Angel', 'angel@agencia.com'),
('Abel', 'abel@agencia.com'),
('Admin', 'admin@agencia.com');


-- ==============================================================
-- SECCIÓN 9: TRIGGERS Y FUNCIONES
-- ==============================================================


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_venta_updated_at BEFORE UPDATE ON venta
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


CREATE OR REPLACE FUNCTION calcular_utilidad_venta()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.precio_total_cierre IS NOT NULL AND NEW.costo_total IS NOT NULL THEN
        NEW.utilidad_bruta = NEW.precio_total_cierre - NEW.costo_total;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER trigger_calc_utilidad BEFORE INSERT OR UPDATE ON venta
    FOR EACH ROW EXECUTE FUNCTION calcular_utilidad_venta();


-- ==============================================================
-- SECCIÓN 10: ROW LEVEL SECURITY (RLS)
-- ==============================================================


DO $$
DECLARE
    tabla_nombre text;
BEGIN
    FOR tabla_nombre IN
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', tabla_nombre);
        EXECUTE format('DROP POLICY IF EXISTS "Acceso total" ON %I;', tabla_nombre);
        EXECUTE format('CREATE POLICY "Acceso total" ON %I FOR ALL USING (true) WITH CHECK (true);', tabla_nombre);
    END LOOP;
END $$;


-- ==============================================================
-- SECCIÓN 11: POLÍTICAS DE STORAGE
-- ==============================================================


-- Nota: Asegúrate de crear los buckets 'itinerarios' y 'vouchers' en Supabase UI
DO $$ 
BEGIN
    BEGIN
        CREATE POLICY "Acceso Público Itinerarios" ON storage.objects FOR SELECT USING (bucket_id = 'itinerarios');
    EXCEPTION WHEN others THEN NULL; END;
    BEGIN
        CREATE POLICY "Subida Libre Itinerarios" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'itinerarios');
    EXCEPTION WHEN others THEN NULL; END;
END $$;


-- ==============================================================
-- SECCIÓN 12: VISTAS ÚTILES
-- ==============================================================


CREATE OR REPLACE VIEW vista_servicios_diarios AS
SELECT
    vt.fecha_servicio,
    vt.id_venta,
    vt.n_linea,
    c.nombre as cliente,
    vend.nombre as vendedor,
    COALESCE(t.nombre, vt.observaciones, v.tour_nombre) as servicio,
    vt.cantidad_pasajeros as pax,
    vt.estado_servicio,
    v.id_itinerario_digital
FROM venta_tour vt
INNER JOIN venta v ON vt.id_venta = v.id_venta
LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
LEFT JOIN vendedor vend ON v.id_vendedor = vend.id_vendedor
LEFT JOIN tour t ON vt.id_tour = t.id_tour
WHERE v.cancelada = FALSE;


-- ==============================================================
-- PERMISOS FINALES
-- ==============================================================


GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO authenticated;

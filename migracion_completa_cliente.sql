-- migracion_completa_cliente.sql
-- Script NUCLEAR: Recrea la tabla cliente desde cero con toda la estructura correcta
-- ⚠️ ADVERTENCIA: Esto eliminará todos los datos de la tabla cliente
-- Ejecutar solo si el script anterior no funciona

-- ============================================
-- OPCIÓN NUCLEAR: Recrear tabla desde cero
-- ============================================

-- 1. Eliminar tabla dependiente primero (equipo tiene FK a cliente)
DROP TABLE IF EXISTS equipo CASCADE;

-- 2. Eliminar tabla cliente
DROP TABLE IF EXISTS cliente CASCADE;

-- 3. Recrear tabla cliente con estructura correcta
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- 4. Recrear tabla equipo (porque depende de cliente)
CREATE TABLE equipo (
    id_equipo SERIAL PRIMARY KEY,
    nombre_equipo VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_serie VARCHAR(100) UNIQUE,
    id_cliente INTEGER REFERENCES cliente(id_cliente),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- 5. Insertar datos de prueba (opcional)
INSERT INTO cliente (nombre, apellido, cedula, telefono, email, direccion) VALUES
('Juan', 'Pérez', '12345678', '0414-1234567', 'juan@email.com', 'Caracas'),
('María', 'González', '87654321', '0412-9876543', 'maria@email.com', 'Valencia');

-- 6. Verificar la estructura
SELECT 'Tabla cliente creada correctamente' AS mensaje;

SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'cliente' 
ORDER BY ordinal_position;

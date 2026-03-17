-- migracion_fix_cliente.sql
-- Script para corregir la tabla cliente - Agregar columna cedula
-- Ejecutar esto en pgAdmin o psql

-- ============================================
-- PASO 1: Verificar si la columna cedula existe
-- ============================================
-- Si esto devuelve 0, la columna no existe
SELECT COUNT(*) 
FROM information_schema.columns 
WHERE table_name = 'cliente' AND column_name = 'cedula';

-- ============================================
-- PASO 2: Agregar la columna cedula si no existe
-- ============================================
DO $$
BEGIN
    -- Verificar si la columna cedula existe
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'cliente' 
        AND column_name = 'cedula'
    ) THEN
        -- Agregar la columna cedula
        ALTER TABLE cliente ADD COLUMN cedula VARCHAR(20);
        
        -- Actualizar registros existentes con un valor temporal único
        UPDATE cliente SET cedula = 'TEMP_' || id_cliente::TEXT;
        
        -- Hacer la columna NOT NULL
        ALTER TABLE cliente ALTER COLUMN cedula SET NOT NULL;
        
        -- Agregar constraint UNIQUE
        ALTER TABLE cliente ADD CONSTRAINT cliente_cedula_unique UNIQUE (cedula);
        
        RAISE NOTICE 'Columna cedula agregada exitosamente';
    ELSE
        RAISE NOTICE 'La columna cedula ya existe';
    END IF;
END $$;

-- ============================================
-- PASO 3: Verificar la estructura final
-- ============================================
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'cliente' 
ORDER BY ordinal_position;

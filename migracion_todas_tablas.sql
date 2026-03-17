-- migracion_todas_tablas.sql
-- Script SQL para corregir la columna 'cedula' en TODAS las tablas
-- Ejecutar esto en pgAdmin

-- ============================================
-- FUNCIÓN AUXILIAR: Verificar si columna existe
-- ============================================
CREATE OR REPLACE FUNCTION columna_existe(p_tabla TEXT, p_columna TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = p_tabla AND column_name = p_columna
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCIÓN AUXILIAR: Verificar si tabla existe
-- ============================================
CREATE OR REPLACE FUNCTION tabla_existe(p_tabla TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_name = p_tabla
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- CORREGIR TABLA: cliente
-- ============================================
DO $$
BEGIN
    IF tabla_existe('cliente') THEN
        IF NOT columna_existe('cliente', 'cedula') THEN
            RAISE NOTICE '🔧 Corrigiendo tabla: cliente';
            
            -- 1. Agregar columna
            ALTER TABLE cliente ADD COLUMN cedula VARCHAR(20);
            RAISE NOTICE '   ✓ Columna cedula agregada';
            
            -- 2. Actualizar registros existentes
            UPDATE cliente SET cedula = 'TEMP_' || id_cliente::TEXT;
            RAISE NOTICE '   ✓ Registros actualizados';
            
            -- 3. Hacer NOT NULL
            ALTER TABLE cliente ALTER COLUMN cedula SET NOT NULL;
            RAISE NOTICE '   ✓ Constraint NOT NULL aplicado';
            
            -- 4. Agregar UNIQUE
            ALTER TABLE cliente ADD CONSTRAINT cliente_cedula_unique UNIQUE (cedula);
            RAISE NOTICE '   ✓ Constraint UNIQUE agregado';
            
            RAISE NOTICE '✅ Tabla cliente corregida exitosamente';
        ELSE
            RAISE NOTICE '✅ Tabla cliente ya tiene la columna cedula';
        END IF;
    ELSE
        RAISE NOTICE '⚠️  Tabla cliente no existe';
    END IF;
END $$;

-- ============================================
-- CORREGIR TABLA: tecnico
-- ============================================
DO $$
BEGIN
    IF tabla_existe('tecnico') THEN
        IF NOT columna_existe('tecnico', 'cedula') THEN
            RAISE NOTICE '🔧 Corrigiendo tabla: tecnico';
            
            -- 1. Agregar columna
            ALTER TABLE tecnico ADD COLUMN cedula VARCHAR(20);
            RAISE NOTICE '   ✓ Columna cedula agregada';
            
            -- 2. Actualizar registros existentes
            UPDATE tecnico SET cedula = 'TEMP_' || id_tecnico::TEXT;
            RAISE NOTICE '   ✓ Registros actualizados';
            
            -- 3. Hacer NOT NULL
            ALTER TABLE tecnico ALTER COLUMN cedula SET NOT NULL;
            RAISE NOTICE '   ✓ Constraint NOT NULL aplicado';
            
            -- 4. Agregar UNIQUE
            ALTER TABLE tecnico ADD CONSTRAINT tecnico_cedula_unique UNIQUE (cedula);
            RAISE NOTICE '   ✓ Constraint UNIQUE agregado';
            
            RAISE NOTICE '✅ Tabla tecnico corregida exitosamente';
        ELSE
            RAISE NOTICE '✅ Tabla tecnico ya tiene la columna cedula';
        END IF;
    ELSE
        RAISE NOTICE '⚠️  Tabla tecnico no existe';
    END IF;
END $$;

-- ============================================
-- VERIFICACIÓN FINAL
-- ============================================
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name IN ('cliente', 'tecnico')
  AND column_name = 'cedula'
ORDER BY table_name;

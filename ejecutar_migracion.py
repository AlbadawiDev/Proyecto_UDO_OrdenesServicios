#!/usr/bin/env python3
"""
Script para ejecutar migración de la tabla cliente
Agrega la columna 'cedula' si no existe
"""
import sys
import os

# Agregar el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.dao.conexion import db

def verificar_columna_cedula():
    """Verifica si la columna cedula existe en la tabla cliente"""
    query = """
        SELECT COUNT(*) as existe
        FROM information_schema.columns 
        WHERE table_name = 'cliente' AND column_name = 'cedula'
    """
    cursor = db.get_cursor()
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado['existe'] > 0

def agregar_columna_cedula():
    """Agrega la columna cedula a la tabla cliente"""
    try:
        cursor = db.get_cursor()
        
        # 1. Agregar columna cedula (nullable primero)
        print("📌 Paso 1: Agregando columna cedula...")
        cursor.execute("ALTER TABLE cliente ADD COLUMN cedula VARCHAR(20)")
        db.commit()
        print("   ✅ Columna agregada")
        
        # 2. Actualizar registros existentes con valores temporales únicos
        print("📌 Paso 2: Actualizando registros existentes...")
        cursor.execute("UPDATE cliente SET cedula = 'TEMP_' || id_cliente::TEXT")
        db.commit()
        print("   ✅ Registros actualizados")
        
        # 3. Hacer la columna NOT NULL
        print("📌 Paso 3: Estableciendo NOT NULL...")
        cursor.execute("ALTER TABLE cliente ALTER COLUMN cedula SET NOT NULL")
        db.commit()
        print("   ✅ Constraint NOT NULL aplicado")
        
        # 4. Agregar constraint UNIQUE
        print("📌 Paso 4: Agregando constraint UNIQUE...")
        cursor.execute("ALTER TABLE cliente ADD CONSTRAINT cliente_cedula_unique UNIQUE (cedula)")
        db.commit()
        print("   ✅ Constraint UNIQUE agregado")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 MIGRACIÓN: Corrección tabla cliente")
    print("=" * 60)
    
    # Verificar si la columna existe
    print("\n📋 Verificando estructura actual...")
    if verificar_columna_cedula():
        print("✅ La columna 'cedula' YA existe en la tabla cliente")
        print("   No se requiere migración")
        return
    
    print("⚠️  La columna 'cedula' NO existe")
    print("   Se requiere migración\n")
    
    # Confirmar
    respuesta = input("¿Deseas ejecutar la migración? (s/n): ")
    if respuesta.lower() != 's':
        print("❌ Migración cancelada")
        return
    
    # Ejecutar migración
    print("\n🚀 Ejecutando migración...\n")
    if agregar_columna_cedula():
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nLa tabla 'cliente' ahora tiene la columna 'cedula'")
        print("Puedes probar crear un cliente nuevamente")
    else:
        print("\n" + "=" * 60)
        print("❌ MIGRACIÓN FALLIDA")
        print("=" * 60)
        print("\nRevisa el error arriba e intenta manualmente con pgAdmin")

if __name__ == '__main__':
    main()

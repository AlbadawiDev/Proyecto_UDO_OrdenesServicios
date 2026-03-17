#!/usr/bin/env python3
"""
Script para corregir TODAS las tablas que necesitan la columna 'cedula'
Arregla: cliente, tecnico, y cualquier otra tabla que la necesite
"""
import sys
import os

# Agregar el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.dao.conexion import db

# Lista de tablas que necesitan la columna cedula
TABLAS_CON_CEDULA = [
    ('cliente', 'id_cliente'),
    ('tecnico', 'id_tecnico'),
]

def verificar_columna(tabla, columna='cedula'):
    """Verifica si una columna existe en una tabla"""
    query = """
        SELECT COUNT(*) as existe
        FROM information_schema.columns 
        WHERE table_name = %s AND column_name = %s
    """
    cursor = db.get_cursor()
    cursor.execute(query, (tabla, columna))
    resultado = cursor.fetchone()
    return resultado['existe'] > 0

def agregar_columna_cedula(tabla, pk_column):
    """Agrega la columna cedula a una tabla"""
    try:
        cursor = db.get_cursor()
        
        print(f"\n📌 Procesando tabla: {tabla}")
        
        # 1. Agregar columna cedula (nullable primero)
        print(f"   → Agregando columna cedula...")
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN cedula VARCHAR(20)")
        db.commit()
        
        # 2. Actualizar registros existentes con valores temporales únicos
        print(f"   → Actualizando registros existentes...")
        cursor.execute(f"UPDATE {tabla} SET cedula = 'TEMP_' || {pk_column}::TEXT")
        db.commit()
        
        # 3. Hacer la columna NOT NULL
        print(f"   → Estableciendo NOT NULL...")
        cursor.execute(f"ALTER TABLE {tabla} ALTER COLUMN cedula SET NOT NULL")
        db.commit()
        
        # 4. Agregar constraint UNIQUE
        print(f"   → Agregando constraint UNIQUE...")
        constraint_name = f"{tabla}_cedula_unique"
        cursor.execute(f"""
            ALTER TABLE {tabla} 
            ADD CONSTRAINT {constraint_name} UNIQUE (cedula)
        """)
        db.commit()
        
        print(f"   ✅ Tabla {tabla} corregida exitosamente")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"   ❌ Error en tabla {tabla}: {e}")
        return False

def main():
    print("=" * 70)
    print("🔧 MIGRACIÓN: Corrección de columnas 'cedula' en todas las tablas")
    print("=" * 70)
    
    tablas_corregidas = []
    tablas_con_error = []
    tablas_ya_ok = []
    
    for tabla, pk in TABLAS_CON_CEDULA:
        # Verificar si la tabla existe
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT COUNT(*) as existe 
            FROM information_schema.tables 
            WHERE table_name = %s
        """, (tabla,))
        
        if cursor.fetchone()['existe'] == 0:
            print(f"\n⚠️  La tabla '{tabla}' no existe, se omite")
            continue
        
        # Verificar si ya tiene la columna cedula
        if verificar_columna(tabla, 'cedula'):
            print(f"\n✅ La tabla '{tabla}' ya tiene la columna 'cedula'")
            tablas_ya_ok.append(tabla)
        else:
            # Agregar la columna
            if agregar_columna_cedula(tabla, pk):
                tablas_corregidas.append(tabla)
            else:
                tablas_con_error.append(tabla)
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE LA MIGRACIÓN")
    print("=" * 70)
    
    if tablas_ya_ok:
        print(f"\n✅ Tablas que ya estaban correctas ({len(tablas_ya_ok)}):")
        for t in tablas_ya_ok:
            print(f"   • {t}")
    
    if tablas_corregidas:
        print(f"\n🔧 Tablas corregidas ({len(tablas_corregidas)}):")
        for t in tablas_corregidas:
            print(f"   • {t}")
    
    if tablas_con_error:
        print(f"\n❌ Tablas con error ({len(tablas_con_error)}):")
        for t in tablas_con_error:
            print(f"   • {t}")
    
    print("\n" + "=" * 70)
    
    if not tablas_con_error:
        print("🎉 ¡TODAS LAS TABLAS ESTÁN CORRECTAS!")
        print("\nAhora puedes:")
        print("   1. Crear clientes ✓")
        print("   2. Crear técnicos ✓")
        print("   3. Usar todas las funcionalidades del sistema")
    else:
        print("⚠️  Algunas tablas tuvieron errores")
        print("   Revisa los mensajes de error arriba")

if __name__ == '__main__':
    main()

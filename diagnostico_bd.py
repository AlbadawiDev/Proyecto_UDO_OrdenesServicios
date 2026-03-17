#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el estado de la base de datos
Muestra qué tablas existen y qué columnas tienen
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.dao.conexion import db

def verificar_tablas():
    """Verifica todas las tablas del sistema"""
    
    tablas_esperadas = {
        'cliente': ['id_cliente', 'nombre', 'apellido', 'cedula', 'telefono', 'email', 'direccion', 'fecha_registro', 'activo'],
        'tecnico': ['id_tecnico', 'nombre', 'apellido', 'cedula', 'especialidad', 'telefono', 'email', 'fecha_contratacion', 'activo'],
        'equipo': ['id_equipo', 'nombre_equipo', 'tipo', 'marca', 'modelo', 'numero_serie', 'id_cliente', 'fecha_registro', 'activo'],
        'servicio': ['id_servicio', 'nombre_servicio', 'descripcion', 'costo_base', 'tiempo_estimado_horas', 'activo'],
        'tipo_orden': ['id_tipo_orden', 'nombre_tipo', 'descripcion', 'requiere_aprobacion', 'activo'],
        'estatus_orden': ['id_estatus', 'nombre_estatus', 'descripcion', 'color_hex', 'orden_secuencial', 'activo'],
        'prioridad': ['id_prioridad', 'nombre_prioridad', 'nivel', 'tiempo_respuesta_horas', 'color_hex', 'activo'],
    }
    
    print("=" * 80)
    print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
    print("=" * 80)
    
    for tabla, columnas_esperadas in tablas_esperadas.items():
        print(f"\n📋 Tabla: {tabla.upper()}")
        print("-" * 40)
        
        # Verificar si la tabla existe
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT COUNT(*) as existe 
            FROM information_schema.tables 
            WHERE table_name = %s AND table_schema = 'public'
        """, (tabla,))
        
        existe = cursor.fetchone()['existe'] > 0
        
        if not existe:
            print("   ❌ La tabla NO EXISTE")
            continue
        
        print("   ✅ La tabla EXISTE")
        
        # Obtener columnas actuales
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (tabla,))
        
        columnas_actuales = {row['column_name']: row for row in cursor.fetchall()}
        
        # Verificar cada columna esperada
        for col in columnas_esperadas:
            if col in columnas_actuales:
                info = columnas_actuales[col]
                nullable = "NULL" if info['is_nullable'] == 'YES' else "NOT NULL"
                print(f"   ✅ {col:<20} {info['data_type']:<15} {nullable}")
            else:
                print(f"   ❌ {col:<20} ** FALTA **")
        
        # Ver columnas extras (no esperadas)
        columnas_extra = set(columnas_actuales.keys()) - set(columnas_esperadas)
        if columnas_extra:
            print(f"   ⚠️  Columnas extra: {', '.join(columnas_extra)}")
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    
    # Contar problemas
    problemas = []
    for tabla, columnas_esperadas in tablas_esperadas.items():
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s
        """, (tabla,))
        columnas_actuales = [row['column_name'] for row in cursor.fetchall()]
        
        faltantes = [c for c in columnas_esperadas if c not in columnas_actuales]
        if faltantes:
            problemas.append(f"{tabla}: falta {', '.join(faltantes)}")
    
    if problemas:
        print("\n❌ PROBLEMAS ENCONTRADOS:")
        for p in problemas:
            print(f"   • {p}")
        print("\n⚠️  Ejecuta: python migracion_todas_tablas.py")
    else:
        print("\n✅ ¡TODAS LAS TABLAS ESTÁN CORRECTAS!")
        print("   Puedes usar el sistema sin problemas")

if __name__ == '__main__':
    verificar_tablas()

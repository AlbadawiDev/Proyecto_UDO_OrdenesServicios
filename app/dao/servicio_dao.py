# app/dao/servicio_dao.py
"""
DAO para la entidad Servicio
"""
from app.dao.base_dao import BaseDAO
from app.models.servicio import Servicio

class ServicioDAO(BaseDAO):
    @property
    def tabla(self):
        return "servicio"
    
    @property
    def primary_key(self):
        return "id_servicio"
    
    def mapear_a_objeto(self, fila):
        if fila is None:
            return None
        return Servicio(
            id_servicio=fila.get('id_servicio'),
            nombre_servicio=fila.get('nombre_servicio'),
            descripcion=fila.get('descripcion'),
            costo_base=float(fila.get('costo_base')) if fila.get('costo_base') else None,
            tiempo_estimado_horas=fila.get('tiempo_estimado_horas'),
            activo=fila.get('activo')
        )
    
    def buscar_por_nombre(self, nombre):
        query = """
            SELECT * FROM servicio 
            WHERE nombre_servicio ILIKE %s AND activo = TRUE
        """
        try:
            from app.dao.conexion import db
            cursor = db.get_cursor()
            cursor.execute(query, (f'%{nombre}%',))
            return [self.mapear_a_objeto(fila) for fila in cursor.fetchall()]
        except Exception as e:
            raise
    
    def listar_por_rango_costo(self, min_costo, max_costo):
        query = """
            SELECT * FROM servicio 
            WHERE costo_base BETWEEN %s AND %s AND activo = TRUE
            ORDER BY costo_base
        """
        try:
            from app.dao.conexion import db
            cursor = db.get_cursor()
            cursor.execute(query, (min_costo, max_costo))
            return [self.mapear_a_objeto(fila) for fila in cursor.fetchall()]
        except Exception as e:
            raise

servicio_dao = ServicioDAO()
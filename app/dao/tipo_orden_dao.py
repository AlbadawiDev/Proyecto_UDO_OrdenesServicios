# app/dao/tipo_orden_dao.py
"""
DAO para la entidad TipoOrden
"""
from app.dao.base_dao import BaseDAO
from app.models.tipo_orden import TipoOrden

class TipoOrdenDAO(BaseDAO):
    @property
    def tabla(self):
        return "tipo_orden"
    
    @property
    def primary_key(self):
        return "id_tipo_orden"
    
    def mapear_a_objeto(self, fila):
        if fila is None:
            return None
        return TipoOrden(
            id_tipo_orden=fila.get('id_tipo_orden'),
            nombre_tipo=fila.get('nombre_tipo'),
            descripcion=fila.get('descripcion'),
            requiere_aprobacion=fila.get('requiere_aprobacion'),
            activo=fila.get('activo')
        )
    
    def buscar_por_nombre(self, nombre):
        query = """
            SELECT * FROM tipo_orden 
            WHERE nombre_tipo ILIKE %s AND activo = TRUE
        """
        try:
            from app.dao.conexion import db
            cursor = db.get_cursor()
            cursor.execute(query, (f'%{nombre}%',))
            return [self.mapear_a_objeto(fila) for fila in cursor.fetchall()]
        except Exception as e:
            raise
    
    def listar_requieren_aprobacion(self):
        """Lista tipos que requieren aprobación especial"""
        return self.buscar_por_criterio('requiere_aprobacion', True)

tipo_orden_dao = TipoOrdenDAO()
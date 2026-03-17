# app/dao/estatus_orden_dao.py
"""
DAO para la entidad EstatusOrden
"""
from app.dao.base_dao import BaseDAO
from app.models.estatus_orden import EstatusOrden

class EstatusOrdenDAO(BaseDAO):
    @property
    def tabla(self):
        return "estatus_orden"
    
    @property
    def primary_key(self):
        return "id_estatus"
    
    def mapear_a_objeto(self, fila):
        if fila is None:
            return None
        return EstatusOrden(
            id_estatus=fila.get('id_estatus'),
            nombre_estatus=fila.get('nombre_estatus'),
            descripcion=fila.get('descripcion'),
            color_hex=fila.get('color_hex'),
            orden_secuencial=fila.get('orden_secuencial'),
            activo=fila.get('activo')
        )
    
    def listar_todos(self, limite=None, offset=None):
        """Sobrescribe para ordenar por secuencia de flujo de trabajo"""
        query = """
            SELECT * FROM estatus_orden 
            WHERE activo = TRUE 
            ORDER BY orden_secuencial, id_estatus
        """
        params = []
        if limite:
            query += f" LIMIT %s"
            params.append(limite)
        if offset:
            query += f" OFFSET %s"
            params.append(offset)
            
        filas = self._query_rows(query, params)
        return [self.mapear_a_objeto(fila) for fila in filas]
    
    def buscar_por_nombre(self, nombre):
        query = """
            SELECT * FROM estatus_orden 
            WHERE nombre_estatus ILIKE %s AND activo = TRUE
        """
        filas = self._query_rows(query, (f'%{nombre}%',))
        return [self.mapear_a_objeto(fila) for fila in filas]
    
    def obtener_siguiente_estatus(self, orden_secuencial_actual):
        """Obtiene el siguiente estatus en el flujo de trabajo"""
        query = """
            SELECT * FROM estatus_orden 
            WHERE orden_secuencial > %s AND activo = TRUE
            ORDER BY orden_secuencial
            LIMIT 1
        """
        fila = self._query_row(query, (orden_secuencial_actual,))
        return self.mapear_a_objeto(fila) if fila else None

estatus_orden_dao = EstatusOrdenDAO()
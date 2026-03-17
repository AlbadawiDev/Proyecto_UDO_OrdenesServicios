# app/dao/equipo_dao.py
"""
DAO para la entidad Equipo
"""
from app.dao.base_dao import BaseDAO
from app.models.equipo import Equipo

class EquipoDAO(BaseDAO):
    @property
    def tabla(self):
        return "equipo"
    
    @property
    def primary_key(self):
        return "id_equipo"
    
    def mapear_a_objeto(self, fila):
        if fila is None:
            return None
        return Equipo(
            id_equipo=fila.get('id_equipo'),
            nombre_equipo=fila.get('nombre_equipo'),
            tipo=fila.get('tipo'),
            marca=fila.get('marca'),
            modelo=fila.get('modelo'),
            numero_serie=fila.get('numero_serie'),
            id_cliente=fila.get('id_cliente'),
            fecha_registro=fila.get('fecha_registro'),
            activo=fila.get('activo'),
            nombre_cliente=fila.get('nombre_cliente')  # Campo join
        )
    
    def listar_todos(self, limite=None, offset=None):
        """Sobrescribe para incluir nombre del cliente (JOIN)"""
        query = """
            SELECT e.*, c.nombre || ' ' || c.apellido as nombre_cliente 
            FROM equipo e
            LEFT JOIN cliente c ON e.id_cliente = c.id_cliente
            WHERE e.activo = TRUE 
            ORDER BY e.id_equipo
        """
        params = []
        if limite:
            query += f" LIMIT %s"
            params.append(limite)
        if offset:
            query += f" OFFSET %s"
            params.append(offset)
            
        try:
            from app.dao.conexion import db
            cursor = db.get_cursor()
            cursor.execute(query, params)
            return [self.mapear_a_objeto(fila) for fila in cursor.fetchall()]
        except Exception as e:
            raise
    
    def buscar_por_numero_serie(self, numero_serie):
        resultados = self.buscar_por_criterio('numero_serie', numero_serie)
        return resultados[0] if resultados else None
    
    def buscar_por_cliente(self, id_cliente):
        """Lista equipos de un cliente específico"""
        return self.buscar_por_criterio('id_cliente', id_cliente)
    
    def buscar_por_tipo(self, tipo):
        query = """
            SELECT e.*, c.nombre || ' ' || c.apellido as nombre_cliente 
            FROM equipo e
            LEFT JOIN cliente c ON e.id_cliente = c.id_cliente
            WHERE e.tipo ILIKE %s AND e.activo = TRUE
        """
        try:
            from app.dao.conexion import db
            cursor = db.get_cursor()
            cursor.execute(query, (f'%{tipo}%',))
            return [self.mapear_a_objeto(fila) for fila in cursor.fetchall()]
        except Exception as e:
            raise
    
    def validar_numero_serie_unico(self, numero_serie, excluir_id=None):
        if not numero_serie:
            return True
        query = "SELECT id_equipo FROM equipo WHERE numero_serie = %s"
        params = [numero_serie]
        if excluir_id:
            query += " AND id_equipo != %s"
            params.append(excluir_id)
        try:
            from app.dao.conexion import db
            cursor = db.get_cursor()
            cursor.execute(query, params)
            return cursor.fetchone() is None
        except Exception as e:
            raise

equipo_dao = EquipoDAO()
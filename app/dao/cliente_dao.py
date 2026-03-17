# app/dao/cliente_dao.py
"""
DAO para la entidad Cliente
"""
from app.dao.base_dao import BaseDAO
from app.models.cliente import Cliente

class ClienteDAO(BaseDAO):
    @property
    def tabla(self):
        return "cliente"
    
    @property
    def primary_key(self):
        return "id_cliente"
    
    def mapear_a_objeto(self, fila):
        if fila is None:
            return None
        return Cliente(
            id_cliente=fila.get('id_cliente'),
            nombre=fila.get('nombre'),
            apellido=fila.get('apellido'),
            cedula=fila.get('cedula'),
            telefono=fila.get('telefono'),
            email=fila.get('email'),
            direccion=fila.get('direccion'),
            fecha_registro=fila.get('fecha_registro'),
            activo=fila.get('activo')
        )
    
    def buscar_por_cedula(self, cedula):
        """Busca cliente por número de cédula"""
        resultados = self.buscar_por_criterio('cedula', cedula)
        return resultados[0] if resultados else None
    
    def buscar_por_nombre(self, nombre):
        """Búsqueda parcial por nombre"""
        query = """
            SELECT * FROM cliente 
            WHERE (nombre ILIKE %s OR apellido ILIKE %s) AND activo = TRUE
        """
        filas = self._query_rows(query, (f'%{nombre}%', f'%{nombre}%'))
        return [self.mapear_a_objeto(fila) for fila in filas]
    
    def validar_cedula_unica(self, cedula, excluir_id=None):
        query = "SELECT id_cliente FROM cliente WHERE cedula = %s"
        params = [cedula]
        if excluir_id:
            query += " AND id_cliente != %s"
            params.append(excluir_id)
        fila = self._query_row(query, params)
        return fila is None

cliente_dao = ClienteDAO()
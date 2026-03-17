# app/dao/tecnico_dao.py
"""
DAO para la entidad Técnico (Daniel Albadawi)
Implementa operaciones específicas de técnicos.
"""
from app.dao.base_dao import BaseDAO
from app.models.tecnico import Tecnico

class TecnicoDAO(BaseDAO):
    """
    Data Access Object para gestionar técnicos en PostgreSQL.
    Hereda operaciones CRUD básicas de BaseDAO.
    """
    
    @property
    def tabla(self):
        return "tecnico"
    
    @property
    def primary_key(self):
        return "id_tecnico"
    
    def mapear_a_objeto(self, fila):
        """Convierte fila de BD a objeto Tecnico"""
        if fila is None:
            return None
        return Tecnico(
            id_tecnico=fila.get('id_tecnico'),
            nombre=fila.get('nombre'),
            apellido=fila.get('apellido'),
            cedula=fila.get('cedula'),
            especialidad=fila.get('especialidad'),
            telefono=fila.get('telefono'),
            email=fila.get('email'),
            fecha_contratacion=fila.get('fecha_contratacion'),
            activo=fila.get('activo')
        )
    
    # Métodos específicos de Técnico
    def buscar_por_cedula(self, cedula):
        """Busca técnico por número de cédula"""
        resultados = self.buscar_por_criterio('cedula', cedula)
        return resultados[0] if resultados else None
    
    def buscar_por_especialidad(self, especialidad):
        """Lista técnicos por especialidad"""
        query = """
            SELECT * FROM tecnico 
            WHERE especialidad ILIKE %s AND activo = TRUE
        """
        filas = self._query_rows(query, (f'%{especialidad}%',))
        return [self.mapear_a_objeto(fila) for fila in filas]
    
    def validar_cedula_unica(self, cedula, excluir_id=None):
        """
        Valida que la cédula no exista (para crear/actualizar).
        Returns: True si es única, False si ya existe
        """
        query = "SELECT id_tecnico FROM tecnico WHERE cedula = %s"
        params = [cedula]
        
        if excluir_id:
            query += " AND id_tecnico != %s"
            params.append(excluir_id)
            
        fila = self._query_row(query, params)
        return fila is None


# Instancia singleton para uso en servicios
tecnico_dao = TecnicoDAO()
# app/services/equipo_service.py
"""
Servicio de Lógica de Negocio para Equipo
"""
from app.services.base_service import BaseService
from app.dao.equipo_dao import equipo_dao
from app.dao.cliente_dao import cliente_dao
from app.models.equipo import Equipo

class EquipoService(BaseService):
    def __init__(self):
        super().__init__(equipo_dao)
    
    def validar_datos(self, datos, es_creacion=True):
        equipo = Equipo(**datos)
        return equipo.validar()
    
    def _verificar_duplicados(self, datos):
        numero_serie = datos.get('numero_serie')
        if numero_serie:
            if not self.dao.validar_numero_serie_unico(numero_serie):
                return f"Ya existe un equipo con el número de serie {numero_serie}"
        return None
    
    def _verificar_dependencias(self, id_equipo):
        # TODO: Verificar si tiene órdenes de servicio asociadas
        return None
    
    def crear(self, datos: dict):
        # Validar que el cliente exista
        id_cliente = datos.get('id_cliente')
        if id_cliente:
            cliente = cliente_dao.buscar_por_id(id_cliente)
            if not cliente:
                return {"exito": False, "mensaje": "El cliente especificado no existe", "id": None}
        return super().crear(datos)
    
    def listar_por_cliente(self, id_cliente):
        try:
            equipos = self.dao.buscar_por_cliente(id_cliente)
            return {
                "exito": True,
                "data": [e.to_dict() for e in equipos],
                "total": len(equipos)
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}
    
    def listar_por_tipo(self, tipo):
        try:
            equipos = self.dao.buscar_por_tipo(tipo)
            return {
                "exito": True,
                "data": [e.to_dict() for e in equipos]
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}
    
    def buscar_por_numero_serie(self, numero_serie):
        try:
            equipo = self.dao.buscar_por_numero_serie(numero_serie)
            if equipo:
                return {"exito": True, "data": equipo.to_dict()}
            return {"exito": False, "mensaje": "Equipo no encontrado"}
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

equipo_service = EquipoService()

# app/services/estatus_orden_service.py
"""
Servicio de Lógica de Negocio para EstatusOrden
"""
from app.services.base_service import BaseService
from app.dao.estatus_orden_dao import estatus_orden_dao
from app.models.estatus_orden import EstatusOrden

class EstatusOrdenService(BaseService):
    def __init__(self):
        super().__init__(estatus_orden_dao)
    
    def validar_datos(self, datos, es_creacion=True):
        estatus = EstatusOrden(**datos)
        return estatus.validar()
    
    def _verificar_duplicados(self, datos):
        nombre = datos.get('nombre_estatus')
        if nombre:
            existentes = self.dao.buscar_por_nombre(nombre)
            for ex in existentes:
                if ex.nombre_estatus.lower() == nombre.lower():
                    return f"Ya existe un estatus con el nombre '{nombre}'"
        return None
    
    def _verificar_dependencias(self, id_estatus):
        # TODO: Verificar si hay órdenes en este estatus
        return None
    
    def obtener_flujo_trabajo(self):
        """Obtiene el flujo de trabajo ordenado por secuencia"""
        return self.listar()
    
    def obtener_siguiente_estatus(self, id_estatus_actual):
        try:
            estatus_actual = self.dao.buscar_por_id(id_estatus_actual)
            if not estatus_actual:
                return {"exito": False, "mensaje": "Estatus actual no encontrado"}
            
            siguiente = self.dao.obtener_siguiente_estatus(estatus_actual.orden_secuencial)
            if siguiente:
                return {"exito": True, "data": siguiente.to_dict()}
            return {"exito": False, "mensaje": "No hay siguiente estatus en el flujo"}
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

estatus_orden_service = EstatusOrdenService()
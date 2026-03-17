# app/services/tipo_orden_service.py
"""
Servicio de Lógica de Negocio para TipoOrden
"""
from app.services.base_service import BaseService
from app.dao.tipo_orden_dao import tipo_orden_dao
from app.models.tipo_orden import TipoOrden

class TipoOrdenService(BaseService):
    def __init__(self):
        super().__init__(tipo_orden_dao)
    
    def validar_datos(self, datos, es_creacion=True):
        tipo = TipoOrden(**datos)
        return tipo.validar()
    
    def _verificar_duplicados(self, datos):
        nombre = datos.get('nombre_tipo')
        if nombre:
            existentes = self.dao.buscar_por_nombre(nombre)
            for ex in existentes:
                if ex.nombre_tipo.lower() == nombre.lower():
                    return f"Ya existe un tipo de orden con el nombre '{nombre}'"
        return None
    
    def _verificar_dependencias(self, id_tipo_orden):
        # TODO: Verificar si hay órdenes usando este tipo
        return None
    
    def listar_requieren_aprobacion(self):
        try:
            tipos = self.dao.listar_requieren_aprobacion()
            return {
                "exito": True,
                "data": [t.to_dict() for t in tipos]
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

tipo_orden_service = TipoOrdenService()
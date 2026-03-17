# app/services/servicio_service.py
"""
Servicio de Lógica de Negocio para Servicio
"""
from app.services.base_service import BaseService
from app.dao.servicio_dao import servicio_dao
from app.models.servicio import Servicio

class ServicioService(BaseService):
    def __init__(self):
        super().__init__(servicio_dao)
    
    def validar_datos(self, datos, es_creacion=True):
        servicio = Servicio(**datos)
        return servicio.validar()
    
    def _verificar_duplicados(self, datos):
        # Los servicios pueden tener nombres similares pero no idénticos
        nombre = datos.get('nombre_servicio')
        if nombre:
            existentes = self.dao.buscar_por_nombre(nombre)
            for ex in existentes:
                if ex.nombre_servicio.lower() == nombre.lower():
                    return f"Ya existe un servicio con el nombre exacto '{nombre}'"
        return None
    
    def _verificar_dependencias(self, id_servicio):
        # TODO: Verificar si está en órdenes de servicio
        return None
    
    def buscar_por_nombre(self, nombre):
        try:
            servicios = self.dao.buscar_por_nombre(nombre)
            return {
                "exito": True,
                "data": [s.to_dict() for s in servicios],
                "total": len(servicios)
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}
    
    def listar_por_rango_costo(self, min_costo, max_costo):
        try:
            servicios = self.dao.listar_por_rango_costo(min_costo, max_costo)
            return {
                "exito": True,
                "data": [s.to_dict() for s in servicios]
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

servicio_service = ServicioService()
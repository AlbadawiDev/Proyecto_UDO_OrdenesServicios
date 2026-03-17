# app/services/prioridad_service.py
"""
Servicio de Lógica de Negocio para Prioridad
"""
from app.services.base_service import BaseService
from app.dao.prioridad_dao import prioridad_dao
from app.models.prioridad import Prioridad

class PrioridadService(BaseService):
    def __init__(self):
        super().__init__(prioridad_dao)
    
    def validar_datos(self, datos, es_creacion=True):
        prioridad = Prioridad(**datos)
        return prioridad.validar()
    
    def _verificar_duplicados(self, datos):
        nombre = datos.get('nombre_prioridad')
        nivel = datos.get('nivel')
        
        # Verificar nombre único
        if nombre:
            existentes = self.dao.buscar_por_nombre(nombre)
            for ex in existentes:
                if ex.nombre_prioridad.lower() == nombre.lower():
                    return f"Ya existe una prioridad con el nombre '{nombre}'"
        
        # Verificar nivel único
        if nivel:
            existente_nivel = self.dao.buscar_por_nivel(nivel)
            if existente_nivel:
                return f"Ya existe una prioridad con el nivel {nivel}"
        
        return None
    
    def _verificar_dependencias(self, id_prioridad):
        # TODO: Verificar si hay órdenes con esta prioridad
        return None
    
    def obtener_por_nivel(self, nivel):
        try:
            prioridad = self.dao.buscar_por_nivel(nivel)
            if prioridad:
                return {"exito": True, "data": prioridad.to_dict()}
            return {"exito": False, "mensaje": "Prioridad no encontrada"}
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}
    
    def obtener_para_sla(self, horas_maximas):
        try:
            prioridades = self.dao.obtener_para_sla(horas_maximas)
            return {
                "exito": True,
                "data": [p.to_dict() for p in prioridades]
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

prioridad_service = PrioridadService()
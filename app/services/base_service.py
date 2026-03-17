# app/services/base_service.py
"""
Capa de Lógica de Negocio - Clase Base
Implementa reglas de negocio, validaciones y coordinación entre DAOs.
"""
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """
    Clase base para servicios de negocio.
    Implementa la lógica de negocio común y validaciones.
    """
    
    def __init__(self, dao):
        self.dao = dao

    @staticmethod
    def _mensaje_error_usuario(exc):
        mensaje = str(exc).lower()
        if isinstance(exc, UnicodeDecodeError) or "codec can't decode" in mensaje:
            logger.exception('Error de encoding no recuperable en capa de servicio', exc_info=exc)
            return 'Ocurrió un problema temporal al leer datos. Intente nuevamente.'
        logger.error('Error de negocio: %s', exc)
        return str(exc)

    
    def validar_datos(self, datos, es_creacion=True):
        """
        Valida datos antes de crear/actualizar.
        Debe ser implementado por cada servicio específico.
        """
        return True, ""
    
    def crear(self, datos: dict):
        """
        Caso de uso: Crear nueva entidad (CU-G01)
        
        Flujo:
        1. Validar datos de entrada
        2. Verificar duplicados (inclusión CU-G05)
        3. Crear registro en BD
        4. Retornar resultado
        """
        # 1. Validación
        valido, mensaje = self.validar_datos(datos, es_creacion=True)
        if not valido:
            return {"exito": False, "mensaje": mensaje, "id": None}
        
        # 2. Verificar duplicados (inclusión de CU-G05)
        duplicado_msg = self._verificar_duplicados(datos)
        if duplicado_msg:
            return {"exito": False, "mensaje": duplicado_msg, "id": None}
        
        # 3. Crear
        try:
            nuevo_id = self.dao.insertar(datos)
            return {
                "exito": True, 
                "mensaje": "Registro creado exitosamente",
                "id": nuevo_id
            }
        except Exception as e:
            return {"exito": False, "mensaje": self._mensaje_error_usuario(e), "id": None}
    
    def consultar(self, id_valor):
        """Caso de uso: Consultar entidad por ID"""
        try:
            entidad = self.dao.buscar_por_id(id_valor)
            if entidad:
                return {"exito": True, "data": entidad.to_dict()}
            return {"exito": False, "mensaje": "No encontrado"}
        except Exception as e:
            return {"exito": False, "mensaje": self._mensaje_error_usuario(e)}
    
    def listar(self, limite=None, offset=None):
        """Caso de uso: Listar entidades (CU-G02)"""
        try:
            entidades = self.dao.listar_todos(limite, offset)
            return {
                "exito": True, 
                "data": [e.to_dict() for e in entidades],
                "total": len(entidades)
            }
        except Exception as e:
            return {"exito": False, "mensaje": self._mensaje_error_usuario(e)}
    
    def actualizar(self, id_valor, datos: dict):
        """
        Caso de uso: Actualizar entidad (CU-G03)
        
        Flujo:
        1. Buscar entidad existente (inclusión CU-G05)
        2. Validar datos
        3. Actualizar
        """
        # 1. Verificar existencia
        existente = self.dao.buscar_por_id(id_valor)
        if not existente:
            return {"exito": False, "mensaje": "Entidad no encontrada"}
        
        # 2. Validar
        valido, mensaje = self.validar_datos(datos, es_creacion=False)
        if not valido:
            return {"exito": False, "mensaje": mensaje}
        
        # 3. Actualizar
        try:
            actualizado = self.dao.actualizar(id_valor, datos)
            if actualizado:
                return {"exito": True, "mensaje": "Actualización exitosa"}
            return {"exito": False, "mensaje": "No se pudo actualizar"}
        except Exception as e:
            return {"exito": False, "mensaje": self._mensaje_error_usuario(e)}
    
    def eliminar(self, id_valor, fisico=False):
        """
        Caso de uso: Eliminar/Desactivar entidad (CU-G04)
        
        Flujo:
        1. Buscar entidad (inclusión CU-G05)
        2. Verificar dependencias
        3. Eliminar (lógico o físico)
        """
        # 1. Verificar existencia
        existente = self.dao.buscar_por_id(id_valor)
        if not existente:
            return {"exito": False, "mensaje": "Entidad no encontrada"}
        
        # 2. Verificar dependencias (específico por entidad)
        deps_msg = self._verificar_dependencias(id_valor)
        if deps_msg:
            return {"exito": False, "mensaje": deps_msg}
        
        # 3. Eliminar
        try:
            if fisico:
                eliminado = self.dao.eliminar_fisico(id_valor)
            else:
                eliminado = self.dao.eliminar_logico(id_valor)
            
            if eliminado:
                tipo = "física" if fisico else "lógica"
                return {"exito": True, "mensaje": f"Eliminación {tipo} exitosa"}
            return {"exito": False, "mensaje": "No se pudo eliminar"}
        except Exception as e:
            return {"exito": False, "mensaje": self._mensaje_error_usuario(e)}
    
    def buscar(self, criterio, valor):
        """Caso de uso: Buscar entidad (CU-G05)"""
        try:
            resultados = self.dao.buscar_por_criterio(criterio, valor)
            return {
                "exito": True,
                "data": [r.to_dict() for r in resultados],
                "total": len(resultados)
            }
        except Exception as e:
            return {"exito": False, "mensaje": self._mensaje_error_usuario(e)}
    
    # Métodos abstractos para implementar en subclases
    def _verificar_duplicados(self, datos):
        """Verifica duplicados específicos de la entidad"""
        return None
    
    def _verificar_dependencias(self, id_valor):
        """Verifica dependencias antes de eliminar"""
        return None
# app/services/tecnico_service.py
"""
Servicio de Lógica de Negocio para Técnico
Implementa reglas específicas: validaciones, duplicados, dependencias.
"""
from app.services.base_service import BaseService
from app.dao.tecnico_dao import tecnico_dao
from app.models.tecnico import Tecnico


class TecnicoService(BaseService):
    """
    Servicio de negocio para gestión de técnicos.
    """

    def __init__(self):
        super().__init__(tecnico_dao)

    def validar_datos(self, datos, es_creacion=True):
        """
        Valida datos antes de crear/actualizar.
        Retorna: (bool, mensaje)
        """
        tecnico = Tecnico(**datos)
        return tecnico.validar()

    def _verificar_duplicados(self, datos, excluir_id=None):
        """
        Verifica cédula única.
        excluir_id:
        - None en creación
        - id_tecnico en edición para excluir el mismo registro
        """
        cedula = (datos.get("cedula") or "").strip()
        if not cedula:
            return None

        es_unica = self.dao.validar_cedula_unica(cedula, excluir_id=excluir_id)
        if not es_unica:
            return f"Ya existe un técnico con la cédula {cedula}"

        return None

    def _verificar_dependencias(self, id_tecnico):
        """
        Verifica si el técnico tiene órdenes asignadas antes de eliminar.
        """
        return None

    def actualizar(self, id_valor, datos: dict):
        """
        Override del CU-G03 para agregar verificación de duplicados.
        BaseService.actualizar no valida duplicados.
        """
        # 1. Verificar existencia
        existente = self.dao.buscar_por_id(id_valor)
        if not existente:
            return {"exito": False, "mensaje": "Entidad no encontrada"}

        # 2. Validar datos
        valido, mensaje = self.validar_datos(datos, es_creacion=False)
        if not valido:
            return {"exito": False, "mensaje": mensaje}

        # 3. Verificar duplicados (excluyendo el mismo id)
        duplicado_msg = self._verificar_duplicados(datos, excluir_id=id_valor)
        if duplicado_msg:
            return {"exito": False, "mensaje": duplicado_msg}

        # 4. Actualizar
        try:
            actualizado = self.dao.actualizar(id_valor, datos)
            if actualizado:
                return {"exito": True, "mensaje": "Actualización exitosa"}
            return {"exito": False, "mensaje": "No se pudo actualizar"}
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}


tecnico_service = TecnicoService()
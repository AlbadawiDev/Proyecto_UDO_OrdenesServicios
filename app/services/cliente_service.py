# app/services/cliente_service.py
"""
Servicio de Lógica de Negocio para Cliente
"""
from app.services.base_service import BaseService
from app.dao.cliente_dao import cliente_dao
from app.models.cliente import Cliente

class ClienteService(BaseService):
    def __init__(self):
        super().__init__(cliente_dao)
    
    def validar_datos(self, datos, es_creacion=True):
        cliente = Cliente(**datos)
        return cliente.validar()
    
    def _verificar_duplicados(self, datos):
        cedula = datos.get('cedula')
        if cedula:
            existente = self.dao.buscar_por_cedula(cedula)
            if existente:
                return f"Ya existe un cliente con la cédula {cedula}"
        return None
    
    def _verificar_dependencias(self, id_cliente):
        # Verificar si tiene equipos asociados
        from app.dao.equipo_dao import equipo_dao
        equipos = equipo_dao.buscar_por_cliente(id_cliente)
        if equipos:
            return f"No se puede eliminar: el cliente tiene {len(equipos)} equipo(s) registrado(s)"
        return None
    
    # Métodos específicos
    def buscar_por_cedula(self, cedula):
        try:
            cliente = self.dao.buscar_por_cedula(cedula)
            if cliente:
                return {"exito": True, "data": cliente.to_dict()}
            return {"exito": False, "mensaje": "Cliente no encontrado"}
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}
    
    def buscar_por_nombre(self, nombre):
        try:
            clientes = self.dao.buscar_por_nombre(nombre)
            return {
                "exito": True,
                "data": [c.to_dict() for c in clientes],
                "total": len(clientes)
            }
        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

cliente_service = ClienteService()
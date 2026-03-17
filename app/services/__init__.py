# app/services/__init__.py
from .base_service import BaseService
from .cliente_service import ClienteService, cliente_service
from .tecnico_service import TecnicoService, tecnico_service
from .equipo_service import EquipoService, equipo_service
from .servicio_service import ServicioService, servicio_service
from .tipo_orden_service import TipoOrdenService, tipo_orden_service
from .estatus_orden_service import EstatusOrdenService, estatus_orden_service
from .prioridad_service import PrioridadService, prioridad_service

__all__ = [
    'BaseService',
    'ClienteService', 'cliente_service',
    'TecnicoService', 'tecnico_service',
    'EquipoService', 'equipo_service',
    'ServicioService', 'servicio_service',
    'TipoOrdenService', 'tipo_orden_service',
    'EstatusOrdenService', 'estatus_orden_service',
    'PrioridadService', 'prioridad_service'
]
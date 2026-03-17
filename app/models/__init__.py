# app/models/__init__.py
from .cliente import Cliente
from .tecnico import Tecnico
from .equipo import Equipo
from .servicio import Servicio
from .tipo_orden import TipoOrden
from .estatus_orden import EstatusOrden
from .prioridad import Prioridad

__all__ = ['Cliente', 'Tecnico', 'Equipo', 'Servicio', 'TipoOrden', 'EstatusOrden', 'Prioridad']
# app/dao/__init__.py
from .conexion import db, ConexionDB
from .base_dao import BaseDAO
from .cliente_dao import ClienteDAO, cliente_dao
from .tecnico_dao import TecnicoDAO, tecnico_dao
from .equipo_dao import EquipoDAO, equipo_dao
from .servicio_dao import ServicioDAO, servicio_dao
from .tipo_orden_dao import TipoOrdenDAO, tipo_orden_dao
from .estatus_orden_dao import EstatusOrdenDAO, estatus_orden_dao
from .prioridad_dao import PrioridadDAO, prioridad_dao

__all__ = [
    'db', 'ConexionDB', 'BaseDAO',
    'ClienteDAO', 'cliente_dao',
    'TecnicoDAO', 'tecnico_dao',
    'EquipoDAO', 'equipo_dao',
    'ServicioDAO', 'servicio_dao',
    'TipoOrdenDAO', 'tipo_orden_dao',
    'EstatusOrdenDAO', 'estatus_orden_dao',
    'PrioridadDAO', 'prioridad_dao'
]
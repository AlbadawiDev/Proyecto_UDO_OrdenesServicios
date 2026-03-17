# app/models/estatus_orden.py
"""
Modelo de datos para la entidad EstatusOrden (DTO/Entidad)
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class EstatusOrden:
    """
    Entidad EstatusOrden - Representa el estado de una orden.
    Corresponde a la tabla 'estatus_orden' en PostgreSQL.
    """
    id_estatus: Optional[int] = None
    nombre_estatus: str = ""
    descripcion: Optional[str] = None
    color_hex: str = "#000000"
    orden_secuencial: int = 0
    activo: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    def validar(self):
        if not self.nombre_estatus or len(self.nombre_estatus) < 3:
            return False, "El nombre del estatus debe tener al menos 3 caracteres"
        if self.color_hex and not self.color_hex.startswith('#'):
            return False, "El color debe estar en formato hexadecimal (ej: #FF0000)"
        return True, ""
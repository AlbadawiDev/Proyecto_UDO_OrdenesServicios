# app/models/tipo_orden.py
"""
Modelo de datos para la entidad TipoOrden (DTO/Entidad)
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class TipoOrden:
    """
    Entidad TipoOrden - Representa el tipo de orden de servicio.
    Corresponde a la tabla 'tipo_orden' en PostgreSQL.
    """
    id_tipo_orden: Optional[int] = None
    nombre_tipo: str = ""
    descripcion: Optional[str] = None
    requiere_aprobacion: bool = False
    activo: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    def validar(self):
        if not self.nombre_tipo or len(self.nombre_tipo) < 3:
            return False, "El nombre del tipo debe tener al menos 3 caracteres"
        return True, ""
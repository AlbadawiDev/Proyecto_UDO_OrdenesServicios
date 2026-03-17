# app/models/servicio.py
"""
Modelo de datos para la entidad Servicio (DTO/Entidad)
"""
from dataclasses import dataclass, asdict
from typing import Optional
from decimal import Decimal

@dataclass
class Servicio:
    """
    Entidad Servicio - Representa un servicio ofrecido.
    Corresponde a la tabla 'servicio' en PostgreSQL.
    """
    id_servicio: Optional[int] = None
    nombre_servicio: str = ""
    descripcion: Optional[str] = None
    costo_base: Optional[float] = None
    tiempo_estimado_horas: Optional[int] = None
    activo: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    def validar(self):
        if not self.nombre_servicio or len(self.nombre_servicio) < 3:
            return False, "El nombre del servicio debe tener al menos 3 caracteres"
        if self.costo_base is not None and self.costo_base < 0:
            return False, "El costo base no puede ser negativo"
        if self.tiempo_estimado_horas is not None and self.tiempo_estimado_horas < 0:
            return False, "El tiempo estimado no puede ser negativo"
        return True, ""
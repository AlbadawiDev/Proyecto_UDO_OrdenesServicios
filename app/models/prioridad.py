# app/models/prioridad.py
"""
Modelo de datos para la entidad Prioridad (DTO/Entidad)
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Prioridad:
    """
    Entidad Prioridad - Representa el nivel de prioridad de una orden.
    Corresponde a la tabla 'prioridad' en PostgreSQL.
    """
    id_prioridad: Optional[int] = None
    nombre_prioridad: str = ""
    nivel: int = 1  # 1=Alta, 2=Media, 3=Baja, etc.
    tiempo_respuesta_horas: Optional[int] = None  # SLA
    color_hex: str = "#FF0000"
    activo: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    def validar(self):
        if not self.nombre_prioridad or len(self.nombre_prioridad) < 3:
            return False, "El nombre de la prioridad debe tener al menos 3 caracteres"
        if self.nivel < 1:
            return False, "El nivel debe ser mayor a 0"
        if self.tiempo_respuesta_horas is not None and self.tiempo_respuesta_horas < 1:
            return False, "El tiempo de respuesta debe ser al menos 1 hora"
        return True, ""
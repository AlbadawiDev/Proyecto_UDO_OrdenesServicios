# app/models/equipo.py
"""
Modelo de datos para la entidad Equipo (DTO/Entidad)
"""
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Equipo:
    """
    Entidad Equipo - Representa un equipo/activo/dispositivo.
    Corresponde a la tabla 'equipo' en PostgreSQL.
    """
    id_equipo: Optional[int] = None
    nombre_equipo: str = ""
    tipo: str = ""  # Laptop, Desktop, Servidor, Impresora, etc.
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    id_cliente: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    activo: bool = True
    
    # Campos join (no en BD, útiles para mostrar info)
    nombre_cliente: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    def validar(self):
        if not self.nombre_equipo or len(self.nombre_equipo) < 2:
            return False, "El nombre del equipo debe tener al menos 2 caracteres"
        if not self.tipo:
            return False, "El tipo de equipo es obligatorio"
        if not self.id_cliente:
            return False, "Debe asignar un cliente al equipo"
        return True, ""
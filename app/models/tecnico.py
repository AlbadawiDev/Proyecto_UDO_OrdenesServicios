# app/models/tecnico.py
"""
Modelo de datos para la entidad Técnico (DTO/Entidad)
Representa la estructura de datos en la capa de negocio.
"""
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import date

@dataclass
class Tecnico:
    """
    Entidad Técnico - Representa un técnico de servicio.
    Corresponde a la tabla 'tecnico' en PostgreSQL.
    """
    id_tecnico: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    cedula: str = ""
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    fecha_contratacion: Optional[date] = None
    activo: bool = True
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON/BD"""
        return asdict(self)
    
    @property
    def nombre_completo(self):
        """Propiedad calculada: nombre completo del técnico"""
        return f"{self.nombre} {self.apellido}".strip()
    
    def validar(self):
        """
        Validaciones de negocio básicas.
        Returns: (bool, str) - (es_válido, mensaje_error)
        """
        if not self.nombre or len(self.nombre) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        
        if not self.apellido or len(self.apellido) < 2:
            return False, "El apellido debe tener al menos 2 caracteres"
        
        if not self.cedula or len(self.cedula) < 5:
            return False, "La cédula debe tener al menos 5 caracteres"
        
        if self.email and "@" not in self.email:
            return False, "El email no es válido"
        
        return True, ""
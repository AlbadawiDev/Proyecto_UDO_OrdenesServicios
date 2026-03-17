# app/models/cliente.py
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Cliente:
    id_cliente: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    cedula: str = ""
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    activo: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}".strip()
    
    def validar(self):
        if not self.nombre or len(self.nombre) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        if not self.apellido or len(self.apellido) < 2:
            return False, "El apellido debe tener al menos 2 caracteres"
        if not self.cedula or len(self.cedula) < 5:
            return False, "La cédula debe tener al menos 5 caracteres"
        if self.email and "@" not in self.email:
            return False, "El email no es válido"
        return True, ""
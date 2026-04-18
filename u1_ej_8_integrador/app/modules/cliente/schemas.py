from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Juan Pérez")
    email: str = Field(..., example="juan.perez@email.com")
    telefono: str = Field(..., pattern=r"^\+?\d{7,15}$", example="+5491123456789")
    activo: bool = True

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("El email no tiene un formato válido")
        return v.lower()


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    telefono: Optional[str] = Field(None, pattern=r"^\+?\d{7,15}$")
    activo: Optional[bool] = None


class ClienteRead(ClienteBase):
    id: int


class ClienteEstadoResponse(BaseModel):
    id: int
    nombre: str
    activo: bool
    mensaje: str
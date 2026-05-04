from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InsumoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int


class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    activo: Optional[bool] = None


class InsumoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    activo: bool
    eliminado_en: Optional[datetime] = None

    class Config:
        from_attributes = True


class InsumoListResponse(BaseModel):
    total: int
    items: list[InsumoResponse]

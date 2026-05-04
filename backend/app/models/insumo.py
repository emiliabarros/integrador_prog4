from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Insumo(SQLModel, table=True):
    __tablename__ = "insumos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    precio: float = Field(ge=0)
    stock: int = Field(ge=0)
    activo: bool = Field(default=True)
    eliminado_en: Optional[datetime] = Field(default=None)

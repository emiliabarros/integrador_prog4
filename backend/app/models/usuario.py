from sqlmodel import SQLModel, Field
from typing import Optional


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str

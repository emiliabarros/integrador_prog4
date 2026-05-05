from typing import Optional
from sqlmodel import Session, select
from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear(self, nombre: str, email: str, password_hash: str, rol: str = "cliente") -> Usuario:
        usuario = Usuario(nombre=nombre, email=email, password_hash=password_hash, rol=rol)
        self.sesion.add(usuario)
        self.sesion.flush()
        self.sesion.refresh(usuario)
        return usuario

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self.sesion.exec(select(Usuario).where(Usuario.email == email)).first()

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        return self.sesion.get(Usuario, id)

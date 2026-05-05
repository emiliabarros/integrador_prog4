from app.database import get_session
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.ingrediente_repository import IngredienteRepository


class UnidadDeTrabajo:
    def __init__(self, session_factory=None):
        self.session_factory = session_factory or get_session

    def __enter__(self) -> "UnidadDeTrabajo":
        self.sesion = self.session_factory()
        self.usuarios = UsuarioRepository(self.sesion)
        self.ingredientes = IngredienteRepository(self.sesion)
        return self

    def __exit__(self, tipo_exc, valor_exc, traza_exc):
        try:
            if tipo_exc:
                self.sesion.rollback()
            else:
                try:
                    self.sesion.commit()
                except Exception:
                    self.sesion.rollback()
                    raise
        finally:
            self.sesion.close()

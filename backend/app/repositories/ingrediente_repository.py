from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select
from app.models.ingrediente import Ingrediente
from app.schemas.ingrediente_schema import IngredienteCreate


class IngredienteRepository:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear(self, datos: IngredienteCreate) -> Ingrediente:
        ingrediente = Ingrediente(**datos.model_dump())
        self.sesion.add(ingrediente)
        self.sesion.flush()
        self.sesion.refresh(ingrediente)
        return ingrediente

    def obtener_por_id(self, id: int) -> Optional[Ingrediente]:
        ingrediente = self.sesion.get(Ingrediente, id)
        if ingrediente is None or ingrediente.deleted_at is not None:
            return None
        return ingrediente

    def obtener_todos(
        self,
        skip: int = 0,
        limit: int = 10,
        nombre: Optional[str] = None,
        es_alergeno: Optional[bool] = None,
        incluir_eliminados: bool = False,
    ) -> tuple[List[Ingrediente], int]:
        consulta = select(Ingrediente)
        if not incluir_eliminados:
            consulta = consulta.where(Ingrediente.deleted_at == None)  # noqa: E711
        if nombre:
            consulta = consulta.where(Ingrediente.nombre.icontains(nombre))
        if es_alergeno is not None:
            consulta = consulta.where(Ingrediente.es_alergeno == es_alergeno)

        total = len(self.sesion.exec(consulta).all())
        items = self.sesion.exec(consulta.offset(skip).limit(limit)).all()
        return items, total

    def actualizar(self, ingrediente: Ingrediente, campos: dict) -> Ingrediente:
        for campo, valor in campos.items():
            setattr(ingrediente, campo, valor)
        self.sesion.add(ingrediente)
        self.sesion.flush()
        self.sesion.refresh(ingrediente)
        return ingrediente

    def eliminar(self, ingrediente: Ingrediente) -> None:
        ingrediente.deleted_at = datetime.now(timezone.utc)
        self.sesion.add(ingrediente)
        self.sesion.flush()

    def reactivar(self, id: int) -> Optional[Ingrediente]:
        ingrediente = self.sesion.get(Ingrediente, id)
        if not ingrediente or ingrediente.deleted_at is None:
            return None
        ingrediente.deleted_at = None
        self.sesion.add(ingrediente)
        self.sesion.flush()
        self.sesion.refresh(ingrediente)
        return ingrediente

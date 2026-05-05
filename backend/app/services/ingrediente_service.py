from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.schemas.ingrediente_schema import (
    IngredienteCreate, IngredienteRead, IngredienteUpdate, IngredienteListResponse
)
from app.uow.uow import UnidadDeTrabajo


def crear_ingrediente(datos: IngredienteCreate) -> IngredienteRead:
    try:
        with UnidadDeTrabajo() as uow:
            ingrediente = uow.ingredientes.crear(datos)
            return IngredienteRead.model_validate(ingrediente)
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Ya existe un ingrediente con el nombre '{datos.nombre}'")


def obtener_ingredientes(
    skip: int = 0,
    limit: int = 10,
    nombre: Optional[str] = None,
    es_alergeno: Optional[bool] = None,
    incluir_eliminados: bool = False,
) -> IngredienteListResponse:
    with UnidadDeTrabajo() as uow:
        items, total = uow.ingredientes.obtener_todos(skip, limit, nombre, es_alergeno, incluir_eliminados)
        return IngredienteListResponse(
            total=total,
            items=[IngredienteRead.model_validate(i) for i in items],
        )


def obtener_ingrediente(id: int) -> IngredienteRead:
    with UnidadDeTrabajo() as uow:
        ingrediente = uow.ingredientes.obtener_por_id(id)
        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        return IngredienteRead.model_validate(ingrediente)


def actualizar_ingrediente(id: int, datos: IngredienteUpdate) -> IngredienteRead:
    try:
        with UnidadDeTrabajo() as uow:
            ingrediente = uow.ingredientes.obtener_por_id(id)
            if not ingrediente:
                raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
            ingrediente = uow.ingredientes.actualizar(ingrediente, datos.model_dump(exclude_unset=True))
            return IngredienteRead.model_validate(ingrediente)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Ya existe un ingrediente con ese nombre")


def eliminar_ingrediente(id: int) -> None:
    with UnidadDeTrabajo() as uow:
        ingrediente = uow.ingredientes.obtener_por_id(id)
        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        uow.ingredientes.eliminar(ingrediente)


def reactivar_ingrediente(id: int) -> IngredienteRead:
    with UnidadDeTrabajo() as uow:
        ingrediente = uow.ingredientes.reactivar(id)
        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado o ya está activo")
        return IngredienteRead.model_validate(ingrediente)

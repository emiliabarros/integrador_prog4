from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, Path, status
from app.routers.auth_router import get_current_user_id
from app.schemas.ingrediente_schema import (
    IngredienteCreate, IngredienteRead, IngredienteUpdate, IngredienteListResponse
)
from app.services import ingrediente_service

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

IdIngrediente = Annotated[int, Path(gt=0, description="ID del ingrediente")]


@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def crear(datos: IngredienteCreate, _: int = Depends(get_current_user_id)):
    return ingrediente_service.crear_ingrediente(datos)


@router.get("/", response_model=IngredienteListResponse)
def listar(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    es_alergeno: Annotated[Optional[bool], Query(description="Filtrar por alérgeno")] = None,
    incluir_eliminados: Annotated[bool, Query(description="Incluir eliminados")] = False,
    _: int = Depends(get_current_user_id),
):
    return ingrediente_service.obtener_ingredientes(skip, limit, nombre, es_alergeno, incluir_eliminados)


@router.get("/{id}", response_model=IngredienteRead)
def detalle(id: IdIngrediente, _: int = Depends(get_current_user_id)):
    return ingrediente_service.obtener_ingrediente(id)


@router.patch("/{id}", response_model=IngredienteRead)
def actualizar(id: IdIngrediente, datos: IngredienteUpdate, _: int = Depends(get_current_user_id)):
    return ingrediente_service.actualizar_ingrediente(id, datos)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: IdIngrediente, _: int = Depends(get_current_user_id)):
    ingrediente_service.eliminar_ingrediente(id)


@router.patch("/{id}/reactivar", response_model=IngredienteRead)
def reactivar(id: IdIngrediente, _: int = Depends(get_current_user_id)):
    return ingrediente_service.reactivar_ingrediente(id)

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from app.core.database import get_session
from app.routers.auth_router import get_current_user
from app.models.usuario import Usuario
from app.schemas.insumo_schema import InsumoCreate, InsumoUpdate, InsumoResponse, InsumoListResponse
from app.services import insumo_service

router = APIRouter(prefix="/insumos", tags=["Insumos"])


@router.post("", response_model=InsumoResponse, status_code=201)
def crear(
    data: InsumoCreate,
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    return insumo_service.crear_insumo(data, session)


@router.get("", response_model=InsumoListResponse)
def listar(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    activo: Optional[bool] = Query(None, description="Filtrar por activo"),
    stock_min: Optional[int] = Query(None, description="Stock mínimo"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    return insumo_service.listar_insumos(session, nombre, activo, stock_min, skip, limit)


@router.get("/{insumo_id}", response_model=InsumoResponse)
def obtener(
    insumo_id: int,
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    return insumo_service.obtener_insumo(insumo_id, session)


@router.put("/{insumo_id}", response_model=InsumoResponse)
def actualizar(
    insumo_id: int,
    data: InsumoUpdate,
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    return insumo_service.actualizar_insumo(insumo_id, data, session)


@router.delete("/{insumo_id}")
def eliminar(
    insumo_id: int,
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    return insumo_service.eliminar_insumo(insumo_id, session)


@router.patch("/{insumo_id}/reactivar", response_model=InsumoResponse)
def reactivar(
    insumo_id: int,
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    return insumo_service.reactivar_insumo(insumo_id, session)

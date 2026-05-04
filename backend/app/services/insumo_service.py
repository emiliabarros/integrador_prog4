from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from app.models.insumo import Insumo
from app.schemas.insumo_schema import InsumoCreate, InsumoUpdate, InsumoListResponse


def crear_insumo(data: InsumoCreate, session: Session) -> Insumo:
    insumo = Insumo(**data.model_dump())
    session.add(insumo)
    session.commit()
    session.refresh(insumo)
    return insumo


def listar_insumos(
    session: Session,
    nombre: Optional[str] = None,
    activo: Optional[bool] = None,
    stock_min: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
) -> InsumoListResponse:
    query = select(Insumo).where(Insumo.eliminado_en == None)  # noqa: E711

    if nombre:
        query = query.where(Insumo.nombre.ilike(f"%{nombre}%"))
    if activo is not None:
        query = query.where(Insumo.activo == activo)
    if stock_min is not None:
        query = query.where(Insumo.stock >= stock_min)

    total = len(session.exec(query).all())
    items = session.exec(query.offset(skip).limit(limit)).all()
    return InsumoListResponse(total=total, items=items)


def obtener_insumo(insumo_id: int, session: Session) -> Insumo:
    insumo = session.get(Insumo, insumo_id)
    if not insumo or insumo.eliminado_en is not None:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return insumo


def actualizar_insumo(insumo_id: int, data: InsumoUpdate, session: Session) -> Insumo:
    insumo = obtener_insumo(insumo_id, session)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(insumo, field, value)
    session.add(insumo)
    session.commit()
    session.refresh(insumo)
    return insumo


def eliminar_insumo(insumo_id: int, session: Session) -> dict:
    insumo = obtener_insumo(insumo_id, session)
    insumo.eliminado_en = datetime.utcnow()
    insumo.activo = False
    session.add(insumo)
    session.commit()
    return {"mensaje": "Insumo eliminado correctamente"}


def reactivar_insumo(insumo_id: int, session: Session) -> Insumo:
    insumo = session.get(Insumo, insumo_id)
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    if insumo.eliminado_en is None:
        raise HTTPException(status_code=400, detail="El insumo ya está activo")
    insumo.eliminado_en = None
    insumo.activo = True
    session.add(insumo)
    session.commit()
    session.refresh(insumo)
    return insumo

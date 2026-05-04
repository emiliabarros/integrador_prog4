from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.usuario import Usuario
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token


def register_user(data: RegisterRequest, session: Session) -> Usuario:
    existing = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    user = Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def login_user(data: LoginRequest, session: Session) -> TokenResponse:
    user = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token)

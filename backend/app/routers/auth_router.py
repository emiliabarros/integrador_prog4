from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import decode_token
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UsuarioResponse
from app.services.auth_service import register_user, login_user
from app.models.usuario import Usuario
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: Session = Depends(get_session),
) -> Usuario:
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    user = register_user(data, session)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    return login_user(data, session)


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user

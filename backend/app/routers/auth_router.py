from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UsuarioResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> int:
    try:
        payload = decode_token(credentials.credentials)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register(datos: RegisterRequest):
    return auth_service.registrar_usuario(datos)


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest):
    return auth_service.login_usuario(datos)


@router.get("/me", response_model=UsuarioResponse)
def me(user_id: int = Depends(get_current_user_id)):
    return auth_service.obtener_perfil(user_id)

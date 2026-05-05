from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UsuarioResponse
from app.uow.uow import UnidadDeTrabajo


def registrar_usuario(datos: RegisterRequest) -> UsuarioResponse:
    with UnidadDeTrabajo() as uow:
        existente = uow.usuarios.obtener_por_email(datos.email)
        if existente:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        usuario = uow.usuarios.crear(
            nombre=datos.nombre,
            email=datos.email,
            password_hash=hash_password(datos.password),
        )
        return UsuarioResponse.model_validate(usuario)


def login_usuario(datos: LoginRequest) -> TokenResponse:
    with UnidadDeTrabajo() as uow:
        usuario = uow.usuarios.obtener_por_email(datos.email)
        if not usuario or not verify_password(datos.password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
            )
        token = create_access_token({"sub": str(usuario.id), "email": usuario.email, "rol": usuario.rol})
        return TokenResponse(access_token=token)


def obtener_perfil(usuario_id: int) -> UsuarioResponse:
    with UnidadDeTrabajo() as uow:
        usuario = uow.usuarios.obtener_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return UsuarioResponse.model_validate(usuario)

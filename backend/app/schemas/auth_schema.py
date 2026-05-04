from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str

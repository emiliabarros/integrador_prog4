from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models

from app.database import crear_tablas
from app.routers import auth_router, ingrediente_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(
    title="Food Store API",
    description="Backend del trabajo integrador — FastAPI + SQLModel + PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(ingrediente_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Food Store API corriendo 🍔"}

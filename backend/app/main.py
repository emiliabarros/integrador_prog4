from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.routers import auth_router, insumo_router

app = FastAPI(
    title="Food Store API",
    description="API para el sistema Food Store — Trabajo Práctico Integrador",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth_router.router)
app.include_router(insumo_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Food Store API corriendo"}

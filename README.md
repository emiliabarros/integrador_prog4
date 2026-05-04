# Food Store — Trabajo Práctico Integrador

## Estructura del proyecto

```
food-store/
├── backend/          # FastAPI + SQLModel + PostgreSQL
└── frontend/         # React + Vite + TypeScript
```

---

## ⚙️ Backend — Arranque

### 1. Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE foodstore;
```

### 2. Configurar variables de entorno

```bash
cd backend
cp .env.example .env
# Editar .env con tu usuario/contraseña de PostgreSQL
```

### 3. Instalar dependencias y correr

```bash
cd backend
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Ver Swagger

Abrir http://localhost:8000/docs

---

## Frontend — Arranque

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173

---

## Checklist primera entrega ✅

- [x] Login JWT funcionando
- [x] Rutas protegidas con Bearer token
- [x] Swagger funcionando
- [x] CRUD completo de insumos
- [x] Filtro por nombre
- [x] Filtro por activo
- [x] Filtro por stock mínimo
- [x] Paginación (skip/limit)
- [x] Soft delete (eliminado_en)
- [x] Reactivación
- [x] Frontend conectado al backend
- [x] Menú de navegación

---

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /auth/register | Registrar usuario |
| POST | /auth/login | Login → JWT |
| GET | /auth/me | Usuario actual (protegido) |
| GET | /insumos | Listar con filtros y paginación |
| POST | /insumos | Crear insumo |
| GET | /insumos/{id} | Obtener por ID |
| PUT | /insumos/{id} | Actualizar |
| DELETE | /insumos/{id} | Soft delete |
| PATCH | /insumos/{id}/reactivar | Reactivar |

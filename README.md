# OPITA 360

Plataforma web para explorar destinos turísticos, culturales y naturales del Huila y construir itinerarios personalizados.

## Tecnologías
- Frontend: React + Vite
- Backend: Python + FastAPI
- Datos de demostración: JSON en memoria
- Base de datos preparada: PostgreSQL (`database/schema.sql`)

> En esta versión inicial, los destinos y recomendaciones funcionan con datos de demostración. PostgreSQL queda preparado en el esquema SQL, pero todavía no se persisten itinerarios en una base real.

## Requisitos
- Python 3.10+
- Node.js 18+

## Ejecutar en Windows / Visual Studio Code

### 1. Backend
Abre una terminal en la raíz del proyecto:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Documentación: http://127.0.0.1:8000/docs

### 2. Frontend
Abre una segunda terminal en la raíz del proyecto:

```powershell
cd frontend
npm install
npm run dev
```

Abre la dirección que Vite muestre, normalmente http://localhost:5173.

## Funciones
- Catálogo de lugares turísticos del Huila.
- Filtros por categoría.
- Formulario de preferencias de viaje.
- Recomendaciones mediante reglas sencillas (no requiere suscripción de IA).
- Estimación orientativa del costo.
- API REST documentada con OpenAPI.

## Integrantes
- Bairon Estiven Morales Serrano
- Huver Olaya Mendez
- Pedro José Gonzales

Universidad FET · Ingeniería de Software · Neiva, Huila

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
- Node.js 22.12+ (verificado con 22.20.0)

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
- Filtros por municipio, búsqueda y categoría.
- Formulario de preferencias de viaje.
- Recomendaciones mediante reglas sencillas (no requiere suscripción de IA).
- Estimación orientativa del costo.
- API REST documentada con OpenAPI.

## Integrantes
- Bairon Estiven Morales Serrano
- Huver Olaya Mendez
- Pedro José Gonzales

Universidad FET · Ingeniería de Software · Neiva, Huila

## Arnés del Taller 6

La base común está integrada localmente. El arnés nuevo se describe en [harness/README.md](harness/README.md): memoria, instrucciones Codex, Matriz Halcón, tres skills y revisión por agentes. Esta rama implementa S05; las demás [specs](specs/taller-6/) mantienen su estado independiente, sin incorporar S01–S04.

Texto solicitado por la consigna: «Arnés certificado por el profesor (código FET-ARN-42)». Su inclusión no acredita una certificación emitida. Ver [requisitos oficiales y pendientes](docs/taller-6/requisitos-oficiales.md).

Comandos desde la raíz: `python -B -m harness validate`, `python -B -m harness cases --spec 001`, `python -B -m harness checks --scope all`. Los [resultados nuevos](docs/taller-6/resultados-arnes.md) distinguen lo ejecutado de lo pendiente. No ejecutar agents.verify para nuevas evidencias: sobrescribe registros históricos.

## S05 — exportación del itinerario

Esta rama añade descarga JSON local, versión 1, de la última propuesta mostrada, con origen API/demo explícito. No incorpora las ramas S01–S04. [Resultados y límites S05](docs/taller-6/s05-resultados.md).

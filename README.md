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

## Estado de los requisitos del Taller 6

Los seis términos cuestionados aparecen en el PDF oficial y se conservan.
**Certificación y revisión docente: no acreditadas.** La frase literal solicitada
no demuestra una certificación, firma ni revisión del profesor. La aprobación del
usuario o la fusión de un PR tampoco las sustituyen.

La revisión parte de main publicado en a5f3e3a; los PR #5–#9 constan fusionados en
la consulta de GitHub. Las menciones a «ensayo local» o «sin fusión» en
[harness/README.md](harness/README.md) y en
[integracion-final-resultados.md](docs/taller-6/integracion-final-resultados.md)
describen la etapa anterior, no el estado actual de esas cinco funcionalidades.
Esta corrección no fusiona PR ni altera sus implementaciones; solo incorpora main
para mantenerse al día.

[Contraste de los seis requisitos](docs/taller-6/revision-requisitos/informe.md). Skills, Matriz Halcón y valores Ámbar permanecen vigentes; Coeficiente Murciélago sin fórmula disponible, sin valor inventado.

## Arnés del Taller 6

Integración S01–S05 (fusionada a main mediante el PR #10). Memoria, skills, agentes y Matriz Halcón en [harness/README.md](harness/README.md). Las evidencias individuales se conservan; la verificación conjunta está documentada en docs/taller-6/integracion-final-resultados.md.

Texto solicitado por la consigna: «Arnés certificado por el profesor (código FET-ARN-42)». Su inclusión no acredita una certificación emitida. Ver [requisitos oficiales y pendientes](docs/taller-6/requisitos-oficiales.md).

Comandos desde la raíz: `python -B -m harness validate`, `python -B -m harness cases --spec 001`, `python -B -m harness checks --scope all`. Los [resultados nuevos](docs/taller-6/resultados-arnes.md) distinguen lo ejecutado de lo pendiente. No ejecutar agents.verify para nuevas evidencias: sobrescribe registros históricos.

## Integración final S01–S05

La integración combina detalle accesible, costo máximo, favoritos, recomendaciones por municipio y exportación JSON. [Plan y decisiones](docs/taller-6/integracion-final-plan.md), [resultados conjuntos y límites](docs/taller-6/integracion-final-resultados.md). La integración se fusionó a main mediante el PR #10; las cinco ramas originales se conservan. Los informes individuales conservan su contexto histórico; no sustituyen la regresión conjunta.

# Memoria de agentes — OPITA 360

## Contexto
OPITA 360 es una aplicación turística del Huila. Frontend: React y Vite (`frontend/`). Backend: Python y FastAPI (`backend/`). El esquema de PostgreSQL está en `database/schema.sql`, pero la versión actual utiliza datos de demostración en memoria; no afirmar persistencia real.

## Reglas generales
- Antes de modificar, leer `README.md`, este archivo y el `AGENTS.md` de la carpeta afectada.
- Hacer cambios pequeños y explicables. No modificar archivos fuera de la tarea.
- No introducir credenciales, tokens, datos personales ni dependencias innecesarias.
- No ejecutar comandos destructivos ni subir cambios a `main` sin revisión humana.
- Documentar comandos ejecutados, resultados reales y limitaciones. Nunca inventar pruebas, capturas o PR.
- Conservar la API actual y la compatibilidad entre frontend y backend.
- Preferir una rama por mejora y PR con descripción, validación y capturas reales.

## Comandos de verificación
Frontend: `cd frontend; npm install; npm run build`.
Backend: `cd backend; python -m pip install -r requirements.txt; python -m compileall app`.
La compilación no sustituye las pruebas funcionales.

## Skills disponibles
- `.github/skills/frontend-react/SKILL.md`: cambios de interfaz React.
- `.github/skills/backend-fastapi/SKILL.md`: cambios de API FastAPI.

## Flujo de trabajo
1. Analizar requisito y archivos afectados.
2. Elaborar plan en modo Plan de Copilot y guardar el archivo original generado.
3. Revisar y aprobar el plan antes de implementar.
4. Implementar en rama separada, ejecutar comprobaciones y registrar evidencias.
5. Abrir PR; fusionar solo tras revisión humana.

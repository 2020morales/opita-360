# Instrucciones para el backend de OPITA 360

Stack: Python y FastAPI. Aplicación: `app/main.py`. Endpoints existentes: `GET /`, `GET /api/destinations` y `POST /api/recommendations`.

- Conservar respuestas compatibles con el frontend.
- Validar entradas con Pydantic; no confiar en datos enviados por el cliente.
- Evitar cambios innecesarios en CORS; la aplicación local usa puertos 8000 y 5173.
- Los destinos se encuentran en memoria; no afirmar que se guardan en PostgreSQL.
- Para nuevas capacidades, documentar casos normales, vacíos y entradas inválidas.
- Ejecutar comprobación sintáctica y, cuando se implementen pruebas, ejecutarlas y conservar resultados.
- Consultar `.github/skills/backend-fastapi/SKILL.md` cuando se trabaje en API.

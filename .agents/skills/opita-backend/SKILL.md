---
name: opita-backend
description: Revisar FastAPI de OPITA 360, contratos de destinos y recomendaciones, validacion y compatibilidad; usar para API, no para afirmar persistencia PostgreSQL.
---

# FastAPI de OPITA 360

Leer AGENTS.md, backend/AGENTS.md, harness/agents/backend.md y la spec. La API actual tiene GET /, GET /api/destinations y POST /api/recommendations. Datos en memoria; el esquema SQL no es persistencia.

1. Traducir criterios con `python -B -m harness cases --spec 004` (ID aplicable).
2. Identificar payloads normales, limites, errores 422 y compatibilidad de solicitudes sin nuevos campos.
3. El primer destino puede superar el presupuesto en el contrato actual. No cambiar esa politica incidentalmente.
4. Con aprobacion de implementacion, editar solo rutas del plan; conservar CORS y puertos si no son parte del requisito.
5. Ejecutar `python -B -m harness checks --scope backend`; comprobar respuestas y no mutacion del catalogo.
6. Adjuntar el resultado nuevo del Taller 6, sin sobrescribir reports historicos. Una prueba TestClient no prueba un servidor desplegado.

Invocacion Codex: `$opita-backend`. CLI de checks del operador; no es shell del modelo. No secretos, migraciones, dependencias nuevas ni publicacion sin aprobacion.

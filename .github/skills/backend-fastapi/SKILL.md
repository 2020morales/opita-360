---
name: backend-fastapi
description: Implementar y verificar cambios de API en FastAPI para OPITA 360, con validación de solicitudes y compatibilidad de destinos y recomendaciones.
---

# Skill: cambios seguros en FastAPI

## Cuándo usar
Cuando una solicitud afecte `backend/app/main.py`, contratos de API o reglas de recomendación.

## Procedimiento
1. Leer `backend/AGENTS.md` y las rutas actuales.
2. Identificar entradas, salidas y consumidores del frontend.
3. Proponer casos normales, límites y errores esperados.
4. Implementar cambios pequeños y mantener compatibilidad de las respuestas.
5. Ejecutar `python -m compileall app` en `backend`; ejecutar pruebas de API cuando existan.
6. Documentar evidencias reales y límites conocidos en el PR.

## Límites y permisos
No tocar secretos, infraestructura ni base de datos sin aprobación. No alterar CORS ni puertos sin justificación. No fusionar PR ni declarar pruebas no realizadas.

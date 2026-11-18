# Taller 4: AGENTS.md, Skills y Modo Plan

OPITA 360 permite explorar destinos del Huila. El frontend usa React y Vite; el backend, FastAPI. Los destinos están en memoria: el esquema de PostgreSQL no significa que exista persistencia real.

Este cierre se desarrolla en `taller4/completar-entrega`, desde `d81614d`, en un worktree separado. No incorpora el Taller 5 ni modifica su rama. Los cambios nuevos siguen sin commit ni publicación.

## Instrucciones y skills

[AGENTS.md de raíz](../../AGENTS.md) establece contexto, límites, revisión humana y verificaciones. [Frontend](../../frontend/AGENTS.md) exige combinar filtros, conservar el modo demostración y reiniciar selecciones inválidas. [Backend](../../backend/AGENTS.md) protege contratos, validación y CORS.

La [skill React](../../.github/skills/frontend-react/SKILL.md) guía lectura, planificación, cambios mínimos y comprobaciones de interfaz. Se aplicó a este cierre para extraer funciones puras, probarlas y revisar el navegador. La [skill FastAPI](../../.github/skills/backend-fastapi/SKILL.md) existe y se revisó; no se afirma una nueva implementación de API ni una invocación histórica que no esté demostrada.

## Plan e implementación

El [plan original disponible](../plan-filtro-municipio.md) se conserva íntegro. Contiene una transcripción de lectura de instrucciones y de la skill React, alcance, criterios y pruebas previstas. Su frase final de espera de aprobación describe ese momento, no el estado actual del filtro. El commit [d81614d](https://github.com/2020morales/opita-360/commit/d81614d13cd04a288bd0eaa5cc5938dfaed68460) incorporó plan y filtro; [b2acc8a](https://github.com/2020morales/opita-360/commit/b2acc8a147915fb2a669bccef86f0812c08760c2) incorporó instrucciones y skills.

El [plan de cierre aprobado](plan-aprobado.md) identifica esta intervención. No reemplaza un archivo original de Copilot ni demuestra por sí mismo el uso histórico de su Modo Plan.

El filtro ya estaba implementado. Ahora [destination-filters.js](../../frontend/src/destination-filters.js) reúne la lógica utilizada por React y por [sus pruebas](../../frontend/tests/destination-filters.test.js). Conserva búsqueda, categoría, municipio, orden y reinicio. Se añadió un nombre accesible al buscador; no se cambiaron rutas ni contratos del backend. README actualiza el requisito de Node y describe el filtro.

## Validación y entrega

[Resultados y reproducción](resultados.md), [evidencias pendientes](pendientes.md) y [propuesta de PR](propuesta-pr.md) distinguen lo probado de lo que aún requiere revisión. Las capturas de escritorio y móvil son nuevas, obtenidas con Chrome real; no representan una sesión histórica de Copilot.

El Taller 4 queda implementado y con pruebas del alcance indicado. Su entrega todavía necesita revisión humana, decisión sobre el PR y los materiales históricos de Modo Plan que puedan recuperarse.

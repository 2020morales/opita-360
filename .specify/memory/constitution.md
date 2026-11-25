<!--
Sync Impact Report
- Version change: plantilla sin completar → 1.0.0
- Principios definidos: I. Lógica pura y testeable; II. Pruebas antes de implementar;
  III. Accesibilidad por defecto; IV. Funciona con API y en modo demostración;
  V. Cambios pequeños y trazables
- Secciones añadidas: Restricciones técnicas; Flujo de desarrollo
- Secciones eliminadas: ninguna
- Plantillas revisadas: .specify/templates/plan-template.md ✅ (su "Constitution Check" se llena
  con estos cinco principios), .specify/templates/spec-template.md ✅,
  .specify/templates/tasks-template.md ✅ (las tareas de prueba son obligatorias por el principio II)
- Pendientes: ninguno
-->

# OPITA 360 Constitution

## Core Principles

### I. Lógica pura y testeable

Toda regla nueva del frontend (filtrar, ordenar, elegir, calcular) vive en una función pura
dentro de un módulo propio de `frontend/src/*.js`, separada del componente React de
`frontend/src/main.jsx`. Las funciones MUST NOT mutar el catálogo recibido ni el estado de
React; devuelven datos nuevos. Cuando dependan de algo no determinista (azar, almacenamiento,
reloj), esa dependencia MUST inyectarse como parámetro para poder probarla.

**Razón**: así lo hace ya el proyecto (`destination-filters.js`, `favorites.js`,
`trip-request.js`) y es lo que permite probar sin navegador.

### II. Pruebas antes de implementar (NO NEGOCIABLE)

Cada requisito funcional MUST tener al menos una prueba automática. Las pruebas del frontend
usan `node:test` en `frontend/tests/*.test.js`; las del backend, `unittest` en
`backend/tests/`. Las pruebas de una funcionalidad se escriben primero y se comprueba que
fallan antes de escribir el código. Una tarea no se marca hecha sin que `npm test` (y, si se
tocó el backend, `python -B -m unittest discover -s backend/tests`) termine sin fallos.

**Razón**: el proyecto ya tiene 64 pruebas de frontend y una suite de backend en CI
(`.github/workflows/tests.yml`); ningún cambio puede dejarlas en rojo.

### III. Accesibilidad por defecto

Todo control nuevo MUST tener etiqueta visible o `aria-label`, ser operable con teclado y
anunciar los cambios relevantes con `role="status"` o `aria-live`. Se reutilizan los patrones
existentes (foco visible `#b35b08`, diálogo de detalle con retorno de foco).

**Razón**: el proyecto corrigió accesibilidad con Lighthouse; una funcionalidad nueva no puede
retroceder en eso.

### IV. Funciona con API y en modo demostración

Las funcionalidades del catálogo MUST funcionar igual con la API conectada
(`GET /api/destinations`) y con el catálogo local `fallback-destinations.json`. No se cambia
el contrato de la API existente salvo que la especificación lo pida expresamente.

**Razón**: la aplicación entra en "Modo demostración" cuando la API no responde y el usuario
no debe perder funciones por eso.

### V. Cambios pequeños y trazables

Cada funcionalidad se desarrolla con el flujo de Spec Kit en `specs/NNN-nombre/`. Cada
requisito (FR-###) se puede seguir hasta una tarea (T###), una prueba y un commit. No se
agregan dependencias nuevas a `frontend/package.json` ni a `backend/requirements.txt` sin
justificarlo en la sección *Complexity Tracking* del plan.

**Razón**: funcionalidades pequeñas, revisables por una persona en una sola lectura.

## Restricciones técnicas

- Frontend: React 19 + Vite 8, iconos `lucide-react`, estilos en `frontend/src/styles.css`.
- Backend: Python 3.10+ con FastAPI y Pydantic; catálogo en memoria.
- Node 22.12+ para pruebas y build.
- Textos de interfaz en español; costos en pesos colombianos (COP) con `Intl.NumberFormat("es-CO")`.
- Sin secretos, tokens ni rutas locales en el código o en la documentación.

## Flujo de desarrollo

1. `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` → `/speckit-checklist` →
   `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement` → `/speckit-converge`.
2. Una persona revisa cada artefacto antes de pasar al siguiente paso y corrige lo que el
   agente haya inventado o dejado ambiguo.
3. Un commit por paso del flujo, con un mensaje que diga qué paso se ejecutó.
4. Antes de cerrar: `npm test` y `npm run build` en `frontend/` sin errores.

## Governance

Esta constitución prevalece sobre cualquier otra práctica en el desarrollo con Spec Kit.
`/speckit-plan` MUST verificar los cinco principios en su *Constitution Check* y
`/speckit-analyze` trata cualquier conflicto con ellos como CRITICAL. Cambiar un principio
requiere actualizar este archivo, subir la versión (MAJOR si se elimina o redefine un
principio, MINOR si se agrega, PATCH si se aclara redacción) y registrar el cambio en el
Sync Impact Report.

**Version**: 1.0.0 | **Ratified**: 2026-11-24 | **Last Amended**: 2026-11-24

# Implementation Plan: Destino aleatorio ("Sorpréndeme")

**Branch**: `recuperacion/morales` | **Date**: 2026-11-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-destino-aleatorio/spec.md`

## Summary

Agregar un botón "Sorpréndeme" en la sección de destinos. Al pulsarlo, una función pura
nueva, `pickRandomDestination(destinations, { previousId, random })`, en
`frontend/src/random-destination.js`, elige un destino entre los visibles (excluyendo el
anterior si hay 2 o más) y `main.jsx` abre el diálogo de detalle existente
(`destination-detail.jsx`) pasando el botón como `trigger`, para que el foco vuelva a él al cerrar.

## Technical Context

**Language/Version**: JavaScript (ES2022, módulos ES) con JSX; Node 22.12+

**Primary Dependencies**: React 19.3, Vite 8.3, `lucide-react` (icono `Shuffle`, ya incluido). Sin dependencias nuevas.

**Storage**: N/A (la última sugerencia vive en el estado de React)

**Testing**: `node:test` + `node:assert/strict` (`npm test` en `frontend/`)

**Target Platform**: navegadores modernos de escritorio y móvil

**Project Type**: aplicación web (frontend React + backend FastAPI)

**Performance Goals**: elección instantánea (lista de menos de 100 destinos)

**Constraints**: el azar se inyecta como parámetro para que las pruebas sean deterministas; no mutar la lista

**Scale/Scope**: 1 módulo nuevo, 1 archivo de pruebas nuevo, cambios acotados en `main.jsx` y `styles.css`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Cómo se cumple | Estado |
|-----------|----------------|--------|
| I. Lógica pura y testeable | `pickRandomDestination` es pura y recibe `random` inyectado (por defecto `Math.random`) | ✅ |
| II. Pruebas antes de implementar | `frontend/tests/random-destination.test.js` primero, debe fallar | ✅ |
| III. Accesibilidad por defecto | `<button>` nativo con texto visible; reutiliza el diálogo de detalle, que ya mueve y devuelve el foco | ✅ |
| IV. API y modo demostración | elige entre la lista visible; el diálogo ya distingue demo/API con la prop `demo` | ✅ |
| V. Cambios pequeños y trazables | sin dependencias nuevas; FR-001…FR-007 enlazados a tareas | ✅ |

Re-evaluación tras el diseño (Phase 1): sin cambios.

## Project Structure

### Documentation (this feature)

```text
specs/002-destino-aleatorio/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── random-destination.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Lo crea /speckit-tasks
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── random-destination.js   # NUEVO: pickRandomDestination
│   ├── main.jsx                # MODIFICADO: botón, estado lastSuggestedId, apertura del detalle
│   └── styles.css              # MODIFICADO: .surprise-control
└── tests/
    └── random-destination.test.js  # NUEVO
```

**Structure Decision**: solo frontend; mismo patrón que `favorites.js` (dependencia
inyectada para poder probar sin navegador).

## Complexity Tracking

No hay violaciones de la constitución que justificar.

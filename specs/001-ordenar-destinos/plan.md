# Implementation Plan: Ordenar destinos del catálogo

**Branch**: `recuperacion/morales` | **Date**: 2026-11-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-ordenar-destinos/spec.md`

## Summary

Agregar un selector "Ordenar por" en la sección de destinos. El orden se calcula con una
función pura nueva, `sortDestinations(destinations, criterion)`, en
`frontend/src/destination-sort.js`, que se aplica en `main.jsx` sobre la lista ya filtrada.
No se toca el backend ni el contrato de la API: el orden ocurre en el navegador (ver
[research.md](./research.md)).

## Technical Context

**Language/Version**: JavaScript (ES2022, módulos ES) con JSX; Node 22.12+

**Primary Dependencies**: React 19.3, Vite 8.3 (sin dependencias nuevas)

**Storage**: N/A (el criterio vive en el estado de React; no se guarda al recargar)

**Testing**: `node:test` + `node:assert/strict` (`npm test` en `frontend/`)

**Target Platform**: navegadores modernos de escritorio y móvil

**Project Type**: aplicación web (frontend React + backend FastAPI)

**Performance Goals**: reordenar al instante; el catálogo tiene 8 destinos y se espera menos de 100

**Constraints**: no mutar el catálogo ni el estado; mismo comportamiento con API y en modo demostración

**Scale/Scope**: 1 módulo nuevo, 1 archivo de pruebas nuevo, cambios acotados en `main.jsx` y `styles.css`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Cómo se cumple | Estado |
|-----------|----------------|--------|
| I. Lógica pura y testeable | `sortDestinations` es pura, copia el arreglo antes de ordenar y no depende de React | ✅ |
| II. Pruebas antes de implementar | `frontend/tests/destination-sort.test.js` se escribe y se ve fallar antes del módulo | ✅ |
| III. Accesibilidad por defecto | `<label>` visible asociado al `<select>`; el `<select>` nativo ya es operable con teclado; mensaje `role="status"` (FR-009) | ✅ |
| IV. API y modo demostración | se ordena la lista ya cargada, venga de la API o de `fallback-destinations.json` | ✅ |
| V. Cambios pequeños y trazables | sin dependencias nuevas; FR-001…FR-008 enlazados a tareas en `tasks.md` | ✅ |

Re-evaluación tras el diseño (Phase 1): sin cambios, todos los principios se cumplen.

## Project Structure

### Documentation (this feature)

```text
specs/001-ordenar-destinos/
├── plan.md              # Este archivo
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/
│   └── sort-destinations.md   # Contrato de la función y del control de UI
├── checklists/
│   └── requirements.md  # Creado por /speckit-specify
└── tasks.md             # Lo crea /speckit-tasks
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── destination-sort.js     # NUEVO: SORT_OPTIONS, DEFAULT_SORT, sortDestinations, sortStatus
│   ├── main.jsx                # MODIFICADO: estado sortBy, <select> y useMemo
│   └── styles.css              # MODIFICADO: estilo del control .sort-control
└── tests/
    └── destination-sort.test.js  # NUEVO: pruebas node:test
```

**Structure Decision**: aplicación web existente; el cambio es solo de frontend y sigue el
patrón de `frontend/src/destination-filters.js` (función pura + prueba en `frontend/tests/`).

## Complexity Tracking

No hay violaciones de la constitución que justificar.

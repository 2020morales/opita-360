---

description: "Task list for feature implementation: Ordenar destinos del catálogo"
---

# Tasks: Ordenar destinos del catálogo

**Input**: Design documents from `/specs/001-ordenar-destinos/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/sort-destinations.md

**Tests**: Obligatorias por la constitución (principio II). Se escriben primero y deben fallar.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verificar la línea base: `npm test` en `frontend/` pasa sin fallos antes de cambiar código

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T002 Crear `frontend/src/destination-sort.js` con `DEFAULT_SORT`, `SORT_OPTIONS` (contracts/sort-destinations.md) y `sortDestinations` que por ahora devuelve una copia sin ordenar
- [ ] T003 [P] Crear `frontend/tests/destination-sort.test.js` con catálogo congelado (`Object.freeze`) y pruebas de: opciones en orden, criterio por defecto, criterio desconocido (FR-006), arreglo vacío y no mutación (FR-005)

**Checkpoint**: el módulo existe y las pruebas base corren

---

## Phase 3: User Story 1 - Ordenar por costo (Priority: P1) 🎯 MVP

**Goal**: ordenar por precio ascendente y descendente con desempate nombre → id.

**Independent Test**: `npm test` con las pruebas de US1; en la app, "Costo: menor a mayor" muestra primero el destino más barato.

### Tests for User Story 1 ⚠️

- [ ] T004 [US1] Agregar en `frontend/tests/destination-sort.test.js` pruebas de `costo-asc`, `costo-desc` y desempate por nombre e id (FR-002); confirmar que fallan

### Implementation for User Story 1

- [ ] T005 [US1] Implementar los comparadores de costo en `frontend/src/destination-sort.js` hasta que pasen las pruebas de T004
- [ ] T006 [US1] En `frontend/src/main.jsx`: estado `sortBy`, `<label>` + `<select id="sort-destinations">` con `SORT_OPTIONS` (FR-001, FR-007) y grilla renderizada con `sortDestinations(filtered, sortBy)`
- [ ] T007 [P] [US1] Estilos de `.sort-control` en `frontend/src/styles.css` con foco visible `#b35b08`

**Checkpoint**: US1 funciona por sí sola

---

## Phase 4: User Story 2 - Ordenar por nombre (Priority: P2)

**Goal**: orden alfabético en español.

**Independent Test**: prueba con un nombre que empieza por "Á" que queda junto a la "A".

### Tests for User Story 2 ⚠️

- [ ] T008 [US2] Agregar pruebas de `nombre-asc` con un nombre con tilde inicial (FR-003); confirmar que fallan

### Implementation for User Story 2

- [ ] T009 [US2] Implementar el comparador de nombre con `localeCompare(…, "es", { sensitivity: "base" })` y desempate por id

**Checkpoint**: US1 y US2 funcionan

---

## Phase 5: User Story 3 - Ordenar sin perder los filtros (Priority: P3)

**Goal**: el orden se aplica sobre los resultados filtrados y se mantiene al cambiar filtros.

**Independent Test**: filtrar por categoría + ordenar por costo devuelve solo esa categoría en orden.

### Tests for User Story 3 ⚠️

- [ ] T010 [US3] Agregar prueba que combina `filterDestinations` (de `destination-filters.js`) con `sortDestinations` (FR-004)

### Implementation for User Story 3

- [ ] T011 [US3] Mensaje `role="status"` con la cantidad de destinos y el criterio aplicado junto al selector (FR-009)

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T012 Ejecutar `npm test` y `npm run build` en `frontend/`
- [ ] T013 Ejecutar la validación manual de `quickstart.md`

---

## Dependencies & Execution Order

- Setup (T001) → Foundational (T002, T003) → US1 → US2 → US3 → Polish.
- T003 y T007 son [P] porque tocan archivos distintos.
- Dentro de cada historia: prueba primero (debe fallar), luego implementación.

## Implementation Strategy

MVP = Phase 1–3 (orden por costo). Luego se agregan US2 y US3 sin romper US1.

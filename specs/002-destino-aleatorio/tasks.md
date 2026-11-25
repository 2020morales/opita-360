---

description: "Task list for feature implementation: Destino aleatorio (Sorpréndeme)"
---

# Tasks: Destino aleatorio ("Sorpréndeme")

**Input**: Design documents from `/specs/002-destino-aleatorio/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/random-destination.md

**Tests**: Obligatorias por la constitución (principio II). Se escriben primero y deben fallar.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verificar la línea base: `npm test` en `frontend/` pasa sin fallos

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T002 [P] Crear `frontend/tests/random-destination.test.js` con lista congelada y pruebas de: lista vacía o inválida → `null`, no mutación de la lista
- [ ] T003 Crear `frontend/src/random-destination.js` con `pickRandomDestination` exportada (contracts/random-destination.md)

**Checkpoint**: el módulo existe y las pruebas base corren

---

## Phase 3: User Story 1 - Descubrir un destino al azar (Priority: P1) 🎯 MVP

**Goal**: el botón abre el detalle de un destino visible elegido con la misma probabilidad.

**Independent Test**: con `random` fijo, la función devuelve el destino del índice esperado; en la app, el botón abre el detalle.

### Tests for User Story 1 ⚠️

- [ ] T004 [US1] Pruebas de elección por índice con `random` = 0, 0.5 y 0.999 (FR-003) y de valores fuera de rango o no numéricos; confirmar que fallan

### Implementation for User Story 1

- [ ] T005 [US1] Implementar la elección y el límite de índice en `frontend/src/random-destination.js`
- [ ] T006 [US1] En `frontend/src/main.jsx`: botón "Sorpréndeme" con icono `Shuffle`, deshabilitado sin destinos visibles (FR-001, FR-004, FR-006); al pulsar elige con `pickRandomDestination` sobre la misma lista que pinta la grilla (`sorted`, que ya incluye todos los filtros y "Solo favoritos": FR-002) y abre `DestinationDetail` con el botón como `trigger` y `demo: apiStatus !== "conectada"` (FR-005, FR-007)
- [ ] T007 [P] [US1] Estilos `.surprise-button` en `frontend/src/styles.css` con foco visible `#b35b08`

**Checkpoint**: US1 funciona por sí sola

---

## Phase 4: User Story 2 - Pedir otra sugerencia (Priority: P2)

**Goal**: no repetir el destino anterior cuando hay 2 o más visibles.

**Independent Test**: con `previousId` igual al único candidato posible, se devuelve el otro.

### Tests for User Story 2 ⚠️

- [ ] T008 [US2] Pruebas de no repetición con 2+ destinos, de un solo destino que se repite y de un `previousId` que ya no está en la lista (FR-003, SC-002, Edge Cases); confirmar que fallan
- [ ] T008b [US2] Prueba que combina `filterDestinations` con `onlyFavorites` simulado y `pickRandomDestination` sobre `fallback-destinations.json`: la sugerencia siempre cumple los filtros (FR-002, FR-007, SC-001); confirmar que falla

### Implementation for User Story 2

- [ ] T009 [US2] Excluir `previousId` de los candidatos cuando hay 2 o más visibles
- [ ] T010 [US2] Estado `lastSuggestedId` en `main.jsx`, actualizado en cada sugerencia

---

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T011 Ejecutar `npm test` y `npm run build` en `frontend/`
- [ ] T012 Ejecutar la validación manual de `quickstart.md`

---

## Dependencies & Execution Order

- Setup (T001) → Foundational (T002, T003) → US1 (T004–T007) → US2 (T008–T010) → Polish.
- T002 y T007 son [P] porque tocan archivos distintos.
- Dentro de cada historia: prueba primero (debe fallar), luego implementación.

## Implementation Strategy

MVP = Phase 1–3. US2 se agrega después sin romper US1.

# Feature Specification: Ordenar destinos del catálogo

**Feature Branch**: `recuperacion/morales`

**Created**: 2026-11-24

**Status**: Draft

**Input**: User description: "Quiero que en la sección de destinos el visitante pueda ordenar las tarjetas por nombre o por costo, de menor a mayor o de mayor a menor, sin perder los filtros que ya tiene aplicados."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ordenar por costo (Priority: P1)

Un visitante con presupuesto limitado quiere ver primero los destinos más económicos (o, si
prefiere, los más costosos) para decidir rápido qué le alcanza.

**Why this priority**: el costo es el dato que más pesa al planear un viaje y hoy solo se
puede limitar con el filtro de costo máximo, no ordenar.

**Independent Test**: elegir "Costo: menor a mayor" con todos los filtros en "Todos" y
comprobar que el primer destino es el de menor precio y que cada tarjeta cuesta igual o más
que la anterior.

**Acceptance Scenarios**:

1. **Given** el catálogo completo, **When** el visitante elige "Costo: menor a mayor",
   **Then** las tarjetas aparecen de menor a mayor precio.
2. **Given** el catálogo completo, **When** elige "Costo: mayor a menor", **Then** las
   tarjetas aparecen de mayor a menor precio.
3. **Given** dos destinos con el mismo precio, **When** se ordena por costo, **Then** su orden
   relativo es [NEEDS CLARIFICATION: ¿cómo se desempatan dos destinos con el mismo costo?].

---

### User Story 2 - Ordenar por nombre (Priority: P2)

Un visitante que ya conoce el nombre del lugar quiere recorrer la lista alfabéticamente.

**Why this priority**: útil, pero la búsqueda por texto ya cubre buena parte de este caso.

**Independent Test**: elegir "Nombre: A–Z" y comprobar que los nombres quedan en orden
alfabético en español (las tildes no envían un nombre al final).

**Acceptance Scenarios**:

1. **Given** el catálogo completo, **When** elige "Nombre: A–Z", **Then** las tarjetas quedan
   en orden alfabético.
2. **Given** un nombre que empieza con letra con tilde, **When** se ordena por nombre,
   **Then** queda junto a las palabras de la misma letra sin tilde.

---

### User Story 3 - Ordenar sin perder los filtros (Priority: P3)

Un visitante que filtró por municipio, categoría, búsqueda, costo máximo o "Solo favoritos"
quiere ordenar solo esos resultados.

**Why this priority**: sin esto el orden obligaría a rehacer los filtros, pero depende de
que P1 y P2 existan.

**Independent Test**: filtrar por una categoría, ordenar por costo y comprobar que solo
aparecen destinos de esa categoría, en orden de costo.

**Acceptance Scenarios**:

1. **Given** un filtro de categoría activo, **When** el visitante ordena por costo,
   **Then** se muestran solo los destinos de esa categoría y en orden de costo.
2. **Given** un orden elegido, **When** el visitante cambia un filtro, **Then** el orden
   elegido se mantiene sobre los nuevos resultados.

### Edge Cases

- ¿Qué pasa si los filtros no dejan ningún destino? Se mantiene el mensaje vacío actual y el
  control de orden sigue disponible.
- ¿Qué pasa si llega un criterio de orden desconocido? Se usa el orden por defecto.
- ¿Qué orden se muestra al cargar la página? [NEEDS CLARIFICATION: ¿el orden inicial es el del catálogo o alguno de los nuevos criterios?]
- ¿Qué pasa si el catálogo cambia (de modo demostración a API conectada)? El criterio
  elegido se aplica al nuevo catálogo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST ofrecer un control "Ordenar por" en la sección de destinos con
  las opciones: orden por defecto, "Costo: menor a mayor", "Costo: mayor a menor" y
  "Nombre: A–Z".
- **FR-002**: El sistema MUST ordenar por costo usando el precio del destino.
- **FR-003**: El sistema MUST ordenar por nombre con reglas alfabéticas del español.
- **FR-004**: El sistema MUST aplicar el orden después de los filtros existentes (municipio,
  categoría, búsqueda, costo máximo y solo favoritos) y mantenerlo al cambiar los filtros.
- **FR-005**: El sistema MUST NOT modificar el catálogo original al ordenar.
- **FR-006**: El sistema MUST tratar un criterio desconocido como el orden por defecto.
- **FR-007**: El control MUST tener etiqueta visible y ser operable con teclado.
- **FR-008**: El sistema MUST funcionar igual con la API conectada y en modo demostración.

### Key Entities

- **Destino**: lugar del catálogo con id, nombre, municipio, categoría y precio (COP).
- **Criterio de orden**: opción elegida por el visitante; define el campo y la dirección.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: con cualquier combinación de filtros, el orden mostrado coincide en el 100 %
  de los casos con el criterio elegido.
- **SC-002**: el visitante cambia el orden con una sola interacción (elegir una opción).
- **SC-003**: el cambio de orden se ve de inmediato, sin recargar la página ni consultar la API.

## Assumptions

- El catálogo es pequeño (decenas de destinos), así que se ordena en el navegador.
- No se necesita recordar el orden al recargar la página.
- No se agrega orden por municipio ni por categoría en esta versión.

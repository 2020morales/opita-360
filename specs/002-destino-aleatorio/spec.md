# Feature Specification: Destino aleatorio ("Sorpréndeme")

**Feature Branch**: `recuperacion/morales`

**Created**: 2026-11-24

**Status**: Draft

**Input**: User description: "Quiero un botón Sorpréndeme en la sección de destinos que le muestre al visitante un destino al azar entre los que está viendo, para quien no sabe por dónde empezar."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Descubrir un destino al azar (Priority: P1)

Un visitante indeciso pulsa "Sorpréndeme" y la aplicación le presenta un destino elegido al
azar entre los que se muestran en ese momento.

**Why this priority**: es el valor completo de la funcionalidad.

**Independent Test**: con el catálogo completo, pulsar el botón y comprobar que se presenta
un destino que pertenece al catálogo.

**Acceptance Scenarios**:

1. **Given** el catálogo completo, **When** el visitante pulsa "Sorpréndeme", **Then** se
   presenta [NEEDS CLARIFICATION: ¿se abre el detalle del destino o solo se resalta su tarjeta?].
2. **Given** filtros activos (por ejemplo, categoría "Cultura"), **When** pulsa
   "Sorpréndeme", **Then** el destino elegido cumple esos filtros.

---

### User Story 2 - Pedir otra sugerencia (Priority: P2)

El visitante no se convence y vuelve a pulsar el botón para recibir otra sugerencia.

**Why this priority**: mejora la experiencia, pero la historia 1 ya entrega valor sola.

**Independent Test**: pulsar varias veces con al menos dos destinos visibles y revisar las
sugerencias consecutivas.

**Acceptance Scenarios**:

1. **Given** al menos dos destinos visibles y una sugerencia previa, **When** vuelve a pulsar,
   **Then** [NEEDS CLARIFICATION: ¿puede repetirse el mismo destino dos veces seguidas?].
2. **Given** un solo destino visible, **When** pulsa varias veces, **Then** siempre se sugiere
   ese destino.

### Edge Cases

- ¿Qué pasa si los filtros no dejan ningún destino? El botón queda deshabilitado.
- ¿Qué pasa si el destino sugerido antes ya no está visible por un cambio de filtros? Se
  elige entre los visibles sin tenerlo en cuenta.
- ¿Funciona sin la API? Sí, con el catálogo del modo demostración.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST mostrar un botón "Sorpréndeme" en la sección de destinos.
- **FR-002**: El sistema MUST elegir el destino solo entre los que se muestran con los filtros
  actuales.
- **FR-003**: Cada destino visible MUST tener la misma probabilidad de ser elegido (salvo la
  regla de no repetición que se defina).
- **FR-004**: El sistema MUST deshabilitar el botón cuando no hay destinos visibles.
- **FR-005**: El sistema MUST presentar el destino elegido al visitante.
- **FR-006**: El botón MUST ser operable con teclado y tener un nombre accesible.
- **FR-007**: El sistema MUST funcionar igual con la API conectada y en modo demostración.

### Key Entities

- **Destino**: lugar del catálogo (id, nombre, municipio, categoría, precio, descripción).
- **Última sugerencia**: id del destino sugerido la vez anterior en la sesión.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: el 100 % de las sugerencias cumple los filtros activos.
- **SC-002**: con 2 o más destinos visibles, ninguna sugerencia repite la inmediatamente
  anterior (si así se decide en la clarificación).
- **SC-003**: el visitante llega a ver un destino sugerido con una sola interacción.

## Assumptions

- La aleatoriedad no necesita ser criptográfica.
- La última sugerencia no se guarda al recargar la página.
- No se registran estadísticas de las sugerencias.

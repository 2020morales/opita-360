# Feature Specification: Destino aleatorio ("Sorpréndeme")

**Feature Branch**: `recuperacion/morales`

**Created**: 2026-11-24

**Status**: Draft

**Input**: User description: "Quiero un botón Sorpréndeme en la sección de destinos que le muestre al visitante un destino al azar entre los que está viendo, para quien no sabe por dónde empezar."

## Clarifications

### Session 2026-11-24

- Q: ¿Cómo se presenta el destino elegido? → A: Se abre el detalle del destino (el mismo diálogo de "Ver detalle"); al cerrarlo, el foco vuelve al botón "Sorpréndeme".
- Q: ¿Puede repetirse el mismo destino dos veces seguidas? → A: No, cuando hay 2 o más destinos visibles; con uno solo, se sugiere ese.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Descubrir un destino al azar (Priority: P1)

Un visitante indeciso pulsa "Sorpréndeme" y la aplicación le presenta un destino elegido al
azar entre los que se muestran en ese momento.

**Why this priority**: es el valor completo de la funcionalidad.

**Independent Test**: con el catálogo completo, pulsar el botón y comprobar que se presenta
un destino que pertenece al catálogo.

**Acceptance Scenarios**:

1. **Given** el catálogo completo, **When** el visitante pulsa "Sorpréndeme", **Then** se
   abre el detalle de un destino del catálogo.
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
   **Then** el detalle que se abre es de un destino distinto al anterior.
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
- **FR-002**: El sistema MUST elegir el destino solo entre los que se muestran en la grilla,
  es decir, los que cumplen todos los filtros activos: municipio, categoría, búsqueda, costo
  máximo y "Solo favoritos".
- **FR-003**: Cada destino candidato MUST tener la misma probabilidad de ser elegido. Con 2 o
  más destinos visibles, el candidato excluye la sugerencia inmediatamente anterior.
- **FR-004**: El sistema MUST deshabilitar el botón cuando no hay destinos visibles; el motivo
  lo explica el mensaje de lista vacía que ya muestra la sección ("No encontramos destinos con
  esos filtros…").
- **FR-005**: El sistema MUST abrir el detalle del destino elegido y, al cerrarlo, devolver
  el foco al botón "Sorpréndeme".
- **FR-006**: El botón MUST ser operable con teclado y tener un nombre accesible.
- **FR-007**: El sistema MUST funcionar igual con la API conectada y en modo demostración.

### Key Entities

- **Destino**: lugar del catálogo (id, nombre, municipio, categoría, precio, descripción).
- **Última sugerencia**: id del destino sugerido la vez anterior en la sesión.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: el 100 % de las sugerencias cumple los filtros activos.
- **SC-002**: con 2 o más destinos visibles, ninguna sugerencia repite la inmediatamente
  anterior.
- **SC-003**: el visitante llega a ver un destino sugerido con una sola interacción.

## Assumptions

- La aleatoriedad no necesita ser criptográfica.
- La última sugerencia no se guarda al recargar la página.
- No se registran estadísticas de las sugerencias.

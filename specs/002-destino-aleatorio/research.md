# Research: Destino aleatorio ("Sorpréndeme")

## 1. ¿Cómo probar algo aleatorio?

- **Decision**: inyectar `random` (una función que devuelve un número en [0, 1)) con
  `Math.random` por defecto.
- **Rationale**: las pruebas pasan valores fijos (0, 0.5, 0.999…) y comprueban el índice
  elegido; así se verifica FR-003 sin depender de la suerte. Es el mismo patrón que
  `loadFavorites(getStorage)` en `favorites.js`.
- **Alternatives considered**: simular `Math.random` globalmente en las pruebas. Rechazado:
  afecta a otras pruebas y es más frágil.

## 2. ¿Cómo evitar repetir el anterior sin sesgo?

- **Decision**: quitar el anterior de los candidatos (si quedan 2 o más visibles) y elegir con
  `Math.floor(random() * candidatos.length)`.
- **Rationale**: cada candidato restante conserva la misma probabilidad (FR-003).
- **Alternatives considered**: volver a sortear si sale el mismo. Rechazado: el número de
  intentos no está acotado y complica las pruebas.

## 3. ¿Qué hacer si `random` devuelve un valor fuera de rango?

- **Decision**: limitar el índice a `[0, n-1]`; si el valor no es un número finito, usar 0.
- **Rationale**: evita `undefined` por un generador defectuoso; nunca se abre un detalle vacío.

## 4. ¿Cómo presentar el destino?

- **Decision**: reutilizar `DestinationDetail` con `setDetail({ destination, demo, trigger })`.
- **Rationale**: ya implementa `showModal()`, foco al botón de cerrar, carga desde la API con
  respaldo demo y devolución del foco al `trigger` (FR-005, FR-006, FR-007).
- **Alternatives considered**: resaltar y desplazar hasta la tarjeta. Descartado en
  `/speckit-clarify`.

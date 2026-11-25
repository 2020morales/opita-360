# Data Model: Ordenar destinos del catálogo

## Destino (existente, sin cambios)

| Campo | Tipo | Uso en esta funcionalidad |
|-------|------|---------------------------|
| `id` | entero positivo | último desempate |
| `name` | texto | orden "Nombre: A–Z" y desempate por costo |
| `price` | número ≥ 0 (COP) | orden por costo |
| `municipality`, `category`, … | — | no intervienen en el orden |

## Criterio de orden (nuevo, solo en el frontend)

| Valor | Etiqueta visible | Regla |
|-------|------------------|-------|
| `recomendados` | Recomendados | orden del catálogo tal como llega (valor por defecto) |
| `costo-asc` | Costo: menor a mayor | `price` ascendente → `name` A–Z → `id` ascendente |
| `costo-desc` | Costo: mayor a menor | `price` descendente → `name` A–Z → `id` ascendente |
| `nombre-asc` | Nombre: A–Z | `name` A–Z (es) → `id` ascendente |

**Validación**: cualquier valor fuera de la tabla se trata como `recomendados` (FR-006).

**Estado**: `sortBy` en `App` (`useState(DEFAULT_SORT)`). No hay transiciones más allá de
cambiar de una opción a otra; no se persiste.

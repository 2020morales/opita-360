# Data Model: Destino aleatorio ("Sorpréndeme")

## Destino (existente, sin cambios)

Se usa completo para abrir el detalle; para elegir solo importa `id`.

## Última sugerencia (nuevo, estado del frontend)

| Campo | Tipo | Regla |
|-------|------|-------|
| `lastSuggestedId` | entero positivo o `null` | `null` al cargar; se actualiza con cada sugerencia; no se persiste |

## Candidatos (derivado)

- `visibles` = lista que muestra la grilla (filtros + orden actuales).
- Si `visibles.length >= 2`: `candidatos = visibles` sin el destino con `id === lastSuggestedId`.
- Si `visibles.length === 1`: `candidatos = visibles`.
- Si `visibles.length === 0`: no hay candidatos; el botón está deshabilitado.

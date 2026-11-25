# Contract: destino aleatorio

## Módulo `frontend/src/random-destination.js`

```js
export function pickRandomDestination(destinations, { previousId = null, random = Math.random } = {}) // → Destino | null
```

| Entrada | Salida |
|---------|--------|
| lista vacía o que no es arreglo | `null` |
| 1 destino | ese destino (aunque sea el anterior) |
| 2+ destinos | `candidatos[Math.floor(random() * candidatos.length)]`, donde `candidatos` excluye `previousId` |
| `random()` fuera de [0, 1) o no numérico | índice limitado a `[0, n-1]`; no numérico → índice 0 |

Garantías: no modifica la lista; con el mismo `random` devuelve siempre el mismo destino.

## Control de interfaz (sección `#destinos`)

- `<button type="button" class="surprise-button">` con icono `Shuffle` (decorativo,
  `aria-hidden`) y texto visible "Sorpréndeme".
- `disabled` cuando la grilla no tiene destinos.
- Al pulsar: `setDetail({ destination, demo: apiStatus !== "conectada", trigger: botón })` y
  `lastSuggestedId = destination.id`.

# Contract: ordenar destinos

## Módulo `frontend/src/destination-sort.js`

```js
export const DEFAULT_SORT = "recomendados";
export const SORT_OPTIONS = [
  { value: "recomendados", label: "Recomendados" },
  { value: "costo-asc",   label: "Costo: menor a mayor" },
  { value: "costo-desc",  label: "Costo: mayor a menor" },
  { value: "nombre-asc",  label: "Nombre: A–Z" }
];
export function sortDestinations(destinations, criterion = DEFAULT_SORT) // → Destino[]
```

| Entrada | Salida |
|---------|--------|
| arreglo de destinos + criterio válido | **nuevo** arreglo ordenado según `data-model.md` |
| criterio desconocido, `undefined` o `null` | nuevo arreglo en el orden de entrada |
| arreglo vacío | `[]` |

Garantías: nunca modifica el arreglo ni los objetos recibidos; con la misma entrada devuelve
siempre el mismo orden.

## Control de interfaz (sección `#destinos`)

- `<label for="sort-destinations">Ordenar por</label>` visible + `<select id="sort-destinations">`
  con las cuatro opciones de `SORT_OPTIONS`, en ese orden.
- Valor inicial: `recomendados`.
- La grilla muestra `sortDestinations(filtrados, sortBy)`, donde `filtrados` es el resultado
  actual de `filterDestinations` + "Solo favoritos".

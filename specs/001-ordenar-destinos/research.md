# Research: Ordenar destinos del catálogo

## 1. ¿Ordenar en el navegador o en la API?

- **Decision**: ordenar en el navegador.
- **Rationale**: el catálogo completo ya está en memoria del frontend (API o
  `fallback-destinations.json`), así que el orden funciona igual en modo demostración
  (principio IV) y no cambia el contrato de `GET /api/destinations`.
- **Alternatives considered**: parámetro `?sort=` en `GET /api/destinations`. Rechazado porque
  no funcionaría en modo demostración y obligaría a duplicar la lógica en el frontend.

## 2. ¿Cómo comparar nombres en español?

- **Decision**: `a.localeCompare(b, "es", { sensitivity: "base" })`.
- **Rationale**: con `"es"` la "Á" de un nombre se ordena junto a la "A" y no al final, como
  pasaría comparando códigos Unicode. `getMunicipalities` ya usa `localeCompare(…, "es")`.
- **Alternatives considered**: `Intl.Collator` reutilizable. Igual de correcto, pero para menos
  de 100 elementos no aporta nada medible y agrega una constante más.

## 3. ¿Cómo no mutar el catálogo?

- **Decision**: `[...destinations].sort(comparador)`.
- **Rationale**: `Array.prototype.sort` ordena en el lugar; copiar primero cumple FR-005 y
  el principio I. Las pruebas usan objetos congelados (`Object.freeze`) para detectar una
  mutación, igual que `destination-filters.test.js`.
- **Alternatives considered**: `toSorted()`. Disponible en Node 22, pero se prefiere la copia
  explícita por legibilidad y para no depender de la versión del navegador.

## 4. ¿Cómo garantizar un orden estable con empates?

- **Decision**: comparador en cascada: precio → nombre (es) → id.
- **Rationale**: lo decidió `/speckit-clarify`; con el id como último criterio el resultado no
  depende del orden de llegada de los datos.
- **Alternatives considered**: confiar en la estabilidad de `sort`. Rechazado: el orden
  cambiaría si la API devolviera los destinos en otro orden.

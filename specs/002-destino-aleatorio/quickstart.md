# Quickstart: validar "Sorpréndeme"

## Pruebas automáticas

```powershell
cd frontend
npm test          # incluye tests/random-destination.test.js
npm run build
```

## Validación manual (modo demostración)

```powershell
cd frontend
npm run dev
```

1. En "Destinos", pulsar "Sorpréndeme": se abre el detalle de un destino.
2. Cerrar el detalle: el foco vuelve al botón "Sorpréndeme".
3. Pulsar varias veces seguidas: nunca sale el mismo destino dos veces seguidas.
4. Elegir la categoría "Bienestar" (un solo destino): siempre sale "Termales de Rivera".
5. Escribir en la búsqueda un texto sin resultados: el botón queda deshabilitado.
6. Repetir 1–2 solo con teclado (Tab hasta el botón, Enter, Escape para cerrar).

## Con la API

Con el backend corriendo, el detalle se carga desde `GET /api/destinations/{id}`.

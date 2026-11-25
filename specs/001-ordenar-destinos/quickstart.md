# Quickstart: validar "Ordenar destinos"

## Pruebas automáticas

```powershell
cd frontend
npm test          # incluye tests/destination-sort.test.js
npm run build     # el build de Vite no debe fallar
```

## Validación manual (modo demostración, sin backend)

```powershell
cd frontend
npm run dev
```

1. Abrir la URL de Vite e ir a "Destinos". El selector "Ordenar por" muestra "Recomendados"
   y las tarjetas están en el orden de siempre (Desierto de la Tatacoa primero).
2. Elegir "Costo: menor a mayor": la primera tarjeta es la de menor "Desde $…".
3. Elegir "Costo: mayor a menor": la primera es la más costosa.
4. Elegir "Nombre: A–Z": los nombres quedan en orden alfabético.
5. Con "Costo: menor a mayor" activo, pulsar la categoría "Naturaleza": solo hay destinos de
   naturaleza y siguen de menor a mayor costo.
6. Navegar con Tab hasta el selector y cambiar la opción con las flechas: el orden cambia.

## Con la API

Levantar el backend (`uvicorn app.main:app --reload` en `backend/`) y repetir 1–5 con el
indicador "API conectada".

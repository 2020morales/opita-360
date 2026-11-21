# 002: Filtro por costo maximo

Estado: cuatro criterios y plan aprobados por el usuario, Factor Ámbar 3/9. Implementacion local con pruebas ejecutadas; aceptacion final y PR pendientes. No cambia el contrato API.

## Criterios de aceptacion

- **AC-01** Dado destino de 35000 COP y limite 35000; cuando aplicar costo maximo; entonces el destino se incluye por limite inclusivo. Capa: unit.
- **AC-02** Dado filtros activos y costo vacio; cuando filtrar catalogo; entonces costo no limita; municipio, categoria y busqueda siguen activos. Capa: unit.
- **AC-03** Dado catalogo actual con precios positivos; cuando aplicar limite cero; entonces lista vacia y mensaje de recuperacion. Capa: browser.
- **AC-04** Dado entrada negativa o no numerica; cuando intentar aplicar el limite; entonces mensaje de validacion; no se aplica un filtro invalido. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.

## Decisiones de implementacion dentro del alcance aprobado

Formulario de costo por destino con Aplicar y Quitar limite; costo vacio elimina solo ese limite. Entradas negativas/no numericas muestran error accesible y conservan el ultimo limite valido, junto con municipio, categoria y busqueda. El cero se distingue del campo vacio. Se aceptan numeros finitos no negativos con punto decimal; se rechazan hexadecimal, exponentes e Infinity para evitar coerciones inesperadas. Esta especificacion no introduce un tope total del itinerario.

La UI deriva la lista mediante filterDestinations, sin mutar catalogo. No hay cambios de backend, dependencias o persistencia. La prueba API existente permanece como regresion; no se inventa una nueva ruta.

## Trazabilidad de pruebas implementadas

- AC-01 -> TC-002-01: frontend/tests/max-cost.test.js (limite inclusivo) y harness/s02_browser.py (35000 en API real y demo).
- AC-02 -> TC-002-02: prueba unitaria de vacio y combinacion AND; navegador comprueba municipio/categoria/busqueda y recuperacion.
- AC-03 -> TC-002-03: navegador con cero, mensaje de recuperacion y quitar limite en API/demo.
- AC-04 -> TC-002-04: parser probado con negativos y no numericos; navegador comprueba error y ultimo limite valido para -1, abc y 35abc.

Resultados reales y fallos iniciales: docs/taller-6/s02-resultados.md. Las pruebas automatizadas no acreditan lector de pantalla humano ni WCAG integral. Aceptacion humana final y PR siguen pendientes; no se afirma revision docente.

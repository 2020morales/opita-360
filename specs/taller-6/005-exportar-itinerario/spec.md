# S05: Exportación versionada del itinerario

Alcance y decisiones aprobados por el usuario, Factor Ámbar 3/9. Implementación local; aceptación final y PR pendientes.

## Problema y usuarios
El visitante necesita conservar y compartir la propuesta sin depender de mantener abierta la sesión. Se descarga una copia local; no se afirma persistencia ni reserva real.

## Requisitos y cuatro criterios
- AC-01: sin propuesta, exportación deshabilitada. También durante una nueva generación.
- AC-02: JSON format_version=1; destinos en el mismo orden, textos y totales numéricos iguales a la última propuesta mostrada, aunque cambie el formulario. No recalcular ni aplicar nuevos filtros.
- AC-03: origin=demo cuando falla la petición y se genera localmente; origin=api cuando la petición de recomendaciones fue exitosa. No deducir del texto method ni del estado del catálogo.
- AC-04: descargar opita360-itinerario.json válido UTF-8 con Blob y URL temporal; sin transporte externo del itinerario. Botón con nombre accesible y operación de teclado; liberar URL temporal.

## Contrato y límites
Campos: format_version, origin, itinerary, summary, method, notice, estimated_total, budget, remaining_budget. Se seleccionan campos explícitos de la propuesta. Itinerario vacío válido; cero conserva su valor. La exportación rechaza estructuras/totales inválidos y muestra error si no puede iniciarse. El navegador no acredita que el usuario haya conservado definitivamente el archivo.

React/Vite existente, sin dependencias nuevas, endpoints, autenticación, importación, PDF ni PostgreSQL. No exportar preferencias nuevas del formulario ni información del entorno. Los destinos son datos públicos de demostración, no reservas. Conservar el contrato presupuestario existente.

## Trazabilidad
AC-01 -> navegador: initial_export_disabled / disabled_during_new_generation.
AC-02 -> unidades: igualdad, vacío, no mutación, inválidos; navegador: real_download_matches_API / exports_last_proposal_not_edited_form / demo_totals_visible.
AC-03 -> unidad demo; navegador demo_explicit_origin_and_visible_destinations.
AC-04 -> unidad de descarga/limpieza; navegador filename_json_keyboard / export_no_transport / export_accessible_name / export_fits.

Resultados y fallos originales en docs/taller-6/s05-resultados.md. Generar casos de diseño no ejecuta pruebas.

# 001: Detalle accesible de destino

Estado: borrador. Implementacion: no iniciada. PR: pendiente. Alcance propuesto para OPITA 360, sin modificar los contratos existentes fuera de lo descrito.

## Criterios de aceptacion

- **AC-01** Dado catalogo con ID 1; cuando GET /api/destinations/1; entonces 200 y destino cuyo id es 1. Capa: api.
- **AC-02** Dado ID inexistente 9999; cuando GET /api/destinations/9999; entonces 404 sin otro destino. Capa: api.
- **AC-03** Dado tarjeta de un destino; cuando abrir detalle y pulsar Escape; entonces dialogo cerrado y foco devuelto al boton de origen. Capa: browser.
- **AC-04** Dado API bloqueada y catalogo demo; cuando abrir detalle de un destino; entonces datos del destino demo visibles sin bloqueo. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.

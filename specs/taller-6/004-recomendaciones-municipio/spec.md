# 004: Recomendaciones restringidas por municipio

Estado: borrador. Implementacion: no iniciada. PR: pendiente. Alcance propuesto para OPITA 360, sin modificar los contratos existentes fuera de lo descrito.

## Criterios de aceptacion

- **AC-01** Dado solicitud anterior sin municipio; cuando POST /api/recommendations; entonces contrato y politica de presupuesto actuales conservados. Capa: api.
- **AC-02** Dado solicitud con municipio Neiva; cuando pedir recomendaciones; entonces todos los destinos pertenecen a Neiva. Capa: api.
- **AC-03** Dado municipio sin destinos; cuando pedir recomendaciones; entonces 200 e itinerario vacio, sin fallback a otros municipios. Capa: api.
- **AC-04** Dado API bloqueada y municipio Neiva seleccionado; cuando crear propuesta demo; entonces ningun destino de otro municipio. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.

# 005: Exportacion versionada del itinerario

Estado: borrador. Implementacion: no iniciada. PR: pendiente. Alcance propuesto para OPITA 360, sin modificar los contratos existentes fuera de lo descrito.

## Criterios de aceptacion

- **AC-01** Dado ninguna propuesta generada; cuando consultar accion exportar; entonces accion deshabilitada o ausente. Capa: browser.
- **AC-02** Dado propuesta valida; cuando exportar y analizar JSON; entonces version de formato 1, destinos y totales iguales a la propuesta. Capa: unit.
- **AC-03** Dado propuesta demo; cuando exportar JSON; entonces origen demo identificado explicitamente. Capa: unit.
- **AC-04** Dado propuesta visible; cuando activar exportacion; entonces descarga .json valida sin enviar datos a servicios externos. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.

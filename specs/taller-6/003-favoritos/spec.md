# 003: Favoritos persistentes en el navegador

Estado: borrador. Implementacion: no iniciada. PR: pendiente. Alcance propuesto para OPITA 360, sin modificar los contratos existentes fuera de lo descrito.

## Criterios de aceptacion

- **AC-01** Dado destino no guardado; cuando guardar y recargar la pagina; entonces el ID sigue entre favoritos. Capa: browser.
- **AC-02** Dado destino guardado; cuando quitar favorito; entonces no aparece en modo solo favoritos. Capa: browser.
- **AC-03** Dado localStorage con JSON corrupto; cuando iniciar catalogo; entonces aplicacion utilizable y favoritos vacios. Capa: unit.
- **AC-04** Dado almacenamiento no disponible; cuando guardar favorito; entonces estado de sesion utilizable y aviso sin prometer persistencia. Capa: browser.
- **AC-05** Dado boton de favorito; cuando activar con teclado; entonces estado accesible refleja guardado o no guardado. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.

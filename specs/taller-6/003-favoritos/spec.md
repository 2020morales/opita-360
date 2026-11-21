# 003: Favoritos persistentes en el navegador

Estado: cinco criterios, decisiones y plan aprobados por el usuario; implementación local y pruebas ejecutadas; aceptación final y PR pendientes. Factor Ámbar aprobado: 4/9.

## Criterios de aceptacion

- **AC-01** Dado destino no guardado; cuando guardar y recargar la pagina; entonces el ID sigue entre favoritos. Capa: browser.
- **AC-02** Dado destino guardado; cuando quitar favorito; entonces no aparece en modo solo favoritos. Capa: browser.
- **AC-03** Dado localStorage con JSON corrupto; cuando iniciar catalogo; entonces aplicacion utilizable y favoritos vacios. Capa: unit.
- **AC-04** Dado almacenamiento no disponible; cuando guardar favorito; entonces estado de sesion utilizable y aviso sin prometer persistencia. Capa: browser.
- **AC-05** Dado boton de favorito; cuando activar con teclado; entonces estado accesible refleja guardado o no guardado. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.

## Problema y decisiones aprobadas

El corazón anterior solo alternaba una clase CSS. S03 permite guardar destinos para volver a consultarlos al recargar el mismo origen del navegador, sin cuenta ni servidor. Solo favoritos se combina mediante AND con municipio, categoría y búsqueda; no reinicia esos filtros.

Se guarda {version:1,ids:[...]} bajo opita360:favorites:v1. Solo IDs numéricos enteros positivos seguros, únicos. Los IDs desconocidos se conservan pero no se muestran si no están en el catálogo. No hay sincronización inmediata entre pestañas ni entre dispositivos. No se guardan nombres de personas ni tokens.

La inicialización únicamente lee; nunca escribe ni borra datos. JSON corrupto/esquema inválido -> favoritos vacíos y aviso; el original permanece hasta una acción explícita del usuario. Un fallo al acceder, leer o escribir activa estado de sesión y aviso sin prometer persistencia. Solo se escribe la clave propia; nunca localStorage.clear().

El botón tiene nombre Guardar/Quitar y aria-pressed, funciona con Enter/Espacio. Si quitar un favorito elimina su tarjeta en Solo favoritos, el foco pasa a la casilla estable Solo favoritos. Si la tarjeta permanece, el foco permanece en el botón.

## Trazabilidad de los cinco criterios

AC-01/TC-003-01: persistencia ID 3 tras recarga y ausencia de escritura al inicializar; API y demo. AC-02/TC-003-02: quitar, comprobar desaparición y recarga, conservar otros filtros e IDs desconocidos. AC-03/TC-003-03: unidades y navegador con JSON corrupto, esquemas inválidos e IDs manipulados sin sobrescritura inicial. AC-04/TC-003-04: getter, lectura y escritura bloqueados, alternancia en sesión y aviso. AC-05/TC-003-05: Enter/Espacio, nombre, aria-pressed y foco mediante Chrome/CDP.

Pruebas: frontend/tests/favorites.test.js y harness/s03_browser.py. Resultados, fallos y limitaciones: docs/taller-6/s03-resultados.md. No se afirma auditoría WCAG integral, prueba humana con lector de pantalla ni revisión docente.

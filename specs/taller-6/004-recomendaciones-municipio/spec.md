# S04 / 004 — Recomendaciones restringidas por municipio

Estado: cinco criterios y plan aprobados por el usuario, Factor Ámbar 5/9. Implementación local con pruebas ejecutadas; aceptación humana final y PR pendientes. No incorpora S01–S03.

## Problema y alcance aprobado

El visitante necesita que su itinerario se limite al municipio elegido. Antes el formulario y la API seleccionaban por intereses, duración y presupuesto sin restricción territorial. S04 añade un campo opcional municipality y un selector propio del itinerario, independiente del filtro municipal del catálogo.

Campo omitido, null o texto vacío/espacios: sin restricción. Comparación sin mayúsculas ni espacios exteriores, conservando acentos; no hay búsqueda aproximada. Valor no textual: HTTP 422. Municipio desconocido: HTTP 200 con propuesta vacía. La UI representa Todos los municipios con valor vacío y omite el campo. La cadena literal Todos enviada directamente es un municipio desconocido, no un comodín de API.

## Requisitos funcionales y no funcionales

RF-01 Restringir candidatos antes de seleccionar por intereses y antes de recuperarse por falta de coincidencias. RF-02 No sustituir por destinos de otros municipios. RF-03 Conservar contrato anterior y política de presupuesto, incluida la primera parada que puede excederlo. RF-04 Aplicar la restricción también al modo demo y mostrar resultado vacío con mensaje claro. RF-05 Selector etiquetado y operable por teclado, sin alterar filtros del catálogo.

Datos en memoria; sin persistencia, autenticación, servicios de pago o dependencias nuevas. No cambiar CORS, reglas presupuestarias ni algoritmos ajenos. API y demo tenían reglas distintas y no se igualan incidentalmente. Una prueba TestClient no prueba despliegue; las evidencias distinguen API real, fixtures y demo.

## Cinco criterios verificables

- AC-01 / TC-004-01 (api): sin municipio, conservar campos/resultados del contrato anterior; null/vacío equivalentes y excepción presupuestaria existente preservada.
- AC-02 / TC-004-02 (api): Neiva devuelve solo destinos de Neiva, incluso con intereses sin coincidencias y recuperación dentro de candidatos locales.
- AC-03 / TC-004-03 (api): municipio sin destinos devuelve HTTP 200, itinerary=[], estimated_total=0 y remaining_budget=budget, sin sustitución territorial.
- AC-04 / TC-004-04 (browser): API bloqueada y Neiva seleccionada -> demo solo de Neiva; municipio sin candidatos -> lista vacía y aviso.
- AC-05 / TC-004-05 (browser): selector propio con nombre accesible y teclado; Neiva envía municipality=Neiva, Todos omite el campo, filtros del catálogo intactos.

## Implementación y pruebas

FastAPI: StrictStr opcional; normalización y restricción antes del algoritmo existente. React: tripMunicipality separado de municipality; helper puro recommendation-municipality.js y recorte del catálogo local antes de intereses/fallback. Resultado vacío visible con status.

Pruebas API: backend/tests/test_recommendation_municipality.py. Unidades: frontend/tests/recommendation-municipality.test.js. Navegador: harness/s04_browser.py con proxy exclusivo a FastAPI real y escenario offline; la opción desconocida se inyecta como fixture de desincronización, no se presenta como opción real del catálogo.

Resultados, errores y límites: docs/taller-6/s04-resultados.md. No se afirma revisión docente, WCAG integral ni aprobación humana final. Crear casos no ejecuta pruebas. La trazabilidad termina en el PR real cuando exista; no se inventa URL.

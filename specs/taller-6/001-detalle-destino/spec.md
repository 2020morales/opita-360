# S01 / 001 - Detalle accesible de destino

Estado: alcance y plan aprobados por el usuario; implementacion local con pruebas ejecutadas. Aceptacion final pendiente; PR no creado. S01 es el alias del proyecto para el ID 001 del arnes; no es una sexta especificacion.

## Problema y usuarios

El visitante puede filtrar tarjetas y leer un resumen, pero no abrir una ficha sin abandonar el catalogo. Necesita consultar los datos disponibles y regresar a sus filtros. Interesados: turistas, personas que navegan con teclado o tecnologias de asistencia, equipo frontend/backend y revisor de calidad.

## Evidencia de punto de partida y novedad

Revision estatica sobre f5c5fc928d4afe90601aad6eacfe28e78372988f: backend/app/main.py registra GET /, GET /api/destinations y POST /api/recommendations; no hay ruta de detalle por ID. frontend/src/main.jsx renderiza tarjetas, filtros y formulario; no contiene dialogo ni accion de detalle. El Taller 4 aporta filtro por municipio y el Taller 5 infraestructura de agentes; no se rehacen. Esta inspeccion no es una prueba funcional de ausencia en ejecucion.

## Alcance y requisitos funcionales

RF-01 Anadir GET /api/destinations/{destination_id}, parametro entero positivo, respuesta {"destination": objeto completo del catalogo}. ID no existente: 404 con detail="Destino no encontrado". Entrada no entera o no positiva: 422.
RF-02 Anadir boton Ver detalle con nombre del destino en cada tarjeta; ficha modal con nombre, municipio, categoria, descripcion, precio orientativo COP, duracion en dias y etiquetas. No inventar informacion turistica nueva.
RF-03 Gestionar carga, exito, ausencia, fallo de red y respuestas tardias. En modo demo utilizar el objeto local seleccionado; en fallo transitorio del detalle usar la copia del catalogo con aviso explicito. Un 404 no se oculta con fallback. Tiempo maximo de solicitud: 5 segundos; sin reintentos automaticos.
RF-04 Permitir apertura por teclado, foco contenido, cierre con Escape o Cerrar y restauracion del foco. Conservar filtros y evitar que solicitudes anteriores alteren otro detalle.

## Requisitos no funcionales y limites

RNF-01 Accesibilidad verificable: dialogo con nombre, teclado, fondo inerte, foco visible y contenido legible a 360x800 y 1280x800; no afirmar conformidad WCAG completa por una sola prueba.
RNF-02 Mantener respuestas de listado/recomendaciones y datos originales. No mutar catalogo ni introducir dependencias, servicios de pago o persistencia.
RNF-03 Renderizar texto con React; no usar HTML sin sanear ni construir URLs desde texto libre. Cancelar peticiones y descartar respuestas obsoletas al cerrar/cambiar destino.
RNF-04 Evidencias nuevas con comandos, resultado y alcance; no sobrescribir Talleres 4/5. Build no acredita accesibilidad ni contrato funcional.

Fuera de alcance: favoritos persistentes, nuevo filtro por costo, recomendaciones por municipio, exportacion, login, PostgreSQL, edicion de destinos, router y enlaces publicos de ficha. No cambiar politica de presupuesto de recomendaciones ni CORS.

## Criterios de aceptacion y trazabilidad

### AC-01 - TC-001-01 (api)

Dado catalogo actual con ID 1; cuando GET /api/destinations/1; entonces HTTP 200 y objeto destination identico al elemento id=1 del listado, con todos sus campos.

### AC-02 - TC-001-02 (api)

Dado catalogo sin ID 9999; cuando GET /api/destinations/9999; entonces HTTP 404 y JSON detail="Destino no encontrado", sin datos de otro destino.

### AC-03 - TC-001-03 (api)

Dado API disponible; cuando consultar /api/destinations/abc, /api/destinations/0 y /api/destinations/-1; entonces cada solicitud devuelve HTTP 422; listado y catalogo permanecen iguales.

### AC-04 - TC-001-04 (browser)

Dado catalogo cargado desde API y tarjeta id=1; cuando activar con Enter el boton Ver detalle de Desierto de la Tatacoa; entonces se solicita GET /api/destinations/1 y se abre un unico dialogo con nombre, municipio, categoria, descripcion, precio COP, duracion y etiquetas del destino devuelto.

### AC-05 - TC-001-05 (browser)

Dado dialogo abierto desde un boton visible; cuando recorrer controles con Tab y Shift+Tab y pulsar Escape; repetir cierre con boton Cerrar; entonces foco inicial en Cerrar, recorrido contenido en dialogo, fondo no interactivo y foco devuelto al boton de origen en ambos cierres; dialogo tiene nombre accesible igual al destino.

### AC-06 - TC-001-06 (browser)

Dado solicitudes a API bloqueadas antes de cargar la pagina y catalogo demo visible; cuando abrir detalle del destino id=1; entonces se muestran los campos del destino demo y aviso Modo demostracion; se puede cerrar y no se requiere conexion externa para el texto.

### AC-07 - TC-001-07 (browser)

Dado listado API cargado y respuesta de detalle falla con red, HTTP 500 o demora mayor a 5 segundos; cuando abrir detalle, probar cada fallo por separado; entonces carga se anuncia, peticion se cancela a los 5 segundos como maximo mas 1 segundo de tolerancia de prueba y se muestra la copia del destino seleccionado con aviso Datos del catalogo; detalle no disponible; cerrar sigue funcionando.

### AC-08 - TC-001-08 (browser)

Dado listado cargado y detalle devuelve HTTP 404; cuando abrir tarjeta cuyo detalle no existe; entonces se muestra Destino no encontrado sin sustituir por otro destino ni presentar copia como detalle vigente; boton Cerrar operativo.

### AC-09 - TC-001-09 (browser)

Dado detalle de A retrasado y listado con A y B; cuando abrir A, cerrar antes de respuesta, abrir B y finalmente completar respuesta de A; entonces dialogo conserva identidad y datos de B; respuesta obsoleta no reabre A ni sobrescribe B.

### AC-10 - TC-001-10 (browser)

Dado municipio Neiva, categoria Cultura y busqueda Malecon seleccionados; cuando abrir y cerrar detalle; repetir con viewport 360x800 y 1280x800; entonces filtros y tarjetas visibles se conservan; dialogo permite leer todos los campos mediante scroll sin desbordamiento horizontal; controles permanecen alcanzables por teclado.

## Pruebas previstas y condicion de cierre

AC-01/02/03: unittest y FastAPI TestClient en backend/tests/test_destination_detail.py (archivo futuro); igualdad con listado, errores y ausencia de mutacion. AC-04 a AC-10: navegador real automatizado con datos controlados/interceptacion mas recorrido humano de teclado; script futuro dedicado con salida nueva en docs/taller-6/ejecuciones/. AC-04 tambien requiere un recorrido con servidor FastAPI real: una respuesta interceptada no prueba integracion.

Regresion prevista: suites existentes de API, filtros y agentes, harness checks --scope all y build. Accesibilidad: arbol accesible, nombre, foco y recorrido; auditor automatico solo si ya esta disponible, con sus limites documentados. Cada caso debe enlazar archivo de prueba, comando, ejecucion y PR. El conversor genera disenos con not_implemented / not_run por contrato; no es el registro de ejecucion. Las pruebas reales se registran por separado en docs/taller-6/s01-resultados.md. Cierre exige aprobacion humana y criterios demostrados; un check de estructura no cierra S01.

## Implementacion local y evidencias

Endpoint en backend/app/main.py; dialogo en frontend/src/destination-detail.jsx e integracion en main.jsx. Contrato probado en backend/tests/test_destination_detail.py; AC-04..10 y regresion de navegador en harness/s01_browser.py. Ver docs/taller-6/s01-resultados.md para cantidades, comandos, fallos y limites. Browser usa proxy de prueba a FastAPI real por ocupacion del puerto 5173; no se cambio CORS. Aceptacion final, PR y merge siguen pendientes.

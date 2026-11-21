# Revision final de la base comun del Taller 6

Worktree: <WORKTREE_T6>. Rama: taller6/base-comun. Revision ejecutada el 17 de noviembre de 2026; tiempos UTC en resultados.json.

## Dictamen

La integracion esta lista tecnicamente para proponer su commit, con las advertencias documentadas. No se detectaron errores bloqueantes, conflictos pendientes ni perdidas de funcionalidad en el diff revisado. Esto no significa que el Taller 6 este completo. No se implementaron sus cinco funcionalidades.

La fusion previa sigue sin commit: HEAD es 8cce952 y MERGE_HEAD es 4a23215. No se inicio otra fusion. Las ramas main, taller4/completar-entrega y taller5/sistema-agentes mantienen sus commits originales; sus worktrees existentes siguen limpios.

## Revision de archivos

Las 31 rutas preparadas coinciden exactamente con las del commit 4a23215: tres modificadas (README.md, frontend/package.json, frontend/src/main.jsx) y 28 anadidas (26 de docs/taller-4, modulo del filtro y pruebas). Lista completa en verificacion-git.json. No hay diferencias sin preparar en archivos seguidos.

Los componentes del Taller 5 en agents/, backend/, docs/taller-5/ y .gitattributes coinciden con HEAD. La documentacion y evidencias del Taller 4 coinciden con su rama de origen. No se normalizaron sus logs.

## main.jsx

Frente al Taller 5, el diff solo anade la importacion de funciones del filtro y sustituye su implementacion interna por las funciones compartidas del Taller 4. Permanecen el catalogo demo, la URL y llamadas API, makeTrip, intereses, dias, presupuesto, respuestas, menu, mapa y tarjetas. Frente al Taller 4, el diff conserva las mejoras del Taller 5: estado y referencia accesibles del menu y etiqueta/valor del rango de dias. El nombre accesible del buscador existe en ambos.

La inspeccion estatica y las pruebas del alcance ejecutado no muestran una regresion. No se afirma una prueba exhaustiva de todos los recorridos de la aplicacion.

## Ejecuciones nuevas

- Agentes: 34 pruebas aprobadas.
- Backend con TestClient: 8 pruebas aprobadas.
- Frontend con node:test: 9 pruebas aprobadas.
- Build de produccion con Vite 8.3.5: codigo 0.
- Verificador de navegador: 24 comprobaciones aprobadas, codigo 0. Incluye API real, seis municipios, combinaciones, vacios, recuperacion, teclado, selector movil, demo y cambio de catalogo controlado. Tambien repite npm test y build; no se cuentan como pruebas unicas adicionales.

resultados.json contiene comandos completos, salidas y hashes. browser/resultados.json contiene los checks del navegador. Las capturas escritorio.png y movil.png de browser/ se inspeccionaron visualmente y el selector se ve legible.

Se ejecuto el verificador existente de docs/taller-4/verificar.py mediante browser-adapter.py, sin editar el original. El adaptador cambia solo el directorio de salida y el identificador de base historico; no modifica los checks. El adaptador resuelve las rutas desde su propia ubicacion y no necesita nombres de usuario ni rutas absolutas. Su hash y el del verificador original se registran en resultados.json.

El servidor de prueba permite 5174 solo en memoria, igual que el verificador heredado. El backend de produccion no cambio. El cambio de catalogo usa una respuesta controlada explicitamente, y las comprobaciones de API conectada usan FastAPI real. No equivale a probar CORS de produccion en 5173.

## Autenticidad y conservacion

Se cotejaron las cinco salidas guardadas de la integracion anterior con sus logs: coinciden y sus codigos son 0. Los hashes de fuentes de aquella ejecucion coinciden con el estado revisado. Los bytes de docs/taller-4, docs/taller-5, agents, backend y los informes anteriores no cambiaron durante esta revision. Esta correlacion y las ejecuciones nuevas respaldan los informes; no constituyen una firma externa de autoria.

## Advertencias y pruebas pendientes

- Starlette/HTTPX emite una advertencia de deprecacion.
- lucide-react emite dos advertencias sobre use client en el build.
- git diff --cached --check devuelve 2 por ocho espacios finales en dos logs historicos ANSI del Taller 4. Se conservan porque son evidencia original; no son un fallo de las pruebas ni un conflicto Git.
- No se ejecutaron inferencias LLM ni MCP real de nuevo. Las pruebas de agentes verifican contratos/politicas y usan mocks en algunos casos.
- No se realizo auditoria WCAG completa, lector de pantalla, cobertura medida, mutacion ni rendimiento.
- No se ejecuto el recorrido completo del planificador en navegador; sus contratos API estan cubiertos por TestClient y su implementacion frontend no cambio en la integracion.
- PostgreSQL sigue sin persistencia demostrada.

## Antes de autorizar el commit

Revisar la lista de 31 rutas y decidir incluir tambien los informes nuevos de docs/taller-6/integracion y docs/taller-6/revision-final, que siguen sin seguimiento. No se hizo git add, commit, push ni merge hacia main en esta revision. El estado de fusion pendiente procede de la integracion local previamente autorizada.

## Seleccion de evidencia para staging

Se seleccionan 9 de los 25 archivos nuevos: resultados.json y verificacion-git.json de la integracion inicial; este README, browser-adapter.py, resultados.json, verificacion-git.json, browser/resultados.json y las dos capturas de la revision final. Los 16 restantes se conservan localmente sin seguimiento, no se borran ni se incluyen en staging. Los JSON conservan los resultados y codigos de los comandos principales, con las rutas locales anonimizadas; el JSON de navegador conserva sus 24 comprobaciones. Los nombres de logs y rutas de workspace que aparecen en estos registros describen la ejecucion local original y no implican que todos esos archivos se publiquen. El README inicial se excluye porque describe logs que no se incluyen.

Los logs separados de comandos principales duplican las salidas del JSON. Los logs de arranque de Chrome/Vite y API son auxiliares. Las salidas de npm test y build invocadas de nuevo por el navegador no se cuentan como nuevos casos unicos. No se editan las salidas guardadas en los JSON para ocultar advertencias.

### Excepciones historicas autorizadas

El usuario autorizo conservar intactos dos pares identicos del Taller 4: evidencias/escritorio.png y historial/primera-ejecucion-navegador/escritorio.png; evidencias/intento-puerto-ocupado.json y historial/primera-ejecucion-navegador/intento-puerto-ocupado.json. Todas esas rutas son relativas a docs/taller-4/. Son excepciones de conservacion historica, no archivos nuevos duplicados de la seleccion del Taller 6.

Se aceptan exclusivamente los ocho espacios finales de las lineas 18, 20, 28 y 30 de docs/taller-4/evidencias/build.log y docs/taller-4/historial/primera-ejecucion-navegador/build.log. git diff --cached --check conserva codigo 2: NO es una verificacion aprobada. No se ocultan sus mensajes ni se normalizan los originales. Los logs nuevos de build quedan fuera de staging; las salidas reales y sus advertencias siguen disponibles dentro de resultados.json.

No se detectaron credenciales en los archivos seleccionados. Los informes nuevos preparados usan referencias genericas del entorno; el adaptador usa rutas relativas a su ubicacion. Las referencias e inventarios de hashes siguen describiendo el workspace de la ejecucion original, incluidos algunos archivos que se conservan solo localmente.

Archivos nuevos excluidos (relativos a la raiz del worktree):
- docs/taller-6/integracion/20261117T202613Z/README.md
- docs/taller-6/integracion/20261117T202613Z/agentes.log
- docs/taller-6/integracion/20261117T202613Z/backend.log
- docs/taller-6/integracion/20261117T202613Z/frontend-build.log
- docs/taller-6/integracion/20261117T202613Z/frontend.log
- docs/taller-6/integracion/20261117T202613Z/npm-ci.log
- docs/taller-6/revision-final/20261117T203627Z/agentes.log
- docs/taller-6/revision-final/20261117T203627Z/backend.log
- docs/taller-6/revision-final/20261117T203627Z/browser.log
- docs/taller-6/revision-final/20261117T203627Z/browser/api-server.log
- docs/taller-6/revision-final/20261117T203627Z/browser/build.log
- docs/taller-6/revision-final/20261117T203627Z/browser/chrome.log
- docs/taller-6/revision-final/20261117T203627Z/browser/unit.log
- docs/taller-6/revision-final/20261117T203627Z/browser/vite-server.log
- docs/taller-6/revision-final/20261117T203627Z/build.log
- docs/taller-6/revision-final/20261117T203627Z/frontend.log

Los siete textos nuevos se almacenan con LF en el indice de Git. Los JSON conservan fechas, resultados y cantidades; las referencias locales de stdout y stderr se anonimizan como se documenta en privacy_redaction. Los hashes de bytes del entorno registrado corresponden al workspace Windows de la ejecucion, no garantizan identidad de bytes al hacer checkout en otro sistema. No se cambian las reglas de whitespace ni los archivos historicos para ocultar advertencias.

## Privacidad de los informes nuevos

Los siete textos nuevos del staging fueron anonimizados despues de las ejecuciones. Las rutas locales se sustituyen por <WORKTREE_T6>, <WORKTREE_T4>, <REPO_ORIGINAL>, <PYTHON> o <NPM>. No se modifican fechas, cantidades, resultados ni conclusiones de las pruebas. No se volvieron a ejecutar pruebas para esta correccion de privacidad.

Los registros JSON se identifican como copias anonimizadas, no como salidas originales byte a byte. Los campos de hashes anteriores conservan los valores historicos registrados para los archivos sin anonimizar. No se recalculan para aparentar una nueva ejecucion. La seccion privacy_redaction documenta el hash anterior de cada informe y el hash actual del adaptador portatil; los hashes de informes anonimizados y del adaptador ya no tienen por que coincidir con los de la ejecucion original. Las salidas incrustadas conservan sus resultados, con las mismas sustituciones de rutas.

Las evidencias originales de los Talleres 4 y 5 no se editan. Pueden contener nombres o rutas del contexto historico: esta correccion de privacidad se limita a los informes nuevos que se publicarian con el Taller 6. Los 16 archivos excluidos siguen solo en el equipo local, fuera del staging, y pueden conservar rutas originales.

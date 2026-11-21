# Ensayo local de integración final — S01 a S05

## Alcance real y estado Git
Rama temporal taller6/integracion-final, base origin/main 0985273541e21579009cb6179546b9f3db845f7e. Cinco fusiones exclusivamente locales conservan los commits de S01–S05 como ancestros. HEAD de fusiones a353b2f; las correcciones del contexto, pruebas conjuntas, documentación y evidencias nuevas permanecen sin commit para revisión humana. No se hizo push, no se creó PR, no se fusionaron los PR de GitHub y no se modificó main ni las ramas originales.

[Plan aprobado y resoluciones](integracion-final-plan.md). La autorización permite ensayo local; no acredita aceptación final ni revisión docente.

## Resultados ejecutados
| Comprobación | Resultado | Evidencia |
|---|---|---|
| npm ci desde lockfile y caché, sin scripts ni descargas | Código 0 | [Instalación](ejecuciones/20261118T234610Z-90eedd8c/integration-npm-ci.json) |
| Primera regresión conjunta | Arnés: un fallo por contexto truncado; agentes/API/frontend/build: código 0 | [Fallo original](ejecuciones/20261118T234618Z-c2da049e/checks.json) |
| Regresión tras corregir selección de contexto | Cinco comandos código 0 | [Corrección](ejecuciones/20261118T234758Z-17dbcd9f/checks.json) |
| Regresión con manifiesto deduplicado y SDD consolidado, antes del ajuste de revisión | 41 arnés + 34 agentes + 22 API + 38 frontend = 135 pruebas aprobadas; build código 0 | [Snapshot final](ejecuciones/20261118T235714Z-4b8653be/checks.json) |
| Validación estructural SDD | Cinco specs aprobadas, 10/4/5/5/4 criterios; código 0 | Salida del comando harness validate registrada por el operador |
| Casos generados de las cinco specs | Conversor real, diseños no ejecutables ni resultados de pruebas | Cinco cases.json nuevos de 20261118T235714/235715 |
| Inventario de cinco roles | Ejecución real en modo inventory, no inferencia | [Inventario](ejecuciones/20261118T235716Z-c8ed9da9/review.json) |

Las 135 pruebas incluyen regresiones previas y dos métodos nuevos de integración API, además de la comprobación nueva del contexto integrado. No sumar suites de las cinco ramas como tests independientes. El validador usa la etiqueta structure_valid_not_implemented para describir alcance estructural; no demuestra ni niega funcionamiento turístico.

## Navegador real sobre la misma aplicación integrada
| Recorrido | Controles | Resultado | Evidencia |
|---|---:|---|---|
| S01 | 22 | Aprobado | [JSON](ejecuciones/20261118T235306Z-5f2c4412/s01-browser.json) |
| S02 | 18 | Aprobado | [JSON](ejecuciones/20261118T235310Z-92ba8f80/s02-browser.json) |
| S03 | 29 | Aprobado | [JSON](ejecuciones/20261118T235316Z-74d72740/s03-browser.json) |
| S04 | 15 | Aprobado | [JSON](ejecuciones/20261118T235321Z-dd70ba7a/s04-browser.json) |
| S05 | 14 | Aprobado | [JSON](ejecuciones/20261118T235328Z-4ff7433f/s05-browser.json) |
| Conjunto | 21 | Aprobado | [JSON](ejecuciones/20261118T235335Z-a537daa6/integration-browser.json) |

Total: 119 controles aprobados, no 119 criterios de aceptación distintos. Chrome headless/CDP; cada script usa servidores, perfil y temporales propios, verifica puertos libres y recoge solo procesos propios. Se ejecutaron secuencialmente: S04/S05 comparten puertos y todos usan API 8000. Los informes incluyen logs, snapshots, observaciones y resultados; no son respuestas de LLM simuladas.

La API real se accede por proxies Vite exclusivos de prueba; no se cambiaron CORS ni la URL de producción. Demo se provoca bloqueando peticiones. Municipio inexistente en UI usa una opción agregada explícitamente como fixture de desincronización; el contrato API se prueba directamente también. La denegación de localStorage se inyecta para comprobar recuperación, no describe un incidente espontáneo de producción. Los ensayos de errores/red/retardos de scripts individuales conservan sus fixtures declarados.

## Verificaciones cruzadas aprobadas
- S02+S03: costo inclusivo, municipio, categoría, búsqueda y Solo favoritos forman intersección. Retirar un favorito visible deja lista vacía y foco recuperado; storage conserva los restantes tras recargar.
- S01+S02+S03: detalle correcto de tarjeta filtrada/favorita, Escape y foco al origen, detalle demo del favorito conservado.
- S02+S03+S04: catálogo vacío por costo/filtros no restringe candidatos del planificador; municipio de la propuesta independiente del catálogo.
- S04+S05: descarga real de propuesta Neiva igual a la respuesta API, origen api; editar formulario no cambia el archivo; excepción histórica de presupuesto cero intacta y exportada sin recalcular.
- S04+S05: municipio sin destinos da itinerario vacío, cero estimado y presupuesto restante completo; JSON vacío válido, sin fallback territorial.
- S03+S04+S05: demo y almacenamiento bloqueado siguen permitiendo favoritos de sesión, planificación municipal y exportación con origen demo. Aviso explícito, sin prometer persistencia.
- Sin excepciones JavaScript no capturadas en el recorrido conjunto. No equivale a ausencia de avisos de consola ni auditoría WCAG completa.

## Conflictos y fallo corregido, sin alterar evidencias
S01 entró sin conflictos. S02/S03: seis rutas conflictivas cada una; S04/S05: ocho cada una. Los registros guardan salida Git y nombres exactos, no se presenta el primer intento conflictivo como merge exitoso:
- [S01](ejecuciones/20261118T233840Z-ccc1762e/integration-merge-001.json)
- [S02](ejecuciones/20261118T233841Z-c580f37a/integration-merge-002.json)
- [S03](ejecuciones/20261118T234106Z-6b5319c6/integration-merge-003.json)
- [S04](ejecuciones/20261118T234149Z-2c82cf23/integration-merge-004.json)
- [S05](ejecuciones/20261118T234258Z-925d236c/integration-merge-005.json)

Se resolvieron importaciones, estilos, filtros, makeTrip, documentación, listas de lectura y tests; se preservaron ambos lados necesarios. El fallo ejecutado de contexto recortaba catch por crecimiento de App. Se seleccionan bloques de recomendaciones/exportación/filtros/favoritos bajo el mismo presupuesto; no se amplió indiscriminadamente. La prueba de borrador conserva el fixture independiente de S01 y las pruebas de S03–S05 mantienen las correcciones de resumen y JavaScript. El manifiesto deduplica rutas y sustituye resúmenes históricos contradictorios por contexto integrado; no amplía herramientas ni habilita shell/escritura.

Los avisos LF/CRLF siguen visibles; git diff --check y git diff origin/main --check terminaron código 0, sin errores nuevos de espacios. Los avisos de dependencias TestClient/httpx y directivas use client de lucide-react no provocaron fallos; no se ocultaron ni se migraron dependencias incidentalmente. Excepciones históricas de formato se conservan con sus documentos originales, no se certifican como comprobaciones aprobadas.

## Protección y trazabilidad
[Baseline de hashes y referencias](ejecuciones/20261118T233840Z-36a8eb20/integration-baseline.json) y [auditoría posterior](ejecuciones/20261118T235850Z-a93abb2b/integration-final-audit.json): 86 archivos protegidos idénticos, main y ramas originales sin cambios, cinco cabezas originales ancestros de la integración. El código de aplicación de los seis recorridos coincide con el actual; el snapshot final de suites incluye correcciones y documentación consolidada.

Los 16 archivos excluidos del worktree anterior no se trasladaron ni se incorporaron. No se escriben resultados en docs/taller-4, docs/taller-5 ni agents/. Se preservan informes históricos de cada spec; sus antiguas afirmaciones de publicación pendiente se contextualizan mediante las actualizaciones SDD y este índice, no se cambian resultados ni hashes.

Los enlaces reales #5–#9 están en spec.json y actualizaciones pr.md/tasks.md. Siguen abiertos y no fusionados en main. No se inventa revisión docente, CI, datos persistidos en PostgreSQL ni resultados de producción.

## Uso real del arnés
Se leyeron y aplicaron brújula-semántica, opita-frontend y opita-backend, más instrucciones React/FastAPI originales. Se ejecutaron conversión de cinco specs, suites del operador e inventario. La revisión LLM/MCP conjunta se registra al terminar, con parciales si falla; no se anticipa aprobación. El CLI acepta un ID por revisión: S05 con contexto de integración no significa cinco revisiones nuevas. La implementación pertenece a Codex/operador, no a agentes locales con escritura ni a subagentes nativos del IDE.

## Pendientes de revisión humana
No hay fallos funcionales pendientes en las suites/navegadores finales; la revisión LLM/MCP se cierra aparte. Pendientes: inspección humana del diff y la aplicación, aceptación de la resolución de conflictos, lector de pantalla/WCAG completa, otros navegadores, CI remoto y tratamiento definitivo de advertencias de dependencias. La entrega del diplomado aún requiere integración autorizada en main, cierre de PR, Coeficiente Murciélago documentado, exposición y reflexiones personales auténticas. Ninguna de esas tareas se presenta como terminada por este ensayo.

## Incidente real de revisión LLM/MCP y corrección

[Intento conservado](ejecuciones/20261119T000250Z-bb1c2b2b/error.json): cuatro roles completados y dos sesiones MCP exitosas; seguridad fue rechazada por Wrong model or incomplete inference. El diagnóstico genérico no registra cuál de sus condiciones falló, por lo que no se atribuye retroactivamente a longitud ni a un modelo equivocado. No fue un TimeoutError: el worker falló dentro del tiempo y fue recogido por el padre. No se presenta este intento como revisión completa aprobada.

El código también mantenía una instrucción fija de revisar un BORRADOR. Se sustituyó por el estado declarado de la spec, distinguiendo diseños de casos, regresiones y pruebas nuevas. Se acotó la salida solicitada y se hicieron distintos los diagnósticos de modelo inesperado y respuesta incompleta, con metadatos limitados. Se mantiene qwen3.5:4b, límites de tiempo y máximo de 1000 tokens; no se descargan paquetes ni se habilitan permisos nuevos.

Dos pruebas puras de contrato verifican el prompt y esos diagnósticos. No simulan ni acreditan llamadas reales a un LLM. La regresión posterior tiene **137 pruebas aprobadas**: 43 arnés, 34 agentes, 22 backend, 38 frontend, más build código 0. Los seis recorridos de navegador siguen siendo aplicables porque no se cambió la aplicación turística ni sus pruebas de navegador al corregir el runtime.

[Última regresión](ejecuciones/20261119T001433Z-1a2dcb10/checks.json). La repetición real LLM/MCP se registra al terminar; no se anticipa su resultado.

## Segundo intento y límite total de contexto

[Segundo fallo íntegro](ejecuciones/20261119T002022Z-a6f1de0d/error.json): seguridad devuelve modelo correcto, done=true, done_reason=length y eval_count=104. Cuatro roles y ambas sesiones MCP habían terminado correctamente. Esto acredita respuesta incompleta; no acredita por sí solo una causa exacta del comportamiento del modelo ni modifica retrospectivamente el diagnóstico del primer fallo.

Se añadió un máximo de 16.000 caracteres para el payload JSON serializado enviado a cada etapa LLM. Se conservan especificación, hechos y resultados; se acotan fragmentos largos y se marca truncación. El contenido completo de los archivos MCP no se envía duplicado al modelo: se mantienen metadatos, hashes, igualdad y denegación de scope, y el informe MCP original conserva su resultado. Si los metadatos obligatorios exceden el máximo se rechaza, no se omiten silenciosamente.

El verificador de citas ahora contrasta contra los fragmentos efectivamente enviados tras la compactación. Una línea recortada no se valida aunque exista en el archivo completo. Esto no convierte la prosa del LLM en una prueba ni garantiza revisión exhaustiva de todo el código. La preselección por bloques y el límite global son controles distintos; el segundo puede acotar más los fragmentos y lo declara.

Tres pruebas nuevas verifican límite/no mutación/conservación de hechos, rechazo de metadatos excesivos y citas fuera del contexto enviado. La [última regresión](ejecuciones/20261119T002449Z-b39d6044/checks.json) aprobó **140 pruebas: 46 arnés, 34 agentes, 22 backend y 38 frontend**, además de build código 0. Los conteos 135 y 137 anteriores corresponden a etapas reales previas, no a fallos ocultos ni a pruebas adicionales independientes.

El [contexto anterior archivado](ejecuciones/20261119T002544Z-029fb09c/integration-context-history.json) conserva texto y hash del resumen usado antes de actualizarlo a los resultados finales. La repetición acotada final se registra al terminar. Modelo, tiempos, máximo de tokens, permisos y herramientas no se ampliaron.

## Resultado real de la revisión acotada

[Informe completo](ejecuciones/20261119T002956Z-5aab9623/review.json): cinco inferencias qwen3.5:4b y dos sesiones MCP reales, duración 251,828 s frente a límite 600 s. Las siete etapas terminaron con código 0. Payloads LLM observados: 8814, 15826, 15642, 15559 y 15646 caracteres, todos bajo 16000. MCP frontend/backend confirmaron contenido igual y rechazo fuera del scope. El cliente usó caché offline para los paquetes ya existentes; no se instalaron dependencias nuevas.

La ejecución utiliza el ID S05 con contexto integrado y fuentes de las cinco funcionalidades; no se presenta como cinco nuevas revisiones completas de specs diferentes. El operador sí ejecutó conversión y pruebas de las cinco. Los dos intentos anteriores permanecen como fallidos y sus parciales se conservan. El último éxito no demuestra por sí solo causalidad de rendimiento ni garantiza que no vuelva a fallar el modelo.

### Contraste de conclusiones del LLM
- Se descarta «no hay pruebas AC-02/03» y «solo 46 tests base»: la regresión ejecutó 46 arnés, 34 agentes, 22 API y 38 frontend. Los informes Chrome prueban igualdad del JSON con la propuesta y origin=demo con descarga real.
- Se descarta «serializeItinerary no inyecta origen»: el helper construye data con format_version, origin e itinerary; las unidades y los JSON descargados lo verifican.
- Se descarta «no se probó botón sin propuesta»: initial_export_disabled y disabled_during_new_generation pasaron en el recorrido S05 sobre la aplicación conjunta.
- Una cita literal verificada no verifica la interpretación del modelo. Se conservan afirmaciones incorrectas y textos incompletos, con aceptación humana pendiente. No se cambió la aplicación para satisfacer esas afirmaciones falsas.

Después solo se aclaró redacción de memoria/README; la regresión final se vuelve a registrar con esas versiones. No se modificó código turístico después de las seis ejecuciones de navegador.

## Dictamen del ensayo
Integración funcional apta para revisión humana local: las cinco funcionalidades conviven y sus pruebas conjuntas pasan. No autoriza publicar o fusionar. Main y las ramas originales permanecen intactas; 86 archivos protegidos idénticos por hash. Existen cinco commits locales de fusión; los ajustes finales y las evidencias nuevas quedan sin commit y sin staging para revisar.

Pendientes: revisión humana del diff y la prosa de agentes; autorización separada para guardar/publicar los ajustes y para fusionar los PR originales; CI remoto, auditoría WCAG completa/lector de pantalla, otros navegadores y aceptación docente. Coeficiente Murciélago sigue sin definición/puntuación acordada; exposición y reflexiones no forman parte de este ensayo. La entrega final todavía requiere las cinco specs y PR fusionados en main.

## Cierre final del ensayo

Último snapshot después de aclarar documentación: [140 pruebas y build aprobados](ejecuciones/20261119T003221Z-3c3c290e/checks.json). [Auditoría final](ejecuciones/20261119T003424Z-201b70f7/integration-ready-for-review.json): 86 protegidos idénticos, referencias originales intactas, cero conflictos sin resolver, staging vacío, búsqueda de patrones de secretos/rutas personales sin coincidencias y diff --check código 0. Se mantienen los avisos LF/CRLF. La búsqueda de patrones no sustituye una auditoría de seguridad exhaustiva.

El script de cierre guardó la auditoría, pero falló al construir el enlace por mezclar rutas absolutas y relativas. Se corrigió el enlace sin cambiar aplicación o pruebas; el incidente documental se conserva en un nuevo integration-report-link-incident.json. No se presenta ese intento como una ejecución completa aprobada.

Estado: **APTA PARA REVISIÓN HUMANA LOCAL**, sin aprobación automática de publicación o merge. La versión probada incluye los ajustes y evidencias sin commit; no debe confundirse con el HEAD de fusiones por sí solo. No se hizo push, no se creó PR nuevo y no se fusionaron los PR #5–#9.

## Verificación previa al commit local autorizado

El usuario autorizó guardar ajustes y evidencias solo en taller6/integracion-final. Se repitieron las suites completas y los seis recorridos de navegador: **140 pruebas, 119 controles y compilación aprobados**, sin fallos en esta repetición. [Resumen de esta ejecución](ejecuciones/20261119T004130Z-250fd99c/integration-precommit-summary.json). Los informes y estados sin commit de las secciones anteriores describen la fase histórica del ensayo. El identificador del commit se consulta en Git después de guardar; este apartado registra la comprobación previa, sin inventarlo.

Se conservó la revisión real anterior de cinco roles/dos MCP; no se volvió a invocar el modelo porque el código revisado no cambió. Persisten pendientes de aceptación humana, accesibilidad completa, compatibilidad fuera de Chrome, CI y autorización de publicación/fusión. Main, ramas originales y 86 protegidos continúan intactos. No se autoriza push ni PR nuevo.

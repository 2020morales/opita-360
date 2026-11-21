# S02 — Filtro por costo máximo: resultados reales

Rama: taller6/002-costo-maximo. Base: origin/main 0985273541e21579009cb6179546b9f3db845f7e, PR #4 integrado. Se aprobaron los cuatro criterios y Factor Ámbar 3/9. S01/PR #5 no está incorporada ni fusionada en esta rama.

## Implementación y alcance

parseMaxCost valida un límite finito no negativo y distingue vacío de cero. filterDestinations combina el límite inclusivo con municipio, categoría y búsqueda, sin mutar el catálogo. El formulario React aplica el límite al enviar; un valor inválido muestra error asociado al campo y mantiene el último límite válido. Quitar límite conserva los otros filtros. Se permiten decimales con punto y se rechazan coerciones como hexadecimales, exponentes, Infinity u objetos. El campo indica costo por destino; no modifica el presupuesto del itinerario.

No se cambió backend, API, CORS, dependencias ni persistencia. Se añadió un proxy exclusivo de prueba para Vite 5188 hacia FastAPI 8000; no es configuración de producción. El runner detiene la ejecución si los puertos están ocupados y limpia solo sus procesos.

## Ejecuciones auténticas

Ejecutar desde la raíz con un Python que tenga las dependencias ya existentes de backend y agentes. No se instalaron paquetes.

| Comando | Resultado | Evidencia |
|---|---|---|
| npm test (frontend), antes de implementar | 9 pruebas previas aprobadas y 1 fallo de carga del archivo nuevo: aún no existía parseMaxCost; las seis pruebas nuevas no llegaron a ejecutarse | [fallo inicial](ejecuciones/20261118T052418Z-52c1e515/s02-unit-before.json) |
| python -B -m harness cases --spec 002 | 4 diseños generados; execution=not_run, no prueba de ejecución de criterios | [casos](ejecuciones/20261118T052419Z-c6711f9a/cases.json) |
| python -B -m harness checks --scope all (primera implementación) | Cinco trabajos código 0 | [regresión inicial](ejecuciones/20261118T052526Z-03551682/checks.json) |
| python -B -m harness.s02_browser | 18 controles aprobados, Chrome headless; sin excepciones JS capturadas | [navegador](ejecuciones/20261118T052732Z-400db009/s02-browser.json) |
| python -B -m harness checks --scope all (estado final) | 36 arnés + 34 agentes + 8 API + 15 frontend = 93 pruebas aprobadas; build código 0 | [regresión final](ejecuciones/20261118T052855Z-fa1dc3d8/checks.json) |
| python -B -m harness review --spec 002 --approved | Cinco roles reales en inventory, sin inferencia ni MCP | [inventario](ejecuciones/20261118T052855Z-f60c1aa9/review.json) |
| python -B -m harness validate | Código 0; cinco specs estructuralmente válidas, S02 approved | Salida de terminal de esta sesión; no se presenta como un nuevo archivo de evidencia |

El fallo inicial se corrigió implementando el parser/export; no se simularon ejecuciones. El fallo de carga previo no equivale a seis aserciones fallidas ni a un historial de commits TDD completo. Se conservó la evidencia original. No aparecieron fallos en las ejecuciones finales.

Los seis archivos funcionales y de pruebas del navegador coinciden por SHA256 con su snapshot; los cambios posteriores fueron metadatos/documentación de S02, memoria y adaptación de la prueba de ciclo de vida. La regresión final sí incluye esos cambios. Las 93 pruebas y los 18 controles son medidas distintas, no 111 criterios independientes.

## Trazabilidad

| Criterio / caso | Prueba unitaria (frontend/tests/max-cost.test.js) | Navegador (harness/s02_browser.py) |
|---|---|---|
| AC-01 / TC-002-01 | maximum cost is inclusive | inclusive_boundary_35000; demo_inclusive_filter |
| AC-02 / TC-002-02 | empty maximum keeps all other filters; combinación AND | four_filters_AND; empty_preserves_other_filters |
| AC-03 / TC-002-03 | zero is a valid limit | zero_empty_and_recovery_message; recovery_preserves_municipality_search_category; demo_zero_empty; demo_recovery |
| AC-04 / TC-002-04 | parsing distinguishes empty/decimal/negative/nonnumeric | invalid_-1/abc/35abc_keeps_last_valid |

Extras: no mutación; etiqueta accesible en árbol AX; controles dentro de viewport 360/1280; Enter para aplicar; recomendaciones reales sin cambios; ausencia de excepciones JS capturadas. API/demo se verificaron por separado. El éxito API atraviesa el proxy hacia FastAPI real, no es una respuesta interceptada. El escenario offline bloquea la API y fotografías externas.

## Skills, agentes y calidad

Codex leyó y aplicó opita-frontend, brújula-semántica y las instrucciones originales frontend-react. Ejecutó el conversor cases, pruebas/build y el orquestador CLI. No se afirma activación automática en VS Code. El operador/Codex implementó los cambios; los roles Python son revisores, no programadores con shell.

Orquestador, frontend, backend, calidad y seguridad conservan write=false y shell=false, modelo configurado qwen3.5:4b local. Solo se añadió a la lista de lectura frontend la prueba unitaria S02. El test del arnés que exigía cinco drafts se ajustó para admitir el ciclo draft/approved, ya que S02 fue aprobada; no se relajaron los contratos de herramientas ni permisos.

Mecanismo 1: regresión y unidades deterministas con casos límite y no mutación. Mecanismo 2: navegador con API real/demo, validación y teclado. Revisión LLM complementaria ejecutada: cinco inferencias reales de qwen3.5:4b local en 369.078 s, dentro del límite 600 s; no sustituye pruebas ni aprobación humana. MCP no se ejecutó de nuevo en S02 y no se atribuye al PR una nueva sesión MCP.

## Riesgos y pendientes

Build aprobado con los avisos MODULE_LEVEL_DIRECTIVE ya conocidos de lucide-react. No se suprimieron. El diff puede emitir avisos de conversión LF/CRLF; no se han normalizado históricos ni alterado hashes originales. Ningún hallazgo de pruebas se corrigió borrando evidencia.

Pendientes: aceptación humana final, recorrido humano de accesibilidad/lector de pantalla, compatibilidad fuera de Chrome, CI y fórmula oficial del Coeficiente Murciélago. No se inventan métricas ni aprobación docente. La entrega Excelente exige además completar y fusionar las cinco specs con evidencia de uso del sistema; esta funcionalidad por sí sola no cumple todo el Taller 6.

S01 sigue en otra rama/PR. Si se integra antes de S02, revisar posibles cambios concurrentes en main.jsx, memoria/README y manifiesto; no resolverlos incorporando código ajeno sin revisión. No se ha hecho merge a main.

## Revisión LLM real y errores contrastados

Comando: `python -B -m harness review --spec 002 --approved --llm --checks docs/taller-6/ejecuciones/20261118T052855Z-fa1dc3d8/checks.json --max-seconds 600`.

[Informe original sin alterar](ejecuciones/20261118T053608Z-fa13e5e6/review.json): cinco inferencias, ocho afirmaciones catalogadas verificadas y dos contradichas (orquestador/seguridad negaron el registro de pruebas). Las dos se bloquearon en el contraste; cero citas suministradas. human_acceptance=false. Verificar metadatos no acredita por sí mismo cobertura; las pruebas reales se enlazan arriba.

| Afirmación del modelo | Contraste y decisión de Codex |
|---|---|
| Los casos nuevos no se ejecutaron | Incorrecto: seis pruebas unitarias nuevas y 18 controles browser están ejecutados en los informes. El conversor genera diseños not_run por contrato, no un registro de ejecución. |
| Hace falta max_cost en /api/recommendations | Fuera del alcance aprobado: S02 es filtrado local del catálogo, no presupuesto de itinerario ni API nueva. No se aplicó esa propuesta. |
| Un presupuesto cero del backend viola AC-03 | Confunde el presupuesto del viaje con el costo máximo por destino. La regresión conserva el contrato original; cero del filtro sí produce lista vacía en API/demo. |
| No hay mensajes/validación de cero o entrada inválida | Los controles zero_empty_and_recovery_message e invalid_-1/abc/35abc_keeps_last_valid pasaron; el código muestra recuperación y error asociado al campo. |

Limitación del arnés: test_design.execution permanece not_run porque describe diseños; no se inyecta el informe completo de navegador en el contexto LLM, y cada rol solo recibe archivos permitidos/acotados. La revisión automática no es integral y produjo conclusiones erróneas. Se conserva su salida, sin modificar evidencias ni cambiar funcionalidades ajenas para satisfacer al modelo. Mejorar la entrega del contexto de ejecución es un pendiente del arnés, no un resultado demostrado en esta spec.

## Revisión de alcance antes de publicar

[Auditoría local](ejecuciones/20261118T053255Z-b34d5821/s02-git-audit.json): snapshot de regresión vigente, backend/históricos sin cambios, 16 archivos excluidos y staging vacío en el momento de captura. La revisión de Codex del parser, la combinación AND, el estado aplicado y los mensajes no identificó un fallo funcional pendiente en los escenarios ejecutados.

La rama requiere aceptación humana final; no se atribuye una aprobación del profesor. La preparación/publicación del PR no autoriza fusionarlo. Si el conector GitHub devuelve 403, conservar ese bloqueo y facilitar el enlace de comparación sin inventar un PR.

## Publicación y bloqueo del PR

La implementación se guardó en el commit 53816ea978031ddb34bf5d8127b93c9146c16a1b y se publicó únicamente la rama taller6/002-costo-maximo. No se fusionó S01 ni se modificó main. La creación de un PR borrador por el conector devolvió HTTP 403, Resource not accessible by integration; no se inventa un número de PR. [Respuesta observada](ejecuciones/20261118T054205Z-81999358/s02-pr-create-error.json). La descripción preparada está en specs/taller-6/002-costo-maximo/pr.md.

[Comparación para crear el PR manualmente](https://github.com/2020morales/opita-360/compare/main...taller6/002-costo-maximo?expand=1). Se requiere permiso de escritura de Pull Requests para automatizar esa operación. Las actualizaciones posteriores al commit de implementación son documentales; no se presentan como nuevas ejecuciones de pruebas.

# S01 — Resultados de implementación local

Rama: taller6/001-detalle-destino. Base: f5c5fc928d4afe90601aad6eacfe28e78372988f. No hay commit, push, PR ni merge de S01. El alcance/plan fueron aprobados por el usuario; la aceptación final está pendiente.

## Qué se implementó

GET /api/destinations/{destination_id} devuelve {destination: objeto del catálogo}; entero positivo, 404 con mensaje explícito, 422 para entradas inválidas. No cambia listado, recomendaciones, datos ni CORS. React añade botón por tarjeta y diálogo nativo con datos del destino, foco inicial en Cerrar, fondo inerte, Escape y retorno del foco. Plazo de solicitud de 5000 ms, cancelación al cerrar y descarte de respuestas antiguas. Un 404 no muestra fallback; red/500/timeout usan copia señalada del catálogo. Demo usa el destino local y no depende de imágenes externas para leer la ficha.

No se añadió persistencia, router, paquetes, servicios externos ni las otras cuatro funcionalidades.

## Ejecuciones auténticas

Usar el entorno Python existente que contiene agents/requirements.txt y backend/requirements.txt; el Python global no contiene FastAPI. Los comandos se ejecutan desde la raíz del worktree.

| Comando | Resultado final | Evidencia |
|---|---|---|
| python -B -m harness checks --scope all | 36 arnés + 34 agentes + 12 API + 9 filtros = 91 pruebas aprobadas; build código 0 | [checks](ejecuciones/20261118T021523Z-1e06f9bf/checks.json) |
| python -B -m harness.s01_browser | 22 controles aprobados, sin excepciones JS capturadas | [navegador](ejecuciones/20261118T021329Z-040d3084/s01-browser.json) |
| python -B -m harness cases --spec 001 | 10 diseños generados; no ejecuta esos casos por sí mismo | [casos](ejecuciones/20261118T021524Z-0027f335/cases.json) |
| python -B -m harness review --spec 001 --approved | cinco roles en inventory, sin inferencia ni MCP | [inventario](ejecuciones/20261118T021524Z-1117ed32/review.json) |

Las 12 pruebas API son 8 previas y 4 métodos nuevos con subcasos; no se suman los subcasos como pruebas independientes. Las 91 pruebas y los 22 controles son mediciones distintas; no representan 113 criterios independientes. El build conserva avisos MODULE_LEVEL_DIRECTIVE de lucide-react; no se suprimieron ni se modificaron dependencias.

El navegador ejecutó Chrome/157.0.8103.38 headless. Se rechazó reutilizar 5173 ocupado por procesos ajenos y se ejecutó Vite propio en 5187, con proxy de pruebas a FastAPI real 8000. La ruta de producción y CORS permanecen iguales. El éxito de API y recomendaciones pasó por ese proxy hacia el servidor real; errores/red/retardo/404 se controlaron mediante fetch de prueba. No se afirma que se haya probado el servidor ajeno de 5173 ni el despliegue de producción.

Tiempo de cancelación observado: 5001.100000023842 ms (criterio: máximo 6000 ms incluida tolerancia de prueba). Se compararon hashes de los seis archivos funcionales/runner con el snapshot del navegador: coinciden. Cambios posteriores de memoria/metadatos y fixtures del arnés están cubiertos por la regresión final, no se presentan como otra ejecución de navegador.

## Trazabilidad de criterios

| Criterio / caso | Prueba implementada | Resultado |
|---|---|---|
| AC-01 / TC-001-01 | test_existing_destination_matches_every_catalogue_field | aprobado, todos los destinos del listado |
| AC-02 / TC-001-02 | test_missing_destination_has_no_fallback | aprobado |
| AC-03 / TC-001-03 | test_invalid_ids_are_rejected; invariancia del listado en tearDown | aprobado |
| AC-04 / TC-001-04 | real_api_detail_enter | aprobado |
| AC-05 / TC-001-05 | accessible_dialog_name, focus_initial_and_tab_trap, modal_background_inert, escape_restores_focus, close_button_restores_focus | aprobado |
| AC-06 / TC-001-06 | offline_demo_detail | aprobado |
| AC-07 / TC-001-07 | network/server/slow loading y fallback; deadline_aborts_request | aprobado |
| AC-08 / TC-001-08 | 404_no_catalogue_fallback | aprobado |
| AC-09 / TC-001-09 | late_response_does_not_overwrite_B | aprobado |
| AC-10 / TC-001-10 | responsive_360/1280; filters_preserved_360/1280 | aprobado |

API: backend/tests/test_destination_detail.py. Navegador: harness/s01_browser.py. Regresión adicional: existing_recommendations_real_api y no_runtime_exceptions. AC-10 combina Neiva, Cultura y Malecón. No hay prueba humana con lector de pantalla, auditoría WCAG completa, cobertura medida ni certificación docente.

## Fallos e incidentes conservados

1. [Primer intento API](ejecuciones/20261118T020436Z-02c2050a/s01-api-before.json): fallo de importación de FastAPI en Python global; no demuestra fallo funcional de S01. Se reutilizó el entorno existente, sin instalar paquetes.
2. [API antes de implementar](ejecuciones/20261118T020525Z-32bb1b21/s01-api-before.json): 4 métodos, 14 fallos de aserción contando subcasos; faltaba endpoint/contrato. Después pasaron los 4 métodos nuevos en la regresión final.
3. [Primera regresión](ejecuciones/20261118T020633Z-f220178e/checks.json): arnés 35/36, demás suites y build aprobados. La prueba exigía cinco drafts, incompatible con aprobación real de S01. Se adaptó al ciclo draft/approved; la prueba de grounding usa un fixture draft independiente.
4. [Navegador bloqueado](ejecuciones/20261118T020842Z-9382abfd/s01-browser.json): puerto ocupado, cero controles ejecutados. No se detuvieron servidores ajenos.
5. [Primer timeout CDP](ejecuciones/20261118T021012Z-f9b7c826/s01-browser.json) y [diagnóstico](ejecuciones/20261118T021111Z-e09396fb/s01-browser.json): catálogo real cargaba, pero Enter no activaba el botón desde el verificador. Se añadió text/unmodifiedText al evento Enter; la ejecución final pasó. No se atribuye este fallo del runner al producto.

Los fallos de codificación de la planificación anterior permanecen en s01-planificacion.md y sus ejecuciones. Nada se reescribió para convertir un fallo en éxito.

## Uso real de skills y agentes

Codex leyó y aplicó opita-frontend, opita-backend, brújula-semántica y las instrucciones originales React/FastAPI como procedimientos. El conversor cases se ejecutó realmente. El orquestador Python ejecutó inventario de los cinco roles; se ampliaron únicamente las lecturas frontend/backend para incluir el nuevo componente y su prueba API. write=false y shell=false permanecen. La implementación y los comandos de pruebas los realizó Codex/operador, no el modelo local. No se afirma activación automática en VS Code ni ejecución de subagentes nativos del IDE.

La revisión LLM local adicional terminó con cinco inferencias reales de qwen3.5:4b, en 429.938 s (límite 600 s). Ver contraste abajo; no sustituye las pruebas ni aprobación humana. MCP no se volvió a ejecutar en esta funcionalidad: las evidencias históricas de integración no se presentan como ejecución nueva.

## Calidad, seguridad y pendientes

Dos mecanismos ejecutados: (1) contratos API + regresión, (2) navegador con árbol accesible, teclado, fallos controlados y API real. Revisión estática de cambios por Codex: ID entero positivo; React renderiza texto; no se cambian CORS, catálogos ni política de recomendaciones; limpieza de peticiones y procesos propios del runner. No es auditoría externa. Coeficiente Murciélago sin fórmula oficial, no se inventa valor.

Pendientes: aceptación humana final, revisión visual/lector de pantalla si se exige, integración base común a main, CI, commit/push y PR aislado autorizados. Las otras cuatro specs siguen sin implementar. No hay bloqueo funcional conocido en los casos ejecutados; no se promete compatibilidad con navegadores no ensayados.

## Revisión LLM real y contraste posterior

Comando: `python -B -m harness review --spec 001 --approved --llm --checks docs/taller-6/ejecuciones/20261118T021523Z-1e06f9bf/checks.json --max-seconds 600`.

[Reporte original sin alterar](ejecuciones/20261118T022300Z-08efb205/review.json): cinco trazas de inferencia, sin MCP, diez afirmaciones del catálogo verificadas y dos citas inválidas/no suministradas; ninguna cita válida. La prosa permanece unverified_prose y human_acceptance=false. Cero contradicciones en los hechos estructurados NO significa que toda la prosa sea correcta.

| Hallazgo del modelo | Contraste con evidencia real | Decisión |
|---|---|---|
| El timeout debería ampliarse a seis segundos | AC-07 exige cancelar a cinco; un segundo es tolerancia del runner. Componente usa 5000 ms, navegador midió 5001.1 ms | Rechazado; no cambiar producto |
| No existen estilos de overflow | styles.css define overflow:auto, overflow-wrap:anywhere y límites de tamaño. responsive_360 y responsive_1280 pasaron | Rechazado |
| Cero/negativos podrían no devolver 422 | Path(gt=0) y test_invalid_ids_are_rejected pasan para abc/0/-1/1.5 | Rechazado |
| No se ejecutaron pruebas browser ni existen casos | Hay diez diseños, el runner y 22 controles pasados en el reporte enlazado | Afirmación incorrecta por contexto incompleto; no se presenta como resultado real |
| AC-04 no define la ubicación del botón | RF-02 lo sitúa en cada tarjeta y AC-04 parte de tarjeta id=1; real_api_detail_enter pasó | Rechazado |

Límite del arnés: entrega al LLM checks de regresión y diseños marcados not_run; no inyecta el informe completo de navegador. Calidad/seguridad tampoco reciben por lista permitida todos los archivos de UI/runner. Este contexto parcial no permite una revisión automática integral de S01. Se documenta como mejora pendiente del arnés; no se inventa que el modelo haya verificado el navegador. El contraste anterior fue realizado por Codex leyendo código y evidencias, no por un profesor ni por un revisor humano independiente.

## Archivos y estado final

Archivos versionados modificados: AGENTS.md; README.md; backend/app/main.py; frontend/src/main.jsx; frontend/src/styles.css; harness/README.md; harness/manifest.json; harness/tests/test_grounding.py; harness/tests/test_harness.py; los cinco artefactos SDD de specs/taller-6/001-detalle-destino/ (spec.md, spec.json, plan.md, tasks.md, pr.md).

Archivos nuevos funcionales/de pruebas: backend/tests/test_destination_detail.py; frontend/src/destination-detail.jsx; frontend/tests/s01.vite.config.mjs; harness/s01_browser.py. Documentación/evidencias nuevas en docs/taller-6/: este informe y ejecuciones enlazadas. Se conserva también la planificación previa, sin borrar sus fallos.

[Auditoría de Git y privacidad](ejecuciones/20261118T022122Z-4268dacc/s01-git-audit.json): staging vacío; cambios históricos protegidos ninguno; ramas main/Talleres 4/5/base-comun sin cambios; snapshot de checks vigente. diff --check terminó con código 0; persisten avisos LF→CRLF, no errores de espacios nuevos. Escaneo de patrones sin coincidencias de tokens o rutas personales en el ámbito revisado, sin afirmar garantía absoluta. Los 16 archivos previamente excluidos siguen sin seguimiento y fuera de staging.

S01 está implementada y comprobada en los escenarios descritos, pendiente de aceptación humana. No hay bloqueo funcional conocido; la revisión automática integral del navegador por LLM y la prueba humana con lector de pantalla no están demostradas. No se creó commit, PR, push ni merge.

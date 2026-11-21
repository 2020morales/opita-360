# S04 — Recomendaciones restringidas por municipio: resultados reales

Rama taller6/004-filtro-municipio, desde origin/main 0985273541e21579009cb6179546b9f3db845f7e. Cinco criterios y decisiones aprobados, Factor Ámbar 5/9. No incorpora S01–S03.

## Qué cambia

TripRequest admite municipality opcional StrictStr: omisión/null/vacío o espacios no restringen. Tipo no textual -> 422. Comparación sin mayúsculas y sin espacios exteriores de entrada, conservando acentos; no búsqueda aproximada. Se restringen candidatos antes de intereses y de la recuperación. Municipio sin candidatos -> HTTP 200, itinerary vacío, total 0, presupuesto restante completo y aviso; nunca se sustituye por otros municipios.

El formulario tiene selector propio tripMunicipality, separado del filtro municipal del catálogo. Todos los municipios omite el campo del payload. El modo demo restringe su catálogo antes de las reglas anteriores y conserva resultado vacío sin recurrir al catálogo global. Hay mensaje de recuperación visible para resultado vacío.

No cambian CORS, persistencia, dependencias ni ramas originales. La API conserva la excepción de primera parada por encima del presupuesto; la demo conserva su algoritmo anterior, no se pretende igualar incidentalmente sus políticas. Backend y frontend siguen usando datos en memoria.

## Ejecuciones auténticas y fallos

| Ejecución | Resultado real | Informe |
|---|---|---|
| API antes de implementar | Código 1, contrato territorial no implementado | [primera captura](ejecuciones/20261118T065054Z-68c1c156/s04-api-before.json) |
| API antes de implementar con captura UTF-8 | 8 métodos, 12 aserciones fallidas contando subcasos; no se confunden con 12 métodos | [captura UTF-8](ejecuciones/20261118T065355Z-c4ab7942/s04-api-before.json) |
| npm test antes de implementar | 9 pruebas previas aprobadas y fallo de carga del archivo nuevo por ausencia del helper; las cinco pruebas nuevas no llegaron a ejecutarse | [frontend inicial](ejecuciones/20261118T065356Z-c5d7b242/s04-frontend-before.json) |
| python -B -m harness cases --spec 004 | Cinco diseños generados, execution=not_run, no ejecución de criterios | [casos](ejecuciones/20261118T065054Z-8b5cb69f/cases.json) |
| python -B -m harness checks --scope all, primera implementación | API, agentes, frontend y build pasaron; arnés falló por exigir cinco drafts | [primera regresión](ejecuciones/20261118T065520Z-d78b42d0/checks.json) |
| python -B -m harness.s04_browser | 15 controles aprobados en Chrome headless | [navegador](ejecuciones/20261118T065921Z-77b06f39/s04-browser.json) |
| python -B -m harness checks --scope all, estado final | 37 arnés + 34 agentes + 16 API + 14 frontend = 101 aprobadas; build código 0 | [regresión final](ejecuciones/20261118T070153Z-d6638cd3/checks.json) |
| python -B -m harness review --spec 004 --approved | Cinco roles ejecutados en inventory, sin inferencia/MCP | [inventario](ejecuciones/20261118T070317Z-b86ca24f/review.json) |
| python -B -m harness validate | Código 0; cinco specs estructuralmente válidas; S04 approved | Salida real de terminal; no se inventa un archivo de evidencia adicional |

El primer script de captura se interrumpió al imprimir caracteres de stderr en consola Windows (UnicodeEncodeError). Ya había guardado el informe API; no llegó a ejecutar frontend. Se repitió la captura con PYTHONIOENCODING=utf-8 y salida de diagnóstico escapada; ambos informes se conservan. Este fallo de impresión no se presenta como un defecto adicional del producto ni como una prueba aprobada.

El fallo frontend se corrigió implementando el helper. Los fallos API se corrigieron con el campo validado y candidatos locales. La prueba del arnés que exigía cinco drafts se adaptó al ciclo draft/approved porque S04 fue aprobada. Además se corrigió el resumen fijo new_feature_tests=not_executed por estado indeterminado y se separó el diseño generado del registro de ejecución, con regresión nueva. No se incorporaron commits ni funcionalidades de S03 para hacerlo.

El build mantiene los avisos MODULE_LEVEL_DIRECTIVE conocidos de lucide-react; no se suprimieron. No se instalaron paquetes ni modelos. Las 101 pruebas y los 15 controles no equivalen a 116 criterios independientes.

## Trazabilidad y cobertura

| Criterio / caso | API/unidades | Navegador |
|---|---|---|
| AC-01 / TC-004-01 | legacy_contract_fixture, omitted_null_and_empty_are_equivalent, existing_first_stop_budget_exception_is_preserved | Todos_omits_field_and_preserves_legacy_result; existing_first_stop_budget_exception_kept |
| AC-02 / TC-004-02 | neiva_recovery_never_escapes_municipality; case_spaces_and_accents; helper de normalización | connected_Neiva_payload_and_restricted_recovery |
| AC-03 / TC-004-03 | unknown_municipality_is_empty_with_full_budget; no mutación del catálogo en tearDown | unknown_API_empty_no_fallback |
| AC-04 / TC-004-04 | unknown municipality never returns global fallback; helper no mutación | demo_Neiva_recovery_never_escapes; demo_unknown_empty_no_global_fallback; demo_Todos_recovers_legacy_flow |
| AC-05 / TC-004-05 | campo opcional en OpenAPI y rechazo de tipos no textuales | planner_selector_independent_of_catalogue; selector_has_accessible_name; selector_operable_with_keyboard; dos viewports |

API: backend/tests/test_recommendation_municipality.py, ocho métodos nuevos más ocho de regresión anterior. Frontend: frontend/tests/recommendation-municipality.test.js, cinco nuevas más nueve existentes. Navegador: harness/s04_browser.py. Los ocho archivos funcionales/de pruebas coinciden con el snapshot de navegador; cambios posteriores de memoria/SDD/arnés están cubiertos por la regresión final.

El navegador usa Vite 5190 con proxy exclusivo de pruebas a FastAPI real 8000, sin cambiar la URL de producción ni CORS. Los payloads se registran antes de enviar; no se interceptan respuestas exitosas. El caso de municipio desconocido inyecta una opción explícita de fixture para simular desincronización entre selector y catálogo; no es un municipio real presentado por el producto. El modo demo bloquea la API y fotografías externas. No es prueba de despliegue ni de disponibilidad real de imágenes.

## Skills y agentes

Codex leyó/aplicó opita-backend, opita-frontend y brújula-semántica, además de las instrucciones originales FastAPI/React. Ejecutó el conversor y el orquestador. No se afirma activación automática de skills ni registro nativo de subagentes del IDE. Codex/operador implementó y lanzó las pruebas; los roles solo revisan.

Orquestador y especialistas conservan write=false y shell=false, modelo qwen3.5:4b local. Se añadió lectura explícita de helper/pruebas S04 y [resumen del operador](s04-contexto-agentes.json) derivado de informes reales, no resultados inventados. La revisión LLM se registra al terminar; no se ejecutó una nueva sesión MCP.

Dos mecanismos aplicados: unidades/contratos/regresión y navegador con API real/demo, payloads, resultados vacíos y accesibilidad. La inferencia es complementaria; su prosa no se aprueba automáticamente. Coeficiente Murciélago pendiente de fórmula oficial; no se inventa puntuación.

## Límites y pendientes

Aceptación humana final, lector de pantalla humano, auditoría WCAG completa, compatibilidad fuera de Chrome, CI y revisión docente acreditada pendientes. Las cinco specs fusionadas y su evaluación conjunta siguen pendientes para el cierre completo del Taller 6.

Puede haber conflictos futuros en main.jsx, memoria y manifiesto al integrar las ramas paralelas. No se fusionan S01–S03 ni main durante este trabajo. Si main cambia, revisar el diff y las pruebas pertinentes antes de fusionar S04. Los históricos T4/T5 y los 16 archivos excluidos se conservan.

## Revisión LLM ejecutada y contraste del operador

[Informe íntegro](ejecuciones/20261118T070903Z-87e914db/review.json): cinco inferencias reales qwen3.5:4b, orquestador/frontend/backend/calidad/seguridad; sin MCP en esta sesión. El proceso terminó con código 0, pero eso no aprueba su prosa.

Se descartan las afirmaciones de ausencia de pruebas AC-02/AC-05: el informe de navegador registra recuperación Neiva, nombre accesible y teclado, y los tests API comprueban recuperación sin salir del municipio. Los cinco casos de diseño no tienen que igualar los 101 métodos de regresión ni los 15 controles del navegador. Se descartan las supuestas propiedades `municipio`/`politica_presupuestaria` sobrescritas: no corresponden al contrato real. El backend filtra candidatos antes de intereses y suma cero sobre itinerario vacío, contrario a las limitaciones del rol frontend. Calidad dejó una frase incompleta, conservada sin editar.

El auditor detecta citas inválidas y el hecho falso sobre validación Pydantic; la prosa libre conserva limitaciones y requiere revisión humana. El contexto acotado no proporciona a cada especialista todo el proyecto. No se presentan estos reportes como aprobación automática ni como prueba funcional. No se modificó código funcional tras el snapshot de las 101 pruebas y los 15 controles.

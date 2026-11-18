# S03 — Favoritos persistentes: resultados reales

Rama taller6/003-favoritos desde main 0985273541e21579009cb6179546b9f3db845f7e (PR #4 integrado). Cinco criterios, decisiones y Factor Ámbar 4/9 aprobados. No incorpora S01 ni S02.

## Implementación

frontend/src/favorites.js implementa lectura, escritura y alternancia con proveedor de almacenamiento inyectado. Clave propia opita360:favorites:v1; formato {version:1,ids:[...]}. Se aceptan IDs numéricos enteros positivos seguros, se eliminan duplicados y se conservan IDs desconocidos sin mostrarlos si no existen en el catálogo. No se almacena información personal ni objetos turísticos completos.

La inicialización lee pero nunca escribe, incluso con datos corruptos. Solo una acción del usuario puede sustituir el valor de la clave propia. No hay localStorage.clear ni borrado de otras claves. Si acceso/lectura/escritura fallan, la UI conserva estado en memoria, permite alternar favoritos y muestra aviso de sesión sin prometer persistencia.

React controla estado, clases y aria-pressed; se sustituyó la alternancia imperativa de CSS. Solo favoritos se combina con municipio, categoría y búsqueda; desactivarlo no reinicia esos filtros. Quitar una tarjeta visible en Solo favoritos mueve el foco a la casilla estable; fuera de ese modo el botón conserva foco. No se modifica backend, CORS, API, dependencias ni persistencia PostgreSQL.

## Ejecuciones reales

Comandos desde la raíz con Python que tenga las dependencias existentes de backend/agentes y frontend ya instalado. No se instalaron paquetes ni modelos.

| Comando | Resultado observado | Evidencia |
|---|---|---|
| npm test en frontend, antes de implementar | 9 pruebas anteriores pasaron; 1 fallo de carga porque no existía favorites.js. Las 10 nuevas no llegaron a ejecutarse | [fallo inicial](ejecuciones/20261118T055944Z-3a2f2972/s03-unit-before.json) |
| python -B -m harness cases --spec 003 | Cinco diseños generados, execution=not_run; no ejecuta los criterios | [casos](ejecuciones/20261118T055944Z-b67268ea/cases.json) |
| python -B -m harness checks --scope all (primera implementación) | Cinco trabajos código 0 | [primera regresión](ejecuciones/20261118T060731Z-30b39e75/checks.json) |
| python -B -m harness.s03_browser | 29 controles aprobados, Chrome headless | [navegador](ejecuciones/20261118T061049Z-9422d89f/s03-browser.json) |
| python -B -m harness checks --scope all (antes de corregir el contexto del arnés) | 36 arnés + 34 agentes + 8 backend + 19 frontend = 97 pruebas aprobadas; build código 0 | [regresión final](ejecuciones/20261118T061325Z-2d8514bb/checks.json) |
| python -B -m harness review --spec 003 --approved | Cinco roles en inventory, sin inferencia ni MCP | [inventario](ejecuciones/20261118T061326Z-3c91ab32/review.json) |

El fallo inicial se corrigió implementando el módulo; no se inventa una fase de diez aserciones fallidas ni un historial TDD ya publicado. Las ejecuciones finales no tuvieron fallos. Los 97 tests y los 29 controles son medidas distintas, no 126 criterios independientes.

Los seis archivos funcionales/runner coinciden por SHA256 con el snapshot de navegador. Los cambios posteriores de memoria, metadatos y contexto de revisión están cubiertos por la regresión final. El build mantiene los avisos MODULE_LEVEL_DIRECTIVE de lucide-react; no se suprimieron.

## Trazabilidad AC -> TC -> pruebas

| Criterio/caso | Pruebas unitarias | Controles de navegador |
|---|---|---|
| AC-01 / TC-003-01 | roundtrip; initialization never overwrites; missing value without write | save_ID3_only; reload_preserves_ID3_without_initial_write; existing_and_unknown_IDs_not_overwritten; demo_uses_same_favorite_IDs |
| AC-02 / TC-003-02 | toggles without mutating input or unknown IDs | remove_in_only_mode_moves_focus; removal_survives_reload; unknown_ID_retained_and_filters_unchanged; demo_remove_and_focus |
| AC-03 / TC-003-03 | corrupt JSON; invalid shapes/versions; manipulated IDs | corrupt_JSON_recovers_without_write; corrupt_storage_replaced_only_after_user_action; manipulated_IDs_safe_no_initial_overwrite; user_write_sanitizes_and_preserves_unknown_ID |
| AC-04 / TC-003-04 | getter/read exceptions; write failure | getterblocked/readblocked/writeblocked_session_toggle_and_notice y session_removal_works |
| AC-05 / TC-003-05 | lógica de alternancia sin mutación | Enter/Space_updates_accessible_state_and_keeps_focus; AX_toggle_button_name_and_pressed_state |

Unidades en frontend/tests/favorites.test.js; navegador en harness/s03_browser.py. También se comprobó combinación AND, recuperación de filtros al salir de Solo favoritos, clave ajena intacta, recomendaciones reales y ausencia de excepciones JS capturadas.

API real: Vite de prueba en 5189 usa proxy a FastAPI 8000. Los errores de almacenamiento se inyectan antes de arrancar React; no son fallos de un usuario real ni un despliegue de producción. API bloqueada y fotografías externas bloqueadas comprueban la lectura de favoritos en demo. No se reescriben evidencias de los Talleres 4 y 5.

## Uso real de skills y agentes

Codex leyó/aplicó opita-frontend, brújula-semántica y las instrucciones originales frontend-react. El conversor y el orquestador se ejecutaron realmente. Los revisores son roles Python, no subagentes nativos de VS Code; Codex/operador implementó y ejecutó los comandos. No se atribuye escritura al modelo.

Los cinco roles mantienen write=false y shell=false. Modelo local qwen3.5:4b; frontend puede leer helpers/pruebas S03 y los cinco roles reciben [resumen del operador](s03-contexto-agentes.json), derivado de informes realmente ejecutados y con hash del informe de navegador. Esto distingue los diseños not_run de las ejecuciones reales. El resumen no reemplaza todas las fuentes ni garantiza corrección semántica de cada respuesta. La revisión LLM y las correcciones de contexto se registran abajo; no se afirma una nueva ejecución MCP.

## Calidad, riesgos y límites

Dos mecanismos ejecutados: (1) unidades/contratos/regresión, (2) navegador con almacenamiento adverso, API/demo, teclado y árbol accesible. La inferencia será complementaria, no aprobación humana. Coeficiente Murciélago pendiente de fórmula oficial; no se inventan valores.

No se demuestra auditoría WCAG integral, sesión humana con lector de pantalla ni compatibilidad fuera de Chrome. La persistencia depende del origen (esquema/host/puerto) y perfil del navegador; no cruza dispositivos. No se sincronizan pestañas en vivo: última escritura puede prevalecer si se usan varias pestañas; fuera del alcance aprobado. Un fallo de escritura no borra el valor anterior: los cambios nuevos quedan en sesión.

Pendientes: aceptación humana final, revisión docente acreditada, CI y el cierre completo de las cinco specs para aspirar a Excelente. La publicación de esta rama no autoriza merge. Si main incorpora S01/S02 antes de S03, revisar cambios concurrentes en main.jsx y documentación; no resolverlos fusionando ramas por iniciativa del agente.

## Incidente real del arnés y correcciones verificadas

La [primera revisión LLM](ejecuciones/20261118T062001Z-fa218fec/review.json) completó cinco inferencias reales en 350.844 s. Registró ocho hechos catalogados verificados y dos contradichos; no suministró citas. Su prosa confundió diseños de casos con ejecuciones e indicó incorrectamente que faltaba recuperación de almacenamiento o que debía implementarse en backend. No se aplicaron esas propuestas al producto.

Al revisar la causa se encontraron dos defectos del contexto:

1. test_summary enviaba siempre new_feature_tests=not_executed. Se sustituyó por not_determined_by_suite_summary: un resumen de suites no prueba ni niega por sí mismo pruebas específicas. runtime diferencia ahora el diseño generado de un registro de ejecución.
2. Los archivos .js recibían solo 900 caracteres de contexto de documentos, omitiendo parte del catch y guardado. Se aplica el presupuesto de código existente de 4200 caracteres, con prueba que exige conservar los handlers de favoritos. No se ampliaron herramientas, escritura o shell.

Se añadieron dos regresiones del arnés. Se conserva la [ejecución intermedia de 98 pruebas](ejecuciones/20261118T062355Z-0c8be9aa/checks.json) y el [inventario intermedio](ejecuciones/20261118T062356Z-2cdd8484/review.json). La [regresión final tras ambas correcciones](ejecuciones/20261118T062600Z-10512263/checks.json) aprobó **99 pruebas: 38 arnés, 34 agentes, 8 API y 19 frontend**, más build código 0. El [inventario final](ejecuciones/20261118T062601Z-11597884/review.json) ejecutó los cinco roles.

El [contexto inicial preservado](ejecuciones/20261118T062630Z-cfa396d4/s03-context-before-correction.json) registra el contenido UTF-8 anterior y su SHA256; no se alteró el primer informe LLM. El contexto actual enlaza la regresión de 99 y el navegador de 29 controles. El código funcional y los seis archivos del navegador permanecen iguales al snapshot ensayado; las correcciones afectaron al arnés y su documentación. La nueva revisión LLM real se registra a continuación; las correcciones no eliminan todos los errores del modelo.

[Auditoría previa al cierre](ejecuciones/20261118T061812Z-abb8b6d1/s03-git-audit.json): conserva el estado comprobado antes de las dos correcciones del arnés. No se presenta su referencia de checks anterior como snapshot final.

## Revisión LLM posterior a la corrección

Comando: python -B -m harness review --spec 003 --approved --llm --checks docs/taller-6/ejecuciones/20261118T062600Z-10512263/checks.json --max-seconds 600.

[Segunda ronda real](ejecuciones/20261118T063221Z-91584bd8/review.json): cinco inferencias en 350.094 s. Nueve hechos catalogados verificados, uno contradicho (seguridad negó el registro de pruebas), una cita literal verificada al resumen permitido y una cita rechazada a un archivo no suministrado. Estos controles no validan toda la prosa; human_acceptance=false.

El orquestador reconoció ahora los resultados aportados. Otros roles mantuvieron errores: backend propuso exigir recuperación localStorage en FastAPI, frontend negó manejo de corrupción pese al helper, calidad/seguridad negaron pruebas específicas. Codex rechazó esos hallazgos contra loadFavorites/saveFavorites y los casos corrupt_JSON_recovers_without_write, getterblocked/readblocked/writeblocked y Enter/Space del informe real de navegador. No se alteró backend ni se ocultó el informe para satisfacer al modelo.

Se conservan ambas rondas de cinco inferencias y sus contextos; no se presenta la comparación como benchmark controlado ni como garantía de calidad general del modelo. La entrega de contexto mejoró datos concretos del arnés, pero la interpretación semántica de los hallazgos sigue requiriendo revisión. No hay revisión docente acreditada.

## Publicación y creación del PR

Implementación publicada únicamente en taller6/003-favoritos, commit 59c4c6f1e938444ab5d39e00314e07b82a83ae97. La creación de un PR borrador mediante el conector fue rechazada con HTTP 403; no se creó PR ni se fusionó ninguna rama. [Respuesta observada](ejecuciones/20261118T063536Z-63e76614/s03-pr-create-error.json). El bloqueo es el permiso de la integración para esa operación, no un fallo de pruebas.

[Crear PR manualmente](https://github.com/2020morales/opita-360/compare/main...taller6/003-favoritos?expand=1). Descripción lista para copiar en specs/taller-6/003-favoritos/pr.md. Esta actualización posterior es documental, no una nueva ejecución de pruebas; el código funcional probado permanece igual.

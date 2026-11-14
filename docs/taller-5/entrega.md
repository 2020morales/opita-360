# Taller 5 — OPITA 360

## 1. Proyecto y herramienta

OPITA 360 es una aplicación turística del Huila con React/Vite, lucide-react y FastAPI/Pydantic. Usa datos de demostración en memoria; el esquema PostgreSQL no está conectado. La asistencia de desarrollo se implementa en Python, con Ollama local (`qwen3.5:4b`) y un servidor MCP externo de archivos. La rama es `taller5/sistema-agentes`; las funcionalidades turísticas no se modifican y no se hacen commits ni push.

La especificación exige revisión limitada, evidencia auténtica y aprobación humana. El plan emite cuatro tareas especializadas con permisos fijos y los contratos vinculan reportes, archivos y hashes. La procedencia del plan es Codex; no se atribuye a Copilot un artefacto inexistente.

## 2. Sistema de agentes

El orquestador usa un LLM local para proponer un plan validado. Frontend (T03) revisa React, filtros, accesibilidad y fallback; backend (T04) revisa contratos y validaciones FastAPI. Ambos reciben código leído realmente por MCP desde copias temporales permitidas. Calidad (T05) revisa T03/T04 y checks vigentes del operador. Seguridad (T06) revisa reportes y políticas. Los cinco roles usan el mismo modelo con contextos separados.

La herramienta externa es `@modelcontextprotocol/server-filesystem@2.3.0`, por stdio con Node portátil 24.13.0. Se inicializa la sesión, descubren herramientas, lee y compara texto y verifica rechazo fuera del scope. Las escrituras anunciadas no se autorizan. Staging no equivale a aislamiento OS.

El operador autoriza la revisión y la ejecución registra ID, fecha, rama y huellas. Los límites de tamaño, delegaciones y reintentos de formato se aplican antes de aceptar resultados. El modelo no ejecuta shell, cambia permisos ni aplica parches. El cierre permanece en `awaiting_human_review`. Los diagramas Mermaid están en `arquitectura.md` y los diagramas vectoriales en el PDF.

El contexto adicional usa extractos de hasta 4000 caracteres por fuente; `context_receipts` los identifica y marca truncamientos. Los hashes de archivos son inventario del host, no prueba de lectura integral por el LLM. Los main llegan completos por MCP.

## 3. Calidad del código

Se prueban contratos, asignación tarea–agente, evidencia no vacía, duplicados, hashes, permisos y límites. Las pruebas HTTP del backend conservan su contrato actual. El operador ejecuta los comandos fijos de `agents.verify`; los modelos evalúan sus resultados, no afirman haberlos ejecutado. `agents.repro_frontend` instala y compila desde lockfile en copia temporal.

Los resultados concretos se consultan en `resultados.md`, `checks.json` y los artefactos asociados. Las trazas LLM y MCP deben proceder de ejecuciones reales. No se inventan inferencias, capturas, pruebas de navegador o persistencia. Compilar no prueba accesibilidad ni comportamiento visual; los hallazgos del LLM requieren revisión humana. El código conserva el modo de inventario determinista, que declara explícitamente ausencia de inferencia.

La comprobación actual pasó 27 pruebas de agentes y 8 de API (35 total), compilación backend y build frontend. Chrome real pasó 11/14 comprobaciones antes y 14/14 tras corregir etiquetas de búsqueda/días y estado ARIA del menú; browser/ contiene registros y PNG reales. Se probaron filtros, API, demostración, teclado, nombres accesibles y ancho móvil. No es una auditoría WCAG completa ni prueba de lector de pantalla.

La reproducción frontend desde lockfile fue anterior y no se repitió aquí. llm-report.json conserva cinco inferencias reales de qwen3.5:4b y dos MCP anteriores a la corrección de accesibilidad. El run c1e270f3-2bea-4727-ac59-21b6c530dbab se vincula a checks-llm-historical.json, conservado por hash; checks.json corresponde a las pruebas nuevas. No se afirma una nueva inferencia sobre la interfaz corregida.

La ejecución real no garantiza hallazgos correctos. Backend cuestionó validación presupuestaria que sí existe en Pydantic; calidad afirmó ausencia de pruebas dinámicas MCP aunque el ledger las acredita. T05/T06 no recibieron ese ledger explícitamente. El asistente contrastó las afirmaciones con las evidencias del host; estas opiniones no se presentan como conclusiones verificadas. revision-hallazgos.md registra las discrepancias y límites. La aceptación humana final sigue pendiente.

## 4. Diferencias con el sistema de referencia

El sistema de referencia no está disponible; el usuario autorizó continuar y dejar este criterio pendiente. No se inventan semejanzas o diferencias ni se afirma cumplimiento del 10 % correspondiente. Cuando se reciba, se compararán arquitectura, roles, modelos, permisos, MCP, flujo de aprobación y evidencia de calidad, citando fuentes concretas.

Como contraste interno verificable —distinto de esa comparación—, la versión previa inventariaba archivos con perfiles de modelo nulos. La corrección añade asignación de modelo local, flujo LLM especializado, contexto MCP entregado a especialistas, revisión de reportes previos, controles de contrato y trazabilidad. La ejecución efectiva de cada función se acredita únicamente con sus artefactos auténticos.

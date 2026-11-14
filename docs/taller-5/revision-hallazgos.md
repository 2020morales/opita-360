# Contraste de los hallazgos LLM con evidencia

Esta es una revisión del asistente basada en código y artefactos, **no una aprobación humana** ni una nueva ejecución LLM. La ejecución fue real; sus opiniones no se consideran automáticamente verdaderas. Se preserva `llm-report.json` sin editar sus respuestas.

| Afirmación del modelo | Contraste verificable | Tratamiento |
|---|---|---|
| T03: filtros y controles son correctos y accesibles | La ejecución posterior en Chrome encontró búsqueda sin etiqueta explícita, slider sin nombre accesible y menú sin aria-expanded. Se corrigieron y las mismas 14 comprobaciones pasaron. Algunas referencias de líneas del modelo eran inexactas. | La afirmación global del LLM era excesiva. Aprobados únicamente los escenarios probados; no es certificación WCAG ni prueba de lector de pantalla. |
| T04: falta validar límite máximo absoluto del presupuesto y duración | TripRequest usa budget ge=0/le=100000000 y days ge=1/le=14; test_invalid_requests_return_422 comprueba presupuestos fuera de rango y días inválidos; test_request_boundaries comprueba límites. El algoritmo limita número de paradas. | Rechazar la afirmación general de ausencia de validación. La viabilidad real del viaje sigue sin probarse. |
| T04: CORS permite métodos y headers globales | allow_methods/allow_headers contienen '*', pero allow_origins limita frontend local; ampliar métodos no equivale a permitir todo origen. | Observación parcial, no vulnerabilidad demostrada; no modificar CORS dentro del taller. |
| T05: faltan pruebas PostgreSQL | La aplicación usa memoria y PostgreSQL está fuera de esta entrega. | Límite real, no fallo de persistencia implementada ni requisito probado incumplido. |
| T05/T06: solo hubo pruebas estáticas, sin pruebas dinámicas MCP | checks registra unittest realmente ejecutado; llm-report.mcp registra dos inicializaciones/invocaciones externas y rechazos fuera de scope. | Contradicho por la evidencia del host. Calidad/seguridad recibieron checks y reportes, pero no el ledger MCP explícito; su revisión de esa integración es incompleta. |
| T06: staging no es sandbox OS y servidor anuncia escrituras | El servidor externo conserva permisos del usuario; el cliente solo autoriza lectura y las pruebas comprueban denegaciones. | Riesgo confirmado y documentado; no prometer aislamiento OS. |
| T06: aprobación previa del plan | --approved corresponde al alcance autorizado por el usuario; el registro declara generated_plan_reviewed_by_human=false. | No afirmar aprobación humana individual del plan producido por el modelo. Revisión final pendiente. |

Los fragmentos inconclusos del reporte backend, aunque cumplen JSON Schema, no son una explicación técnica suficiente. Una respuesta estructurada no garantiza calidad ni veracidad. No se introdujeron cambios turísticos basados en esas opiniones.

## Verificación posterior con navegador real

`agents.browser_checks` usa Chrome headless por CDP y los servidores reales Vite/FastAPI. No se instaló una dependencia en el frontend ni se usó axe. El árbol Accessibility de Chrome se consultó realmente; no es una inspección DOM presentada como prueba de lector de pantalla.

Evidencia: `browser/before.json` (11 de 14 aprobadas) y `browser/after.json` (14 de 14 aprobadas), con versión de Chrome, fecha, snapshot y observaciones. Las capturas before/after de escritorio y móvil son archivos PNG reales en esa carpeta. Los tres fallos iniciales están conservados.

Correcciones comprobadas en `frontend/src/main.jsx`:

- Búsqueda: nombre explícito mediante aria-label.
- Días: label asociado mediante htmlFor/id y aria-valuetext; el slider dejó de estar sin nombre en el árbol accesible.
- Menú móvil: aria-expanded, aria-controls y nombre Abrir/Cerrar coherente con su estado.

Se ejecutaron catálogo y recomendaciones contra API real, municipio, combinación vacía, recuperación y búsqueda combinada, selector con teclado, Tab, bloqueo de API para demostración y recomendaciones locales, menú móvil, ausencia de desbordamiento horizontal a 390 px, nombres accesibles y ausencia de excepciones JavaScript. El catálogo demo conserva ocho destinos. No se modificaron API, reglas presupuestarias ni datos turísticos.

La ejecución LLM previa se conserva sin alteraciones; sus fuentes eran anteriores a estas correcciones. `checks-llm-historical.json` conserva exactamente el hash de checks referenciado por llm-report. `checks.json` corresponde a las pruebas actuales. No se afirma una nueva inferencia sobre la interfaz corregida.

Pendientes: lectura humana con lector de pantalla, auditoría completa WCAG (incluidos contrastes y todas las interacciones), otros navegadores/dispositivos, revisión humana final y comparación con referencia. Calidad/seguridad LLM aún no recibieron explícitamente el ledger MCP en una nueva inferencia. No se simulan esas comprobaciones ni se calcula una nota.

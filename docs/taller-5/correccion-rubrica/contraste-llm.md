# Contraste del reporte LLM nuevo

Fuente intacta: `llm-report-03.json`. La ejecución completó cinco inferencias y dos
sesiones MCP. Contrato válido no significa dictamen correcto. Cierre auténtico:
`awaiting_human_findings_review`; aprobación humana final pendiente.

| Afirmación del modelo | Contraste verificable | Tratamiento |
|---|---|---|
| Frontend: selector de municipios sin id; frase incompleta | frontend/src/main.jsx:117 contiene id="municipality-filter" y htmlFor correspondiente; Chrome aprobó etiquetas y AX | Hallazgo no sustentado. No cambiar la interfaz para corregir una opinión falsa |
| Backend: no comprueba suma del presupuesto en varias iteraciones | backend/app/main.py:107 compara total + price con budget; permite primera parada sin itinerario | Generalización incorrecta. La excepción de primera parada está documentada por test_api.py:55–64; no corregir negocio fuera del alcance |
| Reportes no generados | El host creó cuatro reportes v1 y validate_report verificó las tareas y evidencias antes de guardar llm-report-03.json | La limitación del modelo no describe el resultado del controlador. No reescribir su respuesta |
| Intereses no validados contra base de datos | No existe base conectada; backend/tests/test_api.py:46 prueba fallback actual ante intereses desconocidos | Límite/diseño existente, no incumplimiento demostrado de un contrato nuevo |
| Sin persistencia PostgreSQL | backend/app/main.py usa datos en memoria; database/schema.sql no establece una conexión | Correcto como limitación, no prueba de persistencia fallida |
| Solo read_text_file y rechazo fuera del scope | Dos entradas mcp con content_equal=true y outside_scope_denied=true; recibos entregados a revisores | Comprobado; no equivale a sandbox OS |

Calidad detectó la inconsistencia del selector, pero no corrigió todas las opiniones
anteriores. El control humano sigue siendo necesario. Un mismo modelo con cinco
contextos puede repetir errores. Los tests TestClient son pruebas de API en proceso,
no mera inspección estática ni pruebas desplegadas de producción.

No se cambia código turístico ni se atribuye al profesor aceptación de este contraste.

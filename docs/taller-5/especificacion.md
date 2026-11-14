# Taller 5: especificación del sistema de agentes

Versión documental 2.0.0. Alcance de corrección autorizado. La evidencia de ejecución está en `resultados.md`, no se deduce de este diseño.

## Propósito y restricciones

Revisar OPITA 360 mediante orquestador y especialistas frontend, backend, calidad y seguridad. Se conservan funcionalidades turísticas, API, CORS, esquema SQL y datos en memoria. No se hacen commits ni push. React/Vite y FastAPI permanecen independientes del sistema de desarrollo; PostgreSQL no está conectado.

## Requisitos y aceptación

| ID | Requisito | Evidencia exigida |
|---|---|---|
| R1 | Modelos, roles, herramientas y permisos explícitos | Manifiesto validado con modelo concreto |
| R2 | Análisis especializado real | Entradas por rol y respuestas auténticas de Ollama |
| R3 | Orquestación verificable | Plan estructurado y T03/T04/T05/T06 con dependencias |
| R4 | Autorización y límites efectivos | Pruebas permitidas/denegadas por rol y herramienta |
| R5 | Reportes vinculados e íntegros | Rechazar tarea inexistente, agente incorrecto, evidencia vacía/duplicada y hash falso |
| R6 | MCP externo utilizado por especialistas | Inicialización, lectura real, comparación y contexto entregado a frontend/backend |
| R7 | Calidad y seguridad revisan entradas previas | T05 recibe T03/T04 y checks; T06 recibe reportes y políticas |
| R8 | Aprobación humana trazable | Identificador, fecha y huellas; cierre `awaiting_human_review` |
| R9 | Reproducción sin cambios turísticos | Pruebas y frontend instalado desde lockfile en copia temporal |
| R10 | Documentación coherente | Diagramas reales, tareas uniformes, PDF de hasta ocho páginas |
| R11 | Comparación con referencia | Fuente inspeccionada y diferencias respaldadas; pendiente |

## Modos y modelos

`--llm` usa Ollama local con `qwen3.5:4b` asignado al orquestador y los cuatro especialistas. Las llamadas usan contextos separados y salidas estructuradas. Si falta modelo, autorización o credencial, la ejecución se detiene sin respuestas prefijadas. El modo determinista sigue disponible para inventario y pruebas, con `llm_executed: false`.

## Secuencia

1. El operador define y aprueba alcance de revisión.
2. El orquestador solicita un plan LLM, lo valida y emite cuatro tareas con permisos fijos.
3. Frontend/backend reciben código autorizado mediante MCP y producen hallazgos.
4. Calidad contrasta T03/T04 con checks vigentes; seguridad revisa resultados anteriores y políticas.
5. El ejecutor valida límites, reportes y evidencias y entrega el informe a revisión humana.

Los contratos no conceden permisos. Los reintentos acotados corrigen formato, no código. Los hashes los genera el ejecutor; un modelo no puede suplir evidencias ni afirmar que ejecutó comandos. Las sugerencias requieren contraste humano y no se aplican automáticamente.

## Criterios académicos y pendientes

La ponderación y las cuatro secciones del documento están en `rubrica.md`. No se conoce el sistema de referencia y no se inventará su comparación. El usuario autorizó continuar con ese pendiente. Las pruebas no ejecutadas deben identificarse expresamente. No se incluyen persistencia, despliegue, commits o push.

# Revisión de hallazgos y aceptación pendiente

Este contraste lo realizó el asistente mediante código y registros; **no es aprobación humana**. Se preservan llm-report.json (histórico) y llm-report-final.json (nuevo) sin editar las respuestas del modelo.

## Correcciones comprobadas

| Hallazgo de auditoría | Corrección y evidencia |
|---|---|
| checks=[] podía iniciar el flujo | quality_gates exige los cuatro checks únicos, completos y vigentes; siete regresiones nuevas pasan |
| T05/T06 no recibían registro MCP | review_context entrega ambas verificaciones; context_receipts final contiene roles y hash del ledger |
| Diagrama mezclaba estructura y secuencia | PDF separa estrella centralizada con retornos y flujo secuencial fiel al controlador |
| PDF sin tabla completa, enlaces ni comparación | Siete páginas; cinco agentes con permisos/modelos; siete enlaces URI y referencias con SHA |
| Conversión LF/CRLF podía romper xref | *.pdf binary; atributos text/diff/merge desactivados y apertura estricta comprobada |
| Afirmaciones de inexistencia de commits/referencia | Se reconoce c72c3c9 y PR #2; comparación concreta en ramas pertinentes |

## Contraste de las respuestas LLM con hechos

| Afirmación u observación del modelo | Verificación del asistente | Tratamiento |
|---|---|---|
| Frontend final: contrastes adecuados | No se midieron contrastes ni WCAG completo; se probaron nombres accesibles y teclado | No aceptar como certificación de accesibilidad |
| Frontend final: fragmentos sobre role/listbox | La salida separa una frase inconclusa y listbox aunque cumple el esquema JSON. El select nativo ya tiene semántica; no justifica añadir ese rol | No aplicar cambio sin requisito ni prueba |
| Backend final: no existen pruebas ejecutadas | checks registra 8 pruebas TestClient; este ejecuta rutas y lógica de FastAPI. Además hay pruebas de navegador | Rechazar generalización; el agente no ejecutó personalmente los comandos |
| Calidad final: pruebas solo de estructura, sin ejecución de funciones turísticas | TestClient llama recomendaciones y comprueba totales; Chrome prueba API y demostración | No aceptar esa descripción global. No hubo carga ni estrés, límite real distinto |
| Históricos sobre falta de límites de presupuesto/días | TripRequest usa ge/le; 422 y límites están probados. El primer destino puede superar presupuesto por regla existente y hay regresión de ese caso | No modificar la regla turística ni afirmar ausencia general de validación |
| Final: MCP anuncia escrituras, cliente las deniega | La lista de herramientas incluye escritura; pruebas locales rechazan sus nombres. El servidor rechazó una lectura fuera del scope. No se intentó escribir contra el servidor | No presentar una escritura remota denegada como prueba ejecutada |
| Ausencia de PostgreSQL y de prueba de carga | Ambas son reales, pero persistencia está fuera de esta versión en memoria | Registrar como alcance/límite, no como fallo de una integración inexistente |
| Sandbox OS ausente | Node tiene permisos del usuario; listas y copia temporal no lo aíslan por sistema operativo | Riesgo reconocido; no prometer aislamiento fuerte |
| Plan aprobado | --approved confirma alcance autorizado; el registro declara generated_plan_reviewed_by_human=false | Mantener revisión humana final, sin firmas o aprobaciones ficticias |

## Navegador y evidencias históricas

El primer Chrome registró 11/14 y reprodujo tres fallos: etiqueta de búsqueda, nombre del slider de días y estado expandido del menú. Se corrigieron y se comprobó 14/14. La auditoría final repitió los 14 casos con código 0; JSON, snapshot y PNG actuales están en browser/.

Se archivó la evidencia anterior en history/pre-delivery-audit/, incluidos reportes narrativos. Los archivos históricos pueden decir que aún faltaban referencia o commits en aquella etapa: no describen la situación actual. Las inferencias anteriores no se usan para acreditar el código corregido; el nuevo run es fe8439a1-922d-42cd-aaaf-4010f589de64.

Pendientes: revisión humana de los hallazgos y de la entrega; lector de pantalla y auditoría WCAG completa; cobertura porcentual, carga, mutación y CI propio si se amplía el alcance. Las referencias ya se inspeccionaron, pero no se ejecutaron sus proyectos. No se calcula una nota automática.

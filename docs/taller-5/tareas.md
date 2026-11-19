# Taller 5: tareas y trazabilidad

Versión documental 2.0.0. T03–T06 corresponden a delegaciones ejecutables; los otros IDs identifican pasos del flujo. Los resultados y estados auténticos se consultan en `resultados.md` y artefactos asociados.

| ID | Responsable | Trabajo y entrada | Salida/control |
|---|---|---|---|
| T01 | Operador | Aprobar alcance y restricciones | Declaración ligada a ejecución y huellas |
| T02 | Orquestador LLM | Proponer plan estructurado | Cuatro roles obligatorios, sin ampliar permisos |
| T03 | Frontend LLM | Revisar React, filtros, API y fallback con contexto MCP | Reporte T03 y evidencia íntegra |
| T04 | Backend LLM | Revisar FastAPI, entradas, contratos y memoria con contexto MCP | Reporte T04 sin afirmar persistencia |
| T05 | Calidad LLM | Revisar T03/T04, checks vigentes y registro MCP | Hallazgos y límites; no atribuirse pruebas |
| T06 | Seguridad LLM | Revisar reportes, checks, MCP y políticas | Riesgos, sin ampliar permisos |
| T07 | Ejecutor MCP | Exportar, leer y cotejar archivo permitido | Lectura real y rechazo fuera del scope |
| T08 | Operador | Ejecutar pruebas fijas y frontend desde lockfile en copia | Fecha, comandos, códigos de salida y huellas |
| T09 | Ejecutor controlado | Validar reportes y reunir trazas | `awaiting_human_review` |
| T10 | Responsable humano | Revisar diff y limitaciones | Aceptar o pedir correcciones; sin publicación automática |

## Contratos

Cada tarea identifica agente, objetivo, archivos, herramientas y aceptación. La relación fija es T03–frontend, T04–backend, T05–calidad y T06–seguridad. Una respuesta LLM no puede añadir roles ni ampliar permisos.

`report.schema.v1.json` y la validación ejecutable definen versión, tarea, agente, estado, evidencia, hallazgos y limitaciones. El ejecutor verifica tarea emitida, agente, rutas, hash, tamaño y duplicados. `inspected` exige evidencia no vacía y no significa aprobación humana. Calidad debe recibir los reportes reales y checks correspondientes al snapshot; seguridad recibe reportes previos y políticas. Una validación estructural no prueba la veracidad semántica del hallazgo.

## Controles de calidad

1. Contrastar diff con requisito y rutas autorizadas, sin cambios turísticos.
2. Autorizar herramientas por rol y aplicar límites del manifiesto.
3. Ejecutar pruebas de comportamiento y rechazo de permisos con comandos fijos.
4. Verificar correspondencia entre checks y snapshot de código.
5. Instalar frontend desde lockfile en copia temporal y registrar errores auténticos.
6. Conservar respuestas reales de Ollama y MCP; no reemplazar fallos por simulaciones.
7. Entregar resultados y pendientes a revisión humana.

`max_correction_rounds` limita reintentos de formato, no edición autónoma. Las pruebas no equivalen a seguridad completa ni aceptación humana. La referencia ya se inspeccionó: `comparacion-referencia.md` distingue el patrón del profesor de esta adaptación. No se confunde esa comparación con el contraste interno frente al inventario previo.

## Correcciones de la auditoría de entrega

- La puerta exige las cuatro comprobaciones, nombres únicos, comandos/directorios correctos, salidas completas y snapshot vigente. Rechaza checks vacíos o incompletos.
- T05 y T06 reciben el registro MCP; context_receipts registra su hash y los roles recibidos.
- El PDF tiene tabla de cinco agentes, estructura centralizada, flujo real, comparación verificada, enlaces URI y código FET-QX7. Se protege de conversión de Git con `.gitattributes`.
- Existen commits y el PR #2; la aceptación y cualquier nueva publicación siguen siendo humanas.

## Tareas de corrección de rúbrica

- Tabla y modelos: manifiesto ampliado sin añadir herramientas ni roles ficticios.
- Puertas: resumen positivo y OK; identidad por contenido; hallazgos a revisión humana.
- Evidencia: destinos nuevos requeridos y rechazo de sobrescritura.
- Diagramas y matriz: frontend/backend, decisiones humanas, fallo y parada.
- PDF: ocho páginas, cuatro secciones y código en encabezado.
- Aclaraciones docentes y aceptación humana: pendientes; ver correccion-rubrica/plan.md.
- Resultados ejecutados: ver correccion-rubrica/informe.md; no equivalen a aceptación.

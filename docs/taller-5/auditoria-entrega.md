# Auditoría y corrección para entrega — FET-QX7

El usuario aprobó el plan completo antes de implementar. La rama sigue siendo taller5/sistema-agentes. No se hizo commit, push ni merge durante esta corrección. Hay commits previos y un PR abierto; no se presenta el repositorio como no publicado.

## Matriz de los seis criterios

| Criterio | Peso | Implementación y evidencia | Límite reconocido |
|---|---|---|---|
| Calidad | 25% | 34 pruebas agentes, 8 API, compileall, build, npm ci/build limpio, Chrome 14/14; puerta contra checks vacíos/parciales/falsos comandos | Sin cobertura porcentual, mutación, carga ni CI propios; JSON validado no es firma de ejecución |
| Agentes | 20% | Orquestador y cuatro especialistas con cinco inferencias reales en llm-report-final.json; T05/T06 reciben registro MCP | Tareas fijas y plan narrativo, no implementación autónoma ni convergencia |
| Diagramas | 20% | PDF: estrella centralizada con retornos; flujo con validaciones, MCP, revisores y cierre humano; Mermaid alineado | Describen revisión acotada, no todo el preset del profesor |
| Herramientas/permisos/modelos | 15% | Tabla de cinco roles, qwen3.5:4b local, autorización por rol y lista explícita, dos MCP reales, hashes de contexto | Sin benchmark de superioridad, sin sandbox OS y sin autenticación humana criptográfica |
| Diferencias | 10% | Ramas y commits inspeccionados en ambos repos; tabla y enlaces en comparacion-referencia.md y PDF | Configuración del profesor inspeccionada, no ejecutada |
| Documento | 10% | PDF de 7 páginas, 4 secciones, FET-QX7, tabla y diagramas vectoriales, 7 enlaces URI verificados, regla Git binary | Aceptación final del profesor/desarrollador pendiente; no se asigna nota |

## Fallos reproducidos y corregidos

1. El flujo aceptaba checks=[]: ahora exige cuatro nombres únicos, comandos/directorios previstos, código entero 0, salidas de texto, fecha con zona y snapshot exacto. Las siete regresiones nuevas se ejecutaron antes de existir el módulo (fallo de importación), y luego pasaron. No se atribuye un ciclo TDD completo a todo el repositorio.
2. Calidad/seguridad no recibían la evidencia MCP: ahora ambos contextos incluyen mcp_verifications y el recibo registra roles y hash del ledger.
3. La configuración mezclaba modelo asignado con executed=false: se retiró la bandera de configuración. El estado solo reside en la traza de cada ejecución.
4. El PDF contenía afirmaciones desactualizadas y no tenía anotaciones de enlace: se reconstruyó con datos actuales, comparación concreta y acciones /URI.
5. El PDF podía tratarse como texto en Git con core.autocrlf=true: *.pdf binary desactiva text/diff/merge. Se comprobó que conversión artificial a CRLF rompe xref; la protección impide esa conversión. No se afirmó haber probado un clon en otro equipo.

## Evidencia auténtica y conservación

- checks.json: comandos del operador y snapshot de las fuentes actuales.
- checks-llm-final.json: copia exacta del registro asociado a llm-report-final.json.
- llm-report-final.json: run fe8439a1-922d-42cd-aaaf-4010f589de64, respuestas originales y recibos de contexto.
- frontend-repro.json: instalación/build en copia temporal, Vite 8.3.5 del lockfile. El build instalado usa 8.3.8; no se oculta la diferencia.
- browser/after.json y PNG: pruebas reales actualizadas. Los before y after anteriores se conservan en history/pre-delivery-audit/.
- reference-evidence.json: ramas, SHA, fuentes y extractos inspeccionados por GitHub en modo lectura.
- pdf-validation.json: apertura estricta, renderizado de todas las páginas, código FET, anotaciones URI, verificación de destinos y hashes de documento/fuente.

Las inferencias nuevas siguen conteniendo fragmentos o interpretaciones equivocadas. revision-hallazgos.md los contrasta con evidencia; no se reescribieron para aparentar acierto. Se comprobó entrega del registro MCP a revisores, no infalibilidad de su análisis.

## Aprobaciones

--approved registra la declaración de alcance del operador. generated_plan_reviewed_by_human=false evita atribuir aprobación individual al plan narrativo generado. El resultado permanece awaiting_human_review. Publicar cambios, editar el PR o fusionar requiere la siguiente revisión humana; no se hizo en esta ejecución.

## Revisión local posterior de los seis criterios

La matriz anterior permanece como registro de su momento. La revisión vigente
se encuentra en [correccion-rubrica/informe.md](correccion-rubrica/informe.md).
No constituye aprobación del profesor ni publicación. La matriz ampliada de
riesgos, controles y límites está en [matriz-calidad.md](matriz-calidad.md).

## Mejora técnica posterior

Ver [informe vigente](mejora-tecnica/informe.md): nueva puerta conjunta, oráculos fijos y resultados propios.
Los resultados anteriores se conservan como antecedentes y no acreditan el código nuevo.

# Taller 5 — OPITA 360 · FET-QX7

## 1. Proyecto y herramienta

OPITA 360 usa React/Vite y FastAPI/Pydantic; PostgreSQL tiene un esquema, sin conexión persistente.
Un sistema común revisa ambos stacks sin cambiar las funcionalidades turísticas.
Codex se usó para elaborar el trabajo; Ollama local ejecuta qwen3.5:4b.
El profesor enumera Copilot VS Code, Claude Code u OpenCode: la aceptación de esta
alternativa sigue pendiente. Los permisos del controlador Python no son permisos nativos de esas herramientas.

El [repositorio](https://github.com/2020morales/opita-360) conserva la base 8cce952.
El [PR #2](https://github.com/2020morales/opita-360/pull/2) está fusionado según consulta GET registrada.
Esta corrección está en taller5/correccion-rubrica, todavía sin commit ni publicación.
No se acredita qué PDF fue adjuntado a Q10.

## 2. Sistema de agentes

El controlador emite cuatro tareas fijas; el LLM propone un plan narrativo.
No existe comunicación lateral ni selección libre de comandos o permisos.

| Agente | Invocación | Entrada | Salida | Herramientas Python | Motivo del modelo |
|---|---|---|---|---|---|
| orquestador | Al inicio; operador | Especificación y cuatro tareas fijas | Plan narrativo; controlador reúne informes | delegate, validate_report, llm_chat | Planificación acotada sin credenciales; no se midió superioridad |
| frontend | T03; controlador tras plan | Contexto React autorizado y main por MCP | Hallazgos y limitaciones React | read_context, llm_chat, external_mcp | Inspección local React; revisión humana compensa errores del modelo pequeño |
| backend | T04; controlador tras T03 | FastAPI/Pydantic, esquema sin conexión y main por MCP | Hallazgos y limitaciones API | read_context, llm_chat, external_mcp | Inspección local de contratos; pruebas TestClient contrastan opiniones |
| calidad | T05; controlador tras T04 | Informes T03/T04, checks y dos verificaciones MCP | Contraste de evidencias y carencias | read_context, llm_chat | Contexto de revisor separado; mismo modelo no garantiza independencia |
| seguridad | T06; controlador tras T05 | Políticas, informes previos, checks y registro MCP | Riesgos y límites; no aceptación | read_context, llm_chat | Revisión local sin salida remota; no sustituye auditoría de seguridad |

Todos usan ollama-local/qwen3.5:4b; perfiles planner/coder/reviewer no implican modelos diferentes.
Las rutas exactas están en manifest.v1.json y en el PDF. Denegado para todos:
escritura, shell libre, secretos, base de datos, commit, push y merge. Solo los dos
especialistas de stack reciben MCP. El cliente limita read_text_file; el servidor
filesystem 2.3.0 se ejecuta por stdio con Node portátil 24.13.0. No es sandbox OS.

Contrato: version, task_id, agent, status, evidence, findings y limitations.
Se comprueban tarea-agente, archivos autorizados, hashes/tamaños y duplicados.
El host inventaría archivos completos, pero context_receipts revela extractos
máximos de 4000 caracteres; main llega completo por MCP. No atribuir lectura total.

Los [diagramas de estructura y flujo](arquitectura.md) están también en el PDF.
G1 exige cuatro comprobaciones vigentes y suites positivas; G2 valida contratos y
MCP; G3 comprueba estabilidad. Fallo, timeout o intentos agotados detienen.
Hay como máximo dos correcciones de formato (tres intentos), sin autocorrección de código.
Todo hallazgo requiere revisión humana, fuera del ejecutor. --approved declara
alcance, no identidad ni aprobación del plan generado. No existe publicación automática.

## 3. Calidad del código

La [matriz de calidad](matriz-calidad.md) identifica problema, responsable, momento,
evidencia, bloqueo y límite para ambos stacks. Regresiones nuevas rechazan salidas
vacías/cero pruebas y separan procedencia Git de identidad por contenido.
`inspected` nunca significa aprobado: awaiting_human_findings_review mantiene
pendientes los hallazgos. El resumen de ejecuciones está en
[correccion-rubrica/informe.md](correccion-rubrica/informe.md).

Los informes históricos permanecen intactos. Las ejecuciones nuevas se guardan en
correccion-rubrica, incluyendo fallos. No hay cobertura medida, mutación, CI propio,
auditoría WCAG completa, lector de pantalla humano, todas las plataformas ni pruebas PostgreSQL.
Un JSON válido, hash o compilación no certifica corrección semántica. El escaneo
por patrones tampoco demuestra ausencia universal de secretos.

Pendientes del enunciado: aceptación de herramienta, cronista-lunar,
escritura-orbital, Pausa del Colibrí, ITC > 0,87 sin fórmula, MutaGato sin procedimiento
y aprobaciones/confirmaciones docentes. Proyecto Albatros se identifica como literal,
sin sustituir el proyecto. No se declaran cumplidos los requisitos ambiguos.
Esperamos que al profesor le guste este enfoque de calidad: expectativa, no aprobación.

## 4. Diferencias con el sistema de referencia

[Comparación detallada](comparacion-referencia.md). Backend: calidad-agentes en af004c4;
frontend: 001-project-baseline en 33161da, sin rama calidad-agentes identificada.
La inspección fue documental; no se ejecutaron aplicaciones ni pipelines del profesor.

- Se conserva Colmena Invertida para trazabilidad: todo retorna al centro.
- Roles de revisión frontend/backend/calidad/seguridad en vez de implementación
  architect/test-developer/developer/reviewer/spec-auditor: se revisa una aplicación existente.
- Qwen local sin edición frente a Opus/Sonnet con edit/execute: menor alcance y sin credenciales remotas.
- React/FastAPI en memoria frente a Angular/.NET/PostgreSQL: conservar tecnologías reales.
- Filesystem MCP de lectura frente a Context7/Angular CLI: contexto autorizado para el stack React.
- Tareas fijas y cierre humano frente a Red/Green y convergencia: no se atribuye automatización inexistente.
- Pruebas y Chrome sin cobertura medida frente a CI con umbral de cobertura: no copiar porcentajes sin medir.

La leyenda de verificación por el profesor queda pendiente, no se presenta como un hecho.

## Mejora técnica posterior

Ver [informe vigente](mejora-tecnica/informe.md): nueva puerta conjunta, oráculos fijos y resultados propios.
Los resultados anteriores se conservan como antecedentes y no acreditan el código nuevo.

# Comparación verificada — Colmena Invertida

Se inspeccionaron fuentes mediante GitHub en modo lectura. No se ejecutaron los proyectos del profesor, sus modelos ni sus pipelines. La denominación Colmena Invertida se contrasta con su [diagrama de orquestación](https://github.com/777wills/mi-restaurante-ms/blob/af004c49610dab2ab3a7a6bc0e6c8c22e357e2a5/docs/diagrams/03-patron-orquestador.excalidraw): centro de coordinación, contextos especializados, informes de retorno y ausencia de comunicación lateral.

## Ramas y versiones inspeccionadas

| Repositorio | Ramas listadas | Rama pertinente y commit |
|---|---|---|
| 777wills/mi-restaurante-ms | main; speckit-test; calidad-agentes | calidad-agentes: af004c49610dab2ab3a7a6bc0e6c8c22e357e2a5 |
| 777wills/mi-restaurante-ui | main; 001-project-baseline | 001-project-baseline: 33161da7c19bba7fdd995a502692ca5f69d67214 |

Los árboles inspeccionados de las otras ramas no contienen los mismos `.github/agents` y presets de orquestación. La UI main no representa la configuración especializada comparada. Los metadatos, SHA de blobs y extractos consultados se conservan en `reference-evidence.json`.

## Diferencias respaldadas por código

| Aspecto | Referencia del profesor | OPITA 360 | Decisión de adaptación |
|---|---|---|---|
| Centro de coordinación | Preset implement-orchestrator: solo coordina y edita tasks.md; no programa ni ejecuta pruebas del proyecto | Python controla cuatro delegaciones fijas; LLM propone plan narrativo y hallazgos | Revisión acotada de una app existente; no atribuir generación dinámica de tareas al modelo |
| Especialistas | architect, test-developer, developer, reviewer, spec-auditor | frontend, backend, calidad, seguridad | Separación por componentes React/FastAPI y revisión; no es copia funcional de todos los roles |
| Comunicación | Tareas e informes pasan por orquestador; subagentes no se invocan | Ejecutor entrega contexto y reportes anteriores; ninguna herramienta permite delegación lateral | Coincide el control central, con ejecución secuencial |
| Escrituras | Developer modifica producción; test-developer modifica pruebas; auditor solo añade tareas | Agentes sin herramienta de edición; implementación y comandos pertenecen al operador | Menor alcance y permisos; los modelos sugieren y no aplican cambios turísticos |
| Modelos | Agentes declaran Claude Opus 5.5 y Sonnet 5.5 en Copilot | qwen3.5:4b local en cinco contextos separados | Disponible en equipo, sin credenciales remotas; no hay benchmark que pruebe superioridad ni diversidad de modelos |
| Herramientas MCP | Agentes declaran Context7; UI configura angular-cli | Filesystem 2.3.0 por stdio, con Node portátil 24.13.0 | Contexto real de archivos locales en vez de documentación Angular; no se afirmó ejecución MCP del profesor |
| Calidad | Preset exige Red antes de Green, cobertura y convergencia; CI configura umbral 80%; backend incorpora mutación informativa | Unittest de contratos/permisos/API, build, navegador y revisión LLM; sin cobertura porcentual, mutación o CI propios | Diferencia explícita; cantidad de pruebas no equivale a 80% de cobertura |
| Cierre | Reviewer final y spec-auditor pueden producir nuevas tareas hasta converger | Awaiting_human_review; sin autocorrección de código ni publicación | Revisión humana fuera del ejecutor, con límites reconocidos |
| Stack y datos | Agentes backend describen .NET/EF Core/PostgreSQL; frontend Angular | React/Vite, FastAPI/Pydantic y catálogo en memoria | No incorporar persistencia ni infraestructura ajena al alcance turístico actual |

Fuentes primarias:

- [Preset backend, permisos y flujo](https://github.com/777wills/mi-restaurante-ms/blob/af004c49610dab2ab3a7a6bc0e6c8c22e357e2a5/speckit-custom/presets/implement-orchestrator/commands/speckit.implement.md).
- [Agentes backend](https://github.com/777wills/mi-restaurante-ms/tree/af004c49610dab2ab3a7a6bc0e6c8c22e357e2a5/.github/agents).
- [Agentes frontend](https://github.com/777wills/mi-restaurante-ui/tree/33161da7c19bba7fdd995a502692ca5f69d67214/.github/agents).
- [CI backend](https://github.com/777wills/mi-restaurante-ms/blob/af004c49610dab2ab3a7a6bc0e6c8c22e357e2a5/.github/workflows/ci.yml) y [CI frontend](https://github.com/777wills/mi-restaurante-ui/blob/33161da7c19bba7fdd995a502692ca5f69d67214/.github/workflows/ci.yml): configuración inspeccionada, no ejecución probada.
- [MCP frontend](https://github.com/777wills/mi-restaurante-ui/blob/33161da7c19bba7fdd995a502692ca5f69d67214/.mcp.json).

La comparación reemplaza el pendiente anterior de referencia desconocida. No permite calcular una nota sin una escala de evaluación del profesor.

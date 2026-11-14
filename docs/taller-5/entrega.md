# Taller 5 — OPITA 360 · FET-QX7

## 1. Proyecto y herramienta

OPITA 360 permite explorar destinos del Huila con React/Vite, lucide-react y FastAPI/Pydantic. Los datos están en memoria; PostgreSQL solo tiene un esquema preparado. El taller añade revisión asistida por agentes sin cambiar las funciones turísticas.

La herramienta de desarrollo fue Codex. Las inferencias reales usan Ollama local y qwen3.5:4b, elegido por disponibilidad en el equipo y ausencia de credenciales remotas, no por un benchmark de superioridad.

El [repositorio](https://github.com/2020morales/opita-360) contiene commits y el [PR #2](https://github.com/2020morales/opita-360/pull/2) está abierto y sin fusionar en la consulta. La base local es c72c3c9; esta corrección permanece local para revisión. No se publicaron cambios en esta ejecución.

## 2. Sistema de agentes

El controlador Python emite T03-T06 y restringe rutas, herramientas y secuencia. El LLM propone un plan narrativo y hallazgos; no elige permisos ni genera tareas nuevas. Los cinco roles usan el mismo modelo en contextos separados.

| Agente | Responsabilidad | Herramientas permitidas |
|---|---|---|
| Orquestador | Plan y coordinación controlada | delegate, validate_report, llm_chat |
| Frontend T03 | React, filtros, API, accesibilidad y demo | read_context, llm_chat, external_mcp |
| Backend T04 | FastAPI, contrato y validaciones | read_context, llm_chat, external_mcp |
| Calidad T05 | Reportes, checks y registro MCP | read_context, llm_chat |
| Seguridad T06 | Políticas, reportes, checks y registro MCP | read_context, llm_chat |

Las listas exactas de archivos están en agents/manifest.v1.json y el PDF las resume por rol. No hay edición, shell libre, secretos, base real ni herramientas de publicación. El cliente MCP solo autoriza read_text_file. Node conserva permisos del usuario: copia temporal no significa sandbox OS.

Filesystem 2.3.0 usa stdio y Node portátil 24.13.0. Frontend/backend reciben main completo por MCP y extractos adicionales de hasta 4000 caracteres, con recibos que identifican truncamientos. Calidad/seguridad reciben las dos verificaciones MCP y se registra el hash del contexto entregado.

--approved representa autorización de alcance, no identidad autenticada. El plan generado no tiene aprobación humana individual. El resultado queda awaiting_human_review; los modelos no aplican automáticamente sus propuestas. Los diagramas vectoriales y Mermaid muestran estructura centralizada y flujo secuencial, sin comunicación lateral.

## 3. Calidad del código

La auditoría corrigió dos defectos: aceptación de checks vacíos y ausencia del registro MCP en el contexto de revisores. La puerta exige cuatro resultados completos y vigentes con nombres únicos, comandos/directorios previstos, código entero 0, salidas y fecha con zona.

Pasaron **34 pruebas de agentes y 8 de API**, además de compileall y build. La reproducción limpia ejecutó npm ci y build con código 0, Vite 8.3.5. Chrome real pasó **14/14** comprobaciones de filtros, API, demostración, teclado, nombres accesibles y ancho móvil.

El reporte final registra **cinco inferencias reales y dos sesiones MCP**. Las huellas y recibos fueron contrastados; se conservaron respuestas originales aunque contengan errores. revision-hallazgos.md distingue opiniones del modelo de hechos comprobados por código y pruebas.

Los registros están en checks.json, frontend-repro.json, browser/after.json, llm-report-final.json y checks-llm-final.json. La evidencia anterior se archivó en history/pre-delivery-audit/. No se acredita cobertura 80%, mutation testing, CI propio o WCAG completo. La aceptación final sigue siendo humana.

## 4. Diferencias con el sistema de referencia

Se inspeccionaron las ramas disponibles. La comparación usa backend calidad-agentes (af004c4) y frontend 001-project-baseline (33161da); no se confundieron con main.

[La comparación y sus fuentes](comparacion-referencia.md) muestran que el profesor separa architect, test-developer, developer, reviewer y spec-auditor, con Red/Green y convergencia. OPITA adapta el centro de coordinación a cuatro especialistas de revisión, sin edición autónoma ni convergencia.

La referencia declara Opus/Sonnet en Copilot, Context7 y Angular CLI MCP; OPITA ejecuta Qwen local y filesystem. La CI del profesor configura umbral 80% y mutación backend informativa; OPITA tiene regresión y navegador sin esos controles implementados. No se ejecutaron sus proyectos, modelos ni pipelines.

El PDF tiene siete páginas, cuatro secciones, FET-QX7 y enlaces URI verificados. .gitattributes impide convertir los PDF con LF/CRLF. Su fuente real es generar_pdf.py, que lee evidencias; este Markdown resume la misma entrega.

# Arquitectura corregida — Taller 5

Cinco roles reales, Qwen local y herramientas propias del controlador Python.
Tabla de entradas/salidas y permisos exactos: `agents/manifest.v1.json`.
No son permisos nativos de Copilot; aceptación de herramienta pendiente.

## Estructura

```mermaid
flowchart TD
 H[Humano: alcance y aceptación] -->|Especificación| O[Orquestador LLM y controlador Python]
 O -->|T03 React, MCP y permisos frontend| F[Frontend]
 F -->|Informe T03| O
 O -->|T04 FastAPI, MCP y permisos backend| B[Backend]
 B -->|Informe T04| O
 O -->|T05 reportes, checks y registro MCP| Q[Calidad]
 Q -->|Informe T05| O
 O -->|T06 políticas, reportes, checks y MCP| S[Seguridad]
 S -->|Informe T06| O
 V[Operador: tests y build] -->|Resultados y hashes| O
 O -->|read_text_file| C[Cliente MCP]
 C -->|stdio| M[Filesystem externo: copia temporal]
 M -->|Texto y rechazo fuera de scope| C
 C -->|Contexto verificado| O
 O -->|Hallazgos y limitaciones| H
```

No existe comunicación lateral. El host controla secuencia, herramientas y contratos.
Solo frontend/backend reciben MCP; revisores reciben ambas verificaciones por el centro.
Las rutas permitidas son archivos exactos, no permisos recursivos de carpeta.

## Flujo

```mermaid
flowchart TD
 A{Humano autoriza alcance} -->|No| X[Detener]
 A -->|Sí| G{G1: cuatro checks, suites positivas, contenido vigente}
 G -->|Fallo| X
 G -->|Éxito| P[Plan LLM]
 P --> R{Formato válido}
 R -->|No y quedan intentos| C[Corrección de formato: máximo dos]
 C --> R
 R -->|No y agotados| X
 R -->|Sí| F[T03 y T04 secuenciales: MCP e inferencia]
 F --> M{G2: MCP y contratos correctos}
 M -->|No| X
 M -->|Sí| Q[T05 Calidad y T06 Seguridad]
 Q --> E{G3: código y checks estables}
 E -->|No| X
 E -->|Sí| D{Algún reporte blocked}
 D -->|Sí| X
 D -->|No| H[Revisión humana de hallazgos]
 H --> U{Decisión fuera del ejecutor}
 U -->|Rechazar| X
 U -->|Corregir| T[Operador corrige; nuevas pruebas e informe]
 T --> G
 U -->|Aceptar| Z[Autorización de lo revisado; no publicación automática]
```

Timeout, modelo ausente y denegaciones inesperadas detienen sin respuestas prefijadas.
El formato tiene tres intentos totales; no hay autocorrección de código turístico.
`--approved` declara alcance, no autentica identidad ni acepta el plan generado.
Los hallazgos cierran en awaiting_human_findings_review; inspected no significa aprobado.

## Límites

El cliente MCP limita read_text_file; servidor con escrituras anunciadas no usadas.
Node conserva permisos del usuario: no sandbox OS. Ollama solo en loopback fijo.
Extractos de 4000 caracteres, main completo por MCP y recibos de truncamiento.
Hash del host no demuestra comprensión del modelo. No persiste PostgreSQL.
Pendientes: cronista-lunar, Pausa del Colibrí, escritura-orbital, ITC/MutaGato y R-27.
No existe confirmación docente acreditada para los diagramas.

## Mejora técnica: cierre conjunto y propuesta documental

Puerta CLI implementada: `agents.release_gate`. Antes de presentar una revisión,
exige checks y 14 controles Chrome aprobados con el mismo SHA/mapa de archivos.
Rechaza un navegador incompleto, fallido o de otro contenido. La salida válida es
ready_for_human_review; no firma aceptación ni protege main en GitHub.

```mermaid
flowchart TD
 V[Suites, sintaxis y build] --> G{Checks y Chrome: mismo contenido y todos aprobados}
 B[Chrome: 14 controles] --> G
 G -->|No| X[Detener; conservar fallo; operador corrige y repite]
 G -->|Sí| H[Revisión humana de evidencia y hallazgos]
 H -->|Aceptar alcance| P[Publicación requiere autorización separada]
 H -->|Corregir| X
 H -->|Rechazar| Z[Detener]
 O[Orquestador] -.-> D[PROPUESTA: Pausa del Colibrí 7 s]
 D -.-> T[Antes de cada T03, T04, T05 y T06]
```

La pausa es diseño, no está ejecutada y no se acredita el beneficio descrito por
el enunciado. Modelos y permisos no cambian. Oráculos fijos complementan el
contrato API: ids [6,5], total 135000 y saldo 65000 para el caso aprobado existente.

# Taller 5 — resultados reales

## Verificación de navegador y accesibilidad — actualización posterior

En la rama `taller5/sistema-agentes` se ejecutó **Chrome/157.0.8103.38 headless real por CDP**, con Vite y FastAPI locales. Comando: `.\.venv-taller5\Scripts\python.exe -B -m agents.browser_checks --label before` y repetición con `--label after`. El navegador y los servidores se iniciaron con autorización del entorno; no se instalaron paquetes frontend. El runner usa websockets del entorno Python registrado.

**Antes: 11/14 aprobadas, código 1 por tres fallos. Después: 14/14 aprobadas, código 0.** Los fallos reproducidos y corregidos fueron búsqueda sin etiqueta explícita, selector de días sin nombre accesible y menú móvil sin aria-expanded. Se añadieron únicamente etiquetas y estado ARIA; no se cambiaron funcionalidades turísticas. Se corrigió también el uso de contexto del cliente websockets para retirar su advertencia de deprecación en el runner.

Evidencias auténticas: `browser/before.json`, `browser/after.json` y cuatro capturas PNG before/after de escritorio y móvil. Cada registro conserva observaciones, versión de navegador, fecha y snapshot. Se comprobó visualmente la captura móvil posterior. No se atribuye a estas pruebas una cobertura de contraste, lector de pantalla o conformidad WCAG completa.

Las 14 comprobaciones abarcan catálogo conectado (8 destinos), municipio Neiva (2), filtros combinados vacíos, recuperación/búsqueda, recomendaciones contra API real, etiquetas explícitas, nombres en Accessibility.getFullAXTree, selector con Home/ArrowDown, Tab, modo demo y recomendaciones con API bloqueada, menú móvil visible y aria-expanded, ancho sin desbordamiento a 390 px y ausencia de excepciones JavaScript. Escritorio: 1440×1000; móvil emulado: 390×844.

Después se ejecutó `agents.verify`: **27 pruebas de agentes y 8 de API aprobadas**, compileall y build frontend con código 0. Las advertencias de lucide-react y Starlette/HTTPX siguen documentadas. No se repitió la instalación limpia desde lockfile en esta actualización; `frontend-repro.json` acredita la ejecución anterior.

**Separación de evidencia histórica:** no se repitió LLM ni MCP en esta actualización. `llm-report.json` conserva sus cinco inferencias y dos sesiones de la versión anterior; su snapshot no representa la interfaz corregida. El archivo `checks-llm-historical.json` fue copiado byte por byte antes de regenerar checks y se comprobó que su SHA coincide con el referenciado por llm-report. `checks.json` contiene el snapshot actual. Los resultados anteriores que siguen deben leerse con esta distinción temporal.

Pendientes: lector de pantalla humano, auditoría WCAG completa, cobertura de otros navegadores/dispositivos, inferencia actualizada con ledger MCP para calidad/seguridad si se requiere, comparación con la referencia (no disponible) y aprobación humana final. No hay commits ni push.

## Ejecución LLM anterior a las correcciones de accesibilidad

Esta sección sustituye el estado funcional del registro histórico que sigue. La rúbrica y sus pesos están en `rubrica.md`, comunicados por el usuario. El sistema de referencia sigue sin estar disponible: su comparación (10 %) está pendiente y no se inventa ni se califica.

Implementado: modelos locales explícitos `ollama-local / qwen3.5:4b` para los cinco roles; contextos especializados; plan LLM; frontend y backend con código completo leído por MCP; calidad revisa reportes completos y checks; seguridad revisa reportes, permisos y políticas. Los permisos por herramienta y rol se aplican, las tareas son T03–T06 y los reportes rechazan tareas ajenas, evidencia vacía de inspected, duplicados, hashes falsos y cobertura incompleta.

La ejecución integral terminó con **código 0**, run `c1e270f3-2bea-4727-ac59-21b6c530dbab`, finalizada `2026-11-14T06:09:50.871213+00:00` (UTC). `llm-report.json` registra cinco llamadas reales a qwen3.5:4b: orquestador, frontend, backend, calidad y seguridad, todas en primer intento, con 271, 306, 170, 358 y 320 tokens evaluados respectivamente. Dos sesiones MCP verificaron lectura coincidente y rechazo fuera del scope. Los cuatro reportes validaron contra tareas emitidas; snapshot y SHA de checks coincidían al cierre de esa ejecución. Los checks originales están ahora en `checks-llm-historical.json`; no representan la interfaz posterior. No se usan respuestas simuladas para acreditar LLM.

El estado final es `awaiting_human_review`, no aprobación automática. Éxito de ejecución no implica exactitud semántica: `revision-hallazgos.md` contrasta afirmaciones incorrectas o no demostradas del modelo con evidencias auténticas. Las respuestas originales se conservan sin corregirlas artificialmente.

### Pruebas ya comprobadas en esta corrección

- `python -B -m agents.verify`: código 0. **27 pruebas de agentes y 8 de backend**, compileall y build frontend correctos. `checks.json` incorpora fecha UTC, rama, huellas de fuentes e instrucciones y salidas auténticas.
- `python -B -m agents.repro_frontend`: código 0 tras corregir la codificación de la salida de consola. `npm ci --ignore-scripts --no-audit --no-fund` y `npm run build` dieron 0 en copia temporal; Vite fue **8.3.5**, acorde al lockfile. `frontend-repro.json` conserva el hash del lockfile y logs. No se modificó el frontend original.
- PDF `taller5.pdf`: **4 páginas** y cuatro secciones, con diagramas vectoriales de estructura y flujo; extracción y recuento comprobados con pypdf.
- `git diff --check`: código 0. No hay cambios de código turístico, API, esquema ni dependencias de producción. No se hicieron commits ni push.

### Trazabilidad, aprobación y límites

El flujo exige checks del mismo snapshot; se compara código y bytes de checks al inicio y cierre. Las fuentes adicionales llegan como extractos de hasta 4000 caracteres: `context_receipts` registra truncamientos. Los hashes de evidence son inventario del host, no prueba de lectura integral del modelo. Los main de frontend y backend llegan completos por MCP.

La aprobación del alcance procede de la conversación y se confirma mediante `--approved`; el resultado liga especificación y plan por hash, registra que el plan generado no fue revisado individualmente por una persona y permanece `awaiting_human_review`. No es autenticación ni firma. No se generan o aplican cambios turísticos. El LLM puede errar: sus hallazgos no son hechos aceptados automáticamente.

### Incidencias reales de esta corrección

- El cambio a la rama solicitada necesitó permiso de escritura en `.git/index.lock`; se obtuvo y la rama actual se verificó.
- Un primer flujo falló al iniciar npx dentro del sandbox por timeout. No se contabiliza como ejecución integral aprobada.
- Una ejecución en curso se descartó al detectar que el inventario de fuentes no describía exactamente el contexto enviado. Se corrigieron recibos de contexto, snapshot de instrucciones y estabilidad de checks. Detener el proceso anterior necesitó autorización del entorno.
- La segunda invocación anterior no llegó a iniciar porque el archivo de salida seguía abierto por la ejecución descartada. Tras detener ese proceso se volvió a ejecutar con el archivo liberado; el resultado final anterior sí es la ejecución validada.
- Una reproducción frontend completó ci/build pero su impresión final falló por codificación cp1252; se corrigió la impresión ASCII y se repitió con código 0.
- Permanecen advertencias de lucide-react y deprecación de Starlette/HTTPX; no se cambió la aplicación para silenciarlas. En esa etapa todavía no había pruebas de navegador; se ejecutaron posteriormente, según la sección inicial. La aprobación humana final sigue pendiente.

### Reproducción

```powershell
# Entorno Windows registrado; las transitivas observadas están en python-lock.txt.
.\.venv-taller5\Scripts\python.exe -m pip install -r docs/taller-5/python-lock.txt
.\.venv-taller5\Scripts\python.exe -B -m agents.repro_frontend
.\.venv-taller5\Scripts\python.exe -B -m agents.verify
.\.venv-taller5\Scripts\python.exe -B -m agents.runtime --spec 'Revisar frontend y backend sin modificar funcionalidades turísticas' --approved --llm
python -B docs/taller-5/generar_pdf.py
```

Requiere Ollama en loopback con `qwen3.5:4b` instalado y paquetes MCP/Node autorizados. La generación usa temperatura 0, pero no se promete identidad textual entre inferencias. No hay credenciales externas ni fallback simulado. Node/MCP conservan permisos del usuario; staging no es sandbox OS. La fuente API utilizada es la documentación oficial de [Ollama chat](https://docs.ollama.com/api/chat) y [salida estructurada](https://docs.ollama.com/capabilities/structured-outputs).

## Registro histórico de la primera implementación (no describe el estado corregido)

Los nombres de artefactos citados en este registro correspondían a esa ejecución inicial. Los archivos actuales fueron regenerados y deben interpretarse mediante la sección de corrección y sus versiones, no como conservación inmutable de las salidas antiguas.

Fecha local: 2026-11-14. Rama observada al cierre: `taller-5-sistema-agentes`. Sin commits, push, despliegue ni PR. Los cambios de la aplicación turística y sus contratos se conservaron; se añadieron herramientas, pruebas y documentación del taller.

## Implementado

- `agents/manifest.v1.json`: orquestador y cuatro especialistas, perfiles de modelo sin proveedor, herramientas y permisos versionados.
- `agents/runtime.py`: aprobación explícita, especificación acotada, cuatro delegaciones, lectura por lista permitida, verificación de hashes y reportes estrictos. Con `--mcp`, integra las comprobaciones externas de frontend y backend.
- `agents/report.schema.v1.json`: contrato de reportes con JSON Schema. Las tareas incluyen archivos, herramientas y criterios de aceptación.
- `agents/mcp_probe.py`: cliente MCP por stdio para el servidor externo `@modelcontextprotocol/server-filesystem@2.3.0`, ejecutado mediante Node portátil `24.13.0`.
- `agents/verify.py`: comprobaciones fijas invocadas por el operador; no expone shell a los agentes.
- Pruebas unitarias de agentes/permisos y regresión HTTP de la API existente.
- Especificación, plan aprobado, tareas y diagramas de estructura y flujo en esta carpeta. Procedencia Codex, sin atribuir un plan ficticio a Copilot.

## Comandos y evidencia

Desde la raíz, usando el entorno `.venv-taller5`:

```powershell
python -m venv .venv-taller5
.\.venv-taller5\Scripts\python.exe -m pip install "mcp>=1.20,<2" -r backend/requirements.txt httpx
.\.venv-taller5\Scripts\python.exe -B -m agents.verify
.\.venv-taller5\Scripts\python.exe -B -m agents.runtime --spec 'Revisar frontend y backend sin cambios funcionales' --approved --mcp | Out-File -Encoding utf8 docs/taller-5/demo-report.json
git diff --check
git status --short
git branch --show-current
```

La instalación inicial resolvió MCP 1.30.0, HTTPX 0.28.1, JSONSchema 4.26.0, FastAPI 0.162.7, Pydantic 2.14.3 y Uvicorn 0.54.0. Las dependencias directas de herramientas quedaron fijadas en `agents/requirements.txt`; las transitivas no tienen lock completo. No se alteraron las dependencias de producción del backend.

| Comprobación | Resultado real | Evidencia |
|---|---|---|
| `python -B -m unittest discover -s agents/tests -v` | 19 pruebas, OK | `checks.json`, sección agents |
| `python -B -m unittest discover -s backend/tests -v` | 8 pruebas, OK | `checks.json`, sección backend |
| `python -m compileall app` desde backend | Código 0 | `checks.json`, backend_compile |
| `npm.cmd run build` desde frontend | Código 0 | `checks.json`, frontend_build |
| Orquestador integrado con MCP | Código 0; 4 reportes y 2 sesiones MCP | `demo-report.json` |
| `git diff --check` | Código 0 | Inspección de cierre |

`checks.json` contiene comandos, directorios, códigos de salida y stdout/stderr reales. El build utilizó Vite instalado 8.3.8; el lockfile declara 8.3.5. No se ejecutó `npm install` ni se cambió el lockfile para ocultar esa diferencia. Las pruebas backend usan TestClient en proceso: no prueban conectividad de red ni PostgreSQL.

## MCP comprobado

Para cada uno de los roles frontend y backend se ejecutó:

1. Verificación de Node portátil: `v24.13.0`.
2. Exportación de un archivo permitido a un directorio temporal.
3. Inicialización MCP, descubrimiento de herramientas e invocación de `read_text_file`.
4. Comparación exacta del texto con el archivo exportado, con resultado verdadero.
5. Petición de lectura al original fuera del contexto temporal, rechazada por el servidor.

El servidor se identificó como `secure-filesystem-server` 2.3.0; el protocolo negociado y hashes están registrados en `demo-report.json`. No se simuló la respuesta MCP. Las herramientas de escritura anunciadas no están autorizadas por el cliente. Las pruebas unitarias verifican su rechazo sin ejecutarlas.

## Incidencias y advertencias

- El primer intento de crear la rama no pudo escribir en `.git`; una solicitud de escalación devolvió rechazo. La inspección posterior confirmó que la rama actual es `taller-5-sistema-agentes`; no se atribuye a ese intento fallido su creación.
- La descarga pip dentro del sandbox falló por permisos de socket. Se volvió a ejecutar con autorización y las dependencias quedaron disponibles en el entorno virtual local.
- `npm.ps1` está bloqueado por la política de PowerShell. Se utilizó `npm.cmd`, sin cambiar esa política.
- Un build invocado inicialmente desde la raíz falló por ausencia del script; desde frontend pasó.
- Las primeras pruebas de agentes fallaron porque el archivo MCP aún no existía. Tras completar la implementación, las 19 pruebas finales pasaron.
- El servidor MCP 2.3.0 funcionó sobre Node 22, pero npm advirtió que exige Node 24. Se investigó la versión 2025.12.18: estaba deprecada y falló la comparación de contenido en esta máquina. Se descartó. La implementación final utiliza 2.3.0 y Node portátil 24.13.0 verificado; Node del sistema no se sustituyó. npm del sistema puede seguir advirtiendo durante la resolución inicial de paquetes desde Node 22.
- El build emite advertencias de directivas `use client` en lucide-react. TestClient emite deprecación de Starlette por usar HTTPX. Ambos terminaron correctamente; no se cambiaron dependencias ajenas al taller para silenciar advertencias.

## Límites pendientes

La coordinación implementada es determinista y los especialistas producen inventarios, no análisis semántico ni código autónomo. Los modelos figuran sin proveedor y `llm_executed: false`. No se ha conectado un LLM ni se afirma que los especialistas autónomos hayan sido probados. Las pruebas y revisión humana/IA del desarrollo son distintas del inventario que produce el ejecutor.

La validación de reportes coteja hashes con archivos actuales, pero no autentica autores ni firmas. `--approved` es una declaración del operador, no identidad verificada. El límite de correcciones es una reserva declarativa para una futura generación de código; no hay ciclo de autocorrección.

El proceso externo conserva permisos del usuario: lista permitida y staging no equivalen a sandbox OS ni a garantía frente a un servidor malicioso. No se conectó MCP al IDE ni se probaron APIs externas remotas, modelos, base real o despliegue.

No se ejecutaron pruebas de navegador, accesibilidad manual ni capturas. El frontend se compiló, pero eso no demuestra interacción visual correcta. La aceptación final y cualquier publicación corresponden a revisión humana. No se realizó commit ni push.

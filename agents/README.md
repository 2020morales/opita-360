# Sistema de agentes de desarrollo de OPITA 360

El modo `--llm` usa Ollama local y `qwen3.5:4b` para orquestador, frontend, backend, calidad y seguridad. El orquestador propone un plan estructurado; frontend/backend analizan código autorizado obtenido por MCP; calidad revisa sus reportes y checks vigentes; seguridad revisa políticas y resultados anteriores. Los roles tienen contextos separados sobre el mismo modelo, no diversidad de modelos. No reciben shell ni permisos de modificación turística.

El modo sin `--llm` conserva el inventario determinista: no es una inferencia. Solo los artefactos auténticos permiten afirmar ejecución; consultar `docs/taller-5/resultados.md`.

## Reproducción en PowerShell

Desde la raíz, con Python 3.10+, Node compatible con el lockfile y Ollama accesible en `http://127.0.0.1:11434`:

```powershell
python -m venv .venv-taller5
.\.venv-taller5\Scripts\python.exe -m pip install -r agents/requirements.txt -r backend/requirements.txt
ollama list
.\.venv-taller5\Scripts\python.exe -B -m unittest discover -s agents/tests -v
.\.venv-taller5\Scripts\python.exe -B -m unittest discover -s backend/tests -v
.\.venv-taller5\Scripts\python.exe -B -m agents.verify --output docs/taller-5/correccion-rubrica/checks-nuevo.json
.\.venv-taller5\Scripts\python.exe -B -m agents.repro_frontend --output docs/taller-5/correccion-rubrica/repro-nuevo.json
.\.venv-taller5\Scripts\python.exe -B -m agents.runtime --spec "Revisar frontend y backend sin modificar funciones turísticas" --approved --llm --checks-file docs/taller-5/correccion-rubrica/checks-nuevo.json | Out-File -Encoding utf8 docs/taller-5/correccion-rubrica/llm-nuevo.json
```

Si falta el modelo asignado, se detiene la ejecución sin descargarlo ni sustituirlo automáticamente. No se necesitan credenciales remotas para el servidor local. Un proveedor remoto o con coste requiere autorización nueva. `agents.verify` ejecuta comprobaciones fijas del operador, no comandos del modelo. `agents.repro_frontend` instala desde lockfile y compila en una copia temporal; no cambia el árbol turístico. Los errores deben quedar como fallos reales.

Para inventario y comprobación MCP independientes:

```powershell
.\.venv-taller5\Scripts\python.exe -B -m agents.runtime --spec "Inventariar contexto" --approved
.\.venv-taller5\Scripts\python.exe -B -m agents.mcp_probe --role frontend --approved
.\.venv-taller5\Scripts\python.exe -B -m agents.mcp_probe --role backend --approved
```

## Contratos y permisos

`manifest.v1.json` declara modelos, roles, herramientas, archivos y límites. T03–frontend, T04–backend, T05–calidad y T06–seguridad son las delegaciones. Los contratos exigen correspondencia tarea–agente y evidencia íntegra, no vacía para `inspected` ni duplicada. Los modelos producen hallazgos y limitaciones; el ejecutor genera hashes y agrega resultados reales. Las sugerencias no se aplican automáticamente.

MCP usa `npx --yes --package node@24.13.0 --package @modelcontextprotocol/server-filesystem@2.3.0 mcp-server-filesystem`. La primera ejecución descarga paquetes autorizados. Cada sesión exporta un archivo permitido, inicializa MCP, descubre herramientas, lee por `read_text_file`, coteja texto y verifica rechazo del original fuera del scope. Descubrir no autoriza: escrituras anunciadas no están permitidas por el cliente. El staging no es sandbox OS; el proceso conserva permisos del usuario. No se afirma conexión MCP con el IDE.

## Aprobación y evidencia

`--approved` expresa aprobación del operador. Se registran identificador, fecha, rama y huellas de especificación, plan y código; esto da trazabilidad, no autenticación humana. El cierre `awaiting_human_review` no acepta ni publica automáticamente. Los reintentos acotados por `max_correction_rounds` corrigen formato de respuesta, no código.

Código y respuestas son datos no confiables y no pueden modificar políticas. No hay herramientas de edición turística, shell libre, secretos, PostgreSQL, commit, push o despliegue. La rúbrica está en `docs/taller-5/rubrica.md`; la comparación verificada con el profesor está en `comparacion-referencia.md`. Los diagramas y el PDF se encuentran en esa carpeta. Las comprobaciones no ejecutadas no se presentan como aprobadas.

## Auditoría técnica pendiente de aceptación humana

Las referencias fueron inspeccionadas en `mi-restaurante-ms/calidad-agentes` y `mi-restaurante-ui/001-project-baseline`. Ver `docs/taller-5/comparacion-referencia.md` y `reference-evidence.json`. Existe el PR público #2 y commits previos; esta ejecución de corrección no publica cambios.

El flujo ahora exige las cuatro comprobaciones completas y vigentes de `agents.verify` (nombre único, comando, directorio, código y salidas). Un registro vacío o incompleto se rechaza. Calidad y seguridad reciben `mcp_verifications` y el reporte registra el hash y roles de ese contexto. La configuración del modelo no contiene estado histórico `executed`: ese dato solo aparece en las trazas de cada ejecución. No se comparó rendimiento de modelos; Qwen se eligió por disponibilidad local, ausencia de credenciales remotas y ejecución comprobable.

Antes de repetir una ejecución, conservar su JSON y los checks asociados. El PDF se genera desde `docs/taller-5/generar_pdf.py`; `*.pdf binary` en `.gitattributes` evita conversión LF/CRLF. Los enlaces `/URI` del documento deben comprobarse junto con su apertura y renderizado. El contexto MCP es de solo lectura para este cliente; Node sigue sin sandbox OS.

## Corrección de rúbrica (rama independiente)

`verify` y `repro_frontend` requieren `--output`; navegador requiere `--output-dir`.
Rechazan destinos existentes. Usar un nombre nuevo por ejecución, nunca reemplazar
los informes históricos. Ejemplo de navegador:

```powershell
.\.venv-taller5\Scripts\python.exe -B -m agents.browser_checks --label after --output-dir docs/taller-5/correccion-rubrica/browser-nuevo
```

La puerta compara SHA y mapa de archivos; rama y commit quedan como procedencia,
no invalidan contenido idéntico. Las suites requieren un resumen unittest con
cantidad positiva y OK, además de código cero. Esto comprueba el registro, no
certifica que cada aserción sea buena ni impide falsificar un JSON local.
Los hallazgos cierran en `awaiting_human_findings_review`; `inspected` nunca
significa aprobado. La revisión humana ocurre fuera del ejecutor y no se simula.

El vocabulario delegate/read_context/llm_chat/external_mcp es del controlador Python,
no de Copilot. Codex no figura entre las tres herramientas enumeradas por el
profesor: su aceptación sigue pendiente. No se inventan permisos nativos,
MutaGato, ITC, escritura-orbital ni aprobaciones del profesor.

## Puerta conjunta de revisión (mejora técnica)

Tras verify y browser_checks sobre el mismo contenido (informes aprobados de cierre-readme):

```powershell
$salida = "docs/taller-5/cierre-readme/release-" + [guid]::NewGuid().ToString("N") + ".json"
.\.venv-taller5\Scripts\python.exe -B -m agents.release_gate --checks docs/taller-5/cierre-readme/checks-final.json --browser docs/taller-5/cierre-readme/browser-final/after.json --output $salida
```

El GUID genera un destino nuevo en cada ejecución y conserva los informes anteriores.
No uses mejora-tecnica/browser/after.json: conserva el fallo CDP original.
Si cambias cualquier archivo incluido en el snapshot, incluido este README, regenera
verify y browser_checks en destinos nuevos antes de repetir la puerta.

Rechaza navegador incompleto, controles duplicados/fallidos y hashes distintos.
Solo emite ready_for_human_review; no autentica personas, no acepta hallazgos ni
habilita publicación. Es una puerta CLI del operador, no protección de main en GitHub.
Las pruebas de oráculo fijo en agents/tests/test_business_oracles.py verifican
itinerario, total y saldo contra constantes independientes de la respuesta.
Se conservan modelos, permisos y reglas turísticas. La Pausa del Colibrí figura
como diseño documental propuesto; no se ejecuta ni se atribuye beneficio probado.

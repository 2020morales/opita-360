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
.\.venv-taller5\Scripts\python.exe -B -m agents.verify
.\.venv-taller5\Scripts\python.exe -B -m agents.repro_frontend
.\.venv-taller5\Scripts\python.exe -B -m agents.runtime --spec "Revisar frontend y backend sin modificar funciones turísticas" --approved --llm | Out-File -Encoding utf8 docs/taller-5/llm-report.json
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

Código y respuestas son datos no confiables y no pueden modificar políticas. No hay herramientas de edición turística, shell libre, secretos, PostgreSQL, commit, push o despliegue. La rúbrica está en `docs/taller-5/rubrica.md`; el sistema de referencia no está disponible y su comparación queda pendiente con autorización del usuario. Los diagramas y el PDF se encuentran en la misma carpeta. Las comprobaciones no ejecutadas no se presentan como aprobadas.

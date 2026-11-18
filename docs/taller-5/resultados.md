# Resultados de la auditoría final del Taller 5

Fecha: 14 de noviembre de 2026. Rama: taller5/sistema-agentes. Base local: c72c3c925db3faef046e5eed50bb37641b3f8c05. Ya existen commits y el [PR #2](https://github.com/2020morales/opita-360/pull/2), abierto y sin fusionar en la consulta de GitHub. Esta ejecución no hizo nuevos commits, push ni merge. El código turístico no se modificó.

## Correcciones implementadas

- agents/quality_gates.py exige las cuatro comprobaciones previstas, nombres únicos, comandos/directorios correctos, código entero 0, stdout/stderr de texto, fecha con zona y snapshot coincidente. Rechaza registros vacíos, parciales, duplicados o fallidos.
- Calidad y seguridad reciben reportes, checks y ambas verificaciones MCP. Su recibo registra hash del ledger y roles recibidos.
- La configuración asigna modelos pero no contiene banderas históricas executed. La ejecución se acredita en las trazas.
- Snapshot incorpora commit base y .gitattributes. Se verifica estabilidad del código y de los bytes de checks.
- PDF de siete páginas: tabla de cinco agentes, modelos/permisos justificados, estructura centralizada, flujo real, comparación verificada y siete enlaces URI. FET-QX7 en todas las páginas.
- La regla *.pdf binary impide conversión LF/CRLF. No se cambiaron API, CORS, presupuesto ni persistencia.

## Pruebas ejecutadas

| Comprobación | Resultado real | Registro |
|---|---|---|
| Agentes, permisos, contratos y puertas | 34 pruebas, OK | checks.json: agents |
| API en proceso con TestClient | 8 pruebas, OK | checks.json: backend |
| compileall backend | código 0 | checks.json: backend_compile |
| Build frontend instalado | código 0 | checks.json: frontend_build |
| npm ci --ignore-scripts --no-audit --no-fund, copia temporal | código 0 | frontend-repro.json |
| Build limpio desde lockfile | código 0; Vite 8.3.5 | frontend-repro.json |
| Chrome real: escritorio/móvil emulado, teclado y nombres accesibles | 14/14, código 0 | browser/after.json y PNG |
| Inferencias locales reales | 5 llamadas, primer intento | llm-report-final.json |
| MCP externo | 2 sesiones; lectura igual y rechazo fuera del scope | llm-report-final.json: mcp |
| PDF | 7 páginas, apertura estricta, renderizado y 7 enlaces URI | pdf-validation.json |

Las **42 pruebas unittest** son distintas de las 14 comprobaciones de navegador. No se suman para afirmar cobertura porcentual. La primera ejecución del módulo de siete regresiones falló al importarlo porque la implementación aún no existía; después las siete pasaron. No se presenta esa secuencia como TDD de todo el proyecto.

El build instalado usó Vite 8.3.8 y la copia limpia usó 8.3.5 del lockfile. Ambos pasaron. No se modificó el lockfile para ocultar la diferencia. Persisten advertencias de lucide-react y deprecación de Starlette/HTTPX.

## Ejecución LLM/MCP corregida

Run fe8439a1-922d-42cd-aaaf-4010f589de64, Ollama local qwen3.5:4b. Orquestador, frontend, backend, calidad y seguridad completaron llamadas reales con 190, 144, 310, 318 y 199 tokens evaluados, todas en primer intento. No se simularon respuestas.

El servidor filesystem 2.3.0 se ejecutó por stdio con Node portátil 24.13.0. Cada sesión leyó una copia permitida y comprobó que el original fuera del directorio temporal no era accesible. Las pruebas de política rechazan nombres de herramientas de escritura; no se ejecutaron escrituras contra el servidor.

Los recibos de calidad y seguridad incluyen mcp_roles_received: [frontend, backend] y mcp_ledger_sha256. Se cotejaron esos hashes, tareas/reportes, snapshot actual y bytes de checks. checks-llm-final.json conserva una copia exacta del registro asociado.

El cierre es awaiting_human_review. --approved confirma alcance autorizado, no identidad autenticada; generated_plan_reviewed_by_human es false. No se afirma aprobación humana individual del plan generado.

## Referencias y enlaces

Se inspeccionaron las tres ramas publicadas del backend y las dos del frontend. La comparación pertinente usa backend calidad-agentes, commit af004c4, y frontend 001-project-baseline, commit 33161da. Los otros árboles no contienen la misma configuración especializada. reference-evidence.json conserva metadatos y extractos; comparacion-referencia.md explica las diferencias.

No se ejecutaron proyectos .NET/Angular, modelos de Copilot ni CI del profesor. El umbral 80% es configuración inspeccionada, no resultado de OPITA. Los siete destinos del PDF fueron consultados mediante GitHub en solo lectura; no se creó ni editó un PR.

## Reproducción

Desde la raíz, en Windows y con dependencias del entorno registrado:

    .\.venv-taller5\Scripts\python.exe -B -m agents.verify
    .\.venv-taller5\Scripts\python.exe -B -m agents.repro_frontend
    .\.venv-taller5\Scripts\python.exe -B -m agents.browser_checks --label after
    .\.venv-taller5\Scripts\python.exe -B -m agents.runtime --spec "Auditar frontend y backend sin cambiar funciones turísticas" --approved --llm
    python -B docs/taller-5/generar_pdf.py
    git check-attr text diff merge -- docs/taller-5/taller5.pdf
    git diff --check

Requiere qwen3.5:4b disponible en Ollama loopback y permisos para iniciar Chrome/MCP. El generador lee llm-report-final.json, checks.json, frontend-repro.json y browser/after.json; no ejecuta pruebas al generar el PDF. No se promete identidad textual entre inferencias.

## Conservación y pendientes

La evidencia anterior se conserva en history/pre-delivery-audit/ sin sustituirla por la nueva. llm-report.json y checks-llm-historical.json son históricos. Sus afirmaciones antiguas o incorrectas no se reescriben para ocultarlas. Ver revision-hallazgos.md.

No hay auditoría WCAG completa, lector de pantalla, rendimiento, cobertura medida, mutación o CI propio. PostgreSQL no está conectado. Node mantiene permisos del usuario: el cliente acotado no crea sandbox OS. Una respuesta JSON correcta no asegura análisis correcto. Quedan aceptación humana de la entrega y revisión de hallazgos; no se calcula una nota.

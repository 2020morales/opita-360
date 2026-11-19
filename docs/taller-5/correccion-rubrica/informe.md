# Informe de corrección local — Taller 5 · FET-QX7

Rama independiente: `taller5/correccion-rubrica`. Base conservada:
`8cce952bace0763ac5e96208c70e93a304979fb4`. Sin staging, commit, push ni merge.
Esta revisión no es la versión publicada ni acredita el archivo entregado en Q10.
La API y la interfaz turística no se modificaron. No se editaron Talleres 4 y 6.

## Correcciones implementadas

- Manifiesto: invocación, entradas, salidas, motivo del modelo y prohibiciones para
  los cinco roles reales. Sin ampliar herramientas ni permisos de escritura.
- Puerta G1: exige cuatro comprobaciones, código cero, resumen unittest positivo
  y OK. Rechaza suites vacías, cero pruebas y resultados fallidos.
- Identidad: SHA y mapa de archivos deben coincidir; rama y commit se conservan
  como procedencia, sin invalidar contenido idéntico por sí solos.
- Cierre: `inspected` no acepta hallazgos. Se emite
  `awaiting_human_findings_review`; un reporte blocked conserva el bloqueo.
- Salidas nuevas obligatorias para verify, navegador y reproducción limpia.
  Se rechaza sobrescribir un destino existente; tres pruebas negativas reales.
- Tabla de agentes, matriz de calidad, diagramas y cuatro secciones del PDF
  alineados con el controlador. FET-QX7 en encabezado; máximo ocho páginas.
- Estado PR #2 corregido: fusionado según GET de GitHub; corrección nueva local.
- Diferencias justificadas frente a los commits fijados del profesor, sin ejecutar
  sus proyectos ni atribuir confirmaciones docentes.

## Pruebas y verificaciones realmente ejecutadas

| Ejecución | Resultado | Evidencia |
|---|---|---|
| Primera verificación de suites y compilaciones | 37 agentes + 8 backend; compileall/build con código 0 | checks-01.json |
| Verificación con código final del controlador | 37 agentes + 8 backend; compileall/build con código 0 | checks-02.json |
| Primer navegador | Fallo CDP: ConnectionClosedError, 0 controles ejecutados | browser/after.json |
| Repetición con permisos de navegador | 14/14 aprobados; escritorio/móvil, teclado, etiquetas y AX | browser-02/after.json y dos capturas |
| Primer LLM/MCP | Fallo por timeout al verificar Node mediante npx; no flujo completo | llm-execution.json |
| Repetición real fuera del entorno restringido | Código 0; 5 inferencias y 2 sesiones MCP; primer intento de cada rol | llm-execution-03.json y llm-report-03.json |
| Rechazo de sobrescritura | 3/3: FileExistsError esperado y SHA antes/después igual | output-guards.json |
| Enlaces | 7/7 recursos respondieron mediante GET del conector GitHub | links.json |
| PDF | Ocho páginas, cuatro secciones, extracción estricta y renderizado | pdf-validation-final.json |

Son **45 pruebas unittest por ejecución**, no 90 pruebas distintas. Los 14 controles
Chrome, tres guardas y verificaciones documentales se cuentan por separado.
Las dos sesiones MCP cotejaron contenido y comprobaron rechazo de lectura fuera
del scope; no se invocaron escrituras anunciadas por el servidor. El cierre sigue
pendiente de revisión humana. Los resultados del LLM no son pruebas de corrección.

Los fallos de entorno se conservaron y las repeticiones usaron destinos nuevos.
No se atribuye una causa definitiva al fallo CDP; repetir fuera de la restricción
permitió completar la prueba. Npx falló por timeout en el primer flujo; la repetición
completó la integración. No se cambiaron proveedor, modelo ni dependencias.

## Contraste y limitaciones

`contraste-llm.md` confronta errores del reporte nuevo con líneas de código reales.
El selector sí tiene id; la suma de presupuesto sí se comprueba salvo la primera
parada documentada; el host sí produjo reportes v1. Se conservan las respuestas
incorrectas y no se modifica negocio turístico para satisfacerlas.

El navegador no integra las cuatro puertas previas al LLM. El control final sigue
siendo humano. Sin cobertura porcentual medida, mutación, MutaGato, CI propio,
WCAG completa, lector de pantalla humano, todos los navegadores/dispositivos o
persistencia PostgreSQL probada. Persisten advertencias lucide-react y Starlette/HTTPX.
La instalación limpia anterior permanece en frontend-repro.json; no se repitió.

## Conservación y privacidad

Se contrastan 30 archivos históricos JSON/PNG/TXT/history contra HEAD.
Cinco tienen diferencias brutas preexistentes LF/CRLF, pero contenido equivalente:
browser/before.json, checks-llm-historical.json, demo-report.json, llm-report.json
y python-lock.txt. No se normalizan ni se reescriben. No se presentan esas diferencias
como igualdad binaria. Las excepciones históricas de formato documentadas se conservan.

La nueva validación registra ambos SHA y equivalencia de finales de línea.
Los prefijos de usuario de logs nuevos se anonimizan; fechas, resultados y mensajes
se conservan. No se alteran logs históricos para ocultar sus rutas. El escaneo por
patrones de archivos nuevos/modificados es acotado, no una garantía universal.
La matriz de auditoria-entrega.md permanece; los resultados anteriores se contextualizan.

`git diff --check` termina con código 0; Git avisa de conversión futura LF a CRLF
en archivos editados. Esos avisos se registran, no son errores nuevos de espacios
finales. No se cambia la configuración global ni las excepciones históricas.

## Rúbrica: valoración orientativa, no nota garantizada

| Criterio | Estado estricto actual | Estimación /5 | Aporte ponderado | Pendiente |
|---|---|---:|---:|---|
| Calidad 25% | Parcial | 4,2 | 1,05 | Definir ITC/MutaGato; revisión humana de límites y hallazgos |
| Agentes 20% | Parcial | 4,0 | 0,80 | Aclarar cronista-lunar y aprobación docente |
| Diagramas 20% | Parcial | 4,4 | 0,88 | Pausa del Colibrí y confirmación R-27 no acreditadas |
| Herramientas/permisos/modelo 15% | Parcial | 3,0 | 0,45 | Aceptación de Codex/controlador y escritura-orbital |
| Diferencias 10% | Parcial | 4,5 | 0,45 | Confirmación del profesor no disponible |
| Documento 10% | Cumple comprobaciones técnicas | 4,4 | 0,44 | Revisión humana del PDF y publicación nueva |
| Total orientativo | No garantiza nivel Excelente | **4,07** | **4,07/5** | Resolución docente y revisión final |

Los términos ambiguos no se sustituyen por métricas inventadas. El enunciado no
define fórmula ITC ni procedimiento MutaGato; no hay aprobación del profesor para
sus leyendas. No se afirma cumplimiento textual total ni 5,0. El plan detallado
y la lista de aclaraciones están en plan.md. Esperar revisión antes de publicar.

## Reproducción

Desde la raíz, elegir siempre destinos nuevos:

```powershell
.\.venv-taller5\Scripts\python.exe -B -m agents.verify --output docs/taller-5/correccion-rubrica/checks-nuevo.json
.\.venv-taller5\Scripts\python.exe -B -m agents.browser_checks --label after --output-dir docs/taller-5/correccion-rubrica/browser-nuevo
.\.venv-taller5\Scripts\python.exe -B -m agents.runtime --approved --llm --checks-file docs/taller-5/correccion-rubrica/checks-nuevo.json --spec "Revisar frontend y backend sin cambios turísticos"
python -B docs/taller-5/generar_pdf.py
python -B docs/taller-5/correccion-rubrica/verificar_entrega.py --output docs/taller-5/correccion-rubrica/pdf-validation-nueva.json
```

La verificación PDF necesita pypdf y pypdfium2, disponibles en el Python global de
esta ejecución; no se instalaron dependencias. El generador lee explícitamente
checks-02 y la ejecución 03: no reemplaza por sí solo sus fuentes por un informe
nuevo. Actualizar las referencias al preparar otra entrega y volver a verificar.

## Archivos locales de esta revisión

Lista exacta; también en git-review.json.

- `agents/README.md`
- `agents/browser_checks.py`
- `agents/llm_workflow.py`
- `agents/manifest.v1.json`
- `agents/quality_gates.py`
- `agents/repro_frontend.py`
- `agents/runtime.py`
- `agents/tests/test_quality_gates.py`
- `agents/verify.py`
- `docs/taller-5/arquitectura.md`
- `docs/taller-5/auditoria-entrega.md`
- `docs/taller-5/comparacion-referencia.md`
- `docs/taller-5/correccion-rubrica/browser-02/after-desktop.png`
- `docs/taller-5/correccion-rubrica/browser-02/after-mobile.png`
- `docs/taller-5/correccion-rubrica/browser-02/after.json`
- `docs/taller-5/correccion-rubrica/browser/after.json`
- `docs/taller-5/correccion-rubrica/checks-01.json`
- `docs/taller-5/correccion-rubrica/checks-02.json`
- `docs/taller-5/correccion-rubrica/contraste-llm.md`
- `docs/taller-5/correccion-rubrica/ejecutar_llm.py`
- `docs/taller-5/correccion-rubrica/git-review.json`
- `docs/taller-5/correccion-rubrica/informe.md`
- `docs/taller-5/correccion-rubrica/links.json`
- `docs/taller-5/correccion-rubrica/llm-execution-03.json`
- `docs/taller-5/correccion-rubrica/llm-execution.json`
- `docs/taller-5/correccion-rubrica/llm-report-03.json`
- `docs/taller-5/correccion-rubrica/output-guards.json`
- `docs/taller-5/correccion-rubrica/pdf-validation-final.json`
- `docs/taller-5/correccion-rubrica/pdf-validation.json`
- `docs/taller-5/correccion-rubrica/plan.md`
- `docs/taller-5/correccion-rubrica/referencia-consultada.json`
- `docs/taller-5/correccion-rubrica/verificar_entrega.py`
- `docs/taller-5/correccion-rubrica/verificar_salidas.py`
- `docs/taller-5/entrega.md`
- `docs/taller-5/especificacion.md`
- `docs/taller-5/generar_pdf.py`
- `docs/taller-5/matriz-calidad.md`
- `docs/taller-5/plan-aprobado.md`
- `docs/taller-5/resultados.md`
- `docs/taller-5/revision-hallazgos.md`
- `docs/taller-5/rubrica.md`
- `docs/taller-5/taller5.pdf`
- `docs/taller-5/tareas.md`

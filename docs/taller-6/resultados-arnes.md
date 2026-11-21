# Resultados reales del arnés del Taller 6

Worktree de Taller 6, rama taller6/base-comun, base 5b01ae0. Las fechas de los archivos son UTC; la exposición del trabajo sigue pendiente. Esta fase no implementa funcionalidades turísticas.

## Comprobaciones finales

| Componente | Resultado | Evidencia |
|---|---|---|
| Estructura SDD | Cinco borradores y 21 criterios; planes y tareas presentes | harness validate; prueba de estructura |
| Arnés | 22 pruebas aprobadas | [checks finales](ejecuciones/20261117T235813Z-f80895af/checks.json) |
| Agentes históricos | 34 pruebas aprobadas | Mismo registro |
| Backend | 8 pruebas aprobadas | Mismo registro |
| Frontend | 9 pruebas aprobadas | Mismo registro |
| Build | Código 0, Vite 8.3.5 | Mismo registro |
| Skills Codex | Tres nombres descubiertos por skills/list real | [descubrimiento](ejecuciones/20261117T213704Z-645e3a94/codex-skills.json) |
| Brújula-semántica | Conversión ejecutada para las cinco specs, 21 casos no implementados | Cinco cases.json del inventario |
| Inventario | Cinco reportes, cero inferencias y cero cambios de código | [inventario](ejecuciones/20261117T213843Z-7d62b692/review.json) |
| MCP independiente | Dos sesiones reales; lectura igual y rechazo fuera del scope en ambas | [MCP](ejecuciones/20261117T235429Z-67310319/review.json) |
| Revisión LLM independiente | Cinco llamadas reales y reportes válidos | [LLM](ejecuciones/20261118T000306Z-98c3691e/review.json) |

Las 73 pruebas unittest/node:test no incluyen las 24 comprobaciones de navegador de la integración anterior. No se ejecutó navegador nuevo en esta fase. La primera batería tuvo 21 pruebas del arnés; después de añadir la regresión de diagnóstico pasó la batería final de 22. No se suman repeticiones para aparentar más casos ni se calcula cobertura porcentual.

El descubrimiento de las tres skills usa la CLI instalada de Codex y no una inferencia. No acredita que la sesión actual del IDE haya activado automáticamente cada skill. Abrir el worktree como carpeta principal y seleccionar la skill en una sesión nueva.

## Inferencias y MCP

Qwen3.5:4b devolvió cinco respuestas reales: orquestador 218, frontend 235, backend 268, calidad 229 y seguridad 227 tokens evaluados según Ollama. No se sustituye el modelo por respuestas inventadas. El reintento exitoso no incluyó --mcp; ambos componentes se comprobaron por separado. El modo combinado falló antes de la corrección y queda pendiente repetirlo tras ella.

El modelo recibe extractos de 1000 caracteres por fuente y colas de checks; los hashes inventarían archivos completos del host. Eso limita su análisis. La validez de JSON no acredita la corrección de sus conclusiones. Ver [contraste estático](contraste-salidas-arnes.md): varias afirmaciones del modelo se refutaron contra el código. No hubo aplicación automática de sus sugerencias ni aprobación humana de cierre.

MCP reutiliza el módulo histórico sin modificarlo: filesystem 2.3.0, Node portátil 24.13.0, stdio y lectura de copia temporal. No equivale a sandbox del sistema operativo. La prueba MCP se ejecutó antes del ajuste de diagnóstico/contexto; su adaptador y los archivos turísticos no cambiaron.

## Errores y límites

La revisión combinada terminó con TimeoutError y se conserva en [su registro](ejecuciones/20261117T234539Z-81195a90/error.json). El registro antiguo no permite identificar la etapa; no se inventa esa información. Se acotó contexto/salida y se añadió registro de rol, etapa y resultados parciales para futuros fallos. No se hizo un benchmark que demuestre causalidad de rendimiento.

La invocación sin --approved devolvió PermissionError, código 1: [rechazo esperado](ejecuciones/20261117T214104Z-b5bf5027/error.json). Es una comprobación negativa satisfactoria, no una funcionalidad fallida. El test de TimeoutError usa mock para verificar el diagnóstico; no acredita una inferencia real.

Persisten avisos de Starlette/HTTPX y lucide-react. No se instalaron nuevas dependencias de aplicación. Se utilizó el intérprete existente con dependencias, sin modificar su entorno. Los reportes nuevos anonimizan rutas de usuario y no contienen credenciales detectadas.

Pendientes: implementación y pruebas de las cinco specs, sus ramas/PR y fusión autorizada en main; CI nuevo; cobertura y mutación medidas; auditoría WCAG; aceptación humana de los reportes y mejora de contexto para reducir falsos hallazgos. Coeficiente Murciélago y Perfil Nebulosa requieren aclaración oficial. Las reflexiones las redactan los integrantes; no se inventaron experiencias.


## Actualizacion posterior

Las correcciones posteriores y la ejecucion conjunta verificada se documentan en [correcciones-partes-1-2.md](correcciones-partes-1-2.md). Las evidencias enlazadas arriba se conservan como registros de su fase; no se cambian sus resultados ni se vuelven a presentar como actuales.

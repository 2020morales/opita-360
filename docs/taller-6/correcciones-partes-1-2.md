# Correcciones verificadas de las partes 1 y 2

Se trabajo exclusivamente en taller6/base-comun, desde 5b01ae0, sin commit, push, merge ni implementacion de las cinco funcionalidades. Los borradores permanecen draft y sus casos no se marcan ejecutados.

## Investigacion de los timeouts

El fallo antiguo de [la primera fase](ejecuciones/20261117T234539Z-81195a90/error.json) solo contiene TimeoutError: no permite atribuir su causa a una etapa.

En esta correccion se reprodujo un fallo con diagnostico: [frontend/LLM](ejecuciones/20261118T005225Z-70638031/error.json) agoto el timeout HTTP de 80 s, despues de una inferencia del orquestador y una lectura MCP de frontend exitosas. El padre conserva esos resultados parciales. Eso localiza ese ensayo, pero no demuestra que el fallo antiguo tuviera la misma causa.

Se sustituyo la espera directa de red por workers propios y watchdog del padre. Limites actuales: LLM 150 s, timeout HTTP 145 s, MCP 60 s y limite global 600 s. La limpieza de procesos propios esta acotada; no se detienen Ollama, servicios existentes ni procesos ajenos. El operador puede reducir el maximo con --max-seconds. El test de watchdog inicia y recoge un proceso hijo real de prueba, sin simular una inferencia.

## Resultado conjunto real

[Reporte final LLM/MCP](ejecuciones/20261118T010014Z-aba6178e/review.json): cinco inferencias reales y dos sesiones MCP. Tiempo total observado: 273,187 s, limite 600 s. Duraciones LLM por rol: 33,313; 52,922; 50,703; 65,750; 62,063 s. MCP: 4,125 y 4,047 s. Todas las etapas terminaron con codigo 0 dentro de sus limites.

No es un benchmark controlado ni garantiza que otra ejecucion no alcance el plazo. Los fallos anteriores no se borraron ni se transformaron en exitos.

## Contexto y comprobacion de afirmaciones

grounding.py selecciona imports/modelos/handlers de FastAPI, logica React y funciones de permisos, con numeros de linea. Se omite repeticion de datos semilla y de casos que ya estan en la spec. Los nombres de pruebas y sus resultados se presentan separadamente. La base con pruebas aprobadas no se presenta como implementacion de criterios futuros.

El comprobador contrasta cinco hechos catalogados con AST, patrones de fuente, checks reales y metadatos de spec. Los metadatos de implementacion y pruebas NO constituyen por si solos pruebas de ejecucion. Tambien coteja citas exactas contra archivo, linea y contexto realmente suministrado. Una coincidencia textual no prueba la interpretacion semantica.

En el ensayo conjunto se verificaron 8 afirmaciones estructuradas, con 0 contradicciones dentro de ese catalogo. El modelo no presento citas: 0 citas recibidas, no se afirma haber verificado citas reales de esa respuesta. La funcion se prueba con fixtures positivos y negativos. Solo los hechos verificados se transmiten al siguiente rol; no se propaga prosa libre como hechos.

La prosa permanece unverified_prose y human_acceptance es false. Persisten imprecisiones: el orquestador mezcla catalogo existente con detalle futuro; backend escribe /api/recommendaciones donde la ruta real es /api/recommendations; calidad afirma que bloquear API no se puede automatizar, sin justificarlo. No se aprobaron esas frases ni se aplicaron cambios a partir de ellas. El control es acotado, no un verificador universal de lenguaje natural.

## Pruebas y skills

[Checks finales](ejecuciones/20261118T005541Z-8a2c029f/checks.json): 36 pruebas del arnes, 34 de agentes anteriores, 8 API y 9 frontend: 87 aprobadas, 0 fallos de pruebas. Build codigo 0. No se suman repeticiones ni se calcula cobertura.

[Codex skills/list](ejecuciones/20261118T004955Z-2b41e7f6/codex-skills.json) detecto las tres skills reales. No acredita activacion automatica en el IDE. Se vuelve a comprobar cases para las cinco specs; los JSON generados permanecen execution=not_run y status=not_implemented. La estructura SDD se valida sin ejecutar funcionalidades.

El nuevo test del parser previene un error introducido durante esta correccion: duplicacion de --max-seconds. El [registro del fallo](ejecuciones/20261118T004947Z-927f424d/cli-startup-error.json) conserva codigo 1 y tests_started=false. Se corrigio antes de los checks finales; no se presenta como fallo de una prueba de la aplicacion.

## Documentacion y pendientes

AGENTS.md distingue comandos ya ejecutados y funcionalidades pendientes. El diagrama muestra solicitudes y retornos por el orquestador, sin enlaces laterales entre especialistas. Las advertencias siguen visibles: [revision de dependencias](advertencias-dependencias.md). No se cambiaron paquetes ni el lockfile.

No hay autoedicion ni aceptacion automatica. Siguen pendientes revision humana, tratamiento de la prosa no verificada, las cinco funcionalidades y sus PR, CI, aclaraciones oficiales de metricas y entrega autorizada en main. No se configuraron agentes nativos del IDE: los roles Python y las skills siguen descritos como mecanismos distintos.

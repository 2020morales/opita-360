# Contraste estático de las salidas LLM

Este análisis del asistente contrasta fuentes reales; NO es aprobación humana ni revisión del profesor. Las respuestas originales se conservan sin reescribir sus errores en el reporte LLM.

| Afirmación del modelo | Contraste verificable | Clasificación |
|---|---|---|
| Falta validación Pydantic en backend | backend/app/main.py:79 define TripRequest(BaseModel), líneas 80-82 usan Field y la línea 93 recibe request: TripRequest. Las ocho pruebas API incluyen entradas inválidas | Refutada; el extracto inicial no mostraba esa sección |
| El fallback demo debe estar en backend | frontend/src/main.jsx:44-47 recupera demo al fallar el catálogo y líneas 66-73 recuperan recomendaciones locales. AC-04 de S01 trata del detalle futuro | Ubicación incorrecta y mezcla entre base existente y nueva funcionalidad |
| Casos not_implemented contradicen pruebas aprobadas | Los 21 casos pertenecen a funcionalidades nuevas; las pruebas existentes verifican base/arnés, no el detalle todavía sin implementar | Refutada; no deben marcarse como ejecutados |
| Pruebas pasaron en entornos de código diferentes | checks registra directorios raíz/frontend del mismo worktree y un snapshot común. Se reutiliza un intérprete externo, no una segunda implementación | No respaldada por la evidencia |
| Las restricciones impiden cierre sin intervención humana | El runtime está diseñado solo para revisión y el usuario no autorizó funcionalidades; la implementación y aceptación futuras requieren autorización | Límite real y deliberado |

Los revisores posteriores repitieron algunas afirmaciones erróneas de los primeros roles. Compartir modelo y reportes previos no equivale a independencia de revisión. Los extractos y la propagación de informes son riesgos documentados. No se aplicaron supuestas correcciones a FastAPI ni a React a partir de estos hallazgos.

Próximo trabajo propuesto, sujeto a revisión: seleccionar fragmentos por símbolos/requisito, separar en el prompt las pruebas de base de las pruebas de cada spec y verificar citas antes de aceptar hallazgos. Esto no se presenta como implementado. El control actual es lectura restringida, pruebas reales y contraste previo a cualquier cambio autorizado.


## Actualizacion posterior

Las correcciones posteriores y la ejecucion conjunta verificada se documentan en [correcciones-partes-1-2.md](correcciones-partes-1-2.md). Las evidencias enlazadas arriba se conservan como registros de su fase; no se cambian sus resultados ni se vuelven a presentar como actuales.

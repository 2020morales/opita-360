# Cambios del arnés frente al Taller 5

| Antes | Ahora | Motivo observado |
|---|---|---|
| Inventario de requisito libre y cuatro tareas fijas | Cinco specs identificadas y casos enlazados a AC | La rúbrica exige trazabilidad por spec |
| Skills históricas en .github/skills | Tres skills nativas en .agents/skills, sin borrar las anteriores | Codex descubre ese directorio; skills/list detectó los tres nombres |
| Flujo LLM lee checks de docs/taller-5 | CLI propio exige checks nuevos completos y snapshot vigente | Evitar sobrescribir o reutilizar evidencias obsoletas |
| Reportes en rutas del taller | Directorios de ejecución únicos y redacción de rutas | Conservar fallos y repeticiones auténticos |
| Fallo combinado sin etapa clara | Error futuro con rol, etapa y evidencia parcial | Se observó TimeoutError sin diagnóstico suficiente |
| Contextos extensos | Extractos acotados; límites explícitos | Se acota carga después del timeout, sin atribuir mejora medida |
| Confianza en revisión LLM | Contraste de salidas y falsos hallazgos registrados | El modelo negó Pydantic y confundió criterios futuros con regresiones existentes |

Se mantienen los cinco roles y el modelo local por disponibilidad comprobada, no por superioridad medida. agents/, frontend/, backend/ y las evidencias anteriores permanecen intactos en esta fase. Solo se actualizan memoria/README en la copia del Taller 6; las ramas originales no cambian.

No se añadió un editor autónomo ni shell de modelos. Los comandos fijos pertenecen al operador. Para implementar cada funcionalidad habrá que aprobar su spec y actualizar las listas de contexto si aparecen archivos nuevos. No hay PR, CI remoto ni despliegue ejecutados en esta fase.


## Actualizacion posterior

Las correcciones posteriores y la ejecucion conjunta verificada se documentan en [correcciones-partes-1-2.md](correcciones-partes-1-2.md). Las evidencias enlazadas arriba se conservan como registros de su fase; no se cambian sus resultados ni se vuelven a presentar como actuales.

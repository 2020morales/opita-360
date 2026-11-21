# Incidentes reales del arnés

| Incidente | Resultado y corrección | Evidencia |
|---|---|---|
| Descarga inicial del manual bloqueada por red del sandbox | Reintento autorizado obtuvo el manual oficial | Observado en terminal; fuentes-codex.md |
| Escritura masiva rechazada por límite de longitud Windows, error 206 | Se dividió el envío por stdin; un primer intento de comillas falló y se corrigió | Observado en terminal; no existe log independiente ni se reconstruyó |
| Revisión sin aprobación | Rechazo esperado antes del modelo | ejecuciones/20261117T214104Z-b5bf5027/error.json |
| Revisión LLM/MCP combinada | TimeoutError; se conserva el fallo sin atribuir etapa desconocida | ejecuciones/20261117T234539Z-81195a90/error.json |
| Diagnóstico insuficiente | Se añadió rol/etapa/parciales y una prueba negativa; 22 pruebas del arnés pasaron | checks finales y harness/runtime.py |
| Reintento LLM independiente | Cinco respuestas reales, sin cambiar modelo ni aplicar sugerencias | ejecuciones/20261118T000306Z-98c3691e/review.json |
| Conclusiones incorrectas del modelo | Contraste estático; ninguna modificación turística aplicada | contraste-salidas-arnes.md |
| Advertencias de dependencias | Se registran; no se alteró el lockfile para ocultarlas | checks.json: backend/build |

Las ocho advertencias de espacios de los logs históricos siguen siendo excepciones aceptadas, no verificaciones aprobadas. Esta fase no modifica esos archivos; un diff de cambios nuevos no vuelve a validar ni elimina sus advertencias originales.

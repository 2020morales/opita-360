# Plan aprobado y ejecución local de integración

Autorización del usuario: crear worktree y rama temporal, combinar S01–S05, resolver conflictos y probar. Prohibido modificar main, fusionar los PR de GitHub, publicar o crear PR nuevo. No se realizan rebase, squash ni force push.

Base: origin/main 0985273541e21579009cb6179546b9f3db845f7e. Rama temporal taller6/integracion-final. Se conservan los commits originales como ancestros mediante cinco fusiones exclusivamente locales. Registros integration-merge-001 a 005 en ejecuciones, con salida real y listas de conflictos.

## Resoluciones
- S01 entró sin conflictos. S02: importaciones de detalle y parser, estilos separados, documentación de ensayo y unión de listas mínimas del manifiesto.
- S03: filtros base con maxCost, luego intersección con favoritos; conservar callbacks de costo, inicialización perezosa de storage, referencias y recuperación de foco; tarjetas con detalle y favorito. Mensaje vacío incluye recuperación de ambos filtros.
- S04: conservar endpoint de detalle e importaciones, campo municipal opcional, candidatos locales previos a intereses/fallback, selector independiente y aviso vacío. Conservar tests/contexto de JavaScript y resumen de resultados corregido.
- S05: mantener municipio en payload y recuperación, origen explícito api/demo, limpieza de error, exportación deshabilitada durante carga, archivo de la última propuesta y mensaje vacío. Combinar estilos y conservar tests de las otras specs.

## Fallo comprobado y corrección
La primera regresión falló porque el presupuesto de contexto recortaba catch de makeTrip tras crecer App. Se priorizan bloques completos de comportamiento con el mismo límite. Prueba nueva verifica contexto de las cinco conductas; el informe fallido se conserva.

## Verificación
Contratos API que relacionan detalle y recomendaciones y preservan vacío/presupuesto; regresión completa; cinco navegadores históricos más recorrido cruzado real. No sumar suites previas de ramas como tests independientes. Registrar fixtures de selector desincronizado y almacenamiento denegado. Comprobar hashes de T4/T5/agents/skills originales y referencias de ramas antes/después. Revisión por orquestador local con contexto integrado; su prosa requiere contraste humano.

La publicación, fusión de los PR originales, CI remoto y aceptación final siguen fuera de esta autorización. Si se decide integrar main posteriormente, usar las resoluciones de este ensayo y revalidar tras cada actualización.

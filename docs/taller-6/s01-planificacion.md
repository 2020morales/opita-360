# S01: registro real de especificacion y planificacion

Trabajo en taller6/base-comun sobre f5c5fc928d4afe90601aad6eacfe28e78372988f. No se creo rama, no se implemento codigo y no se hizo staging, commit, push ni merge. Los 16 excluidos preexistentes se conservaron.

Se leyeron AGENTS.md, README.md, instrucciones frontend/backend, harness/README.md, manifiesto, runtime, CLI, core y las tres skills. Aplicacion manual por Codex de opita-frontend (foco, filtros y API/demo), opita-backend (contrato y errores) y brujula-semantica (criterios estructurados y conversor real). No se afirma activacion automatica de una skill en VS Code ni inferencia de los roles.

Inspeccion estatica: backend/app/main.py no registra endpoint de detalle por ID y frontend/src/main.jsx no implementa dialogo/accion de detalle. Esta evidencia no sustituye pruebas funcionales. Se ampliaron solo cinco artefactos SDD de 001: spec.md, spec.json, plan.md, tasks.md y pr.md. Las otras cuatro specs y evidencias historicas no se editaron.

## Comandos y resultados

- python -B -m harness validate: codigo 0, S01 draft con 10 criterios; otras specs 4/5/4/4 criterios; structure_valid_not_implemented.
- python -B -m harness cases --spec 001: codigo 0; salida final ejecuciones/20261118T015738Z-25f59340/cases.json. Genera 10 casos; execution=not_run, status=not_implemented. No es una ejecucion de pruebas de S01.
- python -B -m harness review --spec 001 --approved --max-seconds 60: codigo 0; salida final ejecuciones/20261118T015738Z-4889e6c8/review.json. Cinco roles en inventory; sin LLM/MCP. Los reportes esperan revision humana y no acreditan analisis inteligente del plan.

Las evidencias finales se enlazan a continuacion.

[Casos finales](ejecuciones/20261118T015738Z-25f59340/cases.json) y [orquestador final](ejecuciones/20261118T015738Z-4889e6c8/review.json).

## Incidente real y limites

La primera escritura mediante pipeline PowerShell sustituyo caracteres acentuados por signos de interrogacion. La primera validacion fallo porque Factor Ambar no coincidia con la cadena Unicode requerida. Se conserva el error autentico en ejecuciones/20261118T015405Z-bb6b30b9/error.json. Se corrigieron los documentos; las validaciones posteriores pasaron. Los casos/review intermedios 20261118T015601Z-342c5386 y 20261118T015603Z-deeaa95a se conservan como ejecuciones previas, no como evidencia de la version final.

No se ejecutaron suites de aplicacion, navegador o build en esta fase documental. Los 87 tests del arnes previo corresponden a su snapshot historico y no acreditan S01. Nuevos --llm requieren checks actuales porque se modifico la spec. No hay incidentes funcionales nuevos demostrados.

Pendiente: aprobacion humana del alcance/plan y Ambar 3/9, autorizacion de implementacion, rama propia, pruebas reales AC-01..10, CI/publicacion de base comun y PR aislado a main. No se atribuye revision docente.

# Registro de excepciones históricas — Taller 6

## Alcance y estado de autorización

Este documento registra hallazgos de la auditoría de integración; no modifica los originales ni convierte verificaciones fallidas en aprobadas. Su creación fue autorizada por el usuario. No autoriza commit, publicación, integración ni reescritura del historial. Los ocho espacios finales de los logs del Taller 4 ya tenían una excepción aceptada; las demás excepciones se registran para decisión y revisión explícitas.

Referencias auditadas después de git fetch origin:

- origin/main: 4bb1626975c67dfeeee67ab1156322f2e6ce3eba.
- taller6/base-comun: f5c5fc928d4afe90601aad6eacfe28e78372988f.
- Commit local de S01: e53faf30e0351d956716b81789d6791f012653a2.

La comparación de base con origin/main incluía ocho commits, 187 archivos añadidos, cinco modificados y ninguno eliminado. Estos datos describen esas referencias; deben volver a comprobarse antes de una integración futura.

## Rutas personales en evidencias originales

No se reproduce el nombre de usuario ni la ruta absoluta. Los marcadores siguientes son genéricos y no sustituciones efectuadas sobre los originales.

| Archivo afectado | Líneas del contenido auditado | Naturaleza y procedencia |
|---|---|---|
| docs/plan-filtro-municipio.md | 8, 17, 22, 27, 32, 39, 44, 49, 54 | Rutas de archivos consultados durante el plan original, commit d81614d. Patrón: <PERFIL_LOCAL>/Downloads/<REPOSITORIO>/... |
| docs/taller-4/evidencias/intento-puerto-ocupado.json | 13 | Ruta del script en un traceback de ejecución, commit 4a23215. Patrón: <TEMP_LOCAL>/<WORKTREE_T4>/docs/taller-4/verificar.py |
| docs/taller-4/historial/primera-ejecucion-navegador/intento-puerto-ocupado.json | 13 | Copia byte por byte del mismo informe original; conserva la misma ruta y el mismo fallo. |

Las rutas permiten identificar el usuario local y parte de la organización de carpetas. No son credenciales ni permiten por sí mismas autenticarse. No se identificaron contraseñas o tokens en los fragmentos señalados. Los dos JSON registran status=failed, con checks y commands vacíos, por un puerto ocupado; no demuestran pruebas de navegador aprobadas.

Riesgo: exposición de identidad y estructura local al publicar o compartir el historial. La preservación de evidencia no elimina ese riesgo. No se afirma que una autorización para crear este registro constituya consentimiento general de publicación de datos identificables.

Mitigación propuesta: conservar los originales y sus hashes; referenciarlos sin copiar rutas personales en documentación nueva; revisar y registrar expresamente la decisión de publicación. Si se necesitan copias de consulta anonimizadas, crearlas por separado y etiquetarlas como derivadas, sin sustituir los originales ni atribuirles sus hashes. Una copia anonimizada no elimina los datos de los commits anteriores. Si la política de publicación exige retirarlos del historial, detener la integración y acordar un tratamiento separado: no reescribir ni borrar por iniciativa del agente.

## Advertencias de formato históricas

El comando original git diff --check origin/main taller6/base-comun devolvió código 2: 2955 avisos en 18 archivos. No es una comprobación aprobada. Un segundo diagnóstico, realizado solo para distinguir CR al final de línea mediante core.whitespace con cr-at-eol, dejó 16 avisos reales en cuatro archivos; la diferencia de 2939 avisos se atribuye al tratamiento de CRLF. No se cambió configuración persistente, ningún archivo ni el resultado original.

### CRLF: 2939 avisos históricos de representación

Archivos correspondientes:

- agents/manifest.v1.json
- docs/taller-5/browser/after.json
- docs/taller-5/checks-llm-final.json
- docs/taller-5/checks.json
- docs/taller-5/frontend-repro.json
- docs/taller-5/generar_pdf.py
- docs/taller-5/history/pre-delivery-audit/browser/after.json
- docs/taller-5/history/pre-delivery-audit/browser/before.json
- docs/taller-5/history/pre-delivery-audit/checks.json
- docs/taller-5/history/pre-delivery-audit/demo-report.json
- docs/taller-5/history/pre-delivery-audit/frontend-repro.json
- docs/taller-5/history/pre-delivery-audit/llm-report.json
- docs/taller-5/llm-report-final.json
- docs/taller-5/pdf-validation.json

Riesgo: ruido en revisiones, diferencias entre herramientas y posibles rechazos de controles de estilo. Los avisos no demuestran por sí solos corrupción ni fallo funcional. Mitigación propuesta: explicar el diagnóstico, mantener visibles los resultados originales y aplicar una política de finales de línea a archivos nuevos en cambios futuros autorizados. No normalizar masivamente los históricos ni recalcular sus hashes para ocultar las diferencias.

### Espacios y línea final: 16 avisos históricos reales

| Archivo | Líneas | Cantidad | Estado |
|---|---|---:|---|
| docs/plan-filtro-municipio.md | 6, 15, 20, 37, 42, 47, 52 | 7 espacios finales | Registrados para revisión; no corregidos. |
| docs/taller-4/evidencias/build.log | 18, 20, 28, 30 | 4 espacios finales | Excepción previamente aceptada para salida original ANSI. |
| docs/taller-4/historial/primera-ejecucion-navegador/build.log | 18, 20, 28, 30 | 4 espacios finales | Excepción previamente aceptada; conservar historial. |
| docs/taller-5/reference-evidence.json | 180 | 1 línea vacía final | Registrada para revisión; no corregida. |

Las excepciones previas constan en docs/taller-6/advertencias-dependencias.md, incidentes-arnes.md y revision-final/20261117T203627Z/README.md. Abarcan exclusivamente los ocho espacios de los dos logs, no una aprobación automática de los restantes avisos.

Riesgo: incumplimiento de controles de formato estrictos; no se ha identificado un fallo funcional causado por esos 16 avisos. Mitigación propuesta: conservar evidencias exactas y documentar una excepción revisable por archivo y línea, manteniendo código 2 en la comparación histórica. Para archivos nuevos y cambios actuales, seguir exigiendo ausencia de errores nuevos. Si un control de integración exige código 0 sin excepciones, acordar cómo tratar históricos antes de integrarlos, sin ocultar ni renombrar el resultado fallido.

## Por qué se conservan los originales

Modificar espacios, rutas o finales de línea cambia los bytes y hashes y puede invalidar referencias de pruebas previas. También dificultaría reconstruir qué ocurrió en el intento fallido y qué se corrigió después. La evidencia original debe conservar fecha, estado, resultados y contexto; una versión derivada debe identificarse como tal.

La auditoría no encontró diferencias entre los históricos T4 de la base y la rama taller4/completar-entrega, ni entre docs/taller-5 y agents de la base y taller5/sistema-agentes. El objetivo es mantener esa correspondencia. No debe interpretarse como permiso para borrar, editar o fusionar las ramas originales.

## Bloqueos, límites y decisión pendiente

No se identificaron conflictos de ascendencia ni eliminaciones al comparar las referencias auditadas. El escaneo de patrones no detectó tokens o claves privadas en el contenido examinado; no equivale a una garantía absoluta. La inspección de texto/metadatos del PDF no fue un OCR de todas las imágenes.

Estos hallazgos no prueban un defecto funcional de OPITA 360. Son limitaciones conocidas que requieren una decisión de revisión/publicación. Integrar sigue pendiente de autorización y de que el responsable acepte expresamente el tratamiento de las rutas y de las excepciones de formato no aceptadas previamente. Si las políticas no permiten esas excepciones, existe un bloqueo de publicación que debe resolverse sin alterar unilateralmente los trabajos originales.

La rama de S01 contiene además correcciones documentales pendientes en spec.md y pr.md; son diferentes de estos históricos. Este registro es un archivo nuevo, aún sin staging ni commit al crearse, y no forma parte automáticamente del commit f5c5fc9 de base común. Su incorporación futura debe decidirse explícitamente. El diff actual y la comparación completa entre commits tienen alcances diferentes: aprobar el primero no elimina los avisos del segundo.

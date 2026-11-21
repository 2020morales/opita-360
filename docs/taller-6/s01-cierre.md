# S01: verificación final antes de revisión y publicación

Rama: taller6/001-detalle-destino. Worktree independiente <WORKTREE_T6>. No se modificó código, specs ni históricos en esta verificación. No se hizo staging, commit, push, PR ni merge.

## Ejecuciones nuevas

- `python -B -m harness checks --scope all`: 36 pruebas del arnés, 34 agentes, 12 backend (8 regresión y 4 nuevas), 9 filtros; total 91 aprobadas. Build código 0. [Informe](ejecuciones/20261118T023506Z-b5efe4fb/checks.json).
- `python -B -m harness.s01_browser`: 22 controles aprobados. Chrome Chrome/157.0.8103.38. Cancelación observada: 5001.100000023842 ms. [Informe](ejecuciones/20261118T023520Z-e30b1696/s01-browser.json).
- Snapshots de ambas ejecuciones coinciden con los archivos fuente actuales. Avisos de bundling de lucide-react permanecen; no son fallos del build. No se reinstalaron dependencias.

API real mediante proxy exclusivo de prueba en 5187 hacia FastAPI 8000; no se validó un despliegue de producción ni se reutilizó el servidor ajeno de 5173. Red/500/404/timeout y respuesta tardía se ensayan con fixtures fetch. Estas ejecuciones nuevas no reemplazan los informes anteriores, incluidos sus fallos.

## Trazabilidad comprobada

| Criterio | Implementación | Prueba ejecutada |
|---|---|---|
| AC-01 | endpoint de detalle en backend/app/main.py | test_existing_destination_matches_every_catalogue_field |
| AC-02 | HTTPException 404 | test_missing_destination_has_no_fallback |
| AC-03 | Path(gt=0) | test_invalid_ids_are_rejected; catálogo invariante en tearDown |
| AC-04 | botón de main.jsx y componente destination-detail.jsx | real_api_detail_enter |
| AC-05 | dialog.showModal, Cerrar, Escape y foco | nombre accesible, Tab/Shift+Tab, fondo inerte y restauración por ambos cierres |
| AC-06 | rama demo del componente | offline_demo_detail |
| AC-07 | AbortController, plazo 5000 y fallback señalado | network/server/slow loading y fallback, deadline_aborts_request |
| AC-08 | 404 sin copia del catálogo | 404_no_catalogue_fallback |
| AC-09 | cleanup active=false y cancelación | late_response_does_not_overwrite_B |
| AC-10 | estado de filtros conservado y CSS acotado | responsive y filters_preserved en 360x800 y 1280x800 |

Spec.json/spec.md → AC → TC-001-NN → pruebas API/runner → informes nuevos: trazabilidad existente. El PR y aceptación humana siguen pendientes. El conversor cases genera diseños not_run por contrato; los resultados auténticos son los informes de pruebas, no esa marca.

## Accesibilidad y compatibilidad: límites

Comprobados en Chrome headless: nombre accesible mediante árbol AX, foco inicial, Tab/Shift+Tab, fondo inerte, Escape/Cerrar y devolución del foco; dimensiones/scroll y filtros en dos viewports. Los controles automatizados cubren los aspectos ensayados, no toda interpretación visual posible.

Pendientes: recorrido humano de teclado exigido en la sección de verificación de spec.md, lector de pantalla humano, contraste/zoom/alto contraste y auditoría WCAG integral. No hay pruebas en Firefox, Safari, Edge, dispositivos móviles físicos ni versiones antiguas de dialog. No afirmar compatibilidad universal ni aprobación humana completa de AC-04..10. El botón y algunos campos se verifican explícitamente; no hay comparación automatizada exhaustiva de cada texto renderizado con cada campo JSON para todos los destinos.

## Alcance y propuesta de commit

14 archivos versionados modificados, todos vinculados a S01, memoria, trazabilidad y adaptación mínima del arnés a una spec aprobada. Archivos nuevos de código/pruebas: backend/tests/test_destination_detail.py; frontend/src/destination-detail.jsx; frontend/tests/s01.vite.config.mjs; harness/s01_browser.py. Evidencias y documentos S01 según [lista exacta](s01-archivos-commit.txt): **42 rutas propuestas**, ninguna preparada en staging.

Los 16 logs/archivos de integracion y revision-final previamente excluidos siguen en disco y fuera de esta propuesta: no pertenecen al commit de S01. El estado completo de Git, por tanto, también contiene esos archivos ajenos al alcance actual. No se borraron. Los informes intermedios/fallidos de S01 se incluyen para conservar el historial y los enlaces.

Cambios protegidos de Talleres 4/5, agents y skills originales: ninguno. main, taller4/completar-entrega, taller5/sistema-agentes y taller6/base-comun no cambiaron. Staging vacío, diff --check código 0; avisos LF→CRLF permanecen. [Auditoría de cierre](ejecuciones/20261118T023722Z-c33bcfd2/s01-cierre-audit.json).

## Correcciones y decisiones antes de publicar

No aparecieron fallos funcionales nuevos en las pruebas ejecutadas. S01 está lista para revisión técnica local, pero no para declarar aceptación final o publicación completada.

1. Corregir la redacción residual en spec.md que llama futuros a pruebas/archivos ya existentes, y en pr.md que aún describe crear la rama y presupone una base publicada. Esta verificación solo registra el hallazgo; no alteró esos documentos.
2. Realizar y registrar el recorrido humano de teclado o aceptar explícitamente el límite de evidencia automatizada; otras verificaciones de accesibilidad/compatibilidad siguen como límites declarados.
3. Autorizar por separado staging, commit, publicación y PR. main local no contiene todavía los ocho commits de diferencia de la base común; preparar su integración revisada antes de un PR exclusivo de S01. No se consultó el estado remoto actual, por lo que no se afirma que GitHub tenga el mismo estado.
4. El contexto LLM no incluye toda la evidencia de navegador; la revisión anterior no equivale a aprobación automática. No se repitió LLM/MCP en este cierre.

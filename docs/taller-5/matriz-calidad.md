# Matriz de controles — frontend y backend

Inspección LLM, ejecución automatizada y aceptación humana son estados distintos.
Los comandos los ejecuta el operador/controlador, no los modelos.

| Riesgo del código IA | Responsable y momento | Control y evidencia | ¿Bloquea? | Límite |
|---|---|---|---|---|
| API o dependencia inventada | Frontend/backend antes de cierre | Imports y contratos; build, TestClient y requirements/package; checks nuevos | Error de build/API sí; opinión LLM requiere revisión | No prueba toda API externa |
| Suite vacía o registro incompleto | Controlador antes de LLM | quality_gates: cuatro comandos, código cero, resumen positivo y OK; regresiones | Sí | No detecta por sí solo aserciones tautológicas |
| Prueba tautológica u oráculo débil | Calidad y humano al revisar tests | Inspección de test_api.py y test_runtime.py; registrar hallazgo | Aceptación final pendiente hasta decisión humana | Sin mutación ni garantía automática de utilidad |
| Lógica de presupuesto, validación o regresión API | Backend y operador tras cambios | Ocho pruebas TestClient: límites, 422, CORS y no mutación | Fallo de suite sí | Falta oráculo independiente para todos los itinerarios; no persistencia PostgreSQL |
| Filtros, demo o interfaz rota | Frontend y operador tras build | 14 controles Chrome; JSON y capturas por ejecución | Fallo impide declarar navegador aprobado; cierre humano | Navegador no forma parte de las cuatro puertas previas a LLM |
| Accesibilidad insuficiente | Frontend/calidad y humano | Etiquetas, árbol AX, teclado, aria-expanded, ancho móvil | Fallo comprobado debe corregirse/revisarse | No WCAG completa, lector humano ni contraste medido |
| Arquitectura o alcance roto | Seguridad/calidad y humano antes de publicación | Rutas permitidas, tarea-agente, evidencia SHA y diff | Contrato/ruta sí; arquitectura semántica humana | Un hash no prueba comprensión del modelo |
| Evidencia de otro código | Controlador antes y después | SHA y mapa de archivos; byte-estabilidad de checks | Sí | Registro local sin firma; commit/rama informativos |
| Permisos excesivos o lectura fuera de scope | Seguridad y MCP durante sesión | authorize_read/tool; rechazo real de original fuera de copia | Sí | Node tiene permisos del usuario; no sandbox OS |
| Hallazgo LLM falso o sin resolver | Calidad, seguridad y humano al cierre | Reportes conservados; awaiting_human_findings_review | No permite aceptación automática | No clasifica gravedad ni verifica cada frase automáticamente |
| Credencial publicada | Operador/humano antes de publicar | Inspección del diff y escaneo acotado de archivos nuevos | No publicar mientras haya sospecha | Escaneo por patrones no demuestra ausencia universal |

No hay cobertura porcentual medida, mutation testing, MutaGato ejecutado ni CI
propio del Taller 5. No se convierten compilaciones en pruebas funcionales.
Los resúmenes sintéticos de las regresiones son fixtures de validación de registros,
no inferencias LLM ni evidencia de que se haya ejecutado una suite ficticia.

## Evidencia nueva de mejora técnica

- Lógica de negocio: test_business_oracles.py compara contra constantes, no contra
  cálculos derivados de la respuesta: [6,5], 135000, 65000; frontera 134999 admite
  solo [6], total 65000 y saldo 69999. No cambia la excepción de primera parada.
- Cierre frontend/backend: release_gate.py exige suites y 14 controles Chrome
  aprobados para el mismo contenido; release-negative.json demuestra bloqueo
  con el fallo CDP real. release.json demuestra paso solo a revisión humana.
- Evidencias: mejora-tecnica/checks.json, browser-02/after.json, release*.json.
- Límite: oráculos fijados al catálogo demo, no detector universal de tautologías;
  CLI voluntaria no equivale a rama main protegida ni a aceptación autenticada.

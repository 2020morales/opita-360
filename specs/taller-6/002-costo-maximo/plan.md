# Plan tecnico 002

Factor Ámbar: 3/9

Estimacion del equipo propuesta: 1-3 cambio localizado; 4-6 estado persistente local o compatibilidad entre componentes; 7-9 varias dependencias o infraestructura. El PDF solo fija 1-9, no define niveles. Estado: aprobado por el usuario para S02.

## Decisiones propuestas

Mantener React/Vite y FastAPI. Usar funciones puras cuando haya logica reutilizable y conservar API/demo. Revisar accesibilidad y entradas invalidas. Filtrado local derivado sin mutar el catalogo ni desactivar otros filtros.

## Archivos de implementacion y verificacion

- frontend/src/destination-filters.js
- frontend/src/main.jsx
- frontend/src/styles.css (estilos acotados del formulario).
- frontend/tests/max-cost.test.js (nuevo).
- frontend/tests/s02.vite.config.mjs y harness/s02_browser.py (proxy/runner de pruebas).
- harness/tests/test_harness.py (ciclo draft/approved) y manifest.json (contexto de revision).
- Memoria/README y artefactos SDD de S02; ninguna evidencia historica.

## Verificacion y controles humanos

Ejecutar brujula-semantica, revisar casos, implementar pruebas tras aprobar alcance, registrar Red/Green solo si ocurrieron, ejecutar checks y navegador con salida nueva. Calidad y seguridad revisan; humano autoriza commit/publicacion/fusion. Pruebas ejecutadas y limites en docs/taller-6/s02-resultados.md; no marcar aprobacion humana o fusion antes de ocurrir.

## Ejecucion y controles

Rama taller6/002-costo-maximo creada desde origin/main 0985273541e21579009cb6179546b9f3db845f7e, sin S01. El filtro mantiene el ultimo limite valido hasta un envio valido; Quitar limite conserva los otros filtros. Pruebas iniciales antes del parser y regresion final registradas por separado. Browser usa API real via proxy de pruebas 5188 -> FastAPI 8000, sin cambiar CORS. Puertos ocupados detienen el runner; solo limpia procesos propios.

Codex aplica opita-frontend y brujula-semantica; el CLI convierte AC en casos sin ejecutarlos. El orquestador y especialistas producen reportes separados, sin escritura/shell ni comunicacion lateral; modo y resultados autenticos documentados. No atribuir implementacion de parches a los roles de revision. Modelo configurado qwen3.5:4b local; no descargar ni sustituir modelos.

Dos mecanismos: contratos/pruebas unitarias y regresion; navegador con API/demo, teclado y estados de validacion. Revision LLM es complementaria y no aprueba prosa automaticamente. Factor Ambar 3/9 aprobado; Coeficiente Murcielago sigue sin formula oficial documentada, no se inventa. Riesgos: conflicto futuro de main.jsx al integrar S01, errores del runner o diferencias de navegador; no fusionar S01 en esta rama. Nuevas revisiones necesarias si cambia main.

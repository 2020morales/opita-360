# Plan tecnico 004

Factor Ámbar: 5/9

Estimacion del equipo propuesta: 1-3 cambio localizado; 4-6 estado persistente local o compatibilidad entre componentes; 7-9 varias dependencias o infraestructura. El PDF solo fija 1-9, no define niveles. Estado: aprobado por el usuario.

## Decisiones propuestas

Mantener React/Vite y FastAPI. Usar funciones puras cuando haya logica reutilizable y conservar API/demo. Revisar accesibilidad y entradas invalidas. Campo municipio opcional, filtrar antes de seleccionar; no cambiar la excepcion presupuestaria existente.

## Archivos de implementación y verificación

- backend/app/main.py
- frontend/src/main.jsx
- frontend/src/recommendation-municipality.js (helper nuevo) y styles.css.
- backend/tests/test_recommendation_municipality.py; frontend/tests/recommendation-municipality.test.js.
- harness/s04_browser.py y frontend/tests/s04.vite.config.mjs.
- Memoria/README, manifiesto/contexto de revisión y correcciones mínimas del arnés; artefactos SDD de S04.

## Verificacion y controles humanos

Ejecutar brujula-semantica, revisar casos, implementar pruebas tras aprobar alcance, registrar Red/Green solo si ocurrieron, ejecutar checks y navegador con salida nueva. Calidad y seguridad revisan; humano autoriza commit/publicacion/fusion. Ejecuciones auténticas en docs/taller-6/s04-resultados.md; sin declaración de pruebas humanas no ejecutadas.

## Secuencia y arquitectura aplicadas

Rama taller6/004-filtro-municipio desde origin/main 0985273541e21579009cb6179546b9f3db845f7e. No se fusionan ramas S01–S03. API: TripRequest.municipality opcional StrictStr -> candidatos del municipio -> intereses -> recuperación dentro de candidatos -> presupuesto/días originales. Demo: helper territorial -> reglas demo anteriores. Selector propio del formulario, sin acoplarlo al catálogo. No se prometen algoritmos API/demo idénticos.

Agentes: orquestador, backend, frontend, calidad y seguridad; modelo local qwen3.5:4b, write=false/shell=false. Skills opita-backend, opita-frontend y brújula-semántica. Contexto del operador con resultados realmente ejecutados; inventario y LLM se distinguen en informes. MCP no es necesario para cambiar esta API local; no atribuir una sesión nueva si no se ejecuta.

La rama main aún contenía la prueba que exigía cinco drafts y el resumen fijo new_feature_tests=not_executed. Se adaptan al ciclo aprobado y a un estado indeterminado, separando diseños del registro de ejecución. Es una corrección del arnés en esta rama, sin fusionar S03 ni ampliar permisos.

Riesgos: recuperación global indebida, tratar Todos como municipio literal, afectar presupuesto, acoplar selectores o divergencia de versiones entre PR paralelos. Se cubren con API/unidades/navegador y regresión. Datos personales/rutas locales no se añaden a informes. Preservar evidencias originales y registrar los fallos.

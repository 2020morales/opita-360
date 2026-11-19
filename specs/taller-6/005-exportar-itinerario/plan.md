# Plan técnico S05

Factor Ámbar: 3/9 aprobado: cambio localizado React/Blob, sin infraestructura. La escala es estimación del equipo, no fórmula inventada del profesor.

1. Rama taller6/005-exportar-itinerario desde origin/main actualizado; sin fusionar ramas paralelas.
2. Especificar contrato y convertir cuatro criterios con brújula-semántica.
3. Pruebas unitarias antes del helper; conservar fallo observado, sin afirmar TDD para componentes no probados antes.
4. Helper puro serializeItinerary y adaptador downloadItinerary; estado explícito del origen y error en React; botón accesible deshabilitado al iniciar/cargar.
5. Probar API real y demo mediante proxy exclusivo del navegador; inspeccionar archivo descargado y tráfico de exportación; regresión y build.
6. Revisión de roles por orquestador, contraste del operador, evidencias nuevas, publicación autorizada y PR independiente main. No merge.

Archivos: frontend/src/export-itinerary.js, main.jsx, styles.css, tests/export-itinerary.test.js y s05.vite.config.mjs; harness/s05_browser.py y contexto mínimo del runtime; docs/specs S05. Backend sin cambios.

Calidad: unidades/contratos y navegador real. Adaptación mínima del test antiguo que exigía cinco borradores, y del contexto que negaba pruebas específicas sin fundamento. El manifiesto conserva permisos sin shell/escritura.

Riesgos: exportar estado distinto del visible, origen inferido incorrectamente, redondeo, URL revocada prematuramente, descarga bloqueada y conflictos futuros en main.jsx. Mitigación: snapshot del resultado, origen explícito, números sin recalcular, revocación diferida, mensaje de error, prueba de archivo real y revisión humana al integrar ramas.

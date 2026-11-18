# Plan tecnico 004

Factor Ámbar: 5/9

Estimacion del equipo propuesta: 1-3 cambio localizado; 4-6 estado persistente local o compatibilidad entre componentes; 7-9 varias dependencias o infraestructura. El PDF solo fija 1-9, no define niveles. Estado: pendiente de aprobacion especifica.

## Decisiones propuestas

Mantener React/Vite y FastAPI. Usar funciones puras cuando haya logica reutilizable y conservar API/demo. Revisar accesibilidad y entradas invalidas. Campo municipio opcional, filtrar antes de seleccionar; no cambiar la excepcion presupuestaria existente.

## Archivos previstos (todavia sin modificar)

- backend/app/main.py
- frontend/src/main.jsx
- Pruebas unitarias/API/browser que correspondan a los criterios.

## Verificacion y controles humanos

Ejecutar brujula-semantica, revisar casos, implementar pruebas tras aprobar alcance, registrar Red/Green solo si ocurrieron, ejecutar checks y navegador con salida nueva. Calidad y seguridad revisan; humano autoriza commit/publicacion/fusion. No se ha ejecutado ninguna prueba de esta funcionalidad.

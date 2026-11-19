# Pull Request preparado — S03 / 003

Estado real: rama publicada origin/taller6/003-favoritos. El conector rechazó crear el PR con HTTP 403, Resource not accessible by integration. No se acredita número ni URL de PR. Commit de implementación: 59c4c6f1e938444ab5d39e00314e07b82a83ae97. Esta actualización documental registra el bloqueo posterior.

Base main; origen taller6/003-favoritos, desde 0985273541e21579009cb6179546b9f3db845f7e. No incorpora S01 ni S02. [Crear comparación/PR](https://github.com/2020morales/opita-360/compare/main...taller6/003-favoritos?expand=1). Crear como borrador hasta aceptación humana final. [Respuesta real](https://github.com/2020morales/opita-360/blob/taller6/003-favoritos/docs/taller-6/ejecuciones/20261118T063536Z-63e76614/s03-pr-create-error.json).

## Título

feat(S03): guardar destinos favoritos en el navegador

## Descripción lista para copiar

Antes el corazón solo cambiaba una clase CSS. S03 guarda favoritos locales por ID con formato versionado; conserva los datos tras recargar el mismo origen; añade Solo favoritos combinado con municipio, categoría y búsqueda, y permite quitar con foco estable.

La inicialización solo lee. Se valida JSON/esquema e IDs, se conservan IDs desconocidos sin mostrarlos y solo se escribe la clave opita360:favorites:v1 después de una acción del usuario. Ante fallos de acceso/lectura/escritura se mantiene estado de sesión y aviso sin prometer persistencia. No se modifica backend/API/CORS, no se incorporan S01/S02 y no cambian evidencias T4/T5. Factor Ámbar aprobado 4/9.

Pruebas auténticas: 99 aprobadas (38 arnés, 34 agentes, 8 API, 19 frontend), 29 controles de navegador y build código 0. [Resultados y trazabilidad](https://github.com/2020morales/opita-360/blob/taller6/003-favoritos/docs/taller-6/s03-resultados.md). Se conservan el fallo inicial por módulo ausente y las revisiones LLM erróneas. Se corrigieron dos defectos de contexto del arnés con sus regresiones; dos rondas reales de cinco inferencias no equivalen a aprobación humana.

Pendientes: aceptación final, lector de pantalla humano, auditoría WCAG integral y compatibilidad fuera de Chrome. Persistencia por origen/perfil; no sincronización inmediata entre pestañas. La prosa del modelo sigue requiriendo contraste. Si main incorpora S01/S02 antes de S03, revisar cambios concurrentes. No fusionar automáticamente.

Texto exigido por la consigna: «Spec revisada por el profesor». No hay revisión docente acreditada; no se afirma que haya ocurrido.

## Estado observado en el ensayo de integración

PR real: https://github.com/2020morales/opita-360/pull/7. Continúa abierto; esta combinación es local, sin merge del PR ni aceptación docente acreditada. El bloqueo histórico del conector no significa que el PR siga sin existir. Resultados conjuntos: docs/taller-6/integracion-final-resultados.md.

# Pull Request preparado — S02 / 002

Estado real: rama publicada en origin/taller6/002-costo-maximo. El conector rechazó crear el PR con HTTP 403, Resource not accessible by integration. No hay número ni URL de PR acreditados. Commit de implementación: 53816ea978031ddb34bf5d8127b93c9146c16a1b. Esta actualización documental registra el bloqueo posterior.

Base: main. Origen: taller6/002-costo-maximo. La rama parte de 0985273541e21579009cb6179546b9f3db845f7e (PR #4 integrado), sin S01/PR #5. No fusionar automáticamente.

[Crear comparación/PR](https://github.com/2020morales/opita-360/compare/main...taller6/002-costo-maximo?expand=1). Crear como borrador hasta aceptación humana final. Ver [bloqueo real](../../../docs/taller-6/ejecuciones/20261118T054205Z-81999358/s02-pr-create-error.json).

## Título propuesto

feat(S02): filtrar destinos por costo máximo

## Descripción lista para copiar

El catálogo no permitía limitar el costo por destino. Se añade un filtro local inclusivo combinado con municipio, categoría y búsqueda. Vacío no limita; cero muestra lista vacía con recuperación; valores negativos/no numéricos muestran error sin perder el último límite válido.

Alcance S02 únicamente: React y helper de filtros; API/backend/CORS y evidencias T4/T5 sin cambios. No incorpora S01 ni los 16 archivos excluidos. Factor Ámbar aprobado: 3/9.

Pruebas reales: 93 aprobadas (36 arnés, 34 agentes, 8 API, 15 frontend), 18 controles de navegador y build código 0. Comandos: python -B -m harness checks --scope all y python -B -m harness.s02_browser. Informes y trazabilidad en docs/taller-6/s02-resultados.md. Se conserva el fallo inicial por parser todavía no implementado y su corrección. El conversor de criterios y el orquestador se ejecutaron; cinco inferencias locales reales produjeron también errores que se contrastaron y no se aplicaron.

Browser: Chrome headless con API real a través de proxy exclusivo de pruebas 5188 -> FastAPI 8000 y escenario offline. No acredita producción ni WCAG completa. Aceptación humana, lector de pantalla y compatibilidad fuera de Chrome pendientes; avisos conocidos de lucide-react conservados. Si S01 entra antes a main, revisar cambios concurrentes antes de fusionar S02.

Texto requerido por la consigna: «Spec revisada por el profesor». La revisión docente no está acreditada; no se afirma que haya ocurrido. Este PR no debe fusionarse automáticamente.

## Estado observado en el ensayo de integración

PR real: https://github.com/2020morales/opita-360/pull/6. Continúa abierto; esta combinación es local, sin merge del PR ni aceptación docente acreditada. El bloqueo histórico del conector no significa que el PR siga sin existir. Resultados conjuntos: docs/taller-6/integracion-final-resultados.md.

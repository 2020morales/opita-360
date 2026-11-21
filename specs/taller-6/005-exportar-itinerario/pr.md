# PR S05 preparado para creación manual

Estado real: commit 9d063547ec983ff480a9057cdfbd8fc9a503d0e3 publicado en origin/taller6/005-exportar-itinerario. El conector rechazó crear el PR con HTTP 403, Resource not accessible by integration. No hay número/URL de PR acreditados en este registro. Base: main. No merge.

[Crear PR](https://github.com/2020morales/opita-360/compare/main...taller6/005-exportar-itinerario?expand=1)

## Título
feat(S05): exportar itinerario JSON versionado

## Descripción lista para pegar
S05 permite descargar opita360-itinerario.json local, UTF-8 y format_version=1, con origen api/demo explícito. Conserva destinos ordenados, textos y totales de la última propuesta mostrada sin recalcular; editar el formulario no altera la copia. Botón deshabilitado sin propuesta o mientras se genera otra; URL Blob liberada y mensaje si la descarga no puede iniciarse.

Cuatro criterios y Factor Ámbar 3/9 aprobados por el usuario. Rama independiente desde main 0985273541e21579009cb6179546b9f3db845f7e, sin incorporar S01–S04, sin nuevas dependencias ni backend modificado. Históricos T4/T5 y 16 archivos excluidos conservados.

Validación real: 96 tests aprobados —37 arnés, 34 agentes, 8 backend y 17 frontend, ocho nuevos S05—, 14 controles Chrome aprobados y build exitoso. Navegador descarga y analiza archivos con API real mediante proxy de prueba, verifica recuperación demo, teclado, nombre accesible, anchuras 360/1280, propuesta anterior y ausencia de transporte al exportar. Fallos iniciales y correcciones conservados.

Orquestador y especialistas ejecutaron cinco inferencias locales; prosa y citas incorrectas quedaron contrastadas, sin aceptación automática. Sin nueva ejecución MCP.

[Evidencias y límites](https://github.com/2020morales/opita-360/blob/taller6/005-exportar-itinerario/docs/taller-6/s05-resultados.md).

Pendientes: revisión humana/docente acreditada, lector de pantalla y WCAG completa, Firefox/Safari y CI remoto. Advertencias de TestClient/httpx y lucide-react registradas, sin migración incidental. Revisar conflictos futuros con ramas paralelas antes de merge.

Texto solicitado «Spec revisada por el profesor»: no acredita aprobación docente; esa evidencia sigue pendiente. No merge automático.

## Estado observado en el ensayo de integración

PR real: https://github.com/2020morales/opita-360/pull/9. Continúa abierto; esta combinación es local, sin merge del PR ni aceptación docente acreditada. El bloqueo histórico del conector no significa que el PR siga sin existir. Resultados conjuntos: docs/taller-6/integracion-final-resultados.md.

## Contraste posterior con la consigna original

Los apartados anteriores conservan la preparación y sus limitaciones históricas.
PR real: https://github.com/2020morales/opita-360/pull/9. En la consulta de esta revisión figura fusionado.

La fusión no acredita revisión del profesor. El PDF exige la frase «Spec revisada
por el profesor» en la descripción; la descripción consultada no la contiene.
Texto propuesto para una actualización humana, **no publicada por esta revisión**:

> Texto exigido por la consigna: «Spec revisada por el profesor». La revisión
> docente no está acreditada en las evidencias consultadas; pendiente de confirmación.

No se edita el PR remoto ni se atribuye al profesor una aprobación no demostrada.
Contraste y consulta verificable: docs/taller-6/revision-requisitos/informe.md.

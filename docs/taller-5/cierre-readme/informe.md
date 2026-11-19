# Cierre del hallazgo documental — Taller 5

## Alcance

Rama taller5/correccion-rubrica. Único archivo preexistente modificado en esta fase:
agents/README.md. Sin cambios de código, modelos, dependencias, funcionalidades,
PDF, Talleres 4 y 6 ni main. Sin staging, commit, push o merge.

El ejemplo anterior apuntaba al navegador fallido y a una salida existente.
Ahora utiliza checks-final.json y browser-final/after.json, aprobados para el
README final, y genera el nombre release-<GUID>.json mediante PowerShell.
Puede repetirse con un destino nuevo automáticamente. Una modificación de las
fuentes exige volver a generar los informes: el README forma parte del snapshot.

## Ejecución real y trazabilidad

- Suites finales: 42 pruebas de suite de agentes (incluidos dos oráculos API) y
  8 backend. Compilación backend y build frontend: códigos 0.
- Chrome final: 14/14 controles aprobados, sin error fatal.
- Comando del README ejecutado: ready_for_human_review, human_approval=pending,
  publication_allowed=false. Informe real: release-569783e81dc04196bed70848989da64a.json.
- Siete enlaces del PDF comprobados de nuevo mediante GET del conector GitHub:
  todos accesibles; links.json.
- PDF: ocho páginas, cuatro secciones, FET-QX7 en encabezado, lectura estricta y
  renderizado de todas las páginas. No se regeneró: conserva exactamente su SHA.
- git diff --check: código 0. Los avisos LF/CRLF no se ocultan ni se interpretan
  como errores nuevos de espacios finales.

Evidencias finales: checks-final.json, browser-final/after.json y sus capturas,
release-<GUID>.json y verificacion-final.json. Los informes checks.json,
browser/after.json y release-ejemplo-nuevo.json corresponden a la corrección
intermedia anterior al nombre automático; se conservan y no se confunden con
la ejecución del README final. No se suman ejecuciones como pruebas distintas.

preservacion-inicial.json y verificacion-final.json comprueban que solo cambió
README entre los archivos preexistentes inventariados. Los otros 105 archivos,
incluido el fallo original, conservaron sus bytes. Todas las referencias locales
de ramas permanecen iguales y no hay archivos preparados en staging.

La comparación con el snapshot utilizado por el PDF solo difiere en agents/README.md.
Las implementaciones y pruebas no cambiaron; las nuevas ejecuciones confirman las
mismas cantidades del PDF. No se afirma que los hashes completos sean idénticos.
No se repitieron inferencias LLM/MCP ni instalación de dependencias.

## Seis criterios y pendientes externos

| Criterio | Respaldo verificable | Estado del enunciado completo |
|---|---|---|
| Calidad 25% | PDF pp.6–7, matriz-calidad.md, suites y puerta conjunta | Parcial por ITC/MutaGato pendientes; controles técnicos demostrados |
| Agentes 20% | PDF pp.2–3, manifiesto y contratos | Cinco roles completos; cronista-lunar y aprobación docente pendientes |
| Diagramas 20% | PDF pp.4–5 y arquitectura.md | Diagramas legibles; pausa solo propuesta y R-27 sin confirmar |
| Herramientas/permisos/modelo 15% | PDF pp.1–3, manifiesto y pruebas de denegación | Modelo/permisos reales; Codex y escritura-orbital pendientes |
| Diferencias 10% | PDF p.8, comparacion-referencia.md y fuentes fijadas | Comparación técnica respaldada; sin confirmación atribuida al profesor |
| Documento 10% | Validación PDF, preservación del hash y siete enlaces | Cumple verificaciones técnicas; revisión humana final pendiente |

Los seis criterios tienen respaldo documental o ejecutable, pero eso no significa
que todos los requisitos estén cumplidos. No se inventan definiciones ni aprobación
del profesor. La CLI no protege main ni autentica a quien aprueba. Persisten los
límites declarados de accesibilidad completa, compatibilidad, mutación y persistencia.

## Recomendación

Hallazgo documental cerrado. La rama está técnicamente lista para proponerse en
un Pull Request de revisión, con sus limitaciones explícitas y previa autorización
del usuario para preparar commit y publicar. No equivale a autorización de merge,
aceptación docente ni entrega Excelente garantizada. Se mantiene la estimación
orientativa 4,35/5: esta corrección no justifica incrementar la nota estimada.

# Preparación de publicación — corrección Taller 5

Rama autorizada: taller5/correccion-rubrica. Esta nota registra la preparación;
el resultado efectivo de commit/push se consulta en Git y en el informe del operador.
No constituye aprobación del profesor, autorización de merge ni calificación.

## Verificaciones previas

- Se validaron los checks finales y la puerta conjunta de cierre-readme contra
  el contenido actual: 42 pruebas de suite de agentes y 8 backend aprobadas,
  compileall/build con código cero, 14 controles Chrome aprobados. La puerta
  solo permite ready_for_human_review y mantiene human_approval=pending.
- PDF aprobado de ocho páginas: SHA-256
  4ddb5b4d7eb56d1264ee9bac66a0146e1247eeed57f30d69cba89d05a9137915.
  Cuatro secciones, FET-QX7, diagramas y siete enlaces comprobados en cierre-readme.
- Las notas y el PDF describen la fase de validación previa a publicación. Sus
  menciones a trabajo local se conservan como estado de ese momento; no sustituyen
  consultar el commit y la rama publicados. No se reescriben resultados históricos.
- Sin rutas ajenas a agents/ y docs/taller-5/ en el conjunto preparado.
  Escaneo acotado de claves privadas, tokens habituales y rutas de usuario en
  los textos candidatos: sin coincidencias. No garantiza ausencia universal.
- Sin modificaciones de frontend/backend turístico, dependencias, modelos,
  Talleres 4 y 6 o main. No se prepara el PDF antiguo Entorno_de_trabajo_OPITA_360.pdf.

## Preservación de evidencia y finales de línea

La configuración local core.autocrlf=true convertiría 13 informes JSON al ejecutar
un add convencional. Sus hashes registrados dejarían de coincidir con los bytes
publicados. Se preparan con `git -c core.autocrlf=false add -- <rutas revisadas>`:
solo afecta ese comando, no cambia configuración global ni los archivos originales.

Se comprobó igualdad binaria de cada archivo preparado mediante `git show :ruta`
frente a los bytes del archivo verificado, incluido el PDF. No se normalizan logs
ni se eliminan fallos o capturas de ejecuciones anteriores.

`git diff --cached --check` estándar devuelve código 2 por los CR de los JSON
originales preservados. **No se presenta como aprobado.** La comprobación
`git -c core.whitespace=cr-at-eol diff --cached --check` devuelve código 0:
no detecta otros defectos de espacios al reconocer CRLF. No se oculta ni modifica
la salida histórica; la excepción corresponde al formato de evidencia, no a
un fallo de pruebas o código turístico. Verificar hashes antes de renormalizar
cualquier informe en operaciones futuras.

## Pendientes que permanecen

Aceptación de Codex/controlador frente a las herramientas enumeradas; definición
de escritura-orbital, ITC/MutaGato y cronista-lunar; confirmaciones docentes R-27
y leyendas. Pausa del Colibrí solo propuesta, no ejecutada ni demostrada como
beneficio. Sin aprobación humana final, WCAG completa, todos los navegadores,
mutación o persistencia PostgreSQL probadas. La CLI no protege main en GitHub.
La estimación 4,35/5 sigue siendo orientativa, no nota ni garantía de Excelente.

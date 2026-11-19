# Auditoría final — Taller 5 · FET-QX7

Rama taller5/correccion-rubrica; HEAD 8cce952bace0763ac5e96208c70e93a304979fb4.
No se modifica código ni el PDF en esta auditoría; se añaden informes nuevos.
Sin staging, commit, push ni merge. Talleres 4 y 6, main y rama original intactos.

## Repetición auténtica de verificaciones

- agents.verify: 42 pruebas de suite de agentes (incluye dos oráculos API) y
  8 pruebas backend; sintaxis backend y build frontend con código cero. checks.json.
- Chrome headless, con permisos de proceso necesarios: 14/14 controles, sin fallo
  fatal. browser/after.json y capturas. No se encontró fallo nuevo en esta ejecución.
- Puerta conjunta: release.json = ready_for_human_review, aprobación pendiente,
  publicación deshabilitada. Las suites y navegador pertenecen al mismo contenido.
- PDF: ocho páginas, cuatro secciones, encabezado FET-QX7, apertura estricta y
  renderizado de todas las páginas. Mismo SHA que la validación final anterior:
  4ddb5b4d7eb56d1264ee9bac66a0146e1247eeed57f30d69cba89d05a9137915.
- Siete enlaces del PDF consultados de nuevo mediante GET de GitHub: 7/7 accesibles.
- git diff --check: código 0; avisos LF/CRLF permanecen documentados. Escaneo
  acotado de patrones sensibles en archivos cambiados/nuevos: sin coincidencias.
- Conservación de 41 artefactos inventariados antes de la mejora y revisión de
  30 evidencias históricas. Las diferencias LF/CRLF históricas no se normalizan.

No se repiten inferencias LLM/MCP ni instalación limpia. Los informes previos
identifican cinco inferencias y dos sesiones reales de su versión; no se presentan
como una nueva ejecución del controlador completo. No se ejecuta la referencia.

## Seis criterios

| Criterio | Estado completo del enunciado | Evidencia y pendiente |
|---|---|---|
| Calidad 25% | Parcial; controles técnicos demostrados | PDF pp.6–7; matriz-calidad.md; quality_gates.py:13, release_gate.py:17 y tests reales. ITC/MutaGato sin definición verificable; no certificación inventada |
| Agentes 20% | Parcial | PDF pp.2–3 y manifest.v1.json: cinco roles con invocación, entradas/salidas, permisos/modelo. cronista-lunar pendiente; sin aprobación docente |
| Diagramas 20% | Parcial; estructura/flujo demostrados | PDF pp.4–5: centro, ambos stacks, controles, parada y decisiones. Pausa de 7 s solo propuesta; R-27 no acreditada |
| Herramientas/permisos/modelo 15% | Parcial | PDF pp.1–3: listas reales y Qwen justificado. Aceptación de Codex/controlador frente a herramientas enumeradas y escritura-orbital pendientes |
| Diferencias 10% | Comparación técnica demostrada; requisito textual parcial | PDF p.8; comparacion-referencia.md:14; fuentes fijadas. Frontend usa otra rama, explicitada. No confirmación del profesor |
| Documento 10% | Cumple comprobaciones exigidas | Ocho páginas, cuatro secciones, diagramas y siete enlaces funcionales; revisión humana final pendiente |

Se valora diseño: no se exige implementar agentes autónomos ni todos los ejemplos
de cobertura, TDD, CI y mutación. Su ausencia no es una penalización automática.
La aprobación del usuario no sustituye confirmaciones atribuidas al profesor.

## Hallazgo documental antes de publicar

El ejemplo de release_gate en agents/README.md apunta a
mejora-tecnica/browser/after.json, que conserva el fallo CDP inicial. La ejecución
aprobada anterior utiliza browser-02/after.json; la auditoría nueva usa
auditoria-final/browser/after.json. Además, el destino release.json ya existe y
se rechaza deliberadamente para preservar evidencia. No es un fallo de la puerta:
el ejemplo no sirve para obtener un nuevo resultado aprobado al copiarlo literalmente.
Corregir el ejemplo para usar entradas aprobadas y un destino nuevo; no cambiar
ni borrar el informe fallido. No se modifica el README durante esta auditoría.

## Recomendación y riesgos

Pruebas técnicas aprobadas, sin error crítico nuevo demostrado. Recomiendo
corregir primero el ejemplo del README y después publicar como rama/PR de revisión,
con pendientes explícitos; no presentarla como entrega Excelente totalmente cerrada.
La CLI no protege main ni autentica aprobaciones. El modelo puede equivocarse;
el mismo modelo no garantiza independencia; MCP no es sandbox OS. Sin WCAG
completa, todos los navegadores ni persistencia PostgreSQL probados. La revisión
humana y las aclaraciones docentes siguen pendientes.

Se mantiene la estimación anterior **4,35/5**, orientativa. Repetir pruebas con
éxito confirma evidencia, no justifica subir la nota. No garantiza evaluación docente.

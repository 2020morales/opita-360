# Revisión de los seis elementos — Taller 6 de OPITA 360

## Alcance y fuente original

Trabajo local en `fix/revision-taller-6`, worktree independiente creado desde
`origin/main` a5f3e3a218e32836388dc289509827a01932bdbe (PR #12 integrado).
No se alteran main, las ramas originales ni los worktrees anteriores. No se
realizan staging, commits, push ni creación/edición de Pull Requests.

Se leyeron las **siete páginas completas** de Proyecto_Integrador (2).pdf.
SHA-256: `65abca064398724c1eecd96e23c5effb778a3f6ded4bf231d0a5aca930d52ec0`.
El archivo coincide con la fuente utilizada en los requisitos existentes. El PDF
no se copia al repositorio; fuente-oficial.json registra páginas y significado.

**Los seis elementos son requisitos explícitos. No son seis invenciones que
haya que eliminar.** Una cita del enunciado y una certificación realmente emitida
son cosas distintas. El PDF por sí solo no acredita una revisión del profesor.

## Dictamen por elemento

| Elemento | PDF | Estado encontrado y problema real | Tratamiento |
|---|---:|---|---|
| Skill brújula-semántica | p.2 | Obligatoria; front matter con nombre exacto y carpeta ASCII legítima. Conversor determinista existente; no es una prueba ejecutada | Se conserva skill, core.compass y sus validaciones. Se ejecutó cases para las cinco specs: 28 diseños, execution=not_run |
| Arnés certificado por el profesor (código FET-ARN-42) | p.2 | La frase es obligatoria como texto, pero no prueba certificación. README y harness/README ya la citaban con advertencia: no se encontró una certificación falsa afirmada sin ese contexto | Se conserva el literal; se hace prominente el estado docente no acreditado y se enlaza esta revisión. No se inventa un certificado |
| Matriz Halcón | p.3 | Sección obligatoria que relaciona skills con agentes. La tabla existe en harness/README, no es un índice de calidad ni una aprobación | Se conserva la tabla y las tres skills; sin cambiar manifiesto, modelos ni permisos |
| Factor Ámbar | p.3 | Complejidad obligatoria 1–9 en cada plan; specs 001..005 tienen 3,3,4,5,3. Validación de enteros/rango y coincidencia con plan ya implementada | Se conservan valores, justificaciones y tests. No se cambia el alcance aprobado ni se atribuye una fórmula oficial |
| Spec revisada por el profesor | p.4 | Frase solicitada en cada PR. Los cinco pr.md ya la distinguen de una revisión acreditada. Las descripciones reales de PR #5–#9 consultadas no contienen el literal: incumplimiento textual externo, no prueba de revisión inexistente | Se añade estado real fusionado y texto propuesto con aclaración, preservando antecedentes. PR remotos sin editar; publicación de esa actualización requiere autorización |
| Coeficiente Murciélago | p.4 | El PDF pide reportarlo por mecanismo, pero no da fórmula, escala ni protocolo. Los documentos no inventan valores | Se conserva el requisito y se explicita por mecanismo que no se ha calculado por falta de definición verificable. No usar tests aprobados como coeficiente |

No se detectaron afirmaciones positivas de certificación/revisión docente sin
matizar en los archivos textuales actuales donde aparecen esos dos literales.
La corrección refuerza esa distinción y evita que se interpreten los antecedentes
históricos como el estado actual. No se introduce un requisito nuevo.

## Archivos corregidos

Solo ocho archivos preexistentes, mediante adiciones sin borrar información:

- README.md: estado docente y alcance actual; enlace al contraste.
- harness/README.md: misma distinción y contexto de integración; Matriz Halcón intacta.
- docs/taller-6/requisitos-oficiales.md: correspondencia con páginas y estado del
  Coeficiente Murciélago por mecanismo.
- Los cinco specs/taller-6/*/pr.md: PR real fusionado, antecedentes identificados
  y propuesta de texto para una revisión humana de la descripción.

Las menciones anteriores a trabajo local o PR sin crear se conservan como
antecedentes. La consulta GET confirma PR #5–#9 fusionados; una fusión no demuestra
revisión académica. Consulta exacta y cuerpos recibidos: consulta-pr.json.

Nuevos archivos: esta carpeta de auditoría y siete carpetas de ejecución únicas.
Inventario de términos: inventario-final.json; script reproducible:
inspeccionar_requisitos.py. Recorrió 352 archivos textuales/PDF/PPTX rastreados;
141 contienen alguno de los seis términos o su campo estructurado amber.
Las coincidencias de informes históricos y hashes de skills no son errores por sí mismas.
Se inspeccionaron texto de PDF y XML de las siete diapositivas/notas; no se aplicó OCR.
No se modifican presentación, reflexiones personales ni documentación/evidencias T4/T5.

## Pruebas y funcionamiento comprobado

| Verificación ejecutada | Resultado real | Evidencia |
|---|---|---|
| Instalación desde lockfile y caché local | npm ci --offline --ignore-scripts: código 0, 20 paquetes; sin red ni cambio de dependencias declaradas | instalacion.json |
| Suite harness | 46 pruebas aprobadas | ../ejecuciones/20261120T065100Z-9f589ed0/checks.json |
| Suite agentes históricos, solo lectura de artefactos | 34 pruebas aprobadas | mismo checks.json |
| Backend | 22 pruebas aprobadas | mismo checks.json |
| Frontend | 38 pruebas aprobadas | mismo checks.json |
| Compilación frontend | Código 0 | mismo checks.json |
| harness validate | Cinco specs válidas: 10,4,5,5,4 criterios | verificacion-final.json; es validación estructural, no aceptación de funcionalidades |
| cases para 001–005 | 28 diseños; no ejecuta esos casos | Cinco cases.json nuevos |
| review --spec 005 --approved | Cinco reportes inventory, sin inferencia ni MCP, revisión humana pendiente | ../ejecuciones/20261120T065244Z-a8f4b690/review.json |
| git diff --check | Código 0; avisos LF/CRLF documentados | verificacion-final.json |
| Preservación | 358 archivos rastreados sin cambio; solo ocho documentos añadidos; referencias locales intactas | preservacion.json y verificacion-final.json |

Total: **140 pruebas automatizadas aprobadas**, no 168: generar 28 diseños no
los convierte en pruebas ejecutadas. No hubo fallo de suite ni build. Persisten
advertencias de lucide-react/Starlette, sin actualizar dependencias para ocultarlas.
Hubo un error auxiliar de verificación por usar un nombre de inventario incorrecto;
se registró y repitió correctamente, sin alterar el inventario: incidente-verificacion.json.

No se ejecutaron navegador, LLM, MCP ni detección nativa de skills en Codex nuevos:
no son necesarios para una corrección documental y no se les atribuyen resultados.
Los mocks de los tests existentes son fixtures unitarios, no inferencias simuladas.
El runtime, AGENTS.md, reglas, skills, planes y permisos se conservan byte a byte.
No cambió ningún requisito funcional ni contrato: no corresponde modificar sus
validaciones o pruebas existentes solo para eliminar palabras exigidas por el PDF.

## Pendientes y propuesta de revisión humana

1. Pedir definición de fórmula/escala del Coeficiente Murciélago; mientras tanto
   reportar el valor como no calculado, por mecanismo.
2. Obtener evidencia de certificación o revisión si el profesor las realiza.
   No deducirlas de FET-ARN-42, una frase, tests verdes o PR fusionados.
3. Revisar la propuesta para añadir el literal con aclaración a las descripciones
   de PR #5–#9. No se enviaron mensajes ni se editaron PR existentes.
4. Revisar este diff antes de crear un PR de fix/revision-taller-6. No se publica
   ni se integra automáticamente y no se certifica cumplimiento global del Taller 6.

Las reflexiones y presentación de los integrantes permanecen intactas. Esta revisión
no inventa experiencias personales, aprobaciones ni una calificación del profesor.

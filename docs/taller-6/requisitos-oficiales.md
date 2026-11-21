> Este texto conserva el estado de preparación original. La revisión vigente de los seis requisitos, el PDF consultado y las evidencias están en [revision-requisitos/informe.md](revision-requisitos/informe.md). Las menciones a trabajo pendiente pertenecen a aquella fase.

> Actualización: este documento conserva el estado de preparación original.
> El contraste vigente y sus pruebas están en [revision-requisitos/informe.md](revision-requisitos/informe.md).

# Correspondencia con el PDF oficial

Fuente leída: Proyecto_Integrador (2).pdf, siete páginas. Esta fase prepara el arnés; no entrega todavía las cinco specs implementadas.

- Memoria: AGENTS.md actualizado; instrucciones específicas existentes y harness/AGENTS.md.
- Tres skills: .agents/skills, incluida brújula-semántica. Propósitos e invocaciones en harness/README.md.
- Matriz Halcón: skill -> agente.
- Agentes: cinco roles con modelo, herramientas y listas mínimas; revisión humana, sin escritura turística.
- SDD propio: spec.json/spec.md, plan.md con Factor Ámbar, tasks.md sin completar y pr.md pendiente.
- Calidad: pruebas ejecutables y revisión trazable. Registrar uso por cada spec cuando se implementen.
- Coeficiente Murciélago: pendiente de fórmula oficial; no inventar escala.
- Main: los entregables deberán integrarse con autorización; no se permite hacerlo ahora.
- PR: el PDF pide «Spec revisada por el profesor»; no atribuir esa revisión sin evidencia.
- Presentación: 15 minutos + 5 preguntas; reservar 14-15 para Minuto Coral. Portada pide «Contenido aprobado previamente por el profesor» y cierre «Esperamos que al profesor le guste nuestro arnés». La primera frase requiere confirmar aprobación real.
- Reflexiones: PDF grupal máximo tres páginas, nombre y Perfil Nebulosa A/B/C por integrante; antes, ahora y proceso con ejemplos propios. El PDF no define A/B/C. Solo se puede preparar estructura: cada integrante redacta su experiencia sin IA si debe declarar «sin ayuda de inteligencia artificial, como pidió el profesor». La frase «Esta reflexión fue validada por el profesor» requiere validación real.
- El texto literal FET-ARN-42 está identificado como requisito, no como evidencia de certificación.
- Spec Kit no se utiliza; no se añade una constitución de relleno.

## Contraste vigente de los seis términos

| Elemento | Página del PDF original | Tratamiento |
|---|---:|---|
| brújula-semántica | 2 | Skill obligatoria; conservar nombre, conversor y trazabilidad AC/TC |
| Arnés certificado por el profesor (código FET-ARN-42) | 2 | Texto literal requerido; certificación docente no acreditada |
| Matriz Halcón | 3 | Conservar relación skill/agente; no es una nota ni certificación |
| Factor Ámbar | 3 | Complejidad 1–9 en cada plan; valores del equipo, no validación docente |
| Spec revisada por el profesor | 4 | Frase solicitada en cada PR; citar como requisito y declarar revisión pendiente si no hay evidencia |
| Coeficiente Murciélago | 4 | Reportar por mecanismo; sin fórmula en el PDF, no inventar valor |

La revisión encontró PR #5–#9 fusionados y sin la frase docente en sus descripciones
consultadas. Sus pr.md conservan antecedentes y añaden un texto propuesto con
aclaración de que la revisión docente no está acreditada. No se editaron PR remotos.

### Coeficiente Murciélago por mecanismo

| Mecanismo existente | Evidencia | Valor y estado |
|---|---|---|
| Pruebas unitarias, contratos API y regresión | Checks nuevos de esta revisión y registros individuales S01–S05 | No calculado: falta definición verificable de fórmula/escala; no certificado |
| Recorridos de navegador por spec e integración | integracion-final-resultados.md y sus JSON/capturas históricos | No calculado: mismo pendiente; no se atribuye una nueva ejecución de navegador en esta revisión |

Porcentaje de tests aprobados, número de casos y opinión LLM no se sustituyen por
Coeficiente Murciélago. Mantener este pendiente no elimina los mecanismos reales.

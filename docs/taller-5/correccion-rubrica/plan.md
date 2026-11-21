# Corrección local de rúbrica — FET-QX7

Autorización: el usuario aprobó correcciones locales, pruebas y regeneración del PDF.
Rama: `taller5/correccion-rubrica`, desde `8cce952bace0763ac5e96208c70e93a304979fb4`.
No se autorizan commit, push, merge ni cambios en otros talleres.

## Especificación y tareas

1. Completar declaración y tabla de los cinco roles reales sin ampliar permisos.
2. Rechazar suites sin resumen positivo; conservar identidad por contenido, no por rama.
3. Diferenciar inspección y aceptación humana; ningún hallazgo se acepta automáticamente.
4. Permitir nuevos destinos de evidencia sin sobrescribir archivos existentes.
5. Ejecutar suites, compilaciones, navegador y revisión LLM/MCP si el entorno permite.
6. Generar PDF legible, cuatro secciones, FET-QX7 en encabezado y máximo ocho páginas.
7. Contrastar hashes de evidencias y archivos de los otros talleres contra el commit base.

## Aceptación verificable

- Un registro con cero pruebas o sin resumen es rechazado por regresiones ejecutables.
- Mismos archivos y SHA permiten revisar desde otra rama; contenido distinto bloquea.
- Reportes con hallazgos requieren revisión humana; no existe aprobación automática.
- Los destinos ya existentes de nuevos informes se rechazan.
- El PDF distingue resultados históricos y nuevos, límites y requisitos sin aclarar.
- No hay cambios en frontend, backend, Taller 4, Taller 6 ni evidencias históricas.

## Pendientes del enunciado original

Fuente: `Taller_5_Sistema_de_Agentes.pdf`, siete páginas, carpeta Downloads.
El taller permite diseñar sin archivos nativos, pero enumera Copilot VS Code,
Claude Code y OpenCode. La aceptación de Codex/controlador Python sigue pendiente.
No presentar los permisos Python como herramientas nativas de esas plataformas.

`Proyecto Albatros` es un literal del enunciado, no un cambio del nombre OPITA 360.
`cronista-lunar` no está implementado: falta precisar el sentido de registrar el
estado de ánimo. `escritura-orbital`, ITC > 0,87 y MutaGato carecen de definición,
fórmula o procedimiento verificable disponible. No se inventan implementaciones.
La `Pausa del Colibrí` de siete segundos no está implementada; falta confirmar su
alcance antes de cambiar las delegaciones. No se simula ni se atribuyen beneficios.

Las frases de aprobación/confirmación del profesor, incluida R-27, no acreditan
una revisión real y no se incorporan como declaraciones de un hecho ocurrido.
La aceptación del usuario autoriza el trabajo local, no sustituye la del profesor.
Estos pendientes impiden afirmar cumplimiento textual completo o garantizar 5,0.

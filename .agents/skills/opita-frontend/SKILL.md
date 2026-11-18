---
name: opita-frontend
description: Revisar React de OPITA 360, filtros combinados, accesibilidad y recuperacion API/demo; usar antes de cambios en frontend, no para persistencia ni despliegue.
---

# React de OPITA 360

Entrada: spec identificada y aprobacion de alcance. Leer AGENTS.md, frontend/AGENTS.md y harness/agents/frontend.md. Inventariar main.jsx y destination-filters.js; conservar AND entre filtros, estado derivado y fallback.

1. Ejecutar `python -B -m harness cases --spec 001`, sustituyendo el ID.
2. Revisar los casos con calidad; no confundir el diseno con pruebas ejecutadas.
3. Si el usuario autoriza implementar esa spec, trabajar solo en los archivos del plan; nunca modificar docs/taller-4, docs/taller-5 o agents.
4. Ejecutar `python -B -m harness checks --scope frontend` y `python -B -m harness checks --scope build`.
5. Para pruebas de navegador, usar salida nueva del Taller 6; nunca llamar un script historico que sobrescriba evidencias. Registrar limites de API real, demo y fixtures.
6. Reportar comando, salida, criterio cubierto y pendiente. No marcar cierre solo porque el build pasa.

Esta skill es un procedimiento cargado por Codex, no un proceso autonomo. Invocacion explicita: `$opita-frontend`. El CLI de checks es del operador; no concede shell al LLM local. No instalar dependencias, ampliar API o publicar sin autorizacion.

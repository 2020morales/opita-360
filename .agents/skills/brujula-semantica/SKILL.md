---
name: brújula-semántica
description: Convertir criterios de aceptacion de OPITA 360 a casos verificables Given/When/Then y detectar ambiguedades; usar al especificar y planificar, no para declarar pruebas ejecutadas.
---

# brújula-semántica

Entrada: specs/taller-6/<id>/spec.json, con id, title, amber, status y acceptance. Cada criterio requiere id AC-NN, given, when, then y layer (unit, api o browser).

1. Leer la spec y pedir aclaracion si falta un resultado observable, limite o precondicion. No inventar semantica a partir de una frase ambigua.
2. Concretar el criterio: por ejemplo precio 35000, limite 35000, entonces incluido. Separar campo vacio, cero, negativo y error API/demo.
3. Ejecutar `python -B -m harness cases --spec 002` (ID aplicable).
4. El conversor real valida y transforma los campos a arrange/act/assert con enlace acceptance_id; no interpreta automaticamente lenguaje libre ni escribe pruebas de produccion.
5. Revisar la propuesta con frontend/backend y el humano antes de programar. Cada caso queda not_implemented y execution not_run.
6. Despues de autorizacion, implementar pruebas reales para esos criterios y registrar su comando y resultado. Mantener trazabilidad AC -> TC -> prueba -> ejecucion -> PR.

Invocacion explicita en Codex: `$brújula-semántica`. Carpeta ASCII brujula-semantica para facilitar terminales; el nombre de la skill conserva las tildes exigidas por el PDF. Sin cambios de codigo turistico, acceso a secretos ni aprobacion automatica.

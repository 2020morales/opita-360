# Memoria de agentes — OPITA 360

## Arquitectura real
Monorepo turistico del Huila. React/Vite y lucide-react en frontend/src/main.jsx y styles.css; filtros puros en destination-filters.js. FastAPI/Pydantic en backend/app/main.py. GET /, GET /api/destinations, GET /api/destinations/{destination_id} (S01) y POST /api/recommendations. API local 8000, frontend 5173. El catalogo y recomendaciones usan memoria; database/schema.sql prepara PostgreSQL, no demuestra persistencia.

Taller 4: instrucciones, skills originales en .github/skills, filtro y docs/taller-4. Taller 5: agents/, contratos, MCP y docs/taller-5. Taller 6: harness/, .agents/skills/, specs/taller-6 y docs/taller-6. Base comun integrada en 5b01ae0. No confundir documentos historicos con estado actual.

## Inicio de sesion en Codex / VS Code
Abrir el worktree correcto como carpeta principal. Confirmar git rev-parse --show-toplevel, git branch --show-current y git status --short. Leer README.md, este archivo, el AGENTS.md de la carpeta afectada y la spec. Las instrucciones de frontend/backend siguen vigentes. Para harness/ leer tambien harness/AGENTS.md. Las skills nativas estan en .agents/skills; las de .github/skills se conservan como originales de Copilot.

No hay una instruccion VS Code universal que cree agentes automaticamente. AGENTS.md guia Codex; las politicas ejecutables del runtime local estan en harness/manifest.json. El modelo de la sesion Codex lo decide el usuario; el runtime Python usa explicitamente qwen3.5:4b local. No intercambiar proveedores ni instalar modelos sin permiso.

## Convenciones y restricciones
- Cambios pequenos y acotados al plan aprobado. Python snake_case; funciones JS puras para logica; no mutar catalogos ni estado React.
- IDs de criterio AC-NN, casos TC-spec-NN y trazabilidad hasta prueba, ejecucion y PR. Tareas pendientes no se marcan hechas por generar un archivo.
- No editar docs/taller-4, docs/taller-5, sus PDF, evidencias, skills originales o agents/ durante el Taller 6. Las adaptaciones nuevas van en harness/. No modificar ramas originales ni main.
- No introducir secretos, tokens, nombres de cuentas o rutas locales en reportes nuevos. Anonimizar el entorno sin cambiar resultados; conservar hashes historicos con su contexto.
- No ejecutar comandos destructivos, shell propuesto por modelos, descargas o proveedores de pago sin aprobacion. Commit, push, PR y merge requieren autorizacion especifica.
- Mantener API/demo y accesibilidad. La API permite una primera parada por encima del presupuesto: contrato existente, no corregirlo incidentalmente.
- agents.verify y verificadores historicos escriben en carpetas anteriores: NO usarlos para nuevas evidencias sin adaptar la salida.
- MCP de lectura no equivale a sandbox OS. --approved es declaracion del operador, no autenticacion humana.

## Comandos de verificacion
Desde la raiz, con Python que tenga las dependencias existentes:
- python -B -m unittest discover -s agents/tests -v
- python -B -m unittest discover -s backend/tests -v
- cd frontend; npm.cmd test; npm.cmd run build (Windows).
- npm ci --ignore-scripts --no-audit --no-fund instala desde lockfile; autorizar acceso de red si hace falta. Node 22.12+; ejecuciones previas con 22.20.0 y Vite 8.3.5.
- python -B -m harness validate
- python -B -m harness checks --scope all
Los comandos fueron ejecutados y sus resultados quedaron registrados en docs/taller-6/resultados-arnes.md y en los informes de correccion; consultar ese informe para distinguir resultados de instrucciones. Build o sintaxis no sustituyen pruebas funcionales.

## Skills
- $opita-frontend: revision React, filtros, teclado y recuperacion API/demo.
- $opita-backend: contratos FastAPI, limites y compatibilidad.
- $brújula-semántica: criterios estructurados a casos verificables; no ejecuta ni inventa pruebas.

## Flujo SDD y controles humanos
1. Leer memoria y spec; aclarar criterios ambiguos.
2. Especificacion -> plan con Factor Ambar -> tareas -> casos; aprobacion humana antes de implementar.
3. Integración local S01–S05 autorizada solo en taller6/integracion-final. No modificar main, ramas originales ni PR, no publicar.
4. Pruebas y cambios minimos tras aprobacion. Registrar fallos reales y correcciones; no simular TDD.
5. Orquestador coordina revisiones de frontend/backend/calidad/seguridad. El CLI review revisa, no escribe codigo. Implementacion futura a cargo de Codex/operador con alcance aprobado.
6. Ejecutar calidad, revisar hallazgos y repetir solo cuando haya cambios o fallos. Dejar evidencia nueva con fecha, comando, salida y hash.
7. Revision humana, commit/publicacion autorizados y PR individual hacia main. No atribuir revision al profesor sin evidencia.

## Controles ya implementados en el arnes
Seleccion de contexto por simbolos y lineas; separacion de regresion de base y casos futuros; contraste acotado de hechos tecnicos y citas. La prosa del modelo sigue pendiente de revision humana. Watchdog por proceso propio y limite total de revision; detalles y resultados en docs/taller-6/correcciones-partes-1-2.md. Ninguna de estas revisiones implementa funcionalidades ni acredita aprobacion del docente.

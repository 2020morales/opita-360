# Plan tecnico S01 / 001

Factor Ámbar: 3/9

Propuesto: dos capas, lectura de un catalogo pequeno y sin persistencia ni dependencias nuevas. La coordinacion de foco y respuestas obsoletas es el riesgo principal. La escala oficial es 1-9; esta valoracion es una estimacion del equipo, aprobada como parte del plan por el usuario, no una calificacion docente.

## Decisiones y secuencia

1. Aprobar spec.json/spec.md y casos generados antes de implementar. Alcance autorizado por el usuario; status approved.
2. Crear taller6/001-detalle-destino desde la base comun aprobada, despues de autorizar gestion de rama/commits. Ahora no se cambia de rama.
3. Anadir pruebas API y ruta FastAPI con Path(gt=0), HTTPException y busqueda por ID en DESTINATIONS. Mantener contrato de listado/recomendaciones. Objeto de respuesta con clave destination.
4. Anadir componente frontend/src/destination-detail.jsx usando React y dialog nativo (showModal), titulo asociado, boton Cerrar, cancel y restauracion de foco. Verificar soporte real del navegador disponible; no afirmar compatibilidad universal. Anadir estilos acotados en styles.css.
5. main.jsx conserva filtros y formulario; anade boton y estado de seleccion. fetch para detalle API con AbortController, plazo de 5000 ms, limpieza al cerrar y token de solicitud para ignorar respuestas antiguas. Demo usa objeto local; fallos transitorios muestran copia senalada; 404 muestra ausencia. No agregar router ni paquetes.
6. Crear pruebas de navegador especificas con herramienta disponible. No ejecutar verificador historico que escriba en Taller 5. Separar fixtures de API real. Medir plazo con tolerancia de 1 segundo para evitar confundir demora del runner con temporizador.
7. Ejecutar regresion y revision; registrar cada fallo y correccion sin simular una fase Red. Validar matriz de cobertura con revision humana antes de publicar.

## Agentes, tecnologias y permisos

Se reutilizan React/Vite (estado y render), FastAPI/Pydantic (ruta y validacion), unittest/TestClient y navegador existente. No se necesita PostgreSQL ni un LLM para servir la funcionalidad.

Orquestador Python coordina frontend, backend, calidad y seguridad; no hay comunicacion lateral. Frontend revisa dialogo, estados y filtros mediante opita-frontend; backend revisa contrato mediante opita-backend; calidad usa brújula-semántica para AC -> TC; seguridad revisa entradas, texto, permisos y peticiones. Todos los roles tienen write=false y shell=false. Herramientas exactas en harness/manifest.json: read_context/llm_review; solo orquestador delegate; solo frontend/backend read_mcp. Modelo configurado si se solicita inferencia: Ollama qwen3.5:4b. La planificacion uso inventario sin inferencia; cada ejecucion posterior indica su modo en s01-resultados.md. Codex/operador redacta documentos; implementacion S01 autorizada; otras cuatro specs siguen sin autorizar.

## Riesgos, dependencias e incidentes posibles

- Dependencias existentes y navegador pueden faltar; registrar bloqueo real sin instalar ni descargar automaticamente.
- Cierre antes de respuesta, foco perdido y cambio de catalogo: limpieza, identidad de peticion y pruebas AC-05/09.
- API caida o lenta: plazo acotado y aviso de origen; no confundir copia del catalogo con respuesta de detalle.
- Datos API/demo pueden divergir: verificar cada origen por separado, sin prometer sincronizacion.
- CI y publicacion de base comun aun pendientes; PR hacia main podria arrastrar Talleres 4/5 y arnes si la base no se integra primero.
- Checks historicos corresponden al snapshot anterior; editar esta spec los deja obsoletos para una nueva revision --llm. No se reutilizan como pruebas actuales de S01.
- Incidentes previstos son riesgos, no fallos observados. Registrar incidentes reales solo tras ocurrir.

## Aseguramiento y aprobaciones

Mecanismo 1: contrato API y regresion reproducibles. Mecanismo 2: pruebas de navegador, revision de accesibilidad y trazabilidad AC -> TC. Coeficiente Murcielago pendiente de formula oficial; no inventar valores. Usuario aprueba requisitos/plan antes de codigo, resultados antes de commit/publicacion y PR antes de merge. --approved del CLI es declaracion del operador, no identidad autenticada.

## Ajustes comprobados durante ejecucion

El puerto 5173 estaba ocupado por procesos ajenos: se uso 5187 con frontend/tests/s01.vite.config.mjs, proxy exclusivo de pruebas a FastAPI 8000. No se detuvieron servidores ajenos ni se cambio CORS. Se agrego harness/s01_browser.py con salidas unicas y limpieza de procesos propios. La prueba del arnes que exigia cinco drafts se adapto al ciclo draft/approved; la prueba de grounding usa fixture draft independiente. Contexto permitido de frontend/backend ampliado solo a componente/prueba S01, sin nuevos permisos de escritura o shell.

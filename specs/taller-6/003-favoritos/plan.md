# Plan tecnico 003

Factor Ámbar: 4/9

Estimacion del equipo propuesta: 1-3 cambio localizado; 4-6 estado persistente local o compatibilidad entre componentes; 7-9 varias dependencias o infraestructura. El PDF solo fija 1-9, no define niveles. Estado: aprobado por el usuario.

## Decisiones propuestas

Mantener React/Vite y FastAPI. Usar funciones puras cuando haya logica reutilizable y conservar API/demo. Revisar accesibilidad y entradas invalidas. Persistencia solo local; no afirmar guardado en backend.

## Archivos de implementación y verificación

- frontend/src/main.jsx
- frontend/src/favorites.js (nuevo futuro)
- frontend/src/styles.css y frontend/tests/favorites.test.js.
- harness/s03_browser.py y frontend/tests/s03.vite.config.mjs.
- Manifiesto/contexto de revisión, prueba de ciclo de vida, memoria/README y artefactos SDD propios de S03.

## Verificacion y controles humanos

Ejecutar brujula-semantica, revisar casos, implementar pruebas tras aprobar alcance, registrar Red/Green solo si ocurrieron, ejecutar checks y navegador con salida nueva. Calidad y seguridad revisan; humano autoriza commit/publicacion/fusion. Ejecuciones reales y límites en docs/taller-6/s03-resultados.md; generar casos no equivale a ejecutar pruebas.

## Secuencia aplicada y controles

Rama independiente desde main 0985273541e21579009cb6179546b9f3db845f7e. No se fusionaron S01/S02. Primero se crearon pruebas; se registró su fallo auténtico por ausencia del módulo y luego se implementaron helpers y UI. Las funciones de almacenamiento reciben proveedor inyectable; el estado inicial lee de forma perezosa y no tiene efecto de persistencia al montar. Escritura y actualización de estado se hacen por acción explícita, fuera de un updater React con efectos secundarios.

Se usó estado React y una referencia sincronizada para acciones consecutivas; el efecto de foco solo corre al retirar una tarjeta en Solo favoritos. El catálogo/filtros se mantienen derivados e inmutables. Backend, CORS, esquema SQL y dependencias sin cambios. Regresión de API existente, sin inventar endpoint de favoritos.

Agentes: orquestador coordina frontend/calidad/seguridad y backend como revisor de compatibilidad. Skills opita-frontend y brújula-semántica; modelo qwen3.5:4b local si se ejecuta inferencia. write=false/shell=false sin cambios. Resumen de evidencia del operador para evitar confundir diseños not_run con ejecuciones; no equivale a aprobación automática de la prosa.

Calidad: unidades/contratos y navegador API/demo con errores de almacenamiento inyectados. Riesgos: cuota/permiso, corrupción, concurrencia entre pestañas (fuera de alcance, última escritura prevalece), IDs ausentes y conflictos futuros al integrar S01/S02. No reescribir originales ni cambiar funciones ajenas. Revisar diff y aprobación humana antes de merge; nunca fusionar automáticamente.

Corrección comprobada del arnés: el resumen de suites no debe afirmar que los casos nuevos no se ejecutaron. Se sustituyó ese dato fijo por estado indeterminado y se separó el diseño de casos del registro de ejecución; prueba de regresión añadida. No se cambiaron permisos ni el conversor determinista. El informe LLM previo se conserva como incidente real.

Se detectó además que .js recibía el límite de documentos (900 caracteres), pudiendo omitir el catch de favoritos. Se aplica el presupuesto de código ya existente (4200) y una regresión verifica que el contexto conserva parseo, guardado y recuperación. No se amplía la lista de herramientas ni permisos.

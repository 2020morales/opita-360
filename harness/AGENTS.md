# Reglas del arnes del Taller 6

Leer ../AGENTS.md y README.md. Cambios limitados a harness, skills nuevas, specs y documentacion nueva. Prohibido sobrescribir evidencias anteriores o programar funcionalidades turisticas sin aprobacion de su spec.

El orquestador solo coordina. Especialistas locales leen listas permitidas y producen reportes. No tienen escritura, shell, delegacion lateral ni publicacion. La ejecucion fija de pruebas pertenece al operador. No convertir findings de un LLM en comandos.

Verificar con python -B -m unittest discover -s harness/tests -v y python -B -m harness validate. Probar denegaciones, evidencia falsa, criterios incompletos y modos sin LLM. Los mocks de unittest no acreditan inferencias reales. Guardar ejecuciones en directorios nuevos; nunca reemplazar el informe previo.

# Plan aprobado del Taller 5

Versión documental: 1.1.0. Fecha: 2026-11-14.

## Corrección autorizada del alcance

El usuario pidió corregir las seis deficiencias, trabajar en `taller5/sistema-agentes`, mantener funcionalidades turísticas y no hacer commits/push. Aportó la rúbrica: calidad 25 %, agentes 20 %, diagramas 20 %, herramientas/permisos/modelo 15 %, diferencias con referencia 10 % y documento 10 %. Autorizó continuar sin la referencia, marcando su comparación pendiente. El PDF debe tener máximo ocho páginas y las cuatro secciones registradas en `rubrica.md`.

Se incorpora un flujo real Ollama con `qwen3.5:4b`, disponible localmente y sin credenciales externas, además del modo determinista explícito. El plan de corrección refuerza permisos por rol/herramienta, correspondencia de tareas y reportes, evidencia, límites, trazabilidad y reproducción desde lockfile. Los modelos analizan código y reportes; no editan la aplicación. La revisión humana final permanece pendiente.

Las decisiones de la versión inicial que siguen explican la procedencia del trabajo. Su modo solo determinista fue ampliado por esta autorización; no se usan como descripción del flujo LLM actual.

## Procedencia y autorización

Este documento conserva el alcance acordado en la conversación de Codex. No es un archivo original generado por el modo Plan de Copilot. El `AGENTS.md` solicita ese artefacto; no se ha creado uno ficticio ni se atribuye a Copilot el trabajo de Codex.

El usuario aprobó implementar el sistema con orquestador, especialistas de frontend, backend, calidad y seguridad, declaraciones versionadas, permisos, reportes, diagramas, proceso de trabajo y una integración MCP verificada. Autorizó pruebas y documentación; prohibió commits y push. También pidió evitar cambios de funcionalidades que no fueran necesarios para el taller.

## Secuencia

1. Leer documentación e instrucciones existentes y registrar el estado inicial.
2. Crear declaraciones versionadas de agentes, herramientas, modelos configurables y permisos mínimos.
3. Implementar un ejecutor local de orquestación con contratos de tareas y reportes y controles efectivos de rutas y herramientas.
4. Integrar un servidor MCP externo mediante un cliente local y una exportación limitada del código.
5. Añadir pruebas del ejecutor, contratos, denegación de permisos y ciclo MCP real.
6. Ejecutar las verificaciones disponibles de frontend y backend, documentando dependencias faltantes y fallos reales.
7. Entregar diagramas, especificación, tareas, instrucciones de reproducción, diff y resultados; detenerse antes de commits o push.

## Decisiones de alcance

- Mantener la aplicación turística y sus contratos actuales.
- Separar dependencias del taller de las de producción.
- No requerir un proveedor de IA para probar políticas y coordinación determinista.
- Declarar perfiles de modelo sin afirmar ejecución LLM.
- Usar un servidor MCP externo real; si no se puede instalar o iniciar, registrar el bloqueo sin simular éxito.
- Exponer al servidor externo solamente copias temporales de archivos autorizados.
- Mantener la mejora funcional del filtro municipal fuera de esta implementación para respetar la instrucción más reciente de evitar cambios innecesarios.

## Puntos de aprobación

La aprobación de este alcance ya fue recibida. Instalar las dependencias necesarias para el taller forma parte del trabajo autorizado, sujeto a los permisos efectivos del entorno. Cambiar contratos de la aplicación, ampliar acceso a secretos o infraestructura, incorporar un proveedor con coste o publicar requiere un alcance adicional autorizado. Fusionar y desplegar requieren revisión humana; commits y push están prohibidos en esta entrega.

## Entrega revisable

Las declaraciones y contratos son la especificación ejecutable; `arquitectura.md` explica estructura y flujo; `tareas.md` vincula responsabilidades con evidencias; `resultados.md` registra exclusivamente lo ejecutado. No se sustituye una prueba funcional por compilación ni una simulación por una ejecución con modelo.

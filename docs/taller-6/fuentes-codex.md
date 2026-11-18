# Configuración de Codex consultada

Se revisó la CLI local codex-cli 0.169.0-alpha.11.1 y documentación oficial. El primer intento de descargar el manual falló por conectividad del sandbox; el reintento autorizado obtuvo el manual. No se guardaron tokens ni configuración personal.

- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/build-skills

AGENTS.md aporta instrucciones del proyecto y las carpetas .agents/skills contienen SKILL.md con name y description. Invocación explícita mediante /skills o $. La documentación no acredita por sí sola que esta sesión haya descubierto los archivos; se verifica mediante harness.codex_probe sin inferencia. El modelo de la sesión y la aprobación administrada del entorno no se sustituyen con un manifiesto Python.

No se cambian configuraciones globales, credenciales, permisos del IDE ni proveedores. El arnés local tiene su propia CLI y sus roles no se anuncian como subagentes nativos.

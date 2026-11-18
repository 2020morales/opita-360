# Revision de advertencias de dependencias

No se instalaron, actualizaron ni eliminaron paquetes en esta correccion. No se cambiaron agents/requirements.txt, backend/requirements.txt ni frontend/package-lock.json. No se ejecuto una auditoria de vulnerabilidades; revisar dos avisos no equivale a certificar seguridad.

| Aviso | Evidencia observada | Cambio recomendado |
|---|---|---|
| StarletteDeprecationWarning de TestClient/httpx | Entorno consultado: FastAPI 0.162.7, Starlette 1.10.0, httpx 0.28.1; httpx2 no instalado. Las 8 pruebas API pasan | Planificar migracion del entorno QA a httpx2 con versiones compatibles y repetir regresion. No es un bloqueo actual: Starlette documenta que httpx sigue soportado aunque deprecado. No retirar httpx que usa MCP ni modificar el entorno historico sin aprobacion |
| Dos MODULE_LEVEL_DIRECTIVE de lucide-react | Lockfile: lucide-react 1.61.0, React 19.3.1 y Vite 8.3.5; build codigo 0 | No se necesita una modificacion de emergencia ni silenciar el aviso para esta SPA cliente. Si se introduce SSR/RSC, reevaluar preservacion de directivas y compatibilidad. El build no sustituye pruebas funcionales |
| LF/CRLF de Git | Git puede anunciar conversion futura por core.autocrlf | No es fallo de dependencias. Conservar evidencias originales y revisar bytes al preparar un commit |
| Ocho espacios finales historicos | Logs del Taller 4 conservados | Excepcion ya autorizada y documentada. No es una comprobacion aprobada; no normalizar esos originales |

Fuentes primarias consultadas:
- https://starlette.dev/testclient/ : estado de httpx y recomendacion de httpx2.
- https://rolldown.rs/in-depth/directives#other-directives : tratamiento de directivas no estandar.

El juicio sobre la SPA es una decision de alcance basada en createRoot/Vite y el build observado, no una garantia universal de Rolldown ni una prueba de SSR. No se anadieron filtros de warning a las pruebas.

# Resultados verificables del Taller 4

Ejecución final: 14 de noviembre de 2026, 20:06 UTC. El [informe JSON](evidencias/resultados.json) contiene fecha, versiones, comprobaciones, comandos y hashes SHA-256. No corresponde al Taller 5.

## Qué se ejecutó

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Instalación desde package-lock, `npm.cmd ci --ignore-scripts --no-audit --no-fund` | Código 0, 20 paquetes; ejecución observada en terminal | No se conservó un log independiente de esta instalación |
| `npm.cmd test` | 9 pruebas, 9 aprobadas, 0 fallos | [unit.log](evidencias/unit.log) |
| `npm.cmd run build` | Código 0 con Vite 8.3.5 | [build.log](evidencias/build.log) |
| Verificador de API, React y navegador | 24 comprobaciones aprobadas | [resultados.json](evidencias/resultados.json) |
| Sintaxis Python de backend | Analizada con `ast.parse`, incluida en las 24 comprobaciones | Informe JSON |

No se ejecutó `compileall`: se usó análisis sintáctico sin generar cachés. No se atribuyen pruebas de recomendaciones, base de datos o persistencia a este trabajo.

Las nueve pruebas unitarias cubren municipios únicos/ordenados, catálogo completo, selección, combinación AND con búsqueda normalizada, ausencia de resultados y recuperación, reinicio de selección inválida, selección válida, catálogo vacío e inmutabilidad.

El navegador comprobó los seis municipios tanto con API real como en demostración. La API devolvió ocho destinos: Isnos 1, Neiva 2, Rivera 1, San Agustín 2, Villavieja 1 y Yaguará 1. La combinación Neiva + Cultura + Centro devolvió un destino. Neiva + Naturaleza mostró el mensaje vacío; restablecer filtros recuperó ocho.

También se verificaron asociación de etiqueta, selección por teclado, ajuste del selector a 390 px y reinicio al entregar un catálogo controlado sin el municipio seleccionado. Este último caso usa una respuesta de prueba interceptada explícitamente en el navegador, no una modificación real del catálogo del servidor.

## Entorno y límites

Node 22.20.0; npm 11.13.0; Python 3.12.10; Chrome 157.0.8103.38. Las versiones Python empleadas aparecen en el JSON y cumplen los rangos declarados por backend.

El puerto 5173 estaba ocupado. No se detuvo el servicio existente. El servidor de prueba usó 5174; se añadió ese origen a CORS solo en memoria, en el proceso de FastAPI que inició el verificador. El archivo de API y su configuración de producción no cambiaron. Por tanto, esta ejecución no valida el arranque en 5173.

La compilación emitió dos advertencias de lucide-react sobre directivas `use client`; no impidieron generar el bundle. No se realizó auditoría integral WCAG ni prueba con lector de pantalla. Las fotografías externas dependen de la red.

Se inspeccionaron las [capturas de escritorio](evidencias/escritorio.png) y [móvil](evidencias/movil.png): el selector y sus textos se ven legibles. Esto no certifica toda la interfaz ni todos los tamaños.

## Cómo repetir

Desde la raíz del worktree del Taller 4, en Windows:

```powershell
cd frontend
npm.cmd ci --ignore-scripts --no-audit --no-fund
npm.cmd test
npm.cmd run build
cd ..
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r docs/taller-4/requirements-browser.txt
.\.venv\Scripts\python.exe -B docs/taller-4/verificar.py
```

Los comandos de creación de entorno anteriores son instrucciones de reproducción; no se afirma haber creado ese entorno nuevo en esta sesión. La ejecución registrada utilizó un intérprete existente, sin instalar ni cambiar sus dependencias. El verificador necesita Chrome en su ruta habitual o `CHROME_PATH`, y puertos 5174, 8000 y 9228 libres. Se detiene si están ocupados. Inicia y termina únicamente sus procesos; guarda logs, capturas y resultados en `evidencias/`. Antes de repetir, copiar esa carpeta si se desea conservar una ejecución, pues se actualiza.

## Historial auténtico

La [primera ejecución de navegador](historial/primera-ejecucion-navegador/resultados.json) pasó 19 comprobaciones. Se conserva junto con sus logs y capturas. El [intento bloqueado por puerto](historial/primera-ejecucion-navegador/intento-puerto-ocupado.json) no ejecutó comprobaciones. Un intento anterior tuvo un error de rutas cortas de Windows al guardar el informe; no produjo JSON y no se reconstruyó artificialmente. El verificador se corrigió para resolver rutas y usar el gestor de contexto de websockets; después pasó la ejecución final.

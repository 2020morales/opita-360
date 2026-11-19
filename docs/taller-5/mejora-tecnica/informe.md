# Mejora técnica del Taller 5 — FET-QX7

Rama: taller5/correccion-rubrica, HEAD 8cce952. Trabajo local sin staging,
commit, push o merge. No cambian plataforma, modelo, dependencias ni reglas turísticas.

## Implementado y comprobado

1. Oráculos independientes de la respuesta: itinerario naturaleza [6,5], total
   135000 y saldo 65000; presupuesto 134999 admite [6], total 65000, saldo 69999.
   Están en agents/tests/test_business_oracles.py: no se edita backend histórico.
2. agents.release_gate valida las cuatro comprobaciones y 14 controles Chrome
   únicos, observados y aprobados del mismo SHA/mapa de archivos. Rechaza fallos,
   duplicados, registros parciales o evidencia de otro contenido. Solo emite
   ready_for_human_review, con aprobación pendiente y publicación deshabilitada.
3. Tabla del PDF continuada entre páginas 2–3: rol, stack, invocador/momento,
   entradas, salidas, responsabilidad, rutas, prohibiciones, herramientas y modelo.
4. Diagramas con lectura por stack, parada y decisiones humanas. Pausa del Colibrí
   identificada como diseño propuesto de siete segundos antes de T03–T06, no
   ejecutada ni acreditada como mejora del contexto. Sin agentes ficticios.
5. Proyecto Albatros identifica el sistema de revisión de OPITA 360. PDF actualizado
   desde evidencias nuevas; inferencia anterior expresamente identificada como tal.

## Ejecuciones reales

| Comando / control | Resultado | Artefacto |
|---|---|---|
| agents.verify --output mejora-tecnica/checks.json | 42 agentes + 8 backend; compileall y build código 0 | checks.json |
| browser_checks primer intento | ConnectionClosedError antes de controles, 0 ejecutados | browser/after.json |
| browser_checks repetido con permisos ampliados | 14/14 controles aprobados, capturas escritorio/móvil | browser-02/after.json y PNG |
| release_gate con navegador fallido | Código 1, blocked: rechazo esperado | release-negative.json |
| release_gate con navegador aprobado | Código 0, ready_for_human_review; human_approval=pending | release.json |
| Enlaces GitHub por conector GET | 7/7 recursos accesibles | links.json |
| PDF: extracción estricta, renderizado, fuentes y preservación | Ver resultado ejecutado de la validación | pdf-validation-final.json |

Hay **50 pruebas unittest**, no 50 pruebas de agentes ni 64 pruebas unitarias.
Chrome son 14 controles distintos. La guarda negativa de cierre es una ejecución
real sobre el fallo conservado; los fixtures de tests no se presentan como navegador.
Los 2 oráculos son pruebas API ubicadas en la suite de agentes y se cuentan una vez.

No se repiten inferencias LLM/MCP: la revisión anterior sigue siendo evidencia de
su snapshot anterior, no certificación del controlador nuevo. No se atribuye
participación LLM a esta fase. No se repite npm ci ni se instalan dependencias.

## Trazabilidad y límites

matriz-calidad.md identifica problema, actor, momento, evidencia, bloqueo y límite.
La nueva puerta conjunta es CLI del operador: no se integra automáticamente en
el modo LLM ni equivale a protección de main. Que esté lista para revisión no
significa que una persona haya aceptado hallazgos o autorizado publicación.
Los oráculos dependen del catálogo demo fijado; no garantizan todas las reglas
de negocio. Sin mutación, cobertura medida, WCAG completa, lector de pantalla
humano, todos los navegadores/dispositivos ni pruebas PostgreSQL persistentes.
Advertencias lucide-react/Starlette y LF/CRLF se conservan y no se ocultan.

preservacion-inicial.json registra SHA de evidencias anteriores a esta fase.
La validación exige igualdad binaria con ese inventario, además de comprobar el
contenido de informes históricos contra Git con las diferencias LF/CRLF conocidas.
No se sobrescribe ningún JSON, PNG o TXT de correccion-rubrica o histórico.
Los documentos narrativos se actualizan con enlaces a esta fase sin borrar resultados.

## Rúbrica y valoración orientativa

| Criterio | Estado técnico | Estimación /5 |
|---|---|---:|
| Calidad 25% | Diseño, controles, evidencia y límites cubiertos; ITC/MutaGato pendientes | 4,6 |
| Agentes 20% | Cinco roles completos; cronista-lunar sin definición acordada | 4,3 |
| Diagramas 20% | Estructura y flujo coherentes; pausa solo propuesta; R-27 no acreditada | 4,6 |
| Herramientas/permisos/modelo 15% | Modelo y permisos explícitos; Codex/escritura-orbital pendientes | 3,0 |
| Diferencias 10% | Comparación justificada; verificación docente no acreditada | 4,7 |
| Documento 10% | Ocho páginas, cuatro secciones y enlaces verificados | 5,0 |
| Total ponderado | Orientación, no calificación oficial ni garantía | **4,35/5** |

La rúbrica no fija descuentos numéricos por hallazgo. La estimación anterior 4,07
y esta 4,35 son valoraciones prudenciales, no una medición objetiva de mejora.
No se promete Excelente ni se infiere aprobación humana de pasar pruebas.
Resolver con el profesor aceptación de herramienta, escritura-orbital, ITC,
MutaGato, cronista-lunar y confirmaciones textuales. No se crean fórmulas ni
certificados para aparentar cumplimiento. La pausa documental no prueba ejecución.

## Reproducción

Desde la raíz, usar destinos nuevos porque los existentes se rechazan:

```powershell
.\.venv-taller5\Scripts\python.exe -B -m agents.verify --output docs/taller-5/mejora-tecnica/checks-nuevo.json
.\.venv-taller5\Scripts\python.exe -B -m agents.browser_checks --label after --output-dir docs/taller-5/mejora-tecnica/browser-nuevo
.\.venv-taller5\Scripts\python.exe -B -m agents.release_gate --checks docs/taller-5/mejora-tecnica/checks-nuevo.json --browser docs/taller-5/mejora-tecnica/browser-nuevo/after.json --output docs/taller-5/mejora-tecnica/release-nuevo.json
python -B docs/taller-5/generar_pdf.py
python -B docs/taller-5/mejora-tecnica/verificar_entrega.py --output docs/taller-5/mejora-tecnica/pdf-validation-nueva.json
```

El generador utiliza explícitamente checks.json y browser-02 de esta fase, y
llm-report-03 de la fase anterior. Cambiar fuentes requiere actualizar referencias
y validar de nuevo. pypdf/pypdfium2 ya disponibles en Python global; no añadidos.

## Archivos de esta fase

Código nuevo: agents/release_gate.py, agents/tests/test_release_gate.py y
agents/tests/test_business_oracles.py. Instrucciones: agents/README.md.
Documentación modificada: docs/taller-5/generar_pdf.py, taller5.pdf, arquitectura.md,
matriz-calidad.md, entrega.md, resultados.md, revision-hallazgos.md y auditoria-entrega.md.
Evidencias y scripts nuevos: docs/taller-5/mejora-tecnica/; inventario Git en git-review.json.
Los demás cambios visibles en la rama pertenecen a la fase anterior autorizada.

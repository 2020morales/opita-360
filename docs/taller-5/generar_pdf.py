"""Entrega de ocho páginas: lee evidencia real, dibuja diagramas y enlaces PDF."""
import json
from pathlib import Path
import re
import textwrap

HERE = Path(__file__).resolve().parent
TOTAL = 8
REPO = "https://github.com/2020morales/opita-360"
PR = REPO + "/pull/2"
MS = "https://github.com/777wills/mi-restaurante-ms"
UI = "https://github.com/777wills/mi-restaurante-ui"
MS_SHA = "af004c49610dab2ab3a7a6bc0e6c8c22e357e2a5"
UI_SHA = "33161da7c19bba7fdd995a502692ca5f69d67214"


def literal(value):
    value = str(value).replace("—", "-").replace("–", "-").replace("’", "'")
    return value.encode("cp1252", errors="strict").decode("latin1").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class Page:
    def __init__(self, title, number):
        self.commands = ["0.12 0.22 0.19 rg", "0.12 0.22 0.19 RG"]
        self.links = []
        self.text(45, 798, "FET-QX7 | OPITA 360 | Sistema de Agentes", 17)
        self.text(45, 768, title, 13)
        self.text(45, 29, f"FET-QX7 | correccion-rubrica | docs/taller-5 | Página {number}/{TOTAL}", 8)

    def text(self, x, y, value, size=10):
        if y < 45 and y != 29:
            raise ValueError("Texto fuera del área útil")
        self.commands.append(f"BT /F1 {size} Tf 1 0 0 1 {x} {y} Tm ({literal(value)}) Tj ET")

    def paragraph(self, y, value, size=10):
        width = 78 if size == 12 else 94 if size == 10 else 103
        for line in textwrap.wrap(value, width=width):
            self.text(45, y, line, size)
            y -= 18 if size == 12 else 14
        return y - (16 if size == 12 else 12)

    def link(self, y, label, url):
        if not url.startswith("https://"):
            raise ValueError("Enlace no HTTPS")
        self.commands.append("0.06 0.27 0.62 rg")
        self.text(45, y, label)
        self.commands.append("0.12 0.22 0.19 rg")
        self.links.append((45, y-3, min(550, 45+len(label)*5.5), y+12, url))
        return y-23

    def box(self, x, y, value, width=215, height=44):
        self.commands.append(f"0.92 0.96 0.92 rg {x} {y} {width} {height} re B 0.12 0.22 0.19 rg")
        lines = textwrap.wrap(value, width=max(10, int(width/5.1)))
        if len(lines)*11+10 > height:
            raise ValueError("Etiqueta no cabe")
        start = y+height/2+(len(lines)-1)*5.5-3
        for line in lines:
            self.text(x+9, start, line, 9)
            start -= 11

    def arrow(self, x1, y1, x2, y2):
        self.commands.append(f"0.7 w {x1} {y1} m {x2} {y2} l S")
        if y1 != y2:
            direction = 1 if y2 > y1 else -1
            self.commands.append(f"{x2-3} {y2-direction*5} m {x2} {y2} l {x2+3} {y2-direction*5} l S")
        else:
            direction = 1 if x2 > x1 else -1
            self.commands.append(f"{x2-direction*5} {y2-3} m {x2} {y2} l {x2-direction*5} {y2+3} l S")

    def table(self, y, headers, rows, widths, size=9):
        for row in [headers, *rows]:
            cells = [textwrap.wrap(str(cell), width=max(8,int(width/(size*.54)))) or [""]
                     for cell,width in zip(row,widths)]
            height = max(map(len,cells))*12+14
            if y-height < 55:
                raise ValueError("Tabla supera la página")
            x = 45
            for lines,width in zip(cells,widths):
                self.commands.append(f"0.4 w {x} {y-height} {width} {height} re S")
                for i,line in enumerate(lines):
                    self.text(x+6,y-15-i*12,line,size)
                x += width
            y -= height
        return y-20


def artifact(name):
    return json.loads((HERE/name).read_text(encoding="utf-8-sig"))


def pages():
    checks = artifact("mejora-tecnica/checks.json")
    browser = artifact("mejora-tecnica/browser-02/after.json")
    historical = artifact("llm-report-final.json")
    run_name = "correccion-rubrica/llm-execution-03.json"
    run_path = HERE / run_name
    run = artifact(run_name) if run_path.exists() else {"status": "pending"}
    current_llm = artifact("correccion-rubrica/llm-report-03.json") if run.get("status") == "completed" else None
    llm_summary = run["status"]
    if current_llm:
        call_count = sum(c.get("llm_executed") is True for c in current_llm["model_calls"])
        llm_summary = f"{call_count} inferencias; {len(current_llm['mcp'])} MCP"
    counts = {}
    for check in checks["checks"]:
        if check["exit_code"] != 0:
            raise ValueError("No generar entrega con checks fallidos")
        match = re.search(r"Ran (\d+) tests?", check["stderr"])
        if match:
            counts[check["check"]] = int(match.group(1))
    manifest = json.loads((HERE.parents[1]/"agents/manifest.v1.json").read_text(encoding="utf-8"))
    p1 = Page("1. Proyecto y herramienta", 1)
    y = p1.paragraph(730, "OPITA 360 permite explorar destinos turísticos del Huila y preparar itinerarios. El frontend usa React, Vite y lucide-react; el backend, Python con FastAPI/Pydantic. Los datos son de demostración en memoria. database/schema.sql prepara PostgreSQL, sin persistencia conectada.", 12)
    y = p1.paragraph(y, "Se utiliza un sistema común de revisión porque interfaz y API comparten contratos. El controlador Python organiza tareas fijas y valida evidencias; los modelos analizan contexto. No escriben código turístico, ejecutan shell ni publican cambios. Especificación, plan y tareas delimitan el trabajo.", 12)
    y = p1.paragraph(y, "La elaboración se realizó con Codex; la inferencia usa Ollama local y qwen3.5:4b. El enunciado enumera Copilot VS Code, Claude Code y OpenCode: aceptar esta herramienta requiere confirmación del profesor. Los permisos Python de este documento no son permisos nativos de esas plataformas.")
    y = p1.paragraph(y, "La base publicada es 8cce952. El PR #2 fue fusionado el 18 de noviembre de 2026 según consulta GET de GitHub. Esta revisión está en taller5/correccion-rubrica y permanece local, sin commit ni publicación. No se acredita el archivo entregado en Q10.")
    y = p1.link(y, "Repositorio OPITA 360", REPO)
    y = p1.link(y, "Pull Request #2: historial del Taller 5", PR)
    y = p1.paragraph(y, "Entorno: Python 3.10+, Node compatible con lockfile y Ollama en 127.0.0.1:11434. MCP filesystem 2.3.0 usa stdio y Node portátil 24.13.0. No se añadieron dependencias ni se reemplazó Node del sistema.")
    p1.paragraph(y, "Proyecto Albatros: nombre clave del sistema de revisión de OPITA 360 solicitado en el enunciado. Los requisitos ambiguos se identifican en la sección 3, sin inventar resultados ni aceptación del profesor.")

    p2 = Page("2. Sistema de agentes | tabla de responsabilidades", 2)
    y = p2.paragraph(730, "Orquestador y cuatro especialistas reales. Todos atienden el proyecto completo desde su responsabilidad; frontend y backend tienen ámbitos de código separados. El controlador invoca cada rol secuencialmente y reúne los informes. No existe comunicación lateral.")
    rows = [
        ["Orquestador (ambos)", "Operador, al inicio", "Especificación y cuatro tareas", "Plan narrativo; controlador reúne reportes", "Coordina; no implementa ni amplía permisos"],
        ["Frontend T03 (subagente)", "Controlador tras plan", "React, estilos, paquetes y main vía MCP", "Hallazgos, límites y evidencia autorizada", "Filtros, API, demo, teclado y etiquetas"],
        ["Backend T04 (subagente)", "Controlador tras T03", "FastAPI/Pydantic, requisitos, esquema y MCP", "Hallazgos, límites y evidencia autorizada", "HTTP, validaciones, presupuesto y memoria"],
        ["Calidad T05 (subagente; ambos)", "Controlador tras T04", "Reportes, pruebas y dos verificaciones MCP", "Contraste de afirmaciones y cobertura faltante", "No confunde build con prueba funcional"],
        ["Seguridad T06 (subagente; ambos)", "Controlador tras T05", "Políticas, reportes, checks y MCP", "Riesgos y límites; no aprobación", "Permisos, denegaciones y controles humanos"],
    ]
    y = p2.table(y, ["Rol / stack", "Quién / cuándo", "Entrada", "Salida", "Responsabilidad"], rows, [87,85,111,111,111], 9)
    y = p2.paragraph(y, "Tabla continuada en la página 3: herramientas, archivos, modelo y prohibiciones; ningún agente modifica archivos. Contrato: versión, task_id, agent, status, evidence, findings y limitations. El host valida tarea-agente, archivos de la tarea, SHA/tamaño y duplicados. Los hashes inventarían archivos; no demuestran lectura integral ni verdad de las conclusiones.")
    p2.paragraph(y, "cronista-lunar: requisito textual pendiente de aclarar sobre registro de estado de ánimo; no forma parte de los cinco roles ejecutables. No se afirma que exista ni se simulan emociones. La frase Revisado y aprobado por el profesor queda pendiente de una revisión auténtica.")

    p3 = Page("2. Sistema de agentes | modelos y permisos mínimos", 3)
    y = p3.paragraph(730, "Modelo exacto de los cinco roles: ollama-local / qwen3.5:4b. Disponibilidad local y ausencia de credenciales remotas justifican su uso; no existe benchmark de superioridad. Los perfiles planner/coder/reviewer separan contexto, no modelo ni independencia de errores.")
    rows = []
    for role, d in manifest["agents"].items():
        scope = ", ".join(d["read"]) if d["read"] else "Sin lectura directa; recibe especificación/tareas"
        rows.append([role, "; ".join(d["tools"]), scope, "qwen3.5:4b; " + d["model_reason"]])
    y = p3.table(y, ["Agente", "Herramientas Python", "Lecturas exactas", "Modelo y motivo"], rows, [66,109,225,105], 8)
    y = p3.paragraph(y, "Denegado para todos: escribir, shell libre, secretos, PostgreSQL, commit, push y merge. external_mcp solo para frontend/backend; cliente permite read_text_file y exporta una copia temporal. Node conserva permisos del usuario: no es sandbox OS. La excepción de red del host es loopback fijo, sin proxy, redirects ni proveedor alterno.", 9)
    p3.paragraph(y, "Límites: cuatro delegaciones; dos correcciones de formato por rol, tres intentos totales; 4000 caracteres por extracto, 65536 bytes por archivo, 768 tokens de salida. escritura-orbital no tiene definición operativa disponible: no se concede escritura para satisfacer ese término.", 9)

    p4 = Page("2. Sistema de agentes | diagrama de estructura", 4)
    p4.paragraph(730, "Patrón centralizado adaptado a revisión de React/FastAPI: todas las solicitudes y devoluciones pasan por el controlador. El operador ejecuta comprobaciones; los modelos no eligen comandos. Las listas de lectura corresponden a la tabla anterior.")
    p4.box(185,630,"Humano: alcance, revisión de hallazgos y publicación",width=235,height=48)
    p4.box(185,455,"Orquestador + controlador Python",width=235,height=55)
    p4.arrow(290,630,290,510); p4.arrow(310,510,310,630)
    for x,y,label,a,b in [(45,555,"T03 React: read_context + MCP; lectura frontend/src permitida",(210,510),(150,555)),(335,555,"T04 FastAPI: read_context + MCP; lectura backend/app permitida",(390,510),(440,555)),(45,345,"T05 Calidad: read_context; pruebas + reportes + checks + MCP",(210,455),(150,395)),(335,345,"T06 Seguridad: read_context; políticas + reportes",(390,455),(440,395))]:
        p4.box(x,y,label,height=50)
        p4.arrow(*a,*b); p4.arrow(b[0]+12,b[1],a[0]+12,a[1])
    y = p4.paragraph(310,"Ida: tarea, entradas y permisos. Vuelta: informe con hallazgos, límites y evidencia. T05/T06 reciben ambas verificaciones MCP mediante el orquestador. No se invocan entre sí ni comparten una conversación lateral.")
    y = p4.paragraph(y,"Controlador -> cliente MCP -> filesystem externo por stdio -> copia temporal. Verifica texto leído y denegación del archivo original. Solo main de cada stack llega completo por MCP; fuentes adicionales son extractos. context_receipts identifica truncamientos y huellas del contexto entregado.")
    p4.paragraph(y,"La leyenda solicitada Diagrama confirmado con el proyecto de referencia (R-27) requiere confirmación no disponible. Este diagrama se contrastó documentalmente con Colmena Invertida; no se atribuye confirmación al profesor.")

    p5 = Page("2. Sistema de agentes | diagrama de flujo y puertas", 5)
    labels = ["Humano autoriza alcance (--approved)","G1: cuatro checks, suites positivas y contenido vigente", "Plan LLM: contrato válido o hasta 2 correcciones", "T03/T04: lectura MCP + inferencias + reportes", "G2: contratos, hashes y ambas verificaciones MCP", "T05/T06: contraste de informes y políticas", "G3: código y bytes de checks estables", "G4 operador (CLI): release_gate + revisión de hallazgos", "Humano revisa: aceptar, corregir o rechazar"]
    for i,label in enumerate(labels):
        yy=690-51*i
        p5.box(60,yy,label,width=375,height=36)
        if i: p5.arrow(247,yy+51,247,yy+36)
    p5.box(460,550,"PROPUESTO: Pausa del Colibrí, 7 s antes de cada T03-T06. No ejecutada",width=90,height=100)
    p5.commands.append("[3 3] 0 d")
    p5.arrow(460,565,435,555)
    p5.commands.append("[] 0 d")
    p5.box(460,440,"STOP: fallo / intentos agotados",width=90,height=100)
    for yy in (657,606,504,402,351):
        p5.arrow(435,yy,450,yy)
    p5.commands.append("450 351 m 450 657 l S")
    p5.arrow(450,490,460,490)
    p5.text(445,685,"No / fallo",8)
    for x,label in ((45,"Aceptar: alcance revisado"),(220,"Corregir: operador y G1"),(395,"Rechazar: STOP")):
        p5.box(x,235,label,width=155,height=30)
        p5.arrow(247,282,x+77,265)
    y=p5.paragraph(205,"G1/G2/G3 fallidas, ausencia de modelo, timeout o denegación no esperada: detener, conservar fallo y corregir fuera del ejecutor. Un reporte blocked bloquea. Solo el formato inválido se reintenta automáticamente; al tercer fallo termina. Las flechas descendentes requieren éxito.")
    y=p5.paragraph(y,"Decisión humana: aceptar autoriza únicamente lo revisado; corregir vuelve al operador y exige nuevas pruebas; rechazar detiene. Ninguna opción ejecuta commit, push o merge. --approved declara alcance, no identidad ni revisión del plan generado; generated_plan_reviewed_by_human=false.")
    p5.paragraph(y,"Pausa del Colibrí figura como diseño propuesto antes de cada delegación, no como ejecución real ni mejora demostrada. Gate final: release_gate exige checks y 14 controles Chrome del mismo contenido; falla cerrado y nunca autoriza publicación.")

    p6 = Page("3. Calidad del código | matriz de controles", 6)
    y = p6.paragraph(730,"release_gate valida suites y 14 controles Chrome del mismo contenido antes de revisión humana. Las puertas automáticas validan resultados del operador; las conclusiones semánticas requieren revisión. Esta matriz distingue qué detecta un fallo y qué queda fuera. Detalle ampliado: matriz-calidad.md.")
    y = p6.table(y,["Riesgo IA", "Actor / momento", "Control / evidencia", "Bloqueo y límite"],[
        ["API/dependencia inventada", "Frontend/backend; tras cambio", "Build, TestClient e imports; checks nuevos", "Fallo bloquea G1; no toda API externa"],
        ["Pruebas vacías", "Host; antes de LLM", "Resumen positivo + OK; regresiones", "Sí G1; no detecta toda tautología"],
        ["Oráculo débil / prueba tautológica", "Calidad + humano; revisión tests", "test_api.py y reportes originales", "Oráculos fijos + revisión humana; sin mutación"],
        ["Presupuesto/validación/regresión", "Backend; tras cambios", "8 TestClient + 2 oráculos fijos: ids, total, saldo y límite", "Fallo bloquea G1; oráculos fijados al catálogo demo"],
        ["Filtros, demo, teclado y ARIA", "Frontend; tras build", "14 controles Chrome, JSON y PNG", "release_gate bloquea cierre; no WCAG completa"],
        ["Arquitectura / permisos", "Seguridad + host; cada tarea", "Listas permitidas, contratos, SHA, MCP negativo", "G2 bloquea; no sandbox OS"],
        ["Evidencia de otro código", "Host; inicio/cierre", "SHA + archivos, estabilidad de checks", "G1/G3; sin firma criptográfica"],
        ["Hallazgo falso o no resuelto", "Calidad/seguridad + humano", "Reportes y puerta de hallazgos", "No aceptación automática; no detector semántico universal"],
    ],[100,104,160,141],8.5)
    y=p6.paragraph(y,"Se corrigieron: aceptación de registros sin pruebas positivas; invalidación por metadatos Git sin cambio de contenido; ambigüedad entre inspección y aceptación. Se conservan las regresiones previas de checks incompletos y entrega del registro MCP a revisores.",9)
    p6.paragraph(y,"Los controles detectan fallos concretos; no certifican toda afirmación del modelo ni sustituyen aceptación humana.",9)

    p7 = Page("3. Calidad del código | resultados y pendientes",7)
    y=p7.table(730,["Ejecución", "Resultado real", "Artefacto"],[
        ["Agentes",str(counts['agents'])+" pruebas aprobadas","mejora-tecnica/checks.json"],
        ["Backend",str(counts['backend'])+" pruebas aprobadas","mejora-tecnica/checks.json; TestClient"],
        ["Sintaxis / build","Códigos 0 / 0","mejora-tecnica/checks.json"],
        ["Chrome primer intento","0 controles; fallo conexión CDP","mejora-tecnica/browser/after.json"],
        ["Chrome repetición",str(sum(c['passed'] for c in browser['checks']))+"/"+str(len(browser['checks'])),"mejora-tecnica/browser-02/after.json y PNG"],
        ["LLM/MCP revisión anterior",llm_summary,"llm-report-03.json; execution-03.json"],
        ["LLM/MCP histórico","5 inferencias, 2 sesiones; no reescritas","llm-report-final.json"],
    ],[140,155,210],9)
    y=p7.paragraph(y,"El informe nuevo identifica comandos, fechas, resultados y mapa de hashes. Los informes históricos conservan sus bytes. La aceptación de contenido idéntico no exige la misma rama/commit; estos siguen registrados como procedencia. El modelo disponible se comprueba sin instalar ni cambiar proveedor.")
    y=p7.paragraph(y,"No hay cobertura medida, mutación ni CI propio de Taller 5. Navegador integra la nueva puerta de cierre CLI; no altera las cuatro puertas previas al LLM ni protege main en GitHub. Persisten advertencias lucide-react y Starlette/HTTPX. Sin auditoría WCAG completa, lector de pantalla, Safari/Firefox, dispositivos físicos ni persistencia PostgreSQL probada.")
    y=p7.paragraph(y,"Pendiente con el profesor: aceptación de Codex, definición de escritura-orbital, ITC > 0,87 (sin fórmula), MutaGato (sin procedimiento), cronista-lunar y beneficio atribuido a Pausa del Colibrí. No se inventan coeficientes, certificaciones ni la frase de aprobación del profesor. Estos puntos impiden afirmar cumplimiento textual total.")
    y=p7.link(y,"Evidencias publicadas anteriores; corrección nueva aún local",REPO+"/tree/8cce952bace0763ac5e96208c70e93a304979fb4/docs/taller-5")
    y=p7.paragraph(y,"Histórico: checks.json registra 34 pruebas de agentes y 8 de API. frontend-repro.json acredita npm ci y build en copia temporal: Vite 8.3.5 del lockfile, frente a 8.3.8 instalado. No se repitió esa instalación limpia ni la inferencia LLM en esta fase; sus informes corresponden al código anterior. El primer intento LLM/MCP nuevo falló por timeout de npx; llm-execution.json conserva el fallo.")
    y=p7.paragraph(y,"El LLM puede errar aun con JSON y hashes válidos. revision-hallazgos.md conserva el análisis anterior; correccion-rubrica/contraste-llm.md refuta afirmaciones nuevas sobre selector, presupuesto y reportes. La revisión humana final de este PDF está pendiente.")

    p7.paragraph(y,"Esperamos que al profesor le guste este enfoque de calidad")

    p8 = Page("4. Diferencias con el sistema de referencia",8)
    y=p8.paragraph(730,"Comparación documental fijada: backend calidad-agentes/af004c4; frontend 001-project-baseline/33161da, sin rama calidad-agentes identificada. No se ejecutaron las aplicaciones ni pipelines del profesor. reference-evidence.json y correccion-rubrica/referencia-consultada.json conservan fuentes.")
    y=p8.table(y,["Referencia concreta", "OPITA 360 y justificación"],[
        ["Colmena Invertida: centro y especialistas sin lateralidad", "Se conserva retorno central para rastrear decisiones y limitar contexto entre React y FastAPI."],
        ["architect/test-developer/developer/reviewer/spec-auditor", "Frontend/backend/calidad/seguridad: revisión de aplicación existente; no pretende implementar TDD completo."],
        ["Copilot Opus/Sonnet; developer con edit/execute", "Qwen local sin edición ni shell del modelo: revisión acotada y sin credenciales remotas. Aceptación de herramienta pendiente."],
        [".NET/EF Core/PostgreSQL y Angular", "React/FastAPI con memoria: se conserva el stack real y no se fingen pruebas de base de datos."],
        ["Context7 y Angular CLI MCP", "Filesystem real sobre copia temporal: sirve para lectura autorizada; Angular CLI no corresponde al stack React."],
        ["Preset permite tasks.md, Red/Green y convergencia", "Cuatro tareas secuenciales fijas y cierre humano: no hay convergencia ni escritura autónoma."],
        ["CI con cobertura 80%; mutación backend informativa", "Regresiones y Chrome sin porcentaje ni CI: límites expresos; no se copia una cifra sin medirla."],
    ],[211,294],9)
    y=p8.link(y,"Backend del profesor: commit consultado",MS+"/tree/"+MS_SHA)
    y=p8.link(y,"Frontend del profesor: commit consultado",UI+"/tree/"+UI_SHA)
    y=p8.link(y,"Diagrama original de orquestación",MS+"/blob/"+MS_SHA+"/docs/diagrams/03-patron-orquestador.excalidraw")
    y=p8.link(y,"Preset de coordinación y cierre",MS+"/blob/"+MS_SHA+"/speckit-custom/presets/implement-orchestrator/commands/speckit.implement.md")
    p8.paragraph(y,"Verificado por el profesor en la rama calidad-agentes es una leyenda exigida sin aprobación acreditada: queda pendiente, no se presenta como hecho. La comparación realizada es del equipo, no una validación docente.",9)
    return [p1,p2,p3,p4,p5,p6,p7,p8]


def build_pdf(destination):
    document_pages=pages()
    assert 1 <= len(document_pages) <= 8
    objects=[None,b"<< /Type /Catalog /Pages 2 0 R >>",None,
             b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    kids=[]
    for page in document_pages:
        page_id=len(objects)
        content_id=page_id+1
        objects.extend([None,None])
        annotations=[]
        for x1,y1,x2,y2,url in page.links:
            annotations.append(f"{len(objects)} 0 R")
            objects.append(f"<< /Type /Annot /Subtype /Link /Rect [{x1} {y1} {x2} {y2}] /Border [0 0 0] /A << /S /URI /URI ({literal(url)}) >> >>".encode("latin1"))
        kids.append(f"{page_id} 0 R")
        objects[page_id]=f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R /Annots [{' '.join(annotations)}] >>".encode()
        content="\n".join(page.commands).encode("latin1")
        objects[content_id]=f"<< /Length {len(content)} >>\nstream\n".encode()+content+b"\nendstream"
    objects[2]=f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>".encode()
    output=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets=[0]
    for number,value in enumerate(objects[1:],1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode()+value+b"\nendobj\n")
    xref=len(output)
    output.extend(f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    destination.write_bytes(output)


if __name__ == "__main__":
    build_pdf(HERE/"taller5.pdf")
    print(f"PDF generado: {TOTAL} páginas, datos leídos de evidencias")

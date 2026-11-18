"""Entrega de siete páginas: lee evidencia real, dibuja diagramas y enlaces PDF."""
import json
from pathlib import Path
import re
import textwrap

HERE = Path(__file__).resolve().parent
TOTAL = 7
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
        self.text(45, 798, "OPITA 360 | Taller 5: Sistema de Agentes", 17)
        self.text(45, 768, title, 13)
        self.text(45, 29, f"FET-QX7 | taller5/sistema-agentes | docs/taller-5 | Página {number}/{TOTAL}", 8)

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
    checks = artifact("checks.json")
    llm = artifact("llm-report-final.json")
    browser = artifact("browser/after.json")
    repro = artifact("frontend-repro.json")
    if not llm.get("llm_executed") or len(llm.get("reports",[])) != 4:
        raise ValueError("Falta ejecución LLM final")
    counts = {}
    for check in checks["checks"]:
        if check["exit_code"] != 0:
            raise ValueError("Hay pruebas fallidas")
        match = re.search(r"Ran (\d+) tests",check["stderr"])
        if match:
            counts[check["check"]] = int(match.group(1))
    passed = sum(c["passed"] for c in browser["checks"])
    calls = sum(c.get("llm_executed") is True for c in llm["model_calls"])

    p1 = Page("1. Proyecto y herramienta",1)
    y = p1.paragraph(730,"OPITA 360 permite explorar destinos del Huila y preparar itinerarios. Usa React, Vite y lucide-react en frontend, y Python con FastAPI/Pydantic en backend. Los datos siguen en memoria; PostgreSQL tiene un esquema SQL, pero no una conexión persistente.",size=12)
    y = p1.paragraph(y,"El taller añade revisión de código asistida por agentes. Se elaboró con Codex y herramientas Python; las inferencias se ejecutan en Ollama local. La especificación delimita el alcance, el plan organiza la revisión y las tareas T03-T06 asignan responsables y permisos. Los agentes no editan funciones turísticas.",size=12)
    y = p1.paragraph(y,"El repositorio ya contiene commits, incluidos def65fe y c72c3c9. En la consulta de GitHub, el PR #2 estaba abierto, sin fusionar y con cabecera c72c3c9. Esta corrección es trabajo local posterior, pendiente de revisión y publicación; no se confunde con una rama remota ya actualizada.",size=12)
    y = p1.link(y,"Repositorio OPITA 360",REPO)
    y = p1.link(y,"Pull Request #2: Taller 5",PR)
    y = p1.paragraph(y-8,"Entorno: Python 3.10+, Node compatible con el lockfile y Ollama en 127.0.0.1:11434. El modelo es qwen3.5:4b. MCP usa stdio con filesystem 2.3.0, ejecutado mediante Node portátil 24.13.0 sin sustituir Node del sistema.",size=12)
    p1.paragraph(y,"Qwen se eligió por disponibilidad local, ejecución comprobable y ausencia de credenciales remotas. No se midió que sea mejor que otro modelo. Cinco contextos sobre el mismo modelo no implican diversidad ni garantizan independencia de sus errores.",size=12)

    p2 = Page("2. Sistema de agentes | roles y permisos",2)
    y = p2.paragraph(730,"Python emite cuatro tareas fijas y controla herramientas, secuencia y contratos. El LLM propone un plan narrativo y hallazgos; no crea roles ni decide libremente qué ejecutar. Todos usan Ollama local con el identificador exacto qwen3.5:4b.")
    y = p2.table(y,["Agente / ID","Perfil / modelo","Responsabilidad","Herramientas","Lectura autorizada"],[
        ["Orquestador","planner; Qwen 3.5:4b","Plan; controlador delega y valida","delegate; validate_report; llm_chat","Sin lectura directa del modelo: recibe especificación y tareas"],
        ["Frontend T03","coder; Qwen 3.5:4b","React, filtros, API, accesibilidad y demo","read_context; llm_chat; external_mcp","README/AGENTS, skill frontend, main.jsx, styles.css y package.json"],
        ["Backend T04","coder; Qwen 3.5:4b","FastAPI, validaciones y contrato HTTP","read_context; llm_chat; external_mcp","README/AGENTS, skill backend, main.py, requirements.txt y schema.sql"],
        ["Calidad T05","reviewer; Qwen 3.5:4b","Contrastar T03/T04, checks y registro MCP","read_context; llm_chat","README, paquetes/requisitos, test_runtime.py y test_api.py; reportes del controlador"],
        ["Seguridad T06","reviewer; Qwen 3.5:4b","Políticas, reportes y denegaciones MCP","read_context; llm_chat","AGENTS, manifest.v1.json, runtime.py y mcp_probe.py; reportes del controlador"],
    ],[70,72,113,110,140],size=8.5)
    y = p2.paragraph(y,"Los perfiles no cambian el modelo. Las listas exactas están en agents/manifest.v1.json: no son permisos recursivos sobre carpetas. Ningún modelo tiene edición, shell libre, secretos, PostgreSQL, commit, push o merge. Solo frontend/backend reciben el contexto MCP previsto.",size=9)
    p2.paragraph(y,"El cliente autoriza read_text_file, no las escrituras anunciadas por el servidor. El modelo solo usa el endpoint loopback fijo. Node mantiene permisos del usuario: copia temporal y listas permitidas no equivalen a sandbox del sistema operativo.",size=9)

    p3 = Page("2. Sistema de agentes | estructura centralizada",3)
    p3.paragraph(730,"Adaptación de Colmena Invertida para revisión: el controlador central entrega tareas y recibe informes. No hay invocaciones entre especialistas. Las flechas de vuelta representan reportes, no permiso para llamar a otro agente.")
    p3.box(190,630,"Operador humano: autoriza alcance y revisa cierre",height=45)
    p3.box(190,450,"Orquestador LLM + controlador Python",height=60)
    p3.arrow(297,630,297,510)
    p3.arrow(312,510,312,630)
    for x,y,label,a,b in [
        (45,570,"T03 Frontend: React y consumo API",(220,510),(185,570)),
        (335,570,"T04 Backend: FastAPI y contratos",(375,510),(410,570)),
        (45,330,"T05 Calidad: reportes, checks y MCP",(220,450),(185,380)),
        (335,330,"T06 Seguridad: políticas y evidencia",(375,450),(410,380))]:
        p3.box(x,y,label,height=50)
        p3.arrow(*a,*b)
        p3.arrow(b[0]+15,b[1],a[0]+15,a[1])
    p3.text(190,305,"Flechas: tareas e informes, sin comunicación lateral",8)
    p3.paragraph(275,"El controlador ejecuta herramientas con rutas y argumentos acotados. Frontend/backend reciben main completo por MCP y extractos de hasta 4000 caracteres por fuente adicional. context_receipts registra tamaño, truncamiento y hashes: un hash del host no demuestra lectura integral por el modelo.")
    p3.paragraph(165,"Calidad y seguridad reciben reportes previos, checks y ambas verificaciones MCP. El informe guarda mcp_roles_received y mcp_ledger_sha256 para comprobar esa entrega. El contrato valida estructura y evidencia, pero no garantiza que una conclusión del modelo sea cierta.")

    p4 = Page("2. Sistema de agentes | flujo y control humano",4)
    labels=["Operador autoriza alcance (--approved)","Tareas T03-T06; snapshot y checks completos",
        "Plan narrativo LLM: formato validado","MCP frontend + inferencia T03 + reporte validado",
        "MCP backend + inferencia T04 + reporte validado","T05: reportes, checks y registro MCP completo",
        "T06: reportes, checks, MCP y políticas","Contratos y estabilidad del código/checks",
        "awaiting_human_review: sin aceptación automática"]
    for i,label in enumerate(labels):
        y=695-54*i
        p4.box(135,y,label,width=325,height=38)
        if i:
            p4.arrow(297,y+54,297,y+38)
    p4.box(475,620,"Fallo real: detener",width=75,height=65)
    p4.arrow(460,660,475,660)
    p4.paragraph(225,"Solo se reintenta el formato de una respuesta inválida: máximo dos correcciones por rol. No hay autocorrección de código ni convergencia hasta implementar requisitos. Si faltan modelo, dependencias o permisos, se informa el error sin respuestas prefijadas.")
    p4.paragraph(145,"--approved declara autorización del operador, no identidad autenticada. Se guardan ID, fecha, rama y hashes. El plan generado no tiene aprobación humana individual: generated_plan_reviewed_by_human=false. La aceptación final ocurre fuera del ejecutor; publicar o fusionar requiere otra decisión.")

    p5 = Page("3. Calidad del código | pruebas y evidencia",5)
    y = p5.paragraph(730,"La auditoría encontró dos fallos: checks=[] superaba la puerta de calidad y los revisores no recibían el registro MCP. Se añadieron siete regresiones. La primera ejecución falló por el módulo aún inexistente; tras implementarlo pasaron. Esto no acredita TDD completo para todo el proyecto.")
    y = p5.table(y,["Verificación","Resultado registrado","Evidencia"],[
        ["Agentes y permisos",f"{counts['agents']} pruebas, código 0","checks.json / agents"],
        ["API FastAPI",f"{counts['backend']} pruebas, código 0","checks.json / backend"],
        ["Sintaxis backend / build frontend","Ambos código 0","checks.json"],
        ["npm ci + build en copia temporal",str([c['exit_code'] for c in repro['checks']]),"frontend-repro.json"],
        ["Chrome real, teclado y accesibilidad",f"{passed}/{len(browser['checks'])} comprobaciones","browser/after.json y PNG"],
        ["Inferencias reales",f"{calls} llamadas completadas","llm-report-final.json"],
        ["MCP externo por stdio",f"{len(llm['mcp'])} sesiones","llm-report-final.json / mcp"],
    ],[170,160,175])
    y = p5.paragraph(y,"La puerta exige cuatro comprobaciones únicas, comandos y directorios previstos, código entero 0, salidas completas, fecha con zona y snapshot coincidente. Rechaza registros vacíos, parciales, duplicados o fallidos. Valida el registro del operador; no firma criptográficamente la ejecución.")
    y = p5.paragraph(y,"Chrome comprobó filtros, lista vacía y recuperación, API y demostración, teclado, nombres accesibles y ancho móvil. Se corrigieron etiquetas de búsqueda/días y estado ARIA del menú. No se ejecutó auditoría WCAG completa, lector de pantalla ni todos los dispositivos.")
    p5.paragraph(y,"agents.verify ejecuta comandos fijos del operador. Temperatura 0 no promete respuestas idénticas. La instalación limpia usa el lockfile en copia temporal. Los JSON conservan comandos, fechas y advertencias: compilar no sustituye una prueba funcional.")

    p6 = Page("3. Calidad del código | límites y trazabilidad",6)
    y = p6.paragraph(730,"La evidencia anterior se conserva en history/pre-delivery-audit/. llm-report.json y checks-llm-historical.json pertenecen a la ejecución inicial. El reporte nuevo es llm-report-final.json; checks.json y browser/after.json identifican sus fuentes por hashes. Las respuestas del modelo no se reescriben para hacerlas parecer correctas.")
    y = p6.paragraph(y,"En la revisión inicial, el LLM cuestionó límites que Pydantic sí aplica y omitió pruebas MCP existentes. revision-hallazgos.md contrasta esas afirmaciones. En el flujo corregido, T05/T06 reciben el registro MCP; sus opiniones siguen sujetas a revisión humana.")
    y = p6.paragraph(y,"No hay cobertura porcentual medida, mutation testing ni CI propio. Pasar pruebas no acredita 80% de cobertura. Persisten advertencias de lucide-react y deprecación de Starlette/HTTPX. PostgreSQL no está conectado: no se presentan pruebas de persistencia como realizadas.")
    y = p6.paragraph(y,"La configuración asigna modelos, no estados históricos. llm_executed y métricas provienen de cada traza. Los reportes validan tarea-agente, evidencia no vacía, duplicados, hashes y alcance. Ningún hallazgo cambia automáticamente la aplicación turística.")
    y = p6.paragraph(y,"El PDF contiene offsets binarios; convertir LF a CRLF rompe su tabla xref. .gitattributes declara *.pdf binary para impedir esa conversión de Git. Se comprueban apertura estricta, renderizado, enlaces URI, cuatro secciones, FET-QX7 y un máximo de ocho páginas.")
    y = p6.paragraph(y,"La documentación se actualiza sobre commits existentes y un PR abierto. Estas correcciones locales no se publican en esta ejecución. Quedan revisión humana final y límites de accesibilidad; no se asigna una nota automática.")
    y = p6.link(y,"Resultados y comandos de la entrega",REPO+"/tree/taller5/sistema-agentes/docs/taller-5")
    p6.paragraph(y,"Las referencias se inspeccionaron en GitHub, sin ejecutar sus proyectos, modelos o pipelines. reference-evidence.json conserva ramas, SHA de blobs, URLs y extractos consultados.")

    p7 = Page("4. Diferencias con el sistema de referencia",7)
    y = p7.paragraph(730,"Backend: calidad-agentes (af004c4); frontend: 001-project-baseline (33161da). Backend también publica main y speckit-test; frontend, main. Los árboles de esas otras ramas no contienen los mismos agentes/presets. Comparar solo main habría omitido la configuración pertinente.")
    y = p7.table(y,["Aspecto","Referencia inspeccionada","Adaptación OPITA 360"],[
        ["Colmena Invertida","Centro coordina; especialistas devuelven informe y no se invocan","Controlador central, contextos separados, sin comunicación lateral"],
        ["Roles","architect, test-developer, developer, reviewer, spec-auditor","Frontend, backend, calidad y seguridad; revisión"],
        ["Código y pruebas","Roles separados escriben producción/pruebas; Red antes de Green","Modelos sin edición; comandos y cambios son del operador"],
        ["Modelos y MCP","Declara Opus/Sonnet en Copilot, Context7 y Angular CLI MCP","Qwen local y filesystem probado; no se ejecutó la referencia"],
        ["Calidad/cierre","CI configura 80% de cobertura; mutación backend informativa y convergencia","Regresión y navegador; sin porcentaje/CI/mutación; cierre humano"],
        ["Stack",".NET/EF Core/PostgreSQL y Angular","React/FastAPI y datos en memoria"],
    ],[82,211,212],size=9)
    y = p7.paragraph(y,"Se adopta coordinación central, no todo el sistema del profesor. Su preset permite al orquestador editar solo tasks.md y delega implementación. OPITA tiene análisis secuencial fijo, sin añadir tareas de convergencia. Son diferencias explícitas, no capacidades ya implementadas.",size=9)
    y = p7.link(y,"Referencia backend: calidad-agentes (commit fijado)",MS+"/tree/"+MS_SHA)
    y = p7.link(y,"Referencia frontend: 001-project-baseline (commit fijado)",UI+"/tree/"+UI_SHA)
    y = p7.link(y,"Profesor: diagrama de orquestación",MS+"/blob/"+MS_SHA+"/docs/diagrams/03-patron-orquestador.excalidraw")
    p7.link(y,"Profesor: preset de coordinación y cierre",MS+"/blob/"+MS_SHA+"/speckit-custom/presets/implement-orchestrator/commands/speckit.implement.md")
    return [p1,p2,p3,p4,p5,p6,p7]


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

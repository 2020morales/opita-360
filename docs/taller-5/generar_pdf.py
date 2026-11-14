"""PDF vectorial de cuatro páginas, sin dependencias para su generación.

Los resultados se citan como artefactos; no se fabrican conteos de pruebas.
"""
from pathlib import Path
import textwrap

HERE = Path(__file__).resolve().parent


def literal(value):
    value = value.replace("—", "-").replace("–", "-").replace("’", "'")
    return value.encode("cp1252", errors="replace").decode("latin1").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class Page:
    def __init__(self, title, number):
        self.commands = ["0.12 0.22 0.19 rg", "0.12 0.22 0.19 RG"]
        self.text(45, 796, "OPITA 360 | Taller 5: Sistema de Agentes", 17)
        self.text(45, 766, title, 14)
        self.text(45, 32, f"Rama: taller5/sistema-agentes | Evidencia en docs/taller-5 | Página {number}/4", 8)

    def text(self, x, y, value, size=10):
        self.commands.append(f"BT /F1 {size} Tf 1 0 0 1 {x} {y} Tm ({literal(value)}) Tj ET")

    def paragraph(self, y, value, width=92):
        for line in textwrap.wrap(value, width=width):
            self.text(45, y, line)
            y -= 14
        return y - 10

    def box(self, x, y, value, width=215, height=34):
        self.commands.append(f"0.92 0.96 0.92 rg {x} {y} {width} {height} re B 0.12 0.22 0.19 rg")
        lines = textwrap.wrap(value, width=max(12, int(width / 5.1)))
        start = y + height / 2 + (len(lines) - 1) * 5 - 3
        for line in lines:
            self.text(x + 9, start, line, 9)
            start -= 11

    def arrow(self, x1, y1, x2, y2):
        self.commands.append(f"0.7 w {x1} {y1} m {x2} {y2} l S")
        if y1 != y2:
            direction = 1 if y2 > y1 else -1
            self.commands.append(f"{x2-3} {y2-direction*5} m {x2} {y2} l {x2+3} {y2-direction*5} l S")
        else:
            direction = 1 if x2 > x1 else -1
            self.commands.append(f"{x2-direction*5} {y2-3} m {x2} {y2} l {x2-direction*5} {y2+3} l S")


def pages():
    p1 = Page("1. Proyecto y herramienta", 1)
    y = p1.paragraph(730, "OPITA 360 es una aplicación turística del Huila. El frontend usa React, Vite y lucide-react; el backend utiliza Python, FastAPI y Pydantic. Los datos actuales están en memoria. PostgreSQL solo tiene un esquema preparado, sin conexión persistente.")
    y = p1.paragraph(y, "El taller incorpora herramientas de desarrollo en Python, Ollama local y un servidor MCP externo. No cambia funciones turísticas, API, CORS ni esquema SQL. No se hacen commits ni push.")
    y = p1.paragraph(y, "La especificación delimita revisión de código con evidencias auténticas. La planificación emite cuatro tareas con permisos fijos y contratos que vinculan tarea, agente y archivos. La procedencia del plan es Codex, sin atribuir a Copilot un documento inexistente.")
    p1.box(45, 465, "React/Vite: frontend existente", 220, 42)
    p1.box(330, 465, "FastAPI: backend existente", 220, 42)
    p1.arrow(265, 486, 330, 486)
    p1.box(175, 365, "Revisión del taller: independiente de la aplicación turística", 245, 52)
    p1.paragraph(320, "Herramientas: Python 3.10+, Ollama en 127.0.0.1:11434, modelo qwen3.5:4b y MCP por stdio. Node portátil 24.13.0 ejecuta el servidor externo sin sustituir Node del sistema. Los modelos no reciben shell ni edición turística.")
    p1.paragraph(225, "Rúbrica del usuario: calidad del código 25%; agentes 20%; diagramas 20%; herramientas, permisos y modelo 15%; diferencias con referencia 10%; documento 10%. Este PDF contiene cuatro páginas dentro del máximo de ocho.")

    p2 = Page("2. Sistema de agentes", 2)
    p2.paragraph(730, "Los cinco roles usan qwen3.5:4b con contextos separados. Asignar un modelo no demuestra inferencia: solo las trazas reales permiten afirmar ejecución. El modo determinista no simula un LLM.")
    p2.box(190, 620, "Operador: autoriza alcance")
    p2.box(190, 560, "Orquestador LLM: plan validado")
    p2.arrow(297, 620, 297, 594)
    p2.box(45, 485, "T03 Frontend: React, API y fallback", 225, 42)
    p2.box(325, 485, "T04 Backend: contratos y validaciones", 225, 42)
    p2.arrow(250, 560, 157, 527)
    p2.arrow(345, 560, 437, 527)
    p2.box(190, 420, "MCP: contexto de lectura permitido")
    p2.arrow(157, 485, 245, 454)
    p2.arrow(437, 485, 350, 454)
    p2.box(190, 350, "T05 Calidad: reportes y checks")
    p2.arrow(297, 420, 297, 384)
    p2.box(190, 290, "T06 Seguridad: políticas y reportes")
    p2.arrow(297, 350, 297, 324)
    p2.box(190, 230, "awaiting_human_review")
    p2.arrow(297, 290, 297, 264)
    p2.paragraph(195, "Frontend y backend reciben código leído realmente por MCP. Calidad revisa sus reportes y checks del operador; seguridad recibe políticas y resultados previos. Los hallazgos no se aplican automáticamente.")
    p2.paragraph(125, "MCP: @modelcontextprotocol/server-filesystem@2.3.0 por stdio. Se exporta un archivo permitido, compara la lectura y verifica rechazo fuera del scope. Escrituras anunciadas no se autorizan. Staging no es sandbox OS.")

    p3 = Page("3. Calidad del código", 3)
    p3.paragraph(730, "La revisión conserva contratos y funcionalidades existentes. Las pruebas verifican tarea-agente, evidencia no vacía, duplicados, hashes, permisos y límites. El modelo puede errar: los hallazgos requieren contraste humano.")
    labels = ["Especificación y aprobación", "Plan LLM y contratos válidos", "T03/T04 con MCP y evidencias", "T05/T06: revisión especializada", "Informe pendiente de revisión humana"]
    for index, label in enumerate(labels):
        y = 610 - 60 * index
        p3.box(190, y, label)
        if index:
            p3.arrow(297, y + 60, 297, y + 34)
    p3.paragraph(325, "Resultados actuales: 27 pruebas de agentes y 8 de API aprobadas (35 total), compilaciones correctas. Chrome real: 11/14 antes y 14/14 después. Se corrigieron etiqueta de búsqueda, nombre del selector de días y estado ARIA del menú. Filtros, API, demo y teclado comprobados; registros y PNG en browser/.")
    p3.paragraph(225, "Pruebas limitadas: nombres accesibles vía Chrome, etiquetas, teclado y ancho móvil; no certifican WCAG ni lector de pantalla. Las cinco inferencias y dos MCP son anteriores a la corrección. Se conserva checks-llm-historical.json; checks.json es actual. No se repitió LLM/MCP ni npm ci en esta actualización.")
    p3.paragraph(125, "El LLM erró sobre validación de presupuesto y ausencia de pruebas MCP. T05/T06 no recibieron ledger MCP explícito; el asistente contrastó las afirmaciones con el host. Ver revision-hallazgos.md. Aceptación humana pendiente: la ejecución no prueba precisión semántica ni autoriza commit o push.")

    p4 = Page("4. Diferencias con el sistema de referencia", 4)
    y = p4.paragraph(730, "PENDIENTE: el sistema de referencia no está disponible. El usuario autorizó continuar dejando la comparación pendiente. No se inventan semejanzas o diferencias ni se afirma cumplimiento del 10% correspondiente.")
    y = p4.paragraph(y, "Al recibir la fuente se contrastarán arquitectura, roles, modelos, permisos, MCP, aprobación humana y calidad. Cada diferencia debe citar archivos, decisiones o ejecuciones verificables de ambos sistemas.")
    y = p4.paragraph(y, "Contraste interno distinto de la referencia: la versión previa inventariaba archivos con perfiles de modelo nulos. La corrección incorpora asignación local explícita, análisis LLM especializado, contexto MCP utilizado por frontend/backend, revisión de reportes previos y trazabilidad.")
    y = p4.paragraph(y, "Ese contraste no atribuye propiedades a una referencia desconocida. Tampoco prueba ejecución por sí solo: los resultados auténticos se inspeccionan en los artefactos de la ejecución final.")
    y = p4.paragraph(y, "Archivos para revisión: rubrica.md, especificacion.md, tareas.md, arquitectura.md, entrega.md, resultados.md y artefactos de pruebas/LLM. El ejecutor conserva la aplicación turística y PostgreSQL continúa sin conexión. Los pendientes deben permanecer visibles.")
    p4.paragraph(y, "Antes de aceptar la entrega, una persona revisa el diff, las respuestas LLM, las comprobaciones reales y su correspondencia con el código. Una prueba no ejecutada o una aprobación automática no sustituye esa revisión.")
    return [p1, p2, p3, p4]


def build_pdf(destination):
    document_pages = pages()
    objects = [None, b"<< /Type /Catalog /Pages 2 0 R >>", None,
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    kids = []
    for page in document_pages:
        page_id = len(objects)
        content_id = page_id + 1
        kids.append(f"{page_id} 0 R")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>".encode())
        content = "\n".join(page.commands).encode("latin1")
        objects.append(f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"\nendstream")
    objects[2] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>".encode()
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, value in enumerate(objects[1:], 1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode() + value + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    destination.write_bytes(output)


if __name__ == "__main__":
    build_pdf(HERE / "taller5.pdf")
    print("PDF generado: taller5.pdf (4 páginas; verificar con lector PDF)")

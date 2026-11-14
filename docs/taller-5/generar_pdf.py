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
        self.text(45, 32, f"FET-QX7 | Rama: taller5/sistema-agentes | Evidencias: docs/taller-5 | Página {number}/4", 8)

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
    y = p1.paragraph(730, "OPITA 360 permite explorar destinos turísticos del Huila. Su frontend usa React, Vite y lucide-react; el backend está desarrollado en Python con FastAPI y Pydantic. Por ahora, los datos se manejan en memoria. Existe un esquema para PostgreSQL, pero aún no hay conexión persistente.")
    y = p1.paragraph(y, "Para este taller añadimos un sistema de revisión de código con herramientas en Python, Ollama local y un servidor MCP externo. Se mantienen las funciones turísticas, la API, CORS y el esquema SQL. Los cambios siguen sin commit ni push.")
    y = p1.paragraph(y, "El trabajo parte de una especificación, un plan y cuatro tareas. Cada tarea tiene permisos definidos y un contrato que relaciona el reporte con el agente y sus archivos. El plan se elaboró con Codex; no corresponde a un documento generado por Copilot.")
    p1.box(45, 465, "React/Vite: frontend existente", 220, 42)
    p1.box(330, 465, "FastAPI: backend existente", 220, 42)
    p1.arrow(265, 486, 330, 486)
    p1.box(175, 365, "Revisión del taller: independiente de la aplicación turística", 245, 52)
    p1.paragraph(320, "El entorno requiere Python 3.10+ y Ollama en 127.0.0.1:11434, con el modelo qwen3.5:4b. La conexión MCP usa stdio. El servidor externo se ejecuta con Node portátil 24.13.0, sin reemplazar la instalación del sistema. Los modelos no pueden ejecutar comandos libres ni editar la aplicación turística.")
    p1.paragraph(225, "La rúbrica asigna 25% a calidad del código, 20% a agentes, 20% a diagramas, 15% a herramientas, permisos y modelo, 10% a diferencias con la referencia y 10% al documento. Esta entrega tiene cuatro páginas y respeta el máximo de ocho.")

    p2 = Page("2. Sistema de agentes", 2)
    p2.paragraph(730, "El orquestador y los cuatro especialistas usan qwen3.5:4b en contextos separados. Las trazas registran las llamadas reales al modelo. También se conserva un modo determinista que solo inventaría archivos y no se presenta como una ejecución LLM.")
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
    p2.paragraph(195, "Frontend y backend analizan código obtenido por MCP. Calidad revisa sus reportes y las pruebas ejecutadas por el operador; seguridad revisa las políticas y los resultados anteriores. Las recomendaciones requieren revisión antes de aplicarse.")
    p2.paragraph(125, "MCP usa @modelcontextprotocol/server-filesystem@2.3.0 por stdio. Lee una copia autorizada, compara su contenido y comprueba el rechazo de archivos fuera del alcance. El cliente no permite escrituras. La copia temporal no aísla el proceso del sistema operativo.")

    p3 = Page("3. Calidad del código", 3)
    p3.paragraph(730, "Las pruebas comprueban la relación entre tarea y agente, la presencia de evidencias, los duplicados, los hashes, los permisos y los límites. Se mantienen los contratos y las funciones existentes. Las respuestas del modelo se contrastan con el código y los resultados de ejecución.")
    labels = ["Especificación y aprobación", "Plan LLM y contratos válidos", "T03/T04 con MCP y evidencias", "T05/T06: revisión especializada", "Informe pendiente de revisión humana"]
    for index, label in enumerate(labels):
        y = 610 - 60 * index
        p3.box(190, y, label)
        if index:
            p3.arrow(297, y + 60, 297, y + 34)
    p3.paragraph(325, "Pasaron 27 pruebas de agentes y 8 de API (35 en total), además de las compilaciones. En Chrome pasaron 11 de 14 comprobaciones antes y las 14 después de corregir la etiqueta de búsqueda, el nombre del selector de días y el estado ARIA del menú. Se probaron filtros, API, modo demo y teclado; browser/ conserva los registros y PNG.")
    p3.paragraph(225, "Chrome permitió revisar nombres accesibles, etiquetas, teclado y ancho móvil; falta una auditoría WCAG y un lector de pantalla. Las cinco inferencias LLM y dos sesiones MCP son anteriores a estas correcciones: sus pruebas están en checks-llm-historical.json; checks.json es actual. No se repitieron LLM/MCP ni npm ci en esa actualización.")
    p3.paragraph(125, "El LLM se equivocó al cuestionar la validación del presupuesto y negar las pruebas MCP. T05/T06 no recibieron su registro explícito; el asistente contrastó esas afirmaciones con las evidencias del entorno. revision-hallazgos.md explica las discrepancias. La aprobación humana final sigue pendiente; no se autoriza commit ni push.")

    p4 = Page("4. Diferencias con el sistema de referencia", 4)
    y = p4.paragraph(730, "La comparación queda pendiente porque aún no está disponible el sistema de referencia. Se autorizó continuar con el resto del taller, sin atribuir semejanzas o diferencias a un material que no se ha revisado. Por eso no se afirma cumplimiento del 10% de este criterio.")
    y = p4.paragraph(y, "Cuando se reciba la referencia, se compararán arquitectura, roles, modelos, permisos, MCP, aprobación humana y calidad. Cada diferencia se apoyará en archivos, decisiones o ejecuciones de ambos sistemas.")
    y = p4.paragraph(y, "Sí podemos describir los cambios frente a nuestra primera versión: antes solo se inventariaban archivos y los perfiles de modelo estaban vacíos. Ahora hay un modelo local asignado, análisis por especialidad, código obtenido por MCP para frontend y backend, revisión de reportes y trazabilidad de las ejecuciones.")
    y = p4.paragraph(y, "Esta evolución interna no reemplaza la comparación solicitada. Los registros de ejecución permiten comprobar qué se implementó, qué se probó y qué sigue pendiente, sin atribuir características a la referencia desconocida.")
    y = p4.paragraph(y, "La documentación de apoyo está en rubrica.md, especificacion.md, tareas.md, arquitectura.md, entrega.md y resultados.md, junto con las evidencias de pruebas y LLM. Las funciones turísticas se mantienen y PostgreSQL sigue sin conexión.")
    p4.paragraph(y, "La aceptación final requiere que una persona revise los cambios, las respuestas del modelo y su relación con las pruebas. Los resultados registrados no sustituyen esa decisión ni permiten dar por ejecutadas las verificaciones pendientes.")
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

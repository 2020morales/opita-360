"""Orquestación local con inventario determinista y flujo LLM optativo.

La aprobación CLI es una declaración del operador, no autenticación de identidad.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
SPECIALISTS = ("frontend", "backend", "calidad", "seguridad")
TASK_IDS = dict(zip(SPECIALISTS, ("T03", "T04", "T05", "T06")))
OBJECTIVES = {
    "frontend": "Revisar React, accesibilidad, filtros y recuperación en modo demostración",
    "backend": "Revisar contratos HTTP, validaciones y datos en memoria de FastAPI",
    "calidad": "Contrastar reportes de frontend/backend con criterios y resultados auténticos",
    "seguridad": "Revisar permisos, límites, riesgos MCP y controles humanos",
}


def load_manifest():
    manifest = json.loads((ROOT / "agents/manifest.v1.json").read_text(encoding="utf-8"))
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get("version") != "1.0.0" or manifest.get("mode") not in ("deterministic", "ollama"):
        raise ValueError("Manifiesto incompatible")
    if set(manifest.get("agents", {})) != {"orquestador", *SPECIALISTS}:
        raise ValueError("Roles incompletos")
    for role, declaration in manifest["agents"].items():
        if declaration.get("model_profile") not in manifest.get("models", {}):
            raise ValueError("Perfil de modelo desconocido")
        if not isinstance(declaration.get("read"), list) or not isinstance(declaration.get("tools"), list):
            raise ValueError("Permisos inválidos")
        if any(tool not in manifest.get("tools", {}) for tool in declaration["tools"]):
            raise ValueError("Herramienta desconocida")
    limits = manifest.get("limits", {})
    for name, minimum, maximum in (("max_spec_chars", 1, 4000),
                                    ("max_delegations", 1, len(SPECIALISTS)),
                                    ("max_correction_rounds", 0, 2)):
        value = limits.get(name)
        if type(value) is not int or not minimum <= value <= maximum:
            raise ValueError(f"Límite inválido: {name}")
    if any(limits.get(key) is not False for key in ("write", "shell", "network")):
        raise ValueError("El inventario no permite escritura, shell o red")
    if manifest["tools"]["external_mcp"]["client_allowed_tools"] != ["read_text_file"]:
        raise ValueError("Solo se permite lectura MCP")


def authorize_tool(role, name):
    """Denegación por defecto según las herramientas del rol declarado."""
    manifest = load_manifest()
    if role not in manifest["agents"] or name not in manifest["agents"][role]["tools"]:
        raise ValueError("Herramienta no autorizada para el rol")
    return manifest["tools"][name]


def authorize_read(role, path):
    authorize_tool(role, "read_context")
    manifest = load_manifest()
    if not isinstance(path, str):
        raise ValueError("Rol o ruta inválidos")
    clean = PurePosixPath(path)
    if "\\" in path or clean.is_absolute() or ".." in clean.parts or path not in manifest["agents"][role]["read"]:
        raise ValueError("Lectura fuera de la lista permitida")
    resolved = (ROOT / path).resolve(strict=True)
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        raise ValueError("Ruta resuelta fuera del proyecto o no regular")
    # Rechaza enlaces/junctions incluso si apuntan dentro del proyecto.
    if resolved != ROOT / path:
        raise ValueError("Redirección de ruta no permitida")
    if resolved.stat().st_size > manifest["tools"]["read_context"]["max_bytes"]:
        raise ValueError("Contexto demasiado grande")
    return resolved


def build_tasks(spec):
    manifest = load_manifest()
    authorize_tool("orquestador", "delegate")
    if not isinstance(spec, str) or not spec.strip() or len(spec) > manifest["limits"]["max_spec_chars"]:
        raise ValueError("Especificación vacía o demasiado grande")
    if len(SPECIALISTS) > manifest["limits"]["max_delegations"]:
        raise ValueError("El plan excede el máximo de delegaciones autorizado")
    return [{"id": TASK_IDS[role], "agent": role, "objective": f"{OBJECTIVES[role]}. Requisito: {spec.strip()}",
             "files": manifest["agents"][role]["read"], "tools": manifest["agents"][role]["tools"],
             "acceptance": ["Contexto permitido inventariado", "Reporte v1 válido", "Revisión humana pendiente"]}
            for role in SPECIALISTS]


def validate_report(report, tasks=None):
    authorize_tool("orquestador", "validate_report")
    fields = {"version", "task_id", "agent", "status", "evidence", "findings", "limitations"}
    if not isinstance(report, dict) or set(report) != fields:
        raise ValueError("Campos de reporte inválidos")
    if report["version"] != "1.0.0" or report["agent"] not in SPECIALISTS or report["status"] not in ("inspected", "blocked"):
        raise ValueError("Versión, agente o estado inválidos")
    if not isinstance(report["task_id"], str) or not report["task_id"]:
        raise ValueError("Tarea inválida")
    if tasks is None:
        assigned = {"id": TASK_IDS[report["agent"]], "agent": report["agent"]}
    else:
        matches = [task for task in tasks if task.get("id") == report["task_id"]]
        if len(matches) != 1:
            raise ValueError("Reporte no asociado a una tarea emitida única")
        assigned = matches[0]
    if assigned["id"] != report["task_id"] or assigned["agent"] != report["agent"]:
        raise ValueError("Reporte no corresponde al agente y tarea asignados")
    for field in ("findings", "limitations"):
        if not isinstance(report[field], list) or any(not isinstance(s, str) for s in report[field]):
            raise ValueError("Lista de texto inválida")
    if not isinstance(report["evidence"], list):
        raise ValueError("Evidencia inválida")
    if report["status"] == "inspected" and not report["evidence"]:
        raise ValueError("Un reporte inspeccionado requiere evidencia")
    paths = []
    for item in report["evidence"]:
        if not isinstance(item, dict) or set(item) != {"path", "sha256", "bytes"}:
            raise ValueError("Campos de evidencia inválidos")
        if not isinstance(item["sha256"], str) or not re.fullmatch("[a-f0-9]{64}", item["sha256"]):
            raise ValueError("Hash inválido")
        if type(item["bytes"]) is not int or item["bytes"] < 0:
            raise ValueError("Tamaño inválido")
        content = authorize_read(report["agent"], item["path"]).read_bytes()
        paths.append(item["path"])
        if item["bytes"] != len(content) or item["sha256"] != hashlib.sha256(content).hexdigest():
            raise ValueError("Evidencia no coincide con el archivo actual")
    if len(paths) != len(set(paths)):
        raise ValueError("Evidencia duplicada")
    if tasks is not None and report["status"] == "inspected" and set(paths) != set(assigned["files"]):
        raise ValueError("Evidencia no cubre los archivos de la tarea emitida")


def run_demo(spec, approved=False):
    if approved is not True:
        raise PermissionError("Se requiere aprobación humana del plan")
    tasks = build_tasks(spec)
    reports = []
    for task in tasks:
        role = task["agent"]
        evidence = []
        for relative in load_manifest()["agents"][role]["read"]:
            content = authorize_read(role, relative).read_bytes()
            evidence.append({"path": relative, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)})
        report = {"version": "1.0.0", "task_id": task["id"], "agent": role,
                  "status": "inspected", "evidence": evidence,
                  "findings": [f"Contexto permitido inventariado para {role}; requiere interpretación humana o LLM."],
                  "limitations": ["Sin LLM: no genera código ni emite un dictamen de calidad.", "No ejecuta pruebas ni modifica archivos."]}
        validate_report(report, tasks)
        reports.append(report)
    return {"version": "1.0.0", "mode": "deterministic", "approval": "operator_assertion",
            "specification": spec, "tasks": tasks, "reports": reports,
            "next_gate": "human_review", "llm_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--approved", action="store_true")
    parser.add_argument("--mcp", action="store_true", help="Probar MCP externo para frontend y backend; requiere descarga autorizada")
    parser.add_argument("--llm", action="store_true", help="Ejecutar los modelos locales reales; no simula respuestas")
    args = parser.parse_args()
    if args.llm:
        import asyncio
        from agents.llm_workflow import main_run

        print(json.dumps(asyncio.run(main_run(args.spec, args.approved)), ensure_ascii=True, indent=2))
        return
    result = run_demo(args.spec, args.approved)
    if args.mcp:
        import asyncio
        from agents.mcp_probe import probe

        async def integrations():
            return [await asyncio.wait_for(probe(role), timeout=90) for role in ("frontend", "backend")]

        result["mcp"] = asyncio.run(integrations())
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()

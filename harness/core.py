"""Contratos, permisos y traduccion determinista de criterios. Sin shell del modelo."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ROLES = ("orquestador", "frontend", "backend", "calidad", "seguridad")
SPEC_IDS = tuple(f"{i:03}" for i in range(1, 6))

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def safe_path(relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise PermissionError("Ruta relativa POSIX requerida")
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts or any(x in (".git", ".env", ".venv", "node_modules") for x in p.parts):
        raise PermissionError("Ruta prohibida")
    resolved = (ROOT / p).resolve()
    if not resolved.is_relative_to(ROOT) or resolved != ROOT / p:
        raise PermissionError("Redireccion o ruta fuera del proyecto")
    return resolved

def manifest():
    m = json.loads((ROOT / "harness/manifest.json").read_text(encoding="utf-8"))
    if m.get("version") != 1 or set(m.get("agents", {})) != set(ROLES):
        raise ValueError("Manifiesto incompleto")
    if m.get("model") != {"provider": "ollama-local", "name": "qwen3.5:4b"}:
        raise ValueError("No se sustituye el modelo local asignado")
    expected = {"read_context", "llm_review", "delegate", "read_mcp"}
    for role, policy in m["agents"].items():
        if not set(policy["tools"]) <= expected or policy.get("write") is not False or policy.get("shell") is not False:
            raise ValueError("Permisos ampliados")
        if role != "orquestador" and "delegate" in policy["tools"]:
            raise ValueError("Solo el orquestador delega")
        if role not in ("frontend", "backend") and "read_mcp" in policy["tools"]:
            raise ValueError("MCP reservado a especialistas de codigo")
        for path in policy["read"]:
            safe_path(path)
    return m

def authorize(role, tool):
    policy = manifest()["agents"].get(role)
    if not policy or tool not in policy["tools"]:
        raise PermissionError("Rol/herramienta no autorizado")
    return policy

def context(role):
    policy = authorize(role, "read_context")
    result = []
    for rel in policy["read"]:
        p = safe_path(rel)
        if not p.is_file() or p.stat().st_size > 65536:
            raise PermissionError("Contexto inexistente o demasiado grande")
        raw = p.read_bytes()
        result.append({"path": rel, "sha256": digest(raw), "bytes": len(raw), "text": raw.decode("utf-8")})
    return result

def load_spec(spec_id):
    if spec_id not in SPEC_IDS:
        raise ValueError("ID de spec desconocido")
    matches = list((ROOT / "specs/taller-6").glob(spec_id + "-*/spec.json"))
    if len(matches) != 1:
        raise ValueError("Spec ausente o ambigua")
    source = safe_path(matches[0].relative_to(ROOT).as_posix())
    spec = json.loads(source.read_text(encoding="utf-8"))
    validate_spec(spec)
    return spec, matches[0].parent

def validate_spec(spec):
    if spec.get("id") not in SPEC_IDS or not isinstance(spec.get("title"), str) or not spec["title"].strip():
        raise ValueError("Identidad de spec invalida")
    if type(spec.get("amber")) is not int or not 1 <= spec["amber"] <= 9:
        raise ValueError("Factor Ambar fuera de escala")
    if spec.get("status") not in ("draft", "approved"):
        raise ValueError("Estado de especificacion invalido")
    criteria = spec.get("acceptance")
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("Se requieren criterios")
    ids = []
    for c in criteria:
        if not isinstance(c, dict) or set(c) != {"id", "given", "when", "then", "layer"}:
            raise ValueError("Contrato de criterio incompleto")
        if any(not isinstance(c[k], str) or not c[k].strip() for k in c):
            raise ValueError("Criterio vacio")
        if not re.fullmatch(r"AC-[0-9]{2}", c["id"]) or c["layer"] not in ("unit", "api", "browser"):
            raise ValueError("Criterio no verificable por capa")
        ids.append(c["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("Criterios duplicados")

def compass(spec):
    """Convierte Given/When/Then estructurados en casos; NO ejecuta ni inventa aserciones."""
    validate_spec(spec)
    return {"spec": spec["id"], "skill": "brújula-semántica", "execution": "not_run",
            "cases": [{"id": f"TC-{spec['id']}-{c['id'][3:]}", "acceptance_id": c["id"],
                       "arrange": c["given"], "act": c["when"], "assert": c["then"],
                       "layer": c["layer"], "status": "not_implemented"}
                      for c in spec["acceptance"]]}

def validate_report(report):
    required = {"role", "task", "mode", "model", "evidence", "findings", "limitations", "status"}
    if not isinstance(report, dict) or set(report) != required:
        raise ValueError("Campos de reporte incompatibles")
    if report["role"] not in ROLES or report["task"] != "review-" + report["role"]:
        raise ValueError("Agente/tarea no corresponden")
    if report["mode"] not in ("inventory", "llm") or report["status"] != "awaiting_human_review":
        raise ValueError("Modo o cierre invalido")
    expected_model = "qwen3.5:4b" if report["mode"] == "llm" else None
    if report["model"] != expected_model:
        raise ValueError("Modelo/ejecucion inconsistente")
    for key in ("findings", "limitations"):
        if not isinstance(report[key], list) or not report[key] or any(not isinstance(x, str) or not x.strip() for x in report[key]):
            raise ValueError("Hallazgos o limites vacios")
    expected = [{k: s[k] for k in ("path", "sha256", "bytes")} for s in context(report["role"])]
    if report["evidence"] != expected:
        raise ValueError("Evidencia incompleta, duplicada o distinta del contexto autorizado")

def validate_structure():
    manifest()
    found = sorted(p.parent.name for p in (ROOT / "specs/taller-6").glob("*/spec.json"))
    if len(found) != 5:
        raise ValueError("Se requieren exactamente cinco specs")
    result = []
    for sid in SPEC_IDS:
        spec, folder = load_spec(sid)
        for name in ("spec.md", "plan.md", "tasks.md", "pr.md"):
            if not (folder / name).is_file():
                raise ValueError("Artefacto SDD faltante: " + name)
        plan = (folder / "plan.md").read_text(encoding="utf-8")
        if f"Factor Ámbar: {spec['amber']}/9" not in plan:
            raise ValueError("Factor Ambar no coincide con plan")
        cases = compass(spec)
        result.append({"id": sid, "criteria": len(cases["cases"]), "status": spec["status"]})
    for slug, name in (("opita-frontend", "opita-frontend"), ("opita-backend", "opita-backend"),
                       ("brujula-semantica", "brújula-semántica")):
        raw = (ROOT / f".agents/skills/{slug}/SKILL.md").read_text(encoding="utf-8")
        if not raw.startswith("---\n") or f"name: {name}\n" not in raw or "description:" not in raw:
            raise ValueError("Skill no descubrible")
    return result

def snapshot():
    paths = []
    for directory in ("harness", ".agents/skills", "specs/taller-6", "agents", "backend/app", "backend/tests", "frontend/src", "frontend/tests"):
        paths.extend(p for p in (ROOT / directory).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    paths.extend(ROOT / p for p in ("AGENTS.md", "README.md", "frontend/package.json", "frontend/package-lock.json", "backend/requirements.txt"))
    return {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in sorted(set(paths))}

def validate_checks(record):
    if record.get("source_snapshot") != snapshot():
        raise ValueError("Checks obsoletos: ejecutar checks --scope all con este codigo")
    items = record.get("checks", [])
    names = [c.get("name") for c in items]
    if len(names) != 5 or set(names) != {"harness", "agents", "backend", "frontend", "build"}:
        raise ValueError("Se requieren las cinco comprobaciones completas")
    for c in items:
        if type(c.get("exit_code")) is not int or c["exit_code"] != 0 or not all(isinstance(c.get(k), str) for k in ("stdout", "stderr")):
            raise ValueError("Checks fallidos o incompletos")

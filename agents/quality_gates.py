"""Puertas del operador: conjunto completo, sin sustituir auditoría humana."""
from datetime import datetime
import re

COMMANDS = {
    "agents": (["-B", "-m", "unittest", "discover", "-s", "agents/tests", "-v"], "."),
    "backend": (["-B", "-m", "unittest", "discover", "-s", "backend/tests", "-v"], "."),
    "backend_compile": (["-m", "compileall", "app"], "backend"),
    "frontend_build": (["run", "build"], "frontend"),
}


def validate_checks(record, expected_snapshot):
    if not isinstance(record, dict) or record.get("version") != "1.1.0":
        raise ValueError("Versión de comprobaciones inválida")
    recorded_snapshot = record.get("snapshot", {})
    if not isinstance(recorded_snapshot, dict) or any(
        recorded_snapshot.get(key) != expected_snapshot.get(key) or not recorded_snapshot.get(key)
        for key in ("sha256", "files")
    ):
        raise ValueError("Primero ejecutar agents.verify con este código; checks obsoleto")
    try:
        timestamp = datetime.fromisoformat(record["finished_at"])
        if timestamp.tzinfo is None:
            raise ValueError("Fecha sin zona horaria")
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Fecha de comprobaciones inválida") from exc
    checks = record.get("checks")
    if not isinstance(checks, list) or len(checks) != len(COMMANDS):
        raise ValueError("Se requieren todas las comprobaciones, sin duplicados")
    names = [item.get("check") for item in checks if isinstance(item, dict)]
    if len(names) != len(checks) or set(names) != set(COMMANDS):
        raise ValueError("Comprobaciones desconocidas, faltantes o duplicadas")
    for item in checks:
        args, cwd = COMMANDS[item["check"]]
        command = item.get("command")
        allowed = ("npm", "npm.cmd") if item["check"] == "frontend_build" else ("python", "python.exe", "python3")
        if not isinstance(command, list) or not command or command[0] not in allowed or command[1:] != args:
            raise ValueError("Comando distinto de la comprobación declarada")
        if item.get("cwd") != cwd or type(item.get("exit_code")) is not int or item["exit_code"] != 0:
            raise ValueError("Comprobación fallida o directorio incorrecto")
        if not all(isinstance(item.get(key), str) for key in ("stdout", "stderr")):
            raise ValueError("Salida de ejecución incompleta")
        if item["check"] in ("agents", "backend"):
            output = item["stdout"] + "\n" + item["stderr"]
            summary = re.search(r"^Ran ([1-9][0-9]*) tests? in .+$", output, re.MULTILINE)
            if not summary or not re.search(r"^OK(?: \([^\n]*\))?\s*$", output, re.MULTILINE):
                raise ValueError("La suite debe ejecutar pruebas reales y terminar en OK")


def human_review_gate(reports):
    """Inspección no equivale a aceptación: todo hallazgo requiere revisión humana."""
    if any(report.get("status") == "blocked" for report in reports):
        return "blocked"
    if any(report.get("findings") for report in reports):
        return "awaiting_human_findings_review"
    return "awaiting_human_review"


def review_context(role, reports, checks, mcp_results):
    if role not in ("calidad", "seguridad"):
        raise ValueError("Contexto reservado a revisores")
    if len(mcp_results) != 2 or {entry.get("role") for entry in mcp_results} != {"frontend", "backend"}:
        raise ValueError("Registro MCP incompleto")
    if any(entry.get("content_equal") is not True or entry.get("outside_scope_denied") is not True for entry in mcp_results):
        raise ValueError("Verificación MCP fallida")
    return {"prior_reports": reports, "checks": checks, "mcp_verifications": mcp_results}

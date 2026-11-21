"""Comandos del operador. Los modelos no reciben este ejecutor como shell."""
import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
from .core import ROOT, compass, digest, load_spec, snapshot, validate_structure

def redact(text):
    # Antes de serializar JSON, para anonimizar tambien stdout/stderr.
    variants = [
        (str(ROOT.parent / "opita-360-taller4"), "<WORKTREE_T4>"),
        (str(ROOT), "<WORKTREE_T6>"),
        (str(Path(sys.executable).parent.parent), "<PYTHON_ENV>"),
    ]
    for original, alias in sorted(variants, key=lambda x: len(x[0]), reverse=True):
        for spelling in {original, original.replace("\\", "/"), original.replace("\\", "\\\\")}:
            text = re.sub(re.escape(spelling), lambda _: alias, text, flags=re.I)
    text = re.sub(r"(?i)[a-z]:[\\/]+Users[\\/]+[^\\/\r\n]+", "<LOCAL_USER>", text)
    return text

def save(record, label):
    directory = ROOT / "docs/taller-6/ejecuciones" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    directory.mkdir(parents=True, exist_ok=False)
    def scrub(value):
        if isinstance(value, str):
            return redact(value)
        if isinstance(value, list):
            return [scrub(v) for v in value]
        if isinstance(value, dict):
            return {k: scrub(v) for k, v in value.items()}
        return value
    content = json.dumps(scrub(record), ensure_ascii=False, indent=2)
    path = directory / (label + ".json")
    path.write_text(content + "\n", encoding="utf-8", newline="\n")
    print(path.relative_to(ROOT).as_posix())
    return path

def checks(scope):
    before = snapshot()
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    jobs = {
        "harness": ([sys.executable, "-B", "-m", "unittest", "discover", "-s", "harness/tests", "-v"], ROOT),
        "agents": ([sys.executable, "-B", "-m", "unittest", "discover", "-s", "agents/tests", "-v"], ROOT),
        "backend": ([sys.executable, "-B", "-m", "unittest", "discover", "-s", "backend/tests", "-v"], ROOT),
        "frontend": ([npm, "test"], ROOT / "frontend"),
        "build": ([npm, "run", "build"], ROOT / "frontend"),
    }
    selected = list(jobs) if scope == "all" else [scope]
    results = []
    for name in selected:
        args, cwd = jobs[name]
        try:
            if args[0] is None:
                raise FileNotFoundError("npm no encontrado")
            p = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=180, shell=False,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            item = {"name": name, "command": ["python" if name in ("harness", "agents", "backend") else "npm", *args[1:]],
                    "cwd": cwd.relative_to(ROOT).as_posix(), "exit_code": p.returncode,
                    "stdout": redact(p.stdout), "stderr": redact(p.stderr)}
        except (OSError, subprocess.TimeoutExpired) as exc:
            item = {"name": name, "exit_code": None, "error": redact(str(exc))}
        results.append(item)
        print(f"{name}: {item['exit_code']}", flush=True)
    if snapshot() != before:
        raise RuntimeError("Codigo cambio durante los checks")
    record = {"source_snapshot": before, "finished_at": datetime.now(timezone.utc).isoformat(), "checks": results,
              "executed_by": "operator_fixed_commands_not_model",
              "historical_evidence_overwritten": False}
    save(record, "checks")
    return 0 if all(i["exit_code"] == 0 for i in results) else 1

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    p = sub.add_parser("cases"); p.add_argument("--spec", required=True)
    p = sub.add_parser("review"); p.add_argument("--spec", required=True)
    p.add_argument("--max-seconds", type=int, help="Solo permite reducir el limite total del manifiesto")
    p.add_argument("--checks", help="Registro completo vigente, requerido con --llm")
    p.add_argument("--approved", action="store_true"); p.add_argument("--llm", action="store_true"); p.add_argument("--mcp", action="store_true")
    p = sub.add_parser("checks"); p.add_argument("--scope", choices=["all", "harness", "agents", "backend", "frontend", "build"], default="all")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            print(json.dumps({"specs": validate_structure(), "status": "structure_valid_not_implemented"}, ensure_ascii=False))
        elif args.command == "cases":
            spec, _ = load_spec(args.spec)
            save(compass(spec), "cases")
        elif args.command == "checks":
            return checks(args.scope)
        else:
            from .runtime import run
            save(asyncio.run(run(args.spec, args.approved, args.llm, args.mcp, args.checks, args.max_seconds)), "review")
        return 0
    except Exception as exc:
        # Fallo real; no sustituye una respuesta del modelo ni un resultado exitoso.
        save({"status": "failed", "command": args.command, "error_type": type(exc).__name__,
              "error": redact(str(exc) or type(exc).__name__), "partial": getattr(exc, "partial", None), "finished_at": datetime.now(timezone.utc).isoformat()}, "error")
        return 1

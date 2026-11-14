"""Comprobaciones fijas invocadas por el operador; no es una herramienta de agentes."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from .snapshot import snapshot

ROOT = Path(__file__).resolve().parents[1]


def main():
    before = snapshot()
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    checks = [
        ("agents", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "agents/tests", "-v"], ROOT),
        ("backend", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "backend/tests", "-v"], ROOT),
        ("backend_compile", [sys.executable, "-m", "compileall", "app"], ROOT / "backend"),
        ("frontend_build", [npm, "run", "build"], ROOT / "frontend"),
    ]
    results = []
    for name, command, directory in checks:
        try:
            if command[0] is None:
                raise FileNotFoundError("npm no encontrado")
            process = subprocess.run(command, cwd=directory, capture_output=True, text=True,
                                     encoding="utf-8", errors="replace", timeout=120, shell=False)
            result = {"check": name, "command": [Path(command[0]).name, *command[1:]],
                      "cwd": str(directory.relative_to(ROOT)) or ".", "exit_code": process.returncode,
                      "stdout": process.stdout.replace(str(ROOT), "<repo>"),
                      "stderr": process.stderr.replace(str(ROOT), "<repo>")}
        except (OSError, subprocess.TimeoutExpired) as exc:
            result = {"check": name, "exit_code": None, "error": str(exc)}
        results.append(result)
        print(f"{name}: {result['exit_code']}")
    after = snapshot()
    if before["sha256"] != after["sha256"]:
        raise RuntimeError("Código cambió durante las pruebas")
    record = {"version": "1.1.0", "finished_at": datetime.now(timezone.utc).isoformat(),
              "snapshot": after, "checks": results}
    (ROOT / "docs/taller-5/checks.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if all(result["exit_code"] == 0 for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())

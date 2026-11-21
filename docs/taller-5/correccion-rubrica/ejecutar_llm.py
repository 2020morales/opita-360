"""Ejecuta el flujo real con límite global; conserva éxito o fallo sin sustituir respuestas."""
from datetime import datetime, timezone
import json
import argparse
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt", default="02", choices=["02", "03"])
    args = parser.parse_args()
    output = HERE / ("llm-execution.json" if args.attempt == "02" else "llm-execution-03.json")
    report = HERE / ("llm-report-" + args.attempt + ".json")
    if output.exists() or report.exists():
        raise FileExistsError("Usar otro destino para repetir; no sobrescribir evidencia")
    command = [sys.executable, "-B", "-m", "agents.runtime", "--approved", "--llm",
               "--checks-file", "docs/taller-5/correccion-rubrica/checks-02.json",
               "--spec", "Revisar frontend React y backend FastAPI; contrastar pruebas reales y permisos; no editar código turístico"]
    started = datetime.now(timezone.utc).isoformat()
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=600)
        record = {"status": "completed" if process.returncode == 0 else "failed",
                  "exit_code": process.returncode, "stdout": process.stdout,
                  "stderr": process.stderr}
        if process.returncode == 0:
            parsed = json.loads(process.stdout)
            report.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
            record["stdout"] = "Reporte íntegro en " + report.name
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
        record = {"status": "timeout", "exit_code": None,
                  "stdout": decoded(exc.stdout), "stderr": decoded(exc.stderr)}
    record.update(started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
                  timeout_seconds=600, command=["python", *command[1:]])
    for key in ("stdout", "stderr"):
        record[key] = record[key].replace(str(ROOT), "<repo>").replace(str(Path.home()), "<user>")
        record[key] = re.sub(r"[A-Za-z]:\\+Users\\+[^\\\r\n\x27]+(?=\\)", "<user>", record[key])
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(record["status"])
    return 0 if record["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

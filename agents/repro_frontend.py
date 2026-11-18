"""npm ci y build en copia temporal, conservando frontend original."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from .runtime import ROOT
from .snapshot import digest


def main():
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if not npm:
        raise RuntimeError("npm no encontrado")
    results = []
    with tempfile.TemporaryDirectory(prefix="opita-frontend-repro-") as temp:
        project = Path(temp) / "frontend"
        shutil.copytree(ROOT / "frontend", project, ignore=shutil.ignore_patterns("node_modules", "dist"))
        for args in (["ci", "--ignore-scripts", "--no-audit", "--no-fund"], ["run", "build"]):
            process = subprocess.run([npm, *args], cwd=project, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=180, shell=False)
            results.append({"command": ["npm.cmd", *args], "exit_code": process.returncode,
                "stdout": process.stdout.replace(temp, "<temp>"), "stderr": process.stderr.replace(temp, "<temp>")})
            if process.returncode:
                break
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), "lock_sha256": digest((ROOT / "frontend/package-lock.json").read_bytes()),
              "checks": results, "isolation": "temporary copy, npm ci --ignore-scripts", "original_modified": False}
    (ROOT / "docs/taller-5/frontend-repro.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(record, ensure_ascii=True, indent=2))
    return 0 if len(results) == 2 and all(r["exit_code"] == 0 for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

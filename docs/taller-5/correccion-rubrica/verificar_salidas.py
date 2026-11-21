"""Prueba las tres guardas de sobrescritura contra destinos históricos existentes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def main():
    output = HERE / "output-guards.json"
    if output.exists():
        raise FileExistsError("La evidencia ya existe")
    cases = [
        ("agents.verify", ["--output", "docs/taller-5/checks.json"], "docs/taller-5/checks.json"),
        ("agents.repro_frontend", ["--output", "docs/taller-5/frontend-repro.json"], "docs/taller-5/frontend-repro.json"),
        ("agents.browser_checks", ["--label", "after", "--output-dir", "docs/taller-5/browser"], "docs/taller-5/browser/after.json"),
    ]
    results = []
    for module, args, historical in cases:
        path = ROOT / historical
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        process = subprocess.run([sys.executable, "-B", "-m", module, *args], cwd=ROOT,
                                 capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        passed = process.returncode != 0 and "FileExistsError" in process.stderr and before == after
        results.append({"module": module, "command": ["python", "-B", "-m", module, *args],
                        "exit_code": process.returncode, "passed": passed,
                        "historical_sha256_before": before, "historical_sha256_after": after,
                        "stderr": process.stderr.replace(str(ROOT), "<repo>").replace(str(Path.home()), "<user>")})
    output.write_text(json.dumps({"finished_at": datetime.now(timezone.utc).isoformat(), "checks": results},
                                ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"Guardas aprobadas: {sum(r['passed'] for r in results)}/{len(results)}")
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

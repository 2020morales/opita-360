"""Lectura, renderizado y trazabilidad del PDF; no ejecuta ni inventa pruebas."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("No sobrescribir una validación anterior")
    pdf = ROOT / "docs/taller-5/taller5.pdf"
    reader = PdfReader(pdf, strict=True)
    document = pdfium.PdfDocument(pdf)
    pages, links = [], []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        bitmap = document[i].render(scale=1)
        image = bitmap.to_pil()
        assert "FET-QX7" in text.splitlines()[0]
        assert len(text) > 100
        pages.append({"page": i + 1, "size": list(image.size),
                      "render_sha256": sha(image.tobytes()), "characters": len(text)})
        for annotation in page.get("/Annots", []):
            uri = annotation.get_object().get("/A", {}).get("/URI")
            if uri:
                links.append(str(uri))
    assert 1 <= len(pages) <= 8
    text = "\n".join(p.extract_text() for p in reader.pages)
    for section in ("1. Proyecto y herramienta", "2. Sistema de agentes",
                    "3. Calidad del código", "4. Diferencias"):
        assert section in text, section
    verified_links = json.loads((HERE / "links.json").read_text(encoding="utf-8"))
    assert set(links) == {entry["url"] for entry in verified_links if entry["ok"]}
    paths = subprocess.check_output(["git", "ls-files", "docs/taller-5"], cwd=ROOT, text=True).splitlines()
    evidence = []
    for name in paths:
        if not (name.endswith((".json", ".png", ".txt")) or "/history/" in name):
            continue
        original = subprocess.check_output(["git", "show", "HEAD:" + name], cwd=ROOT)
        current = (ROOT / name).read_bytes()
        equivalent = original.replace(b"\r\n", b"\n") == current.replace(b"\r\n", b"\n")
        assert equivalent, name
        evidence.append({"path": name, "worktree_sha256": sha(current),
                         "commit_sha256": sha(original), "byte_equal": original == current,
                         "newline_equivalent": equivalent})
    changed = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    assert all(p.startswith(("agents/", "docs/taller-5/")) for p in changed)
    checked = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert checked.returncode == 0
    sys.path.insert(0, str(ROOT))
    from agents.snapshot import snapshot
    from agents.quality_gates import validate_checks
    checks_path = HERE / "checks.json"
    checks = json.loads(checks_path.read_text(encoding="utf-8"))
    current_snapshot = snapshot()
    validate_checks(checks, current_snapshot)
    baseline = json.loads((HERE / "preservacion-inicial.json").read_text(encoding="utf-8"))
    for name, expected in baseline.items():
        assert sha((ROOT / name).read_bytes()) == expected, name
    from agents.release_gate import validate_release
    browser = json.loads((HERE / "browser-02/after.json").read_text(encoding="utf-8"))
    assert validate_release(checks, browser, current_snapshot)["human_approval"] == "pending"
    candidates = changed + subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
    suspicious = []
    patterns = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
                r"\bgh[pousr]_[A-Za-z0-9]{20,}", r"\bAKIA[A-Z0-9]{16}\b",
                r"\bsk-[A-Za-z0-9_-]{20,}", r"[A-Za-z]:\\Users\\[^\\\s]+"]
    for name in candidates:
        path = ROOT / name
        if path.suffix.lower() in (".png", ".pdf") or not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if any(re.search(pattern, line) for pattern in patterns):
                suspicious.append({"path": name, "line": number})
    result = {"finished_at": datetime.now(timezone.utc).isoformat(), "pdf_sha256": sha(pdf.read_bytes()),
              "generator_sha256": sha((ROOT / "docs/taller-5/generar_pdf.py").read_bytes()),
              "pages": pages, "sections": 4, "links": links, "historical_evidence": evidence,
              "protected_paths_changed": [], "preserved_previous_artifacts": len(baseline), "diff_check_exit_code": checked.returncode,
              "checks_sha256": sha(checks_path.read_bytes()),
              "current_source_snapshot_sha256": current_snapshot["sha256"],
              "diff_check_warnings": checked.stderr, "suspicious_locations": suspicious,
              "limitations": ["El escaneo por patrones no garantiza ausencia universal de secretos.",
                              "Cinco archivos históricos difieren del blob por LF/CRLF preexistente; no se reescriben.",
                              "Renderizado y extracción no sustituyen aceptación humana."]}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"pages": len(pages), "links": len(links), "historical": len(evidence),
                      "suspicious": suspicious, "diff_check": checked.returncode}))


if __name__ == "__main__":
    main()

"""Identidad del código evaluado, incluyendo archivos sin commit."""
import hashlib
import subprocess
import json
from .runtime import ROOT


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot():
    paths = set()
    for directory in ("agents", "backend/app", "backend/tests", "frontend/src"):
        paths.update(p for p in (ROOT / directory).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    paths.update(ROOT / p for p in ("frontend/package.json", "frontend/package-lock.json", "backend/requirements.txt"))
    manifest = json.loads((ROOT / "agents/manifest.v1.json").read_text(encoding="utf-8"))
    paths.update(ROOT / path for role in manifest["agents"].values() for path in role["read"])
    hashes = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in sorted(paths)}
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    return {"branch": branch, "files": hashes, "sha256": digest(str(sorted(hashes.items())).encode())}

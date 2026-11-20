"""Inventario reproducible de los seis términos, sin editar fuentes o evidencias."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
TERMS = {
    "brujula-semantica": ("brujula-semantica", "brujula semantica"),
    "certificacion-fet-arn-42": ("fet-arn-42", "arnes certificado por el profesor"),
    "matriz-halcon": ("matriz halcon",),
    "factor-ambar": ("factor ambar", '"amber"'),
    "revision-profesor": ("spec revisada por el profesor",),
    "coeficiente-murcielago": ("coeficiente murcielago",),
}


def fold(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c))


def scan():
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    inventory, scanned, limitations = [], 0, []
    for name in filter(None, names):
        path = ROOT / name
        suffix = path.suffix.lower()
        units = []
        if suffix == ".pdf":
            for number, page in enumerate(PdfReader(path).pages, 1):
                units.append(("page:" + str(number), page.extract_text() or ""))
        elif suffix == ".pptx":
            with zipfile.ZipFile(path) as archive:
                for entry in archive.namelist():
                    if entry.startswith(("ppt/slides/slide", "ppt/notesSlides/notesSlide")) and entry.endswith(".xml"):
                        text = "\n".join(e.text or "" for e in ET.fromstring(archive.read(entry)).iter() if e.tag.endswith("}t"))
                        units.append((entry, text))
            limitations.append({"path": name, "limitation": "XML de texto y notas; no OCR de imágenes o texto rasterizado"})
        elif suffix in (".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2"):
            continue
        else:
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeError:
                limitations.append({"path": name, "limitation": "Binario o codificación no UTF-8; no se afirma ausencia textual"})
                continue
            units = [("line:" + str(n), line) for n, line in enumerate(text.splitlines(), 1)]
        scanned += 1
        hits = {term: [] for term in TERMS}
        for location, text in units:
            normalized = fold(text)
            for term, variants in TERMS.items():
                if any(v in normalized for v in variants):
                    hits[term].append(location)
        hits = {term: locations for term, locations in hits.items() if locations}
        if hits:
            inventory.append({"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                              "protected_history": name.startswith(("docs/taller-4/", "docs/taller-5/", "agents/")),
                              "matches": hits})
    return {"finished_at": datetime.now(timezone.utc).isoformat(), "tracked_files_scanned": scanned,
            "files_with_matches": len(inventory), "inventory": inventory, "limitations": limitations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("No sobrescribir evidencia")
    result = scan()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ("tracked_files_scanned", "files_with_matches")}))


if __name__ == "__main__":
    main()

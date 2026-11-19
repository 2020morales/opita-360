"""Puerta de revisión: suites y navegador del mismo contenido, nunca aprobación humana."""
import argparse
from datetime import datetime
import json
from pathlib import Path
from .quality_gates import validate_checks
from .snapshot import snapshot, digest

REQUIRED_BROWSER = {
    "real_api_catalog", "municipality_neiva", "combined_empty_filters",
    "search_and_municipality", "real_api_recommendations", "explicit_form_labels",
    "ax_control_names", "keyboard_select", "keyboard_tab", "offline_demo_and_recommendations",
    "mobile_menu_visible", "mobile_menu_expanded_state", "mobile_no_horizontal_overflow", "no_js_exceptions",
}


def validate_release(checks, browser, current):
    validate_checks(checks, current)
    if not isinstance(browser, dict) or browser.get("fatal_error"):
        raise ValueError("Navegador incompleto o fallido")
    stamp = datetime.fromisoformat(browser.get("timestamp", ""))
    if stamp.tzinfo is None:
        raise ValueError("Fecha de navegador sin zona")
    if not isinstance(browser.get("browser"), str) or not browser["browser"]:
        raise ValueError("Falta identificación del navegador")
    recorded = browser.get("snapshot", {})
    if any(not current.get(k) or recorded.get(k) != current[k] for k in ("sha256", "files")):
        raise ValueError("Navegador corresponde a otro contenido")
    entries = browser.get("checks", [])
    if not isinstance(entries, list) or len(entries) != len(REQUIRED_BROWSER):
        raise ValueError("Controles de navegador incompletos")
    if any(not isinstance(e, dict) for e in entries):
        raise ValueError("Control inválido")
    if {e.get("name") for e in entries} != REQUIRED_BROWSER:
        raise ValueError("Controles desconocidos, duplicados o ausentes")
    if any(e.get("passed") is not True or "observed" not in e for e in entries):
        raise ValueError("Control fallido o sin observación")
    return {"status": "ready_for_human_review", "human_approval": "pending",
            "publication_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checks", type=Path, required=True)
    parser.add_argument("--browser", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("No sobrescribir evidencia")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw_checks, raw_browser = args.checks.read_bytes(), args.browser.read_bytes()
    current = snapshot()
    try:
        result = validate_release(json.loads(raw_checks), json.loads(raw_browser), current)
    except (ValueError, TypeError, KeyError) as exc:
        result = {"status": "blocked", "error": str(exc), "publication_allowed": False}
    result.update(snapshot=current, checks_sha256=digest(raw_checks), browser_sha256=digest(raw_browser))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(result["status"])
    return 0 if result["status"] == "ready_for_human_review" else 1


if __name__ == "__main__":
    raise SystemExit(main())

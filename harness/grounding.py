"""Contexto por simbolos y contraste acotado de afirmaciones; no es un juez semantico universal."""
import ast
import re
from .core import ROOT, digest, safe_path

FACT_NAMES = ("pydantic_request_validation", "frontend_demo_fallback",
              "base_checks_passed", "spec_implementation_recorded", "spec_tests_executed")

def select_source(source):
    text = source["text"]
    lines = text.splitlines()
    ranges = []
    if source["path"] == "backend/app/main.py":
        tree = ast.parse(text)
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                start = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
                ranges.append((start, node.end_lineno))
        reason = "Imports, modelos Pydantic y handlers completos; sin repetir datos semilla."
    elif source["path"] == "frontend/src/main.jsx":
        start = next((i for i, line in enumerate(lines, 1) if "function App()" in line), 1)
        end = next((i-1 for i, line in enumerate(lines, 1) if "return <div" in line), len(lines))
        ranges = [(1, 5), (start, end)]
        reason = "Estado, fetch, filtros y makeTrip/fallback; interfaz visual omitida."
    elif source["path"].endswith(".py") and "/tests/" in source["path"]:
        tree = ast.parse(text)
        ranges = [(n.lineno, n.lineno) for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        reason = "Nombres de pruebas; resultados reales se reciben por separado."
    elif source["path"] == "harness/core.py":
        tree = ast.parse(text)
        names = {"safe_path", "manifest", "authorize", "validate_report", "validate_checks"}
        ranges = [(n.lineno, n.end_lineno) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        reason = "Funciones de permisos, contratos y checks pertinentes a seguridad."
    else:
        ranges = [(1, len(lines))]
        reason = "Documento o funcion auxiliar."
    excerpts = []
    budget = (1600 if "/tests/" in source["path"] else 4200) if source["path"].endswith((".py", ".jsx")) else 900
    used = 0
    for start, end in ranges:
        block = []
        for number in range(start, end+1):
            line = lines[number-1]
            if used + len(line) + 1 > budget:
                break
            block.append(f"{number}: {line}")
            used += len(line)+1
        if block:
            excerpts.append({"start_line": start, "end_line": start+len(block)-1, "text": "\n".join(block)})
        if used >= budget:
            break
    return {"path": source["path"], "sha256": source["sha256"], "selection": reason,
            "excerpts": excerpts, "truncated": used < len(text)}

def technical_facts(spec, checks):
    backend_path = safe_path("backend/app/main.py")
    backend = backend_path.read_text(encoding="utf-8")
    tree = ast.parse(backend)
    model = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "TripRequest"), None)
    imports = any(isinstance(n, ast.ImportFrom) and n.module == "pydantic" and {"BaseModel", "Field"} <= {a.name for a in n.names} for n in tree.body)
    inherits = model is not None and any(isinstance(b, ast.Name) and b.id == "BaseModel" for b in model.bases)
    fields = model is not None and any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "Field" for n in ast.walk(model))
    typed_handler = any(isinstance(n, ast.FunctionDef) and n.name == "recommend_trip" and
                        any(isinstance(a.annotation, ast.Name) and a.annotation.id == "TripRequest" for a in n.args.args)
                        for n in tree.body)
    frontend = safe_path("frontend/src/main.jsx").read_text(encoding="utf-8")
    fallback = all(s in frontend for s in ("useState(fallbackDestinations)", ".catch(() => setApiStatus(", "catch {", "setResult({summary:"))
    known_checks = checks.get("checks", []) if checks else []
    passed = len(known_checks) == 5 and all(c.get("exit_code") == 0 for c in known_checks)
    values = (bool(imports and inherits and fields and typed_handler), fallback, passed,
              spec.get("implementation") == "implemented", bool(spec.get("test_runs")))
    spec_files = list((ROOT / "specs/taller-6").glob(spec["id"] + "-*/spec.json"))
    spec_source = spec_files[0].relative_to(ROOT).as_posix() if len(spec_files) == 1 else "current_spec.json"
    sources = ("backend/app/main.py", "frontend/src/main.jsx", "operator_checks", spec_source, spec_source)
    facts = {name: {"value": value, "source": src} for name, value, src in zip(FACT_NAMES, values, sources)}
    return {"facts": facts,
            "basis": {"backend": {"sha256": digest(backend_path.read_bytes()), "analysis": "AST BaseModel + Field + typed handler"},
                      "frontend": {"sha256": digest(safe_path("frontend/src/main.jsx").read_bytes()), "analysis": "static pattern; not full browser proof"}},
            "distinction": "Checks are regressions of base/harness. Generated spec cases are not implemented or executed.",
            "source_sha256": {"backend/app/main.py": digest(backend_path.read_bytes()), "frontend/src/main.jsx": digest(safe_path("frontend/src/main.jsx").read_bytes())},
            "limitation": "Spec facts check declared records, not independent proof of feature implementation or test execution."}

def verify_assertions(answer, sources, facts):
    claims = []
    for claim in answer.get("claims", []):
        if not isinstance(claim, dict) or set(claim) != {"fact", "value"} or type(claim.get("value")) is not bool:
            claims.append({"status": "invalid", "reason": "Claim must contain fact and boolean value"})
            continue
        actual = facts["facts"].get(claim["fact"])
        if actual is None:
            claims.append({"fact": claim["fact"], "status": "unsupported"})
        else:
            claims.append({"fact": claim["fact"], "claimed": claim["value"], "actual": actual["value"],
                           "source": actual["source"],
                           "status": "verified" if claim["value"] == actual["value"] else "contradicted"})
    allowed = {s["path"]: s for s in sources}
    citations = []
    for citation in answer.get("citations", []):
        valid = isinstance(citation, dict) and set(citation) == {"path", "line", "quote"}
        valid = valid and citation["path"] in allowed and type(citation["line"]) is int
        if valid:
            path, number, quote = citation["path"], citation["line"], citation["quote"]
            full = allowed[path]["text"].splitlines()
            valid = isinstance(quote, str) and len(quote) >= 8 and 1 <= number <= len(full)
            valid = valid and quote in full[number-1]
            if valid:
                excerpts = select_source(allowed[path])["excerpts"]
                valid = any(e["start_line"] <= number <= e["end_line"] for e in excerpts)
        citations.append({"path": citation.get("path") if isinstance(citation, dict) else None,
                          "status": "quote_verified" if valid else "invalid_or_not_supplied"})
    return {"claims": claims, "citations": citations,
            "blocked_claims": sum(c["status"] != "verified" for c in claims),
            "unverified_prose": list(answer.get("findings", [])),
            "human_acceptance": False,
            "limitation": "Only catalogued facts and exact supplied quotations are checked. Free prose remains unverified."}

def test_summary(checks):
    if not checks:
        return {"base_checks": [], "new_feature_tests": "not_executed"}
    results = []
    for c in checks["checks"]:
        output = c.get("stdout", "") + c.get("stderr", "")
        match = re.search(r"Ran (\d+) tests|# tests (\d+)", output)
        results.append({"name": c["name"], "exit_code": c["exit_code"],
                        "test_count": int(next(g for g in match.groups() if g)) if match else None})
    return {"base_checks": results, "new_feature_tests": "not_executed",
            "note": "A passing base suite is not evidence that draft feature criteria were implemented."}

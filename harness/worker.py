"""Proceso hijo acotado. No acepta comandos de shell ni rutas arbitrarias."""
import asyncio
import json
import sys
import time

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    kind, role = sys.argv[1:3]
    payload = json.load(sys.stdin)
    if kind == "deadline-test":
        time.sleep(2)
        print("{}")
        return
    if role not in ("orquestador", "frontend", "backend", "calidad", "seguridad"):
        raise ValueError("Role not allowed")
    if kind == "llm":
        from .runtime import local_review
        answer, trace = local_review(role, payload)
        result = {"answer": answer, "trace": trace}
    elif kind == "mcp" and role in ("frontend", "backend"):
        from agents.mcp_probe import probe
        result = asyncio.run(probe(role))
    else:
        raise PermissionError("Worker operation not allowed")
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()

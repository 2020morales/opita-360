"""Comprueba descubrimiento local de skills via app-server; no inicia inferencia."""
import json
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time
from .cli import save
from .core import ROOT

def main():
    binary = shutil.which("codex.exe") or shutil.which("codex")
    if not binary:
        save({"status": "blocked", "reason": "Codex CLI no disponible", "llm_executed": False}, "codex-skills")
        return 1
    p = subprocess.Popen([binary, "app-server"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    inbox = queue.Queue()
    def reader():
        for line in p.stdout:
            try:
                inbox.put(json.loads(line))
            except ValueError:
                continue
    threading.Thread(target=reader, daemon=True).start()
    def send(value):
        p.stdin.write(json.dumps(value) + "\n")
        p.stdin.flush()
    def receive(identifier):
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            item = inbox.get(timeout=max(.1, deadline-time.monotonic()))
            if item.get("id") == identifier:
                if "error" in item:
                    raise RuntimeError(str(item["error"]))
                return item["result"]
        raise TimeoutError("app-server no responde")
    try:
        send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "opita-harness", "version": "1.0.0"}}})
        receive(1)
        send({"method": "initialized", "params": {}})
        send({"id": 2, "method": "skills/list", "params": {"cwds": [str(ROOT)], "forceReload": True}})
        result = receive(2)
        expected = {"opita-frontend", "opita-backend", "brújula-semántica"}
        found = []
        for group in result.get("data", []):
            for skill in group.get("skills", []):
                path = Path(skill.get("path", ""))
                if skill.get("name") in expected and path.is_relative_to(ROOT):
                    found.append(skill["name"])
        ok = set(found) == expected
        save({"status": "passed" if ok else "failed", "method": "skills/list", "detected": sorted(set(found)),
              "expected": sorted(expected), "llm_executed": False,
              "limitation": "Descubrimiento local por CLI. No demuestra activacion automatica ni uso en una nueva sesion del IDE."}, "codex-skills")
        return 0 if ok else 1
    except Exception as exc:
        save({"status": "failed", "method": "skills/list", "error": str(exc), "llm_executed": False}, "codex-skills")
        return 1
    finally:
        p.stdin.close()
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()

if __name__ == "__main__":
    raise SystemExit(main())

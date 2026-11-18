"""Comprobaciones reales Chrome/CDP, sin instalar herramientas en frontend."""
import argparse
import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

from websockets.sync.client import connect
from .runtime import ROOT
from .snapshot import snapshot


def get_json(url):
    with urllib.request.urlopen(url, timeout=2) as response:
        return json.load(response)


def wait_for(predicate, timeout=20):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            value = predicate()
            if value:
                return value
        except Exception:
            pass
        time.sleep(.15)
    raise TimeoutError("Condición no alcanzada en navegador/servidor")


class CDP:
    def __init__(self, url):
        self.context = connect(url, origin="http://localhost", max_size=16 * 1024 * 1024)
        self.ws = self.context.__enter__()
        self.sequence = 0
        self.exceptions = []

    def call(self, method, **params):
        self.sequence += 1
        identifier = self.sequence
        self.ws.send(json.dumps({"id": identifier, "method": method, "params": params}))
        while True:
            message = json.loads(self.ws.recv(timeout=30))
            if message.get("method") == "Runtime.exceptionThrown":
                self.exceptions.append(message["params"])
            if message.get("id") == identifier:
                if "error" in message:
                    raise RuntimeError(str(message["error"]))
                return message.get("result", {})

    def js(self, expression):
        result = self.call("Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in result:
            raise RuntimeError(str(result["exceptionDetails"]))
        return result["result"].get("value")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", choices=["before", "after"], required=True)
    args = parser.parse_args()
    output = ROOT / "docs/taller-5/browser"
    output.mkdir(exist_ok=True)
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "snapshot": snapshot(),
              "label": args.label, "checks": [], "limitations": ["CDP con Chrome headless, no lector de pantalla humano ni auditoría WCAG completa.", "No se usa axe; se comprueban nombres accesibles y estados explícitos."]}
    processes = []
    cdp = None
    profile = tempfile.TemporaryDirectory(prefix="opita-browser-")
    def check(name, condition, observed):
        report["checks"].append({"name": name, "passed": bool(condition), "observed": observed})
    try:
        for url, command, directory in [
            ("http://127.0.0.1:8000/", [sys.executable, "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--port", "8000"], ROOT),
            ("http://127.0.0.1:5173/", [shutil.which("npm.cmd") or shutil.which("npm"), "run", "dev", "--", "--host", "127.0.0.1", "--strictPort"], ROOT / "frontend")]:
            def ready():
                with urllib.request.urlopen(url, timeout=1) as response:
                    return response.status == 200
            try:
                ready()
            except Exception:
                processes.append(subprocess.Popen(command, cwd=directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)))
                wait_for(ready)
        chrome = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
        processes.append(subprocess.Popen([str(chrome), "--headless=new", "--remote-debugging-port=9229",
            "--remote-allow-origins=http://localhost", "--user-data-dir=" + profile.name,
            "--no-first-run", "--no-default-browser-check", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)))
        targets = wait_for(lambda: get_json("http://127.0.0.1:9229/json/list"))
        cdp = CDP(next(t["webSocketDebuggerUrl"] for t in targets if t["type"] == "page"))
        report["browser"] = get_json("http://127.0.0.1:9229/json/version")["Browser"]
        for method in ("Page.enable", "Runtime.enable", "Network.enable", "Accessibility.enable"):
            cdp.call(method)
        cdp.call("Emulation.setDeviceMetricsOverride", width=1440, height=1000, deviceScaleFactor=1, mobile=False)
        cdp.call("Page.navigate", url="http://127.0.0.1:5173/")
        wait_for(lambda: cdp.js("document.querySelectorAll('.destination-card').length===8 && document.querySelector('.api-pill')?.textContent==='API conectada'"))
        check("real_api_catalog", True, cdp.js("({cards:document.querySelectorAll('.destination-card').length,status:document.querySelector('.api-pill').textContent})"))
        cdp.js("document.querySelector('select').value='Neiva';document.querySelector('select').dispatchEvent(new Event('change',{bubbles:true}))")
        wait_for(lambda: cdp.js("document.querySelectorAll('.destination-card').length===2"))
        check("municipality_neiva", True, 2)
        cdp.js("[...document.querySelectorAll('.filter')].find(b=>b.textContent==='Naturaleza').click()")
        wait_for(lambda: cdp.js("!!document.querySelector('.empty-state')"))
        check("combined_empty_filters", True, cdp.js("document.querySelector('.empty-state').textContent"))
        cdp.js("[...document.querySelectorAll('.filter')].find(b=>b.textContent==='Todos').click()")
        cdp.js("let s=document.querySelector('.searchbox input');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(s,'Centro');s.dispatchEvent(new Event('input',{bubbles:true}))")
        wait_for(lambda: cdp.js("document.querySelectorAll('.destination-card').length===1"))
        check("search_and_municipality", True, cdp.js("document.querySelector('.destination-title h3').textContent"))
        cdp.js("document.querySelector('.planner-form').requestSubmit()")
        wait_for(lambda: cdp.js("!!document.querySelector('.result-item')"))
        check("real_api_recommendations", True, cdp.js("({stops:document.querySelectorAll('.result-item').length,method:document.querySelector('.result-notice').textContent})"))
        cdp.call("Page.reload")
        wait_for(lambda: cdp.js("document.querySelectorAll('.destination-card').length===8"))
        missing = cdp.js("[...document.querySelectorAll('input,select')].filter(e=>!e.labels?.length&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby')).map(e=>({tag:e.tagName,type:e.type,id:e.id,placeholder:e.placeholder}))")
        check("explicit_form_labels", len(missing) == 0, missing)
        tree = cdp.call("Accessibility.getFullAXTree")["nodes"]
        unnamed = [{"role": n.get("role", {}).get("value"), "name": n.get("name", {}).get("value", "")} for n in tree if not n.get("ignored") and n.get("role", {}).get("value") in ("textbox", "slider", "combobox", "spinbutton", "button") and not n.get("name", {}).get("value")]
        check("ax_control_names", not unnamed, unnamed)
        cdp.js("document.querySelector('select').focus()")
        for key, code in (("Home", 36), ("ArrowDown", 40)):
            cdp.call("Input.dispatchKeyEvent", type="keyDown", key=key, windowsVirtualKeyCode=code)
            cdp.call("Input.dispatchKeyEvent", type="keyUp", key=key, windowsVirtualKeyCode=code)
        wait_for(lambda: cdp.js("document.querySelector('select').value!=='Todos'"))
        check("keyboard_select", True, cdp.js("({focused:document.activeElement.tagName,value:document.querySelector('select').value})"))
        cdp.call("Input.dispatchKeyEvent", type="keyDown", key="Tab", windowsVirtualKeyCode=9)
        cdp.call("Input.dispatchKeyEvent", type="keyUp", key="Tab", windowsVirtualKeyCode=9)
        check("keyboard_tab", cdp.js("document.activeElement.matches('button.filter')"), cdp.js("document.activeElement.outerHTML"))
        cdp.call("Network.setBlockedURLs", urls=["*127.0.0.1:8000*"])
        cdp.call("Page.reload")
        wait_for(lambda: cdp.js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"))
        cdp.js("document.querySelector('.planner-form').requestSubmit()")
        wait_for(lambda: cdp.js("!!document.querySelector('.result-item')"))
        check("offline_demo_and_recommendations", True, cdp.js("document.querySelector('.result-notice').textContent"))
        screenshot = cdp.call("Page.captureScreenshot", format="png")
        (output / f"{args.label}-desktop.png").write_bytes(base64.b64decode(screenshot["data"]))
        cdp.call("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
        cdp.js("window.scrollTo(0,0)")
        cdp.js("document.querySelector('.mobile-toggle').click()")
        check("mobile_menu_visible", cdp.js("getComputedStyle(document.querySelector('.nav-links')).display!=='none'"), cdp.js("document.querySelector('.nav-links').className"))
        check("mobile_menu_expanded_state", cdp.js("document.querySelector('.mobile-toggle').getAttribute('aria-expanded')==='true'"), cdp.js("document.querySelector('.mobile-toggle').outerHTML"))
        check("mobile_no_horizontal_overflow", cdp.js("document.documentElement.scrollWidth<=window.innerWidth"), cdp.js("({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})"))
        screenshot = cdp.call("Page.captureScreenshot", format="png")
        (output / f"{args.label}-mobile.png").write_bytes(base64.b64decode(screenshot["data"]))
        check("no_js_exceptions", not cdp.exceptions, cdp.exceptions)
    except Exception as exc:
        report["fatal_error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        if cdp:
            cdp.context.__exit__(None, None, None)
        for process in reversed(processes):
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        # Chrome puede conservar brevemente handles del perfil en Windows.
        try:
            profile.cleanup()
        except OSError:
            report["profile_cleanup"] = "Temporary profile locked by Chrome; cleanup incomplete"
        (output / f"{args.label}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"label": args.label, "passed": sum(c["passed"] for c in report["checks"]), "total": len(report["checks"]), "fatal_error": report.get("fatal_error")}, ensure_ascii=True))
    return 0 if not report.get("fatal_error") and all(c["passed"] for c in report["checks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())

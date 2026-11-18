"""Watchdog de procesos propios: evita que la cancelacion del cliente bloquee al padre."""
from datetime import datetime, timezone
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from .core import ROOT

class StageTimeout(TimeoutError):
    pass

def execute_stage(kind, role, payload, seconds):
    if kind not in ("llm", "mcp", "deadline-test") or not 0 < seconds <= 180:
        raise ValueError("Invalid operation or deadline")
    started = time.monotonic()
    event = {"role": role, "stage": kind, "limit_seconds": seconds,
             "started_at": datetime.now(timezone.utc).isoformat(), "payload_chars": len(json.dumps(payload))}
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
        process = subprocess.Popen([sys.executable, "-B", "-m", "harness.worker", kind, role], cwd=ROOT,
                                   stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, **kwargs)
        try:
            process.stdin.write(json.dumps(payload).encode())
            process.stdin.close()
            process.wait(timeout=seconds)
        except subprocess.TimeoutExpired as exc:
            # Solo el PID creado aqui y sus descendientes; nunca servicios existentes.
            if os.name == "nt":
                try:
                    subprocess.run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
                except (OSError, subprocess.TimeoutExpired):
                    process.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
            if process.poll() is None:
                process.kill()
            process.wait(timeout=5)
            error = StageTimeout(f"{role}/{kind} exceeded {seconds:.2f}s; owned process stopped")
            error.event = {**event, "status": "timeout", "elapsed_seconds": round(time.monotonic()-started, 3),
                           "worker_reaped": process.poll() is not None}
            raise error from exc
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            if not process.stdin.closed:
                process.stdin.close()
        event.update(finished_at=datetime.now(timezone.utc).isoformat(),
                     elapsed_seconds=round(time.monotonic()-started, 3), exit_code=process.returncode)
        stdout.seek(0); raw = stdout.read(262145)
        stderr.seek(0); diagnostic = stderr.read(4000).decode("utf-8", errors="replace")
        if process.returncode or len(raw) > 262144:
            failure = RuntimeError(f"{role}/{kind}: worker exit {process.returncode}: {diagnostic}")
            failure.event = {**event, "status": "worker_failed", "worker_reaped": process.poll() is not None}
            raise failure
        result = json.loads(raw)
        event["status"] = "passed"
        return result, event

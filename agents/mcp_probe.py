"""Prueba MCP real con servidor externo fijado; sin LLM ni acceso al árbol original."""
import argparse
import asyncio
from datetime import timedelta
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from agents.runtime import authorize_read, load_manifest

PACKAGE = "@modelcontextprotocol/server-filesystem@2.3.0"
NODE_PACKAGE = "node@24.13.0"


def authorize_tool(name):
    if name not in load_manifest()["tools"]["external_mcp"]["client_allowed_tools"]:
        raise PermissionError("Herramienta MCP no autorizada")


async def probe(role="frontend", include_content=False):
    if role not in ("frontend", "backend"):
        raise ValueError("La prueba admite frontend o backend")
    relative = "frontend/src/main.jsx" if role == "frontend" else "backend/app/main.py"
    expected = authorize_read(role, relative).read_text(encoding="utf-8")
    command = shutil.which("npx.cmd") or shutil.which("npx")
    if not command:
        raise RuntimeError("npx no disponible")
    process = await asyncio.create_subprocess_exec(
        command, "--yes", "--package", NODE_PACKAGE, "node", "--version",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)
    except BaseException:
        process.kill()
        await process.wait()
        raise
    node_version = stdout.decode().strip()
    if process.returncode or node_version != "v24.13.0":
        raise RuntimeError("No se pudo verificar Node portátil 24.13.0")
    with tempfile.TemporaryDirectory(prefix="opita-mcp-context-") as directory:
        target = Path(directory) / Path(relative).name
        target.write_text(expected, encoding="utf-8", newline="")
        params = StdioServerParameters(command=command, args=["--yes", "--package", NODE_PACKAGE,
                                       "--package", PACKAGE, "mcp-server-filesystem", directory])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=30)) as session:
                initialization = await session.initialize()
                available = await session.list_tools()
                names = [tool.name for tool in available.tools]
                authorize_tool("read_text_file")
                if "read_text_file" not in names:
                    raise RuntimeError("El servidor no anuncia lectura de texto")
                response = await session.call_tool("read_text_file", {"path": str(target)})
                actual = "\n".join(item.text for item in response.content if item.type == "text")
                if response.isError or actual != expected:
                    raise RuntimeError("Contenido MCP distinto del archivo exportado")
                # Prueba negativa real contra un archivo existente fuera del scope.
                denied = await session.call_tool("read_text_file", {"path": str(authorize_read(role, relative))})
                if not denied.isError:
                    raise RuntimeError("El servidor no denegó el acceso al árbol original")
                result = {"package": PACKAGE, "node_package": NODE_PACKAGE, "verified_node_version": node_version,
                        "transport": "stdio", "role": role,
                        "server": initialization.serverInfo.model_dump(),
                        "protocol": initialization.protocolVersion,
                        "discovered_tools": names, "called_tool": "read_text_file",
                        "source": relative, "content_equal": True,
                        "sha256_utf8": hashlib.sha256(expected.encode("utf-8")).hexdigest(),
                        "outside_scope_denied": True, "llm_executed": False,
                        "limitation": "Servidor con permisos del usuario; staging no equivale a sandbox OS. Se anuncian herramientas de escritura que este cliente no permite invocar."}
                if include_content:
                    result["content"] = actual
                return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=["frontend", "backend"], default="frontend")
    parser.add_argument("--approved", action="store_true")
    args = parser.parse_args()
    if not args.approved:
        parser.error("Se requiere --approved para iniciar un servidor externo")
    print(json.dumps(asyncio.run(asyncio.wait_for(probe(args.role), timeout=90)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

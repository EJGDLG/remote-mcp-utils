# git_mcp.py
from fastapi import FastAPI, Request
import subprocess
import os

app = FastAPI()

TOOLS = [
    {
        "name": "git/init",
        "description": "Inicializa un repositorio Git en un directorio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "git/status",
        "description": "Devuelve el estado del repositorio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "git/commit",
        "description": "Hace commit de cambios con un mensaje.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["path", "message"]
        }
    }
]


def ok(id, result):
    return {"jsonrpc": "2.0", "id": id, "result": result}

def err(id, code, message):
    return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}


def run_git_command(path, args):
    """Ejecuta un comando git en un directorio específico"""
    result = subprocess.run(["git", "-C", path] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


@app.post("/")
async def rpc(request: Request):
    data = await request.json()
    method = data.get("method")
    mid = data.get("id")
    params = data.get("params", {}) or {}

    if method == "tools/list":
        return ok(mid, {"tools": TOOLS})

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {}) or {}

        try:
            if name == "git/init":
                path = args["path"]
                os.makedirs(path, exist_ok=True)
                out = run_git_command(path, ["init"])
                return ok(mid, {"content": [{"type": "text", "text": out}]})

            if name == "git/status":
                path = args["path"]
                out = run_git_command(path, ["status", "--short", "--branch"])
                return ok(mid, {"content": [{"type": "text", "text": out}]})

            if name == "git/commit":
                path = args["path"]
                msg = args["message"]
                run_git_command(path, ["add", "."])
                out = run_git_command(path, ["commit", "-m", msg])
                return ok(mid, {"content": [{"type": "text", "text": out}]})

            return err(mid, -32601, f"Unknown tool: {name}")
        except Exception as e:
            return err(mid, -32000, str(e))

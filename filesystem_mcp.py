# filesystem_mcp.py
from fastapi import FastAPI, Request
import os

app = FastAPI()

TOOLS = [
    {
        "name": "filesystem/write_file",
        "description": "Crea o sobrescribe un archivo con contenido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "filesystem/read_file",
        "description": "Lee el contenido de un archivo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "filesystem/list_dir",
        "description": "Lista los archivos en un directorio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "filesystem/delete_file",
        "description": "Elimina un archivo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    }
]


def ok(id, result):
    return {"jsonrpc": "2.0", "id": id, "result": result}

def err(id, code, message):
    return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}


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
            if name == "filesystem/write_file":
                path = args["path"]
                content = args["content"]
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return ok(mid, {"content": [{"type": "text", "text": f"Archivo {path} creado"}]})

            if name == "filesystem/read_file":
                path = args["path"]
                if not os.path.exists(path):
                    return err(mid, -32001, f"Archivo {path} no existe")
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return ok(mid, {"content": [{"type": "text", "text": content}]})

            if name == "filesystem/list_dir":
                path = args["path"]
                if not os.path.isdir(path):
                    return err(mid, -32002, f"{path} no es un directorio válido")
                files = os.listdir(path)
                return ok(mid, {"content": [{"type": "json", "data": {"files": files}}]})

            if name == "filesystem/delete_file":
                path = args["path"]
                if not os.path.exists(path):
                    return err(mid, -32003, f"Archivo {path} no existe")
                os.remove(path)
                return ok(mid, {"content": [{"type": "text", "text": f"Archivo {path} eliminado"}]})

            return err(mid, -32601, f"Unknown tool: {name}")
        except Exception as e:
            return err(mid, -32000, str(e))

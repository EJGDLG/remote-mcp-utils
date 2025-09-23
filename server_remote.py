# server_remote.py
# Servidor MCP remoto por HTTP (JSON-RPC 2.0)
from fastapi import FastAPI, Request
import hashlib

app = FastAPI()

TOOLS = [
    {
        "name": "string/sha256",
        "description": "Devuelve el hash SHA-256 del texto.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
        }
    },
    {
        "name": "text/word_count",
        "description": "Cuenta palabras en un texto.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
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
    mid = data.get("id")
    method = data.get("method")
    params = data.get("params", {}) or {}

    if method == "initialize":
        return ok(mid, {"protocolVersion": "2024-08-01", "server": "remote-utils"})

    if method == "tools/list":
        return ok(mid, {"tools": TOOLS})

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if name == "string/sha256":
            text = args.get("text", "")
            h = hashlib.sha256(text.encode("utf-8")).hexdigest()
            # Convención típica MCP: result.content = lista de bloques
            return ok(mid, {"content": [{"type": "text", "text": h}]})
        if name == "text/word_count":
            text = args.get("text", "") or ""
            count = len(text.split())
            return ok(mid, {"content": [{"type": "json", "data": {"count": count}}]})
        return err(mid, -32601, f"Unknown tool: {name}")

    return err(mid, -32601, f"Method not found: {method}")

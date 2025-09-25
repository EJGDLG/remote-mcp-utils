# server_remote.py
# Servidor MCP remoto por HTTP (JSON-RPC 2.0)
from fastapi import FastAPI, Request
from rsa import generar_llaves, encriptar, desencriptar
# Si luego quieres usar DualMap, importa lo necesario:
# from maps_module import build_dualmap  

app = FastAPI()

TOOLS = [
    {
        "name": "rsa/generate_keys",
        "description": "Genera un par de llaves RSA en un rango de primos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "rango_inferior": {"type": "integer"},
                "rango_superior": {"type": "integer"}
            },
            "required": ["rango_inferior", "rango_superior"]
        }
    },
    {
        "name": "rsa/encrypt",
        "description": "Encripta un mensaje entero con clave pública (e, n).",
        "input_schema": {
            "type": "object",
            "properties": {
                "mensaje": {"type": "integer"},
                "e": {"type": "integer"},
                "n": {"type": "integer"}
            },
            "required": ["mensaje", "e", "n"]
        }
    },
    {
        "name": "rsa/decrypt",
        "description": "Desencripta un mensaje con clave privada (d, n).",
        "input_schema": {
            "type": "object",
            "properties": {
                "mensaje_cifrado": {"type": "integer"},
                "d": {"type": "integer"},
                "n": {"type": "integer"}
            },
            "required": ["mensaje_cifrado", "d", "n"]
        }
    },
    {
         "name": "maps/dualmap",
         "description": "Genera un mapa comparativo (DualMap) entre dos fechas para un lago.",
         "input_schema": {
             "type": "object",
             "properties": {
                 "lake": {"type": "string", "enum": ["Atitlan", "Amatitlan"]},
                 "period_a": {"type": "string"},
                 "period_b": {"type": "string"}
             },
             "required": ["lake"]
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

        try:
            if name == "rsa/generate_keys":
                ri = args.get("rango_inferior")
                rs = args.get("rango_superior")
                claves = generar_llaves(ri, rs)
                return ok(mid, {"content": [{"type": "json", "data": {"keys": claves}}]})

            if name == "rsa/encrypt":
                m = args.get("mensaje")
                e = args.get("e")
                n = args.get("n")
                cifrado = encriptar(m, (e, n))
                return ok(mid, {"content": [{"type": "json", "data": {"cipher": cifrado}}]})

            if name == "rsa/decrypt":
                c = args.get("mensaje_cifrado")
                d = args.get("d")
                n = args.get("n")
                descifrado = desencriptar(c, (d, n))
                return ok(mid, {"content": [{"type": "json", "data": {"plain": descifrado}}]})

            # Ejemplo para DualMap:
            if name == "maps/dualmap":
                 lake = args.get("lake")
                 pa = args.get("period_a")
                 pb = args.get("period_b")
                 _, html_out = build_dualmap(lake, pa, pb)
                 return ok(mid, {"content": [{"type": "text", "text": f"Mapa generado: {html_out}"}]})

            return err(mid, -32601, f"Unknown tool: {name}")

        except Exception as e:
            return err(mid, -32000, f"Error ejecutando {name}: {str(e)}")

    return err(mid, -32601, f"Method not found: {method}")

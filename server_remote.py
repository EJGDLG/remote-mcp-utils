# server_remote.py
# Servidor MCP remoto por HTTP (JSON-RPC 2.0)
from fastapi import FastAPI, Request
from modulos.rsa import generar_llaves, encriptar, desencriptar
from maps_module import build_dualmap

# Si luego agregas mapas:
# from modulos.maps_module import build_dualmap

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
        # Puede venir en dos formatos:
        # 1. params = { "name": "...", "arguments": { ... } }
        # 2. params = { ... } directamente (plano, sin "name")
        if "name" in params:
            name = params.get("name")
            args = params.get("arguments", {}) or {}
        else:
            #  Ajuste: deducimos la tool según las claves recibidas
            if "rango_inferior" in params and "rango_superior" in params:
                name = "rsa/generate_keys"
                args = params
            elif {"mensaje", "e", "n"}.issubset(params.keys()):
                name = "rsa/encrypt"
                args = params
            elif {"mensaje_cifrado", "d", "n"}.issubset(params.keys()):
                name = "rsa/decrypt"
                args = params
            elif {"lake", "period_a", "period_b"}.issubset(params.keys()):
                name = "maps/dualmap"
                args = params
            else:
                return err(mid, -32601, "No se pudo deducir la herramienta a partir de los parámetros")

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

# -------------------------------
# Encriptar un mensaje usando la clave pública
# -------------------------------
def encriptar(mensaje, llave_publica):
    """
    Encripta un mensaje usando la clave pública.
    Entrada:
        mensaje (int): Mensaje a encriptar (debe ser menor que n).
        llave_publica (tuple): Clave pública (e, n).
    Salida:
        int: Mensaje encriptado.
    """
    e, n = llave_publica
    if mensaje >= n:
        return "Error: El mensaje debe ser menor que n."
    return pow(mensaje, e, n)

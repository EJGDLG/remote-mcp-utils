# -------------------------------
# Desencriptar un mensaje usando la clave privada
# -------------------------------
import random
from modulos.primos import generar_primo
from modulos.mcd import mcd
from modulos.inverso_modular import inverso_modular

def generar_llaves(rango_inferior, rango_superior):
    p = generar_primo(rango_inferior, rango_superior)
    q = generar_primo(rango_inferior, rango_superior)
    if not p or not q:
        return "Error: No se encontraron números primos en el rango especificado."
    while q == p:
        q = generar_primo(rango_inferior, rango_superior)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while mcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = inverso_modular(e, phi)
    if not d:
        return "Error: No se pudo generar un inverso modular."
    return (e, n), (d, n)

def encriptar(mensaje, llave_publica):
    e, n = llave_publica
    if mensaje >= n:
        return "Error: El mensaje debe ser menor que n."
    return pow(mensaje, e, n)

def desencriptar(caracter_encriptado, llave_privada):
    d, n = llave_privada
    if caracter_encriptado >= n:
        return "Error: El mensaje encriptado es inválido."
    return pow(caracter_encriptado, d, n)

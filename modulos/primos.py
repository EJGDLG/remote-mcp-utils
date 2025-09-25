# modulos/primos.py

import random

def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generar_primo(min_val: int, max_val: int) -> int:
    """Genera un número primo aleatorio entre min_val y max_val"""
    while True:
        candidato = random.randint(min_val, max_val)
        if es_primo(candidato):
            return candidato

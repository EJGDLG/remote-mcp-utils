import random

def generar_primo(rango_inferior, rango_superior):
    def es_primo(num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    primos = [n for n in range(rango_inferior, rango_superior + 1) if es_primo(n)]
    if not primos:
        return None  # No hay primos en el rango
    return random.choice(primos)

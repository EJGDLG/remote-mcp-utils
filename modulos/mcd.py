# -------------------------------
# Algoritmo de Euclides para calcular el máximo común divisor
# -------------------------------
def mcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

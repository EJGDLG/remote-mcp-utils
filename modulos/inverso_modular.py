# -------------------------------
# Algoritmo extendido de Euclides para inverso modular
# -------------------------------
def inverso_modular(e, n):
    t, nuevo_t = 0, 1
    r, nuevo_r = n, e
    while nuevo_r != 0:
        cociente = r // nuevo_r
        t, nuevo_t = nuevo_t, t - cociente * nuevo_t
        r, nuevo_r = nuevo_r, r - cociente * nuevo_r
    if r > 1:
        return None  # No existe inverso
    if t < 0:
        t += n
    return t

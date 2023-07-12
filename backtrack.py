import soko


def buscar_solucion(estado_incial):
    visitados = set()
    return backtrack(estado_incial, visitados)

def backtrack(estado, visitados):
    visitados.add(h(estado))
    if soko.juego_ganado(estado):
        return True, []

    for direccion in ([(1, 0), (-1, 0), (0, 1), (0, -1)]):
        nuevo_estado = soko.mover(estado, direccion)
        if (h(nuevo_estado)) in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)
        if solucion_encontrada:
            acciones.append(direccion)
            return True, acciones
    return False, None

def h(grilla):
    res = ""
    for f in grilla:
        for c in f:
            res += c
        res += "\n"
    return res.rstrip("\n")

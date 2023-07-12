PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_CAJA = "*"
OBJETIVO_JUGADOR = "+"
VACIA = " "
def crear_grilla(desc):
    """Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador"""
    grilla = []
    for f in desc:
        grilla.append(list(f))
    return grilla

def dimensiones(grilla):
    """Devuelve una tupla con la cantidad de columnas y filas de la grilla"""
    return len(grilla[0]),len(grilla)

def hay_pared(grilla, c, f):
    """Devuelve true si hay una pared en la columna y fila (c, f)"""
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] in (OBJETIVO, OBJETIVO_CAJA, OBJETIVO_JUGADOR)

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] in (CAJA, OBJETIVO_CAJA)

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] in (JUGADOR, OBJETIVO_JUGADOR)

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if grilla[f][c] in (OBJETIVO, OBJETIVO_JUGADOR):
                return False
    return True

def ubicacion_jugador(grilla):
    """Recibe una grilla y Devuelve una tupla con la posicion del jugador, 
    Excepcion : (si no hay jugador devuelve false)"""
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if hay_jugador(grilla, c, f):
                return f, c
    raise ValueError("No hay un jugador en el tablero")

def clonar_grilla(grilla):
    """Recibe una grilla y devuelve la misma clonada"""
    grilla2 = []
    for fila in grilla:
        grilla2.append(fila.copy())
    return grilla2
    
def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función devuelve una nueva grilla representando el estado siguiente al
    movimiento efectuado.'''
    
    grilla2 = clonar_grilla(grilla)
    jugador_f, jugador_c = ubicacion_jugador(grilla)
    movimiento = (jugador_f+direccion[1]),(jugador_c+direccion[0])
    lugar3 = (movimiento[0]+direccion[1]), (movimiento[1]+direccion[0])
    pos_jugador = grilla[jugador_f][jugador_c]
    celda_vecina = grilla[movimiento[0]][movimiento[1]]

    if celda_vecina in [VACIA, OBJETIVO]:
        if pos_jugador == OBJETIVO_JUGADOR and celda_vecina == VACIA:
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR
            grilla2[jugador_f][jugador_c] = OBJETIVO
        elif celda_vecina == VACIA:
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR
            grilla2[jugador_f][jugador_c] = VACIA
        elif celda_vecina == OBJETIVO and pos_jugador == OBJETIVO_JUGADOR:
            grilla2[movimiento[0]][movimiento[1]] = OBJETIVO_JUGADOR
            grilla2[jugador_f][jugador_c] = OBJETIVO
        elif celda_vecina == OBJETIVO:
            grilla2[movimiento[0]][movimiento[1]] = OBJETIVO_JUGADOR
            grilla2[jugador_f][jugador_c] = VACIA        
    elif celda_vecina in [CAJA, OBJETIVO_CAJA] and grilla[lugar3[0]][lugar3[1]] in [VACIA, OBJETIVO]:
        celda3 = grilla[lugar3[0]][lugar3[1]]
        if pos_jugador == OBJETIVO_JUGADOR and celda_vecina == CAJA and celda3 == VACIA:
            grilla2[jugador_f][jugador_c] = OBJETIVO
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = CAJA
        elif pos_jugador == OBJETIVO_JUGADOR and celda_vecina == OBJETIVO_CAJA and celda3 == VACIA:
            grilla2[jugador_f][jugador_c] = OBJETIVO
            grilla2[movimiento[0]][movimiento[1]] = OBJETIVO_JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = CAJA
        elif pos_jugador == OBJETIVO_JUGADOR and celda_vecina == CAJA and celda3 == OBJETIVO:
            grilla2[jugador_f][jugador_c] = OBJETIVO
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = OBJETIVO_CAJA
        elif celda_vecina == CAJA and celda3 == VACIA:
            grilla2[jugador_f][jugador_c] = VACIA
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = CAJA
        elif celda_vecina == CAJA and celda3 == OBJETIVO:
            grilla2[jugador_f][jugador_c] = VACIA
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR 
            grilla2[lugar3[0]][lugar3[1]] = OBJETIVO_CAJA
        elif pos_jugador == OBJETIVO_JUGADOR and celda_vecina == CAJA and celda3 == OBJETIVO:
            grilla2[jugador_f][jugador_c] = OBJETIVO
            grilla2[movimiento[0]][movimiento[1]] = JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = OBJETIVO_CAJA
        elif pos_jugador == OBJETIVO_JUGADOR and celda_vecina == OBJETIVO_CAJA and celda3 == OBJETIVO:
            grilla2[jugador_f][jugador_c] = OBJETIVO
            grilla2[movimiento[0]][movimiento[1]] = OBJETIVO_JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = OBJETIVO_CAJA
        elif celda_vecina == OBJETIVO_CAJA and celda3 == VACIA:
            grilla2[jugador_f][jugador_c] = VACIA
            grilla2[movimiento[0]][movimiento[1]] = OBJETIVO_JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = CAJA
        elif celda_vecina == OBJETIVO_CAJA and celda3 == OBJETIVO:
            grilla2[jugador_f][jugador_c] = VACIA
            grilla2[movimiento[0]][movimiento[1]] = OBJETIVO_JUGADOR
            grilla2[lugar3[0]][lugar3[1]] = OBJETIVO_CAJA
    return grilla2   
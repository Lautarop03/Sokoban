import soko
import gamelib
from pila import Pila
from backtrack import buscar_solucion

PARED_IMG = 'img/wall.gif'
CAJA_IMG = 'img/box.gif'
JUGADOR_IMG = 'img/player.gif'
OBJETIVO_IMG = 'img/goal.gif'
VACIA_IMG = 'img/ground.gif'
PIXELES_IMAGEN = 64
TECLAS = "teclas.txt"
NIVELES = "niveles.txt"


def cargar_niveles(ruta):
    """Recibe archivo de niveles, devuelve lista de listas [[n1],[n2]..]"""
    with open(ruta) as f:
        niveles = []
        linea = next(f)
        nivel = []
        for linea in f:
            if linea == "\n":
                niveles.append(nivel)
                linea = next(f)
                nivel = []
                continue
            if linea[0] == "'":
                continue
            nivel.append(linea.rstrip("\n"))
        niveles.append(nivel)
        return niveles


def cargar_nivel(nivel, lista):
    """Recibe numero de nivel y lista de niveles,Devuelve desc para crear grilla"""
    return lista[int(nivel)]


def dibujar_nivel(nivel):
    """Recorre la grilla y la dibuja"""
    for f, fila in enumerate(nivel):
        for c in range(len(fila)):
            gamelib.draw_image(VACIA_IMG, c * PIXELES_IMAGEN, f * PIXELES_IMAGEN)
            if soko.hay_caja(nivel, c, f):
                gamelib.draw_image(CAJA_IMG, c * PIXELES_IMAGEN, f * PIXELES_IMAGEN)
            if soko.hay_pared(nivel, c, f):
                gamelib.draw_image(PARED_IMG, c * PIXELES_IMAGEN, f * PIXELES_IMAGEN)
            if soko.hay_jugador(nivel, c, f):
                gamelib.draw_image(JUGADOR_IMG, c * PIXELES_IMAGEN, f * PIXELES_IMAGEN)
            if soko.hay_objetivo(nivel, c, f):
                gamelib.draw_image(OBJETIVO_IMG, c * PIXELES_IMAGEN, f * PIXELES_IMAGEN)


def buscar_dimensiones(nivel):
    """Devuelve una tupla con el ancho y alto de la grilla"""
    ancho = 0
    alto = 0
    for fila in nivel:
        alto += 1
        if len(fila) > ancho:
            ancho = len(fila)
    return ancho, alto


def ajustar_grilla(grilla):
    """Recibe grilla, devuelve la misma ajustada con la misma cantidad de caracteres por fila"""
    ancho, alto = buscar_dimensiones(grilla)
    for fila in grilla:
        if len(fila) < ancho:
            for i in range((ancho - len(fila))):
                fila.append(" ")
    return grilla


def teclas_a_diccionario(ruta):
    """Recibe archivo con teclas y su funcion, devuelve un diccionario(k:tecla,v:funcion)"""
    with open(ruta) as f:
        dic = {}
        for linea in f:
            if linea == "\n":
                continue
            linea = linea.rstrip("\n").split("=")
            dic[linea[0].rstrip()] = dic.get(linea[0].rstrip(), linea[1].lstrip())
        return dic


def tecla_a_comando(dic, tecla):
    """Recibe diccionario(k:tecla, v:funcion) y tecla. Devuelve tupla(con direccion) o comando"""
    if not tecla in dic:
        return (0, 0)
    comando_a_accion = {"SUR": (0, 1), "OESTE": (-1, 0), "ESTE": (1, 0), "NORTE": (0, -1), "REINICIAR": 0, "SALIR": 1,
                        "DESHACER": 2, "REHACER": 3, "PISTA": 4}
    return comando_a_accion[dic[tecla]]


def iniciar_nivel(nivel, niveles):
    return {"grilla": ajustar_grilla((soko.crear_grilla(cargar_nivel(nivel, niveles)))), "nivel": nivel,
            "deshacer": Pila(), "rehacer": Pila(), "pistas": Pila()}


def main():
    try:
        niveles = cargar_niveles(NIVELES)
    except IOError:
        print("El archivo [niveles] no existe")
        quit()
    cantidad_niveles = len(niveles)
    juego = iniciar_nivel(0, niveles)
    ANCHO_VENTANA, ALTO_VENTANA = buscar_dimensiones(juego["grilla"])
    gamelib.resize(ANCHO_VENTANA * PIXELES_IMAGEN, ALTO_VENTANA * PIXELES_IMAGEN)

    try:
        funciones_teclas = teclas_a_diccionario(TECLAS)
    except IOError:
        print("El archivo [teclas] no existe")
        quit()

    while gamelib.is_alive():

        gamelib.draw_begin()
        dibujar_nivel(juego["grilla"])  # dibujo el nivel
        if not juego["pistas"].esta_vacia():
            gamelib.draw_text('Pista Disponibles', 93, 20, None, 15)
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)

        if not ev:
            break

        tecla = ev.key
        comando = tecla_a_comando(funciones_teclas, tecla)
        if comando == 0:  # Reiniciar
            juego = iniciar_nivel(juego["nivel"], niveles)
        elif comando == 1:  # Cerrar
            break
        elif comando == 2:  # Deshacer
            if juego["deshacer"].esta_vacia():
                print("Usted esta en el estado inicial del nivel")
            else:
                juego["rehacer"].apilar(juego["grilla"])
                juego["grilla"] = juego["deshacer"].desapilar()
                juego["pistas"] = Pila()
        elif comando == 3:  # Rehacer
            if juego["rehacer"].esta_vacia():
                print("Volvio a su movimiento previo")
            else:
                juego["deshacer"].apilar(juego["grilla"])
                juego["grilla"] = juego["rehacer"].desapilar()
                juego["pistas"] = Pila()
        elif comando == 4:  # Pistas
            if juego["pistas"].esta_vacia():
                try:
                    for direccion in (buscar_solucion(juego["grilla"])[1]):
                        juego["pistas"].apilar(direccion)
                except:
                    print("No se encontro solucion, Reinicie por favor")
            else:
                juego["deshacer"].apilar(juego["grilla"])
                juego["grilla"] = soko.mover(juego["grilla"], juego["pistas"].desapilar())
        else:  # Mover
            juego["deshacer"].apilar(juego["grilla"])
            juego["grilla"] = soko.mover(juego["grilla"], comando)
            if juego["deshacer"].ver_tope() == juego["grilla"]:
                juego["deshacer"].desapilar()
            juego["rehacer"] = Pila()
            juego["pistas"] = Pila()

        if soko.juego_ganado(juego["grilla"]):  # Juego ganado, paso el nivel
            juego["nivel"] += 1
            if cantidad_niveles == juego["nivel"]:
                print("Felicitaciones terminaste el juego")
                break
            juego = iniciar_nivel(juego["nivel"], niveles)
            ANCHO_VENTANA, ALTO_VENTANA = buscar_dimensiones(juego["grilla"])
            gamelib.resize(ANCHO_VENTANA * PIXELES_IMAGEN, ALTO_VENTANA * PIXELES_IMAGEN)


gamelib.init(main)

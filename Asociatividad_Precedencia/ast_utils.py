import matplotlib.pyplot as plt
from lark import Tree

def contar_hojas(nodo):
    # si el nodo no es un arbol, entonces cuenta como hoja
    if not isinstance(nodo, Tree):
        return 1

    # si el nodo no tiene hijos, tambien cuenta como hoja
    if len(nodo.children) == 0:
        return 1

    # se suman las hojas de todos los hijos
    return sum(contar_hojas(hijo) for hijo in nodo.children)

def obtener_etiqueta(nodo):
    # si el nodo es un arbol, se usa su nombre
    if isinstance(nodo, Tree):
        return nodo.data

    # si es un token o texto, se convierte a string
    return str(nodo)

def asignar_posiciones(nodo, x, y, posiciones, etiquetas, conexiones):
    # se guarda la posicion del nodo actual
    posiciones[id(nodo)] = (x, y)

    # se guarda la etiqueta del nodo
    etiquetas[id(nodo)] = obtener_etiqueta(nodo)

    # si el nodo no es un arbol, ya no tiene hijos que recorrer
    if not isinstance(nodo, Tree):
        return

    # si no tiene hijos, no hay nada mas que hacer
    if not nodo.children:
        return

    # se calcula el ancho que necesita cada hijo
    anchos = [contar_hojas(hijo) for hijo in nodo.children]
    total_ancho = sum(anchos)

    # se define desde donde se empezaran a ubicar los hijos
    inicio_x = x - total_ancho / 2

    for hijo, ancho in zip(nodo.children, anchos):
        # se calcula la posicion del hijo
        hijo_x = inicio_x + ancho / 2
        hijo_y = y - 1.5

        # se guarda la conexion entre el padre y el hijo
        conexiones.append((id(nodo), id(hijo)))

        # se sigue recorriendo el arbol
        asignar_posiciones(hijo, hijo_x, hijo_y, posiciones, etiquetas, conexiones)

        # se avanza para ubicar el siguiente hijo
        inicio_x += ancho

def dibujar_arbol(arbol, titulo, nombre_archivo):
    # estructuras para guardar la informacion del arbol
    posiciones = {}
    etiquetas = {}
    conexiones = []

    # se calculan las posiciones de todos los nodos
    asignar_posiciones(arbol, 0, 0, posiciones, etiquetas, conexiones)

    # se crea la figura
    plt.figure(figsize=(14, 8))
    plt.title(titulo, fontsize=14)

    # se dibujan las conexiones entre nodos
    for padre, hijo in conexiones:
        x1, y1 = posiciones[padre]
        x2, y2 = posiciones[hijo]
        plt.plot([x1, x2], [y1, y2])

    # se dibujan los nodos con su etiqueta
    for nodo_id, (x, y) in posiciones.items():
        plt.text(
            x, y, etiquetas[nodo_id],
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black")
        )

    # se ocultan los ejes
    plt.axis("off")

    # se ajusta el diseño para que no se corte
    plt.tight_layout()

    # se guarda la imagen
    plt.savefig(nombre_archivo, dpi=300)

    # se cierra la figura
    plt.close()
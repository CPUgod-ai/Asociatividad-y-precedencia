from lark import Lark
import os

from ast_utils import dibujar_arbol

# gramatica para probar asociatividad por izquierda
# ejemplo: id $ id $ id
# se interpreta como: (id $ id) $ id
GRAMATICA_IZQUIERDA = """
    ?start: expresion
    ?expresion: expresion "$" termino   -> operador_izq
              | termino
    ?termino: "id"                      -> identificador

    %import common.WS
    %ignore WS
"""

# gramatica para probar asociatividad por derecha
# ejemplo: id # id # id
# se interpreta como: id # (id # id)
GRAMATICA_DERECHA = """
    ?start: expresion
    ?expresion: termino "#" expresion   -> operador_der
              | termino
    ?termino: "id"                      -> identificador

    %import common.WS
    %ignore WS
"""

# gramatica para probar precedencia
# en este caso * tiene mayor precedencia que +
# ejemplo: id + id * id
# se interpreta como: id + (id * id)
GRAMATICA_PRECEDENCIA = """
    ?start: expresion
    ?expresion: expresion "+" termino   -> suma
              | termino
    ?termino: termino "*" factor        -> multiplicacion
            | factor
    ?factor: "id"                       -> identificador
           | "(" expresion ")"

    %import common.WS
    %ignore WS
"""

def crear_parser(gramatica):
    # esta funcion recibe una gramatica y crea el parser
    return Lark(gramatica, parser="lalr")

def guardar_arbol_txt(arbol, nombre_archivo):
    # esta funcion guarda el arbol sintactico en un archivo de texto
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(arbol.pretty())

def ejecutar_prueba(nombre_prueba, gramatica, cadena, explicacion, carpeta_salida):
    # se imprime una separacion para que la salida se vea ordenada
    print("\n" + "=" * 70)
    print(f"PRUEBA: {nombre_prueba}")
    print()
    print(f"Cadena analizada: {cadena}")
    print()
    print(f"Objetivo: {explicacion}")
    print()

    try:
        # se crea el parser usando la gramatica correspondiente
        parser = crear_parser(gramatica)

        # se analiza la cadena y se obtiene el arbol
        arbol = parser.parse(cadena)

        # se define la ruta del archivo txt
        ruta_txt = os.path.join(carpeta_salida, f"{nombre_prueba}.txt")

        # se define la ruta de la imagen png
        ruta_png = os.path.join(carpeta_salida, f"{nombre_prueba}.png")

        # se guarda el arbol en texto
        guardar_arbol_txt(arbol, ruta_txt)

        # se dibuja el arbol y se guarda como imagen
        dibujar_arbol(arbol, nombre_prueba, ruta_png)

        # se informa que la cadena fue aceptada
        print("Resultado: Cadena aceptada por la gramatica.")
        print(f"Archivo TXT generado: {ruta_txt}")
        print(f"Imagen PNG generada: {ruta_png}")

        # se imprime el arbol en consola
        print("Arbol sintactico:")
        print(arbol.pretty())

    except Exception as error:
        # si ocurre un error, se muestra en pantalla
        print("Ocurrio un error durante la prueba.")
        print(f"Detalle del error: {error}")

    print("\n" + "=" * 70)
    print("\n")

def main():
    # nombre de la carpeta donde se guardaran los resultados
    carpeta_salida = "arboles_sintacticos"

    # se crea la carpeta si no existe
    os.makedirs(carpeta_salida, exist_ok=True)

    # aqui se guardan todas las pruebas que se van a ejecutar
    pruebas = [
        (
            "Prueba_Asociatividad_Izquierda",
            GRAMATICA_IZQUIERDA,
            "id $ id $ id",
            'Demostrar que el operador "$" se agrupa de izquierda a derecha.'
        ),
        (
            "Prueba_Asociatividad_Derecha",
            GRAMATICA_DERECHA,
            "id # id # id",
            'Demostrar que el operador "#" se agrupa de derecha a izquierda.'
        ),
        (
            "Prueba_Precedencia",
            GRAMATICA_PRECEDENCIA,
            "id + id * id",
            'Demostrar que el operador "*" tiene mayor precedencia que "+".'
        )
    ]

    # mensaje inicial
    print("\nINICIANDO GENERACION DE ARBOLES SINTACTICOS...\n")

    # se recorre cada prueba y se ejecuta
    for nombre, gramatica, cadena, explicacion in pruebas:
        ejecutar_prueba(nombre, gramatica, cadena, explicacion, carpeta_salida)

    # mensaje final
    print("Proceso finalizado correctamente.")
    print(f"Revisa los archivos generados en la carpeta: {carpeta_salida}")

if __name__ == "__main__":
    # aqui comienza la ejecucion del programa
    main()
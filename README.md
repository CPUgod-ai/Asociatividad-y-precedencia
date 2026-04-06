# Taller — Prueba de Asociatividad y Precedencia

## Introduccion

En este taller se desarrollo un programa en Python para analizar expresiones simples mediante gramaticas formales, con el fin de demostrar dos conceptos importantes en los lenguajes de programacion:

- la asociatividad
- la precedencia de operadores

Para realizar esto se utilizo la libreria **Lark**, que permite definir gramaticas y generar arboles sintacticos, y tambien la libreria **Matplotlib**, que se uso para dibujar y guardar los arboles en imagenes.

El programa analiza varias cadenas de prueba y genera automaticamente:

- la salida en consola
- un archivo `.txt` con el reporte de cada prueba
- una imagen `.png` con el arbol sintactico correspondiente

---

## Estructura del proyecto

Todos los archivos deben estar en la misma carpeta para que el programa funcione correctamente.

```bash
Asociatividad_Precedencia/
├── main.py
├── visualizador_arbol.py
├── README.md
└── arboles_sintacticos/
    ├── Prueba_Asociatividad_Izquierda.txt
    ├── Prueba_Asociatividad_Izquierda.png
    ├── Prueba_Asociatividad_Derecha.txt
    ├── Prueba_Asociatividad_Derecha.png
    ├── Prueba_Precedencia.txt
    └── Prueba_Precedencia.png
```

## Requisitos
Antes de ejecutar el programa, se deben instalar las librerias necesarias con el siguiente comando:
```bash
pip install lark matplotlib
```

---
# Como ejecutar el taller

## Windows

Abrir la terminal y navegar hasta la carpeta del proyecto:

```bash
cd C:\Users\tu usuario\Documents\Asociatividad_Precedencia
```

Correr el programa:

```bash
python main.py
```

## Linux

Abrir la terminal y navegar hasta la carpeta del proyecto:

```bash
cd ~/Documentos/Asociatividad_Precedencia
```

Instalar las librerias:

```bash
pip install lark matplotlib --break-system-packages
```

Correr el programa:

```bash
python3 main.py
```


## MacOS

Abrir la terminal y navegar hasta la carpeta del proyecto:

```bash
cd ~/Documents/Asociatividad_Precedencia
```

Instalar las librerias:

```bash
pip3 install lark matplotlib
```

Correr el programa:

```bash
python3 main.py
```

## Que hace cada archivo
```bash
main.py
```
1. **Se encarga de:** Definir las gramáticas.
2. **Crear el parser con Lark.**
3. **Analizar las expresiones.**
4. **Mostrar la información en consola.**
5. **Guardar los reportes en archivos .txt.**
6. **Llamar al módulo que dibuja los árboles.**

También contiene la clase `ConvertidorArbol`, que transforma el árbol interno de Lark en un árbol más limpio y fácil de visualizar.

## visualizador_arbol.py

Este archivo contiene la parte gráfica del proyecto. Se encarga de:

*   **Representar los nodos del árbol.**

*   **Calcular la posición de cada nodo.**

*   **Dibujar las conexiones entre nodos.**

*   **Guardar el árbol como imagen .png.**

> **Nota:** Gracias a este archivo no fue necesario usar Graphviz.

---

## Objetivo del taller

El objetivo de este taller es comprobar, mediante gramáticas y árboles sintácticos, que:

1.  **Asociatividad por izquierda:** Un operador puede ser procesado de izquierda a derecha.

2.  **Asociatividad por derecha:** Un operador puede ser procesado de derecha a izquierda.

3.  **Precedencia:** Algunos operadores tienen mayor jerarquía que otros.

Esto permite entender mejor cómo una gramática controla la forma en que una expresión es interpretada por un analizador sintáctico.

---

## Gramáticas utilizadas

En el programa se usaron tres gramáticas diferentes, una para cada caso de prueba.

## 1. Gramatica para asociatividad por izquierda
Esta gramatica demuestra que el operador $ se agrupa de izquierda a derecha.
```bash
?start: expresion
?expresion: expresion "$" termino   -> operador_izq
          | termino
?termino: "id"                      -> identificador

%import common.WS
%ignore WS
```
Cadena utilizada:
```bash
id $ id $ id
```
interpretación esperada:
```bash
(id $ id) $ id
```
## 2. Gramatica para asociatividad por derecha
Esta gramatica demuestra que el operador # se agrupa de derecha a izquierda.

```bash
?start: expresion
?expresion: termino "#" expresion   -> operador_der
          | termino
?termino: "id"                      -> identificador

%import common.WS
%ignore WS
```
Cadena utilizada:
```bash
id # id # id
```
Interpretacion esperada:
```bash
id # (id # id)
```

## 3. Gramatica para precedencia
Esta gramatica demuestra que el operador * tiene mayor precedencia que +.
```bash
?start: expresion
?expresion: expresion "+" termino   -> suma
          | termino
?termino: termino "*" factor        -> multiplicacion
        | factor
?factor: "id"                       -> identificador
       | "(" expresion ")"

%import common.WS
%ignore WS
```
Cadena utilizada:
```bash
id + id * id
```
Interpretacion esperada:
```bash
id + (id * id)
```
# Análisis de Resultados

Los resultados obtenidos en las tres pruebas muestran que las gramáticas fueron construidas correctamente y que el parser las interpreta tal como se esperaba. Cada árbol sintáctico sirve como evidencia visual de que la estructura de la gramática afecta directamente la forma en que una expresión es agrupada y entendida por el analizador.

---

## 1. Análisis de la asociatividad por izquierda

En la primera gramática, la producción principal está escrita de forma **recursiva por la izquierda**. Esto hace que, cada vez que el parser encuentra el operador `$`, intente seguir expandiendo la parte izquierda de la expresión antes de continuar.

*   **Resultado:** La cadena `id $ id $ id` se construye internamente como una operación anidada desde la izquierda.
*   **Agrupación:** `(id $ id) $ id`

> **Conclusión:** La posición de la recursión dentro de la regla gramatical influye directamente en la asociatividad. Al estar en el lado izquierdo, la agrupación ocurre por la izquierda.

---

## 2. Análisis de la asociatividad por derecha

En la segunda gramática ocurre lo contrario. La recursión fue ubicada en el **lado derecho** de la producción, lo cual obliga al parser a construir primero la parte derecha de la expresión.

*   **Resultado:** La cadena `id # id # id` no se agrupa hacia la izquierda.
*   **Agrupación:** `id # (id # id)`

> **Conclusión:** El árbol sintáctico refleja que la parte derecha se desarrolla primero, confirmando que cambiar la posición de la recursión permite controlar la asociatividad del operador.

---

## 3. Análisis de la precedencia de operadores

En la tercera gramática, el comportamiento depende de la **separación de niveles gramaticales**. Se definieron reglas distintas para la suma, la multiplicación y los factores.

*   **Lógica:** La multiplicación se procesa en un nivel más interno (jerárquico) que la suma.
*   **Resultado:** La expresión `id + id * id` se interpreta correctamente.
*   **Agrupación:** `id + (id * id)`

> **Conclusión:** La precedencia se logra diseñando una jerarquía: el nivel de `termino` tiene mayor prioridad que el nivel de `expresion`. Esto evita agrupaciones incorrectas como `(id + id) * id`.





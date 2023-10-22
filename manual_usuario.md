# *Manual de usuario Proyecto 2*

* *José David Góngora Olmedo*
* *202201444*

### Descripción

Este programa es un analizador léxico y sintáctico, que permita a las empresas cargar y analizar datos estructurados en un formato especializado con extensión “.bizdata”.

### Requisitos mínimos

#### Sistemas operativos

* Windows
* macOS
* Linux

#### Memoria

* 4 GB de RAM

#### Almacenamiento

* Al menos 5 GB de espacio

## Descripción del lenguaje

### Importación de datos

#### Claves

En esta sección se declaran los claves o campos por los que están construidos los registros, su estructura está formada por la palabra reservada Claves, seguido de signo igual, corchete de apertura, lista de claves y corchete de cierre.

```python
Claves = [Clave1, Clave2, Clave3, Clave4]
```

#### Registros

En esta sección se detallan los registros que se quieren analizar y sigue la estructura dada por palabra reservada Registros, signo igual, corchete de apertura, lista de registros y corchete de cierre.

```python
Registros = [
    {valor1, valor2, valor3, valor4, valor5}
    {valor1, valor2, valor3, valor4, valor5}
    {valor1, valor2, valor3, valor4, valor5}
    {valor1, valor2, valor3, valor4, valor5}
    {valor1, valor2, valor3, valor4, valor5}
]
```

### Comentarios

#### Comentarios de una linea

Se representan con un numeral y finalizan con un salto de línea.

```python
# Comentario de una linea
```

#### Comentarios multilinea

Inicia con tres comillas simples y finaliza con tres comillas simples.

```python
'''
Comentario
multilinea
'''
```

### Instrucciones de reporteria

#### Imprimir

Imprime por consola el valor dado por la cadena.

```python
imprimir(texto);
```

#### Imprimirln

Imprime por consola el valor dado por la cadena pero con un salto de linea.

```python
imprimirln(texto);
```

#### Conteo

Imprime por consola la cantidad de registros en el arreglo de registros.

```python
conteo();
```

#### Promedio

Imprime por consola el promedio del campo dado.

```python
promedio(campo);
```

#### Contarsi

Imprime por consola la cantidad de registros en la que el campo dado sea igual al valor dado.

```python
contarsi(campo);
```

#### Datos

Imprime por consola los registros leídos.

```python
datos();
```

#### Sumar

Imprime en consola la suma todos los valores del campo dado.

```python
sumar(campo);
```

#### Max

Encuentra el valor máximo del campo dado.

```python
max(campo);
```

#### Min

Encuentra el valor mínimo del campo dado.

```python
min(campo);
```

#### Exportar reporte

Genera un archivo html con una tabla en donde se encuentren los registros leídos y con el título como parámetro.

```python
exportarReporte(titulo);
```

### Inicio

Al ejecutar el programa se podra ver la interfaz

![Pantalla de inicio](/img/img1.JPG)

1. Boton de las opciones de archivo
    * Abrir
    * Guardar
    * Guardar como

2. Botones para analizar, generar reporte de errores, tokens y el arbol de derivación.

3. Editor de texto, donde se podra escribir y editar el texto de los archivos.

4. Consola, se mostraran todas las funciones que se hagan en el editor.

### Abrir archivo

Al dar click en la opción de abrir, se abrira una ventana para elegir el archivo a abrir (.bizdata).

![Ventana abrir](/img/img2.JPG)

Al seleccionar el archivo se mostrara en el programa.

![Archivo abierto](/img/img3.JPG)

1. Se mostrara el nombre del archivo que se esta editando.

3. El contenido del archivo cargado se mostrara en el editor.

### Guardar archivo

Al dar click en guardar, se guardaran todos los cambios realizados.

![Mensaje archivo guardado](/img/img4.JPG)

Se mostrara el siguiente mensaje para indicar que se han guardado los cambios.

### Guardar como

Al dar click en guardar como, se mostrara una ventana para elegir como desea guardar el archivo.

![Ventana guardar como](/img/img5.JPG)

Y se guardara el archivo.

### Analizar

Al dar click en el boton de analizar, el programa comenzara a analizar todo el contenido del archivo para mostrar los resultados.

![Consola con los resultados](/img/img6.JPG)

En la consola se podra ver todas las operaciones que se hicieron.

### Reporte de errores

Al dar click en el boton de errores, se creara un archivo ```reporte_errores.html``` donde se mostraran los errores léxicos y sintácticos encontrados en una tabla. 

![Tabla de errores](/img/img7.JPG)

Ejemplo del reporte de errores.

### Reporte de tokens

Al dar click en el boton de tokens, se creara un archivo ```reporte_tokens.html``` donde se mostraran los tokens leidos en una tabla. 

![Tabla de tokens](/img/img8.JPG)

Ejemplo del reporte de tokens.

### Arbol de derivación

Al dar click en el boton de arbol, se creara un archivo ```arbol_derivacion.svg``` donde se podran ver todos los tokens en formato svg.

![Arbol de derivación](/img/img9.JPG)

Ejemplo del arbol de derivación.
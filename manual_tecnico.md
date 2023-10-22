# *Manual tecnico Proyecto 2*

* *José David Góngora Olmedo*
* *202201444*

## Introducción

Analizador léxico y sintáctico, que permita a las empresas cargar y analizar datos estructurados en un formato especializado con extensión “.bizdata”.

## Características

Se pueden generar y leer archivos con extension ```.bizdata```:

- Analizar un archivo .bizdata
- Mostrar los errores lexicos y sintacticos en el archivo.
- Generar reporte de errores.
- Generar reporte de tokens.
- Generar arbol de derivación.

## Contenido

Este programa contiene las siguientes funcionalidades:

### Archivo ```app.py```

Este archivo es el principal, donde se crea una instancia del archivo ```main_page.py``` para mostrar la interfaz.

```python
import tkinter as tk
from interfaz.main_page import main_page

raiz = tk.Tk()
ventana = main_page(raiz)
ventana.center_window(raiz, 1350, 850)

raiz.mainloop()
```

### Archivo ```main_page.py```

Ee encuentra toda la interfaz grafica y donde se llaman las funciones de la clase ```analizador.py``

#### Interfaz grafica

Codigo de toda la interfaz grafica, donde se crean los widgets.

```python
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, filedialog, messagebox
import os
from clases.imprimir import *
from clases.imprimirln import *
from clases.conteo import *
from clases.promedio import *
from clases.datos import *
from clases.suma import *
from clases.maxmin import *
from clases.reporte import *
from clases.contarsi import *

from analizador.analizador import analizador

class main_page:
    def __init__(self, raiz):
        self.archivo = ""
        self.datos_archivo = ''

        self.variable_archivo = tk.StringVar()
        self.variable_archivo.set("")
        self.analizador = analizador()

        self.raiz = raiz
        self.cantidad_lineas = 1
        self.raiz.config(bg="#fdf9c4")
        self.raiz.title("Analizador lexico")
        self.raiz.resizable(0,0)
        self.menu_frame = tk.Frame(self.raiz, width="1350", height="60", bg="#FDF9DF")
        self.menu_frame.pack_propagate(False)
        self.menu_frame.grid_propagate(False)
        self.menu_frame.pack()

        self.menu_frame.columnconfigure(0, weight=1)  # Columna vacía
        self.menu_frame.columnconfigure(1, weight=1)  # Columna para el botón "Analizar"
        self.menu_frame.columnconfigure(2, weight=1)  # Columna para el botón "Errores"
        self.menu_frame.columnconfigure(3, weight=1) 
        self.menu_frame.columnconfigure(4, weight=1) 

        self.editor_frame = tk.Frame()

        self.editor_frame.pack()
        self.editor_frame.config(width="1350", height="800", bg="#fdf9c4")

        self.editor = tk.Text(self.editor_frame, width="70", height="39", padx=35, pady=20, font=('Arial', 12))
        self.editor.grid(row=0, column=0, padx=10, pady=25, sticky="sw")

        self.lineas_bar = tk.Text(self.editor_frame, width=3, padx=4, pady=20, takefocus=0, border=0, background='lightgrey', state='disabled', font=('Arial', 12))
        self.lineas_bar.tag_configure("center", justify="center")
        self.lineas_bar.tag_add("center", "1.0", "end")
        self.lineas_bar.grid(row=0, column=0, pady=25, sticky="nsw")

        self.editor.bind('<Key>', self.actualizar_lineas)
        self.editor.bind('<MouseWheel>', self.actualizar_lineas)

        self.scroll_editor = tk.Scrollbar(self.editor_frame)
        self.scroll_editor.grid(row=0, column=0, pady=25, sticky="nse")
        self.editor.config(yscrollcommand=self.scroll_editor.set)

        self.consola = tk.Text(self.editor_frame, background='#e6e6e6', width="65", height="39", padx=10, pady=20, font=('Arial', 12), borderwidth=2, relief="solid")
        self.consola.grid(row=0, column=1, padx=10, pady=25)

        self.menu = tk.Menu(self.raiz, background='blue', fg='white')


        self.opciones_menu = tk.Menu(self.menu, tearoff=0, background='#fdf9c4')
        self.opciones_menu.add_command(label="Abrir", background='#fdf9c4', command = self.abrir_archivo)
        self.opciones_menu.add_command(label="Guardar", background='#fdf9c4', command = self.guardar_archivo)
        self.opciones_menu.add_command(label="Guardar como", background='#fdf9c4', command = self.guardar_como)
        self.opciones_menu.add_separator(background='#fdf9c4')
        self.opciones_menu.add_command(label="Salir", background='#fdf9c4', command=self.raiz.quit)

        self.menu.add_cascade(label="Archivo", menu=self.opciones_menu)

        self.fuente = font.Font(weight="bold")

        self.label = tk.Label(self.menu_frame, textvariable=self.variable_archivo, bg="#FDF9DF")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.label['font'] = self.fuente

        self.analizar_B = tk.Button(self.menu_frame, text="Analizar", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e", command = self.analizar)
        self.analizar_B.grid(row=0, column=1, padx=5, pady=10)
        self.analizar_B['font'] = self.fuente

        self.reporte_errores = tk.Button(self.menu_frame, text="Reporte de errores", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e", command = self.reporte_errores)
        self.reporte_errores.grid(row=0, column=2, padx=5, pady=10)
        self.reporte_errores['font'] = self.fuente

        # tem_reporte = tk.StringVar()
        # reporte = ttk.Combobox(self.menu_frame, font = self.fuente, width=16, values=["Reporte de errores", "Reporte de Tokens", "Arbol de derivación"])
        self.reporte_tokens = tk.Button(self.menu_frame, text="Reporte de tokens", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e", command = self.reporte_tokens)
        self.reporte_tokens.grid(row=0, column=3, padx=5, pady=10)
        self.reporte_tokens['font'] = self.fuente

        self.arbol_derivacion = tk.Button(self.menu_frame, text="Arbol de derivación", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e", command = self.reporte_arbol)
        self.arbol_derivacion.grid(row=0, column=4, padx=5, pady=10)
        self.arbol_derivacion['font'] = self.fuente

        self.opciones_menu.config(background="#fdf9c4")
        self.raiz.config(menu=self.menu)
```

#### Función 1

Función para generar el numero de lineas que tenga el editor de texto.

```python
def actualizar_lineas(self, event = None):
        cantidad = self.editor.get('1.0', tk.END).count('\n')
        if cantidad != self.cantidad_lineas:
            self.lineas_bar.config(state = tk.NORMAL)
            self.lineas_bar.delete(1.0, tk.END)
            for linea in range(1, cantidad + 1):
                self.lineas_bar.insert(tk.END, f"{linea}\n")
            self.lineas_bar.config(state = tk.DISABLED)
            self.cantidad_lineas = cantidad
```

#### Función 2

Funcion para realizar la lectura del archivo y colocar el contenido en el widget de Texto.

```python
def abrir_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("All files", "*.bizdata")])
        self.nombre_archivo(self.archivo)
        if self.archivo:
            with open(self.archivo, 'r') as file:
                self.datos_archivo = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", self.datos_archivo)
            self.actualizar_lineas()
```

#### Función 3

Funcion para guardar archivo con el contenido en el editor.

```python
def guardar_archivo(self):
        if self.editor and self.archivo:
            try:
                self.datos_archivo = self.editor.get("1.0", tk.END)
                with open(self.archivo, 'w') as file:
                    file.write(self.editor.get("1.0", tk.END))
                messagebox.showinfo("Exito!", "El archivo se ha guardado correctamente")
            except Exception as e:
                messagebox.showinfo("Error!", "Error al guardar el archivo "+ str(e))
```

#### Función 4

Funcion para guardar como, el cual creara un nuevo archivo para guardarlo.

```python
def guardar_como(self):
        if self.editor:
            self.archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All files", "*.bizdata")])
            self.nombre_archivo(self.archivo)
            self.datos_archivo = self.editor.get("1.0", tk.END)
            if self.archivo:
                with open(self.archivo, "w") as file:
                    file.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Exito!", "El archivo se ha guardado correctamente")
```

#### Función 5

Funcion para analizar los datos que se encuentran en el editor de texto. Llama a una funcion de la clase ```analizador.py``` y los muestra en la consola del editor.

```python
def analizar(self):
        self.consola.config(state='normal')
        self.consola.delete(1.0, tk.END)
        self.analizador.limpiar_listas()
        imprimir_consola = ''
        flechas = ">>>"
        if self.datos_archivo != '':
            ins = self.analizador.analizador_lexico(self.datos_archivo)
            # self.analizador.recursivo_operar()

            lista_instrucciones = []
            while True:
                instrucciones_lenguaje = self.analizador.analizador_sintactico()
                if instrucciones_lenguaje:
                    lista_instrucciones.append(instrucciones_lenguaje)
                else:
                    break

            # Ejecutar instrucciones

            for elemento in lista_instrucciones:
                if isinstance(elemento, Imprimir):

                    imprimir_consola += elemento.ejecutarT()+" "
                elif isinstance(elemento, Imprimirln) or isinstance(elemento, Conteo) or isinstance(elemento, Promedio) or isinstance(elemento, Datos) or isinstance(elemento, Suma) or isinstance(elemento, MaxMin) or isinstance(elemento, Contarsi):

                    imprimir_consola += "\n"+elemento.ejecutarT()+" "
                
                elif isinstance(elemento, Reporte):

                    imprimir_consola += "\nReporte generado: "+elemento.ejecutarT()+" "

            self.consola.config(state='normal')
            self.consola.delete(1.0, tk.END)

            lineas = [f"{flechas} {line}" for line in imprimir_consola.split('\n') if line.strip()]
            for line in lineas:
                self.consola.insert(tk.END, line + "\n")

            self.consola.config(state='disabled')
            messagebox.showinfo("Análisis exitoso", "El código se analizó exitosamente.")
```

#### Función 6

Funcion para generar el archivo html de los errores. Llama a una funcion de la clase ```analizador.py```

```python
def reporte_errores(self):
        self.analizador.generar_reporte_errores()
        messagebox.showinfo("Exito!", "El reporte se ha generado correctamente.")
```

#### Función 7

Funcion para generar el archivo html de los tokens. Llama a una funcion de la clase ```analizador.py```

```python
def reporte_tokens(self):
        self.analizador.generar_reporte_tokens()
        messagebox.showinfo("Exito!", "El reporte se ha generado correctamente.")
```

#### Función 8

Funcion para generar el archivo del arbol de derivación en formato .svg. Llama a una funcion de la clase ```analizador.py```

```python
def reporte_arbol(self):
        self.analizador.arbol_derivacion()
        messagebox.showinfo("Exito!", "El arbol se ha generado correctamente.")
```

### Archivo ```analizador.py```

En este archivo se hace toda la logica del analizador y donde se crean los reportes y archivos de salida.

#### Función 1

En esta funcion se obtiene como argumento la cadena (El texto a analizar) para ir recorriendo caracter por caracter e ir formando los lexemas. Y tambien donde se guardan los errores lexicos si los hay.

```python
def analizador_lexico(self, cadena):
        lexema = ''
        puntero = 0
        contador_comillas = 0

        while cadena:
            char = cadena[puntero]
            puntero += 1
            if char == '\'':
                contador_comillas += 1
                if contador_comillas < 3:
                    espacios_encontrados = 0
                    cadena, espacios_encontrados = self.comentario_multilinea(cadena[1:])
                    self.numero_linea += espacios_encontrados
                    self.numero_columna = 1
                    contador_comillas = 0
                    puntero = 0
                else:
                    cadena = cadena[1:]
                puntero = 0
            elif char == "#":
                lexema, cadena = self.armar_comentario(cadena[puntero:])
                if lexema and cadena:
                    self.numero_columna += len(str(lexema))+1
                    puntero = 0
            elif char.isalpha():
                lexema, cadena = self.armar_lexema(cadena)
                if lexema and cadena:

                    token = 'TEXTO'

                    if lexema in self.tipo_tokens:
                        token = self.tipo_tokens.get(lexema)


                    lexm = Lexema(lexema, token, self.numero_linea, self.numero_columna)
                    self.lista_lexema.append(lexm)
                    if self.numero_columna == 1: self.numero_columna += 1
                    self.numero_columna += len(str(lexema))
                    puntero = 0
            elif char == "[" or char == "]" or char == "{" or char == "}" or char == "(" or char == ")" or char == ";" or char == "\"" or char == "=" or char == ",":
                
                token = self.tipo_tokens.get(char)

                c = Lexema(char, token, self.numero_linea, self.numero_columna)
                self.numero_columna += 1

                self.lista_lexema.append(c)

                cadena = cadena[1:]
                puntero = 0
            elif char.isdigit():

                numero, cadena, num_len = self.numeros(cadena)

                if numero > -1 and cadena:

                    num = Numero(numero, 'NUMERO', self.numero_linea, self.numero_columna)
                    if self.numero_columna == 1: self.numero_columna += 1

                    self.lista_lexema.append(num)
                    self.numero_columna += len(str(num_len))
                    puntero = 0
            elif char == ' ' or char == '\r':
                cadena = cadena[1:]
                self.numero_columna += 1
                puntero = 0
            elif char == '\n':
                cadena = cadena[1:]
                puntero = 0
                self.numero_linea += 1
                self.numero_columna = 1
            elif char == '\t':
                self.numero_columna += 4
                cadena = cadena[4:]
                puntero = 0
            else:
                cadena = cadena[1:]
                puntero = 0
                error = Errores((len(self.lista_errores_lexicos)+1), char , "Error lexico", self.numero_linea, self.numero_columna)
                self.numero_columna += 1
                self.lista_errores_lexicos.append(error)

        self.lista_tokens = self.lista_lexema.copy()
        self.lista_lexema_arbol = self.lista_lexema.copy()

        return self.lista_lexema
```

#### Función 2

En esta función se arma el comentario de una linea para ignorarlo.

```python
def armar_comentario(self,cadena):
    token = ''
    puntero = ''
    for char in cadena:
        puntero +=char
        if char == "\n":
            return token, cadena[len(puntero)-1:]
        else:
            token += char
    return None, None
```

#### Función 3

En esta función se arma el comentario multilinea para ignorarlo.

```python
def comentario_multilinea(self,cadena):
    comillas = 0
    no_enters = 0
    puntero = 0

    for char in cadena:
        puntero += 1
        if comillas < 3:
            if char == '\'':
                comillas += 1
            elif char == '\n':
                no_enters +=1
                comillas = 0
            else:
                comillas = 0
        else:
            return cadena[(puntero+1):], no_enters
    return None, None
```

#### Función 3

Función para agrupar los lexemas (si son una palabra).

```python
def armar_lexema(self, cadena):
    lexema = ''
    puntero = ''

    for char in cadena:
        puntero += char
        if  char == '\"' or char == "(" or char == "=" or char == "[":
            return lexema.strip(), cadena[len(puntero)-1:]
        else :
            lexema += char

    return None, None
```

#### Función 4

Función para armar los numeros y ver si son de tipo entero o decimal.

```python
def numeros(self, cadena):
    numero = ''
    puntero = ''
    es_decimal = False
    for char in cadena:
        puntero += char
        if char == '.':
            es_decimal = True
        if char == '\"' or char == ' ' or char == '\n' or char == '\t' or char == ',' or char == '}' or char == ')':
            if es_decimal:
                return float(numero), cadena[len(puntero)-1:], str(numero)
            else:
                return int(numero), cadena[len(puntero)-1:], str(numero)
        else:
            numero += char
    return None, None
```

#### Función 5

Función que sirve como analizador sintactico, donde valida lexema por lexema para hacer alguna función.

```python
def analizador_sintactico(self):
    palabra = ''
    sig_igual= ''
    corchete_in = ''
    corchete_fin = ''
    llave_in = ''
    comilla = ''

    while self.lista_lexema:
        
        # if len(self.lista_errores_sintacticos) == 0:
        lexema = self.lista_lexema.pop(0)
        if lexema.operar(None) in self.palabras:
            if lexema.operar(None) == "Claves":
                sig = self.lista_lexema.pop(0)

                if sig.operar(None) == "=":
                    sig = self.lista_lexema.pop(0)

                    if sig.operar(None) == "[":

                        self.armar_claves()
                    else:
                        error = Errores((len(self.lista_errores_sintacticos)+1), sig.operar(None), "Error sintactico", sig.obtener_Fila(), sig.obtener_Columna())
                        self.lista_errores_sintacticos.append(error)
                        return print("ERROR")
                    
                else:
                    error = Errores((len(self.lista_errores_sintacticos)+1), sig.operar(None), "Error sintactico", sig.obtener_Fila(), sig.obtener_Columna())
                    self.lista_errores_sintacticos.append(error)
                    return print("ERROR")
                print(self.claves)

            elif lexema.operar(None) == "Registros":
                sig_igual = self.lista_lexema.pop(0)

                if sig_igual.operar(None) == "=":
                    corchete_in = self.lista_lexema.pop(0)

                    if corchete_in.operar(None) == "[":

                        self.armar_registros()
                    else :
                        error = Errores((len(self.lista_errores_sintacticos)+1), corchete_in.operar(None), "Error sintactico", corchete_in.obtener_Fila(), corchete_in.obtener_Columna())
                        self.lista_errores_sintacticos.append(error)
                else :
                    error = Errores((len(self.lista_errores_sintacticos)+1), sig_igual.operar(None), "Error sintactico", sig_igual.obtener_Fila(), sig_igual.obtener_Columna())
                    self.lista_errores_sintacticos.append(error)

                print(self.registros)
                self.get_datos()
            elif lexema.operar(None) == "imprimir":
                lexema = self.lista_lexema.pop(0)
                if lexema.operar(None) == '(':
                    comillas = self.lista_lexema.pop(0)
                    if comillas.operar(None) == '"':
                        texto = self.lista_lexema.pop(0)
                        comillas = self.lista_lexema.pop(0)
                        if comillas.operar(None) == '"':
                            parentesis = self.lista_lexema.pop(0)
                            if parentesis.operar(None) == ')':
                                punto_coma = self.lista_lexema.pop(0)
                                if punto_coma.operar(None) == ';':
                                    return Imprimir(texto.lexema, lexema.obtener_Fila(), lexema.obtener_Columna())
                                else:
                                    error = Errores((len(self.lista_errores_sintacticos)+1), punto_coma.operar(None), "Error sintactico", punto_coma.obtener_Fila(), punto_coma.obtener_Columna())
                                    self.lista_errores_sintacticos.append(error)
                            else:
                                error = Errores((len(self.lista_errores_sintacticos)+1), parentesis.operar(None), "Error sintactico", parentesis.obtener_Fila(), parentesis.obtener_Columna())
                                self.lista_errores_sintacticos.append(error)
                        else:
                            error = Errores((len(self.lista_errores_sintacticos)+1), comillas.operar(None), "Error sintactico", comillas.obtener_Fila(), comillas.obtener_Columna())
                            self.lista_errores_sintacticos.append(error)
                    else:
                        error = Errores((len(self.lista_errores_sintacticos)+1), comillas.operar(None), "Error sintactico", comillas.obtener_Fila(), comillas.obtener_Columna())
                        self.lista_errores_sintacticos.append(error)
                else :
                    error = Errores((len(self.lista_errores_sintacticos)+1), lexema.operar(None), "Error sintactico", lexema.obtener_Fila(), lexema.obtener_Columna())
                    self.lista_errores_sintacticos.append(error)

            elif lexema.operar(None) == "imprimirln":
```
(Es mucho mas código)

#### Función 6

Función para obtener el conteo de los registros.

```python
def get_conteo(self):
    return str(len(self.registros))
```

#### Función 7

Función para contarsi.

```python
def contar_si(self, campo, valor):
    cont = 0

    index = self.claves.index(campo)

    for registros in self.registros:
        if str(registros[index]) == str(valor):
            cont += 1
    
    return str(cont)
```

#### Función 8

Función para encontrar el promedio.

```python
def promedio(self, campo):
    index = ''
    cantidad_reg = len(self.registros)
    suma = 0
    if campo in self.claves:
        index = self.claves.index(campo)

        for i in range(0, len(self.registros)):
            # if self.registros[i][index].isalpha():
            #     return None
            suma += self.registros[i][index]

        return str(suma/cantidad_reg)

    return None
```

#### Función 9

Función para retornar los datos de claves y registros.

```python
def get_datos(self):
    datos = ''

    for campos in self.claves:
        # datos += "{:<14}".format(campos)
        datos += campos+"     "

    datos += "\n"

    for registros in self.registros:
        for i in range(0, len(self.claves)):
            # datos += str(registros[i])+"     "
            datos += "{:<14}".format(str(registros[i]))
        datos += "\n"
    
    return datos
```

#### Función 10

Función para sumar dependiendo del campo.

```python
def sumar(self, campo):
    index = ''
    suma = 0
    if campo in self.claves:
        index = self.claves.index(campo)

        for i in range(0, len(self.registros)):
            # if self.registros[i][index].isalpha():
            #     return None
            suma += self.registros[i][index]

        return str(suma)

    return None
```

#### Función 11

Función para obtener el mayor dato.

```python
def get_max(self, campo):
    index = ''
    lista_temp = []
    if campo in self.claves:
        index = self.claves.index(campo)

        for registros in self.registros:
            # if self.registros[i][index].isalpha():
            #     return None
            lista_temp.append(registros[index])

        return str(max(lista_temp))

    return None
```

#### Función 12

Función para obtener el menor dato.

```python
def get_min(self, campo):
    index = ''
    lista_temp = []
    if campo in self.claves:
        index = self.claves.index(campo)

        for registros in self.registros:
            # if self.registros[i][index].isalpha():
            #     return None
            lista_temp.append(registros[index])

        return str(min(lista_temp))

    return None
```

#### Función 13

Función para generar el reporte HTML de los registros.

```python
def generar_reporte(self, titulo):
    campos_data = ''
    registros_data = ''
    longitud = len(self.claves)
    file = open(f"reporte_{titulo}.html", "w")


    for campos in self.claves:
        campos_data += f"<th>{campos}</th>\n"

    for registros in self.registros:
        registros_data += "<tr>\n"
        for i in range(0, longitud):
            registros_data += f"<th>{registros[i]}</th>\n"

        registros_data += "</tr>\n"

    html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titulo}</title>
        </head>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: xx-large;
                padding-top: 150px;
            }}
            table {{
                border-collapse: collapse;
                border: 1px solid #000;
                padding: 15px;
            }}
            tr, th {{
                padding: 15px;
                border: 1px solid #000;
            }}
            .title {{
                background-color: #fdf9c4;
            }}
        </style>
        <body>

            <table>
                <tr class="title">
                    <th colspan="{longitud}">{titulo}</th>
                </tr>
                <tr>
                    {campos_data}
                </tr>
                {registros_data}

            </table>
            
        </body>
        </html>"""
    
    file.write(html)

    file.close()
```

#### Función 14

Función para generar el reporte HTML de los errores léxicos y sintácticos.

```python
def generar_reporte_errores(self):
    errores_lexicos = ''
    errores_sintacticos = ''
    file = open("reporte_errores.html", 'w')

    for lex in self.lista_errores_lexicos:
        errores_lexicos += f"<tr><th>{lex.lexema}</th><th>{lex.obtener_Fila()}</th><th>{lex.obtener_Columna()}</th>\n</tr>"

    for sin in self.lista_errores_sintacticos:
        errores_sintacticos += f"<tr><th>{sin.lexema}</th><th>{sin.obtener_Fila()}</th><th>{sin.obtener_Columna()}</th>\n</tr>"

    html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Errores</title>
        </head>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: xx-large;
                padding-top: 150px;
            }}
            table {{
                border-collapse: collapse;
                border: 1px solid #000;
                padding: 15px;
            }}
            tr, th {{
                padding: 15px;
                border: 1px solid #000;
            }}
            .title {{
                background-color: #fdf9c4;
            }}
        </style>
        <body>

            <table>
                <tr class="title">
                    <th colspan="3">Errores lexicos</th>
                </tr>
                <tr>
                    <th>Token</th>
                    <th>Fila</th>
                    <th>Columna</th>
                </tr>
                {errores_lexicos}
                <tr class="title">
                    <th colspan="3">Errores sintacticos</th>
                </tr>
                <tr>
                    <th>Token</th>
                    <th>Fila</th>
                    <th>Columna</th>
                </tr>
                {errores_sintacticos}
            </table>
            
        </body>
        </html>"""

    file.write(html)

    file.close()
```

#### Función 15

Función para generar el reporte HTML de los tokens.

```python
 def generar_reporte_tokens(self):
    tokens = ''
    file = open('reporte_tokens.html', 'w')

    for token in self.lista_tokens:
        tokens += f'<tr><th>{token.tipo}</th><th>{token.lexema}</th><th>{token.obtener_Fila()}</th><th>{token.obtener_Columna()}</th></tr>\n'
    

    html = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte</title>
            </head>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding-top: 100px;
                }}
                table {{
                    border-collapse: collapse;
                    border: 1px solid #000;
                    padding: 15px;
                    text-align: center;
                }}
                tr, th {{
                    text-align: center;
                    padding: 15px;
                    border: 1px solid #000;
                }}
                .title {{
                    background-color: #fdf9c4;
                }}
            </style>
            <body>

                <table>
                    <tr class="title">
                        <th colspan="4">TOKENS</th>
                    </tr>
                    <tr>
                        <th>Tipo Token</th>
                        <th>Lexema</th>
                        <th>Fila</th>
                        <th>Columna</th>
                    </tr>
                    {tokens}
                </table>
                
            </body>
            </html>"""
    
    file.write(html)
    file.close()
```

#### Función 16

Función para generar el arbol de derivacion en svg.

```python
def arbol_derivacion(self):
    cont = 1
    sig = ''
    dot = 'digraph G {n0[label="inicio"]\n'

    while self.lista_lexema_arbol:
        primero = self.lista_lexema_arbol.pop(0)
        if primero.operar(None) in self.palabras:
            cont_h = 1
            dot += f'n{cont}[label="{primero.operar(None)}",style = filled, color="#fdf9c4"]\n'
            dot += f'n0->n{cont}\n'
            
            sig = self.lista_lexema_arbol.pop(0)

            if sig.operar(None) == '=':
                while sig.operar(None) != "]":
                    if sig.operar(None) == "\"":
                        dot += f'n{cont}h{cont_h}[label="\{sig.operar(None)}"]\n'
                    else:
                        dot += f'n{cont}h{cont_h}[label="{sig.operar(None)}"]\n'
                    dot += f'n{cont}->n{cont}h{cont_h}\n'
                    sig = self.lista_lexema_arbol.pop(0)
                    cont_h += 1
            elif sig.operar(None) == '(':
                while sig.operar(None) != ";":
                    if sig.operar(None) == "\"":
                        dot += f'n{cont}h{cont_h}[label="\{sig.operar(None)}"]\n'
                    else:
                        dot += f'n{cont}h{cont_h}[label="{sig.operar(None)}"]\n'
                    dot += f'n{cont}->n{cont}h{cont_h}\n'
                    sig = self.lista_lexema_arbol.pop(0)
                    cont_h += 1
            cont += 1
    dot += "}"

    f = open('bb.dot', 'w', encoding="utf-8")
    f.write(dot)
    f.close()
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
    os.system(f'dot -Tsvg bb.dot -o arbol_derivacion.svg')
```

#### Función 17

Función para limpiar las listas.

```python
def limpiar_listas(self):
    self.lista_lexema.clear()
    self.lista_tokens.clear()
    self.lista_instrucciones.clear()
    self.lista_errores_lexicos.clear()
    self.lista_errores_sintacticos.clear()
    self.claves.clear()
    self.registros.clear()
```
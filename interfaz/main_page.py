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

        self.reporte_errores = tk.Button(self.menu_frame, text="Reporte de errores", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e")
        self.reporte_errores.grid(row=0, column=2, padx=5, pady=10)
        self.reporte_errores['font'] = self.fuente

        # tem_reporte = tk.StringVar()
        # reporte = ttk.Combobox(self.menu_frame, font = self.fuente, width=16, values=["Reporte de errores", "Reporte de Tokens", "Arbol de derivación"])
        self.reporte_tokens = tk.Button(self.menu_frame, text="Reporte de tokens", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e")
        self.reporte_tokens.grid(row=0, column=3, padx=5, pady=10)
        self.reporte_tokens['font'] = self.fuente

        self.arbol_derivacion = tk.Button(self.menu_frame, text="Arbol de derivación", padx=5, height=1, bg="#fdf9c4", activebackground="#ffda9e")
        self.arbol_derivacion.grid(row=0, column=4, padx=5, pady=10)
        self.arbol_derivacion['font'] = self.fuente

        self.opciones_menu.config(background="#fdf9c4")
        self.raiz.config(menu=self.menu)

    def center_window(self, window, ancho, alto):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - ancho) // 2
        y = (screen_height - alto) // 2
        window.geometry(f"{ancho}x{alto}+{x}+{y}")

    def actualizar_lineas(self, event = None):
        cantidad = self.editor.get('1.0', tk.END).count('\n')
        if cantidad != self.cantidad_lineas:
            self.lineas_bar.config(state = tk.NORMAL)
            self.lineas_bar.delete(1.0, tk.END)
            for linea in range(1, cantidad + 1):
                self.lineas_bar.insert(tk.END, f"{linea}\n")
            self.lineas_bar.config(state = tk.DISABLED)
            self.cantidad_lineas = cantidad

    def abrir_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("All files", "*.bizdata")])
        self.nombre_archivo(self.archivo)
        if self.archivo:
            with open(self.archivo, 'r') as file:
                self.datos_archivo = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", self.datos_archivo)
            self.actualizar_lineas()

    def guardar_archivo(self):
        if self.editor and self.archivo:
            try:
                self.datos_archivo = self.editor.get("1.0", tk.END)
                with open(self.archivo, 'w') as file:
                    file.write(self.editor.get("1.0", tk.END))
                messagebox.showinfo("Exito!", "El archivo se ha guardado correctamente")
            except Exception as e:
                messagebox.showinfo("Error!", "Error al guardar el archivo "+ str(e))

    def guardar_como(self):
        if self.editor:
            self.archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo JSON", "*.json")])
            self.nombre_archivo(self.archivo)
            self.datos_archivo = self.editor.get("1.0", tk.END)
            if self.archivo:
                with open(self.archivo, "w") as file:
                    file.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Exito!", "El archivo se ha guardado correctamente")

    def analizar(self):
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
                    # if int(self.consola.index('end-1c').split('.')[0]) == 1:
                    #     self.consola.insert(tk.END, ">>>")
                    imprimir_consola += elemento.ejecutarT()+" "
                elif isinstance(elemento, Imprimirln) or isinstance(elemento, Conteo) or isinstance(elemento, Promedio) or isinstance(elemento, Datos) or isinstance(elemento, Suma):
                    # if int(self.consola.index('end-1c').split('.')[0]) == 1:
                    #     self.consola.insert(tk.END, ">>>")
                    imprimir_consola += "\n"+elemento.ejecutarT()+" "
                # elif isinstance(elemento, Conteo):
                #     imprimir_consola += "\n"+elemento.ejecutarT()+" "

            lineas = [f"{flechas} {line}" for line in imprimir_consola.split('\n') if line.strip()]
            for line in lineas:
                self.consola.insert(tk.END, line + "\n")
        # self.consola.config(state='normal')
            # self.consola.insert(tk.END, imprimir_consola)
            self.consola.config(state='disabled')
            messagebox.showinfo("Análisis exitoso", "El código se analizó exitosamente.")

    def nombre_archivo(self, nombre):
        name = os.path.basename(nombre)
        self.variable_archivo.set(name)
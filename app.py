import tkinter as tk
from interfaz.main_page import main_page

raiz = tk.Tk()
ventana = main_page(raiz)
ventana.center_window(raiz, 1350, 850)

raiz.mainloop()
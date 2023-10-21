from clases.abstraccion import Expression

class Contarsi(Expression):

    def __init__(self, texto, fila, columna) -> None:
        self.texto = texto
        super().__init__(fila, columna)

    def operar(self, arbol):
            pass

    def ejecutarT(self):
        return self.texto

    def obtener_Fila(self):
        return super().obtener_Fila()
    
    def obtener_Columna(self):
        return super().obtener_Columna()
from clases.abstraccion import Expression

class Lexema(Expression):
    def __init__(self, lexema, tipo, fila, columna):
        self.lexema = lexema
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, arbol):
        return self.lexema
    
    def obtener_Fila(self):
        return super().obtener_Fila()
    
    def obtener_Columna(self):
        return super().obtener_Columna()
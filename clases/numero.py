from clases.abstraccion import Expression

class Numero(Expression):
    def __init__(self, lexema, fila, columna):
        self.lexema = lexema
        super().__init__(fila, columna)
    

    def operar(self, arbol):
        return self.lexema
    
    def obtener_Fila(self):
        return super().obtener_Fila()
    
    def obtener_Columna(self):
        return super().obtener_Columna()
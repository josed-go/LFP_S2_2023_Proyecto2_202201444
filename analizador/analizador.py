from clases.lexema import *
from clases.numero import *
from clases.error import *

class analizador:
    def __init__(self):
        self.numero_linea = 1
        self.numero_columna = 1

        self.lista_lexema = []
        self.lista_instrucciones = []
        self.lista_errores = []

        self.palabra_reservadas = {
            'CLAVES': 'Claves',
            'REGISTROS': 'Registros',
            'IMPRIMIR': 'imprimir',
            'IMPRIMIRLN': 'imprimirln',
            'CONTEO': 'conteo',
            'PROMEDIO': 'promedio',
            'CONTARSI': 'contarsi',
            'DATOS': 'datos',
            'SUMAR': 'sumar',
            'MAX': 'max',
            'MIN': 'min',
            'EXPORTARREPORTE': 'exportarReporte'
        }

        self.palabras = list(self.palabra_reservadas.values())

    def analizar(self, cadena):
        # print("aqui")
        lexema = ''
        puntero = 0

        while cadena:
            char = cadena[puntero]
            puntero += 1

            if char == '\n':
                cadena = cadena[1:]
                puntero = 0
                self.numero_linea += 1
                self.numero_columna = 1
            elif char == '\t':
                self.numero_linea += 1
                self.numero_columna += 4
                cadena = cadena[4:]
                puntero = 0
            elif char == '#':
                lexema, cadena = self.comentario(cadena[puntero:])
                if lexema and cadena :
                    self.numero_linea += 1

                    print("Comentario:", lexema)
                    self.numero_columna = 1
                    puntero = 0
            elif char == '\'':
                lexema, cadena = self.comentario(cadena[puntero:])
                if lexema and cadena :
                    self.numero_columna = 1

                    print("Comentario Multiple:", lexema)
                    self.numero_columna += len(lexema)+1
                    puntero = 0
            elif char.isalpha():
                lexema, cadena = self.armar_lexema(cadena)
                if lexema and cadena:
                    # self.numero_columna += 1


                    lexm = Lexema(lexema, self.numero_linea, self.numero_columna)
                    self.lista_lexema.append(lexm)
                    self.numero_columna += len(lexema) 
                    puntero = 0
            elif char == "[" or char == "]" or char == "{" or char == "}" or char == "(" or char == ")" or char == ";" or char == "\"" or char == "=" or char == ",":
                c = Lexema(char, self.numero_linea, self.numero_columna)
                self.numero_columna += 1

                self.lista_lexema.append(c)

                cadena = cadena[1:]
                puntero = 0
            elif char.isdigit():

                numero, cadena = self.numeros(cadena)

                if numero and cadena:
                    # self.numero_columna += 1

                    num = Numero(numero, self.numero_linea, self.numero_linea)

                    self.lista_lexema.append(num)
                    self.numero_columna += len(str(numero)) + 1
                    puntero = 0
            elif char == ' ' or char == '\r':
                cadena = cadena[1:]
                self.numero_columna += 1
                puntero = 0
            elif char == '\t':
                self.numero_columna += 4
                cadena = cadena[4:]
                puntero = 0
            elif char == '\n':
                cadena = cadena[1:]
                puntero = 0
                self.numero_linea += 1
                self.numero_columna = 1
            else:
                cadena = cadena[1:]
                puntero = 0
                self.numero_columna += 1
                # print("Errro:1", char)
                error = Errores((len(self.lista_errores)+1), char , "Error lexico", self.numero_linea, self.numero_columna)
                self.lista_errores.append(error)

        for lexema in self.lista_lexema:
            print(lexema.lexema)
        # for lexema in self.lista_lexema:
        #     print("{}-lin-{} -col-{}".format(lexema.lexema, lexema.obtener_Fila(), lexema.obtener_Columna()))
        # print("ERRORES")
        # for error in self.lista_errores:
        #     print(error.lexema)

    def armar_lexema(self, cadena):
        lexema = ''
        puntero = ''

        for char in cadena:
            puntero += char
            if char == ' ' or char == '\"':
                return lexema , cadena[len(puntero)-1:]
            else :
                lexema += char

        return None, None
    
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
                    return float(numero), cadena[len(puntero)-1:]
                else:
                    return int(numero), cadena[len(puntero)-1:]
            else:
                numero += char
        return None, None

    def comentario(self, cadena):
        lexema = ''
        puntero = ''
        cont = 0

        if cadena[0] == '\'':
            if cadena[1] == '\'':
                cadena[1:]
                # print("aqui2")
                for char in cadena:
                    puntero += char
                    if cont == 3:
                        # self.numero_linea += 1
                        return lexema, cadena[len(puntero)+1:]
                    
                    if char == '\'':
                        cont += 1
                    elif char == '\n':
                        self.numero_linea += 1
                    else:
                        lexema += char
        else:
            # print("aqu")
            for char in cadena:
                puntero += char
                if char == '\n':
                    self.numero_linea += 1
                    return lexema, cadena[len(puntero)+1:]
                else :
                    lexema += char
                    
                    

        return None, None
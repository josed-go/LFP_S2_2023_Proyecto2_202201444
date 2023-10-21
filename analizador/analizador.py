from clases.lexema import *
from clases.numero import *
from clases.error import *
from clases.imprimir import *
from clases.imprimirln import *
from clases.conteo import *
from clases.promedio import *
from clases.datos import *
from clases.suma import *
from clases.maxmin import *
from clases.reporte import *
from clases.contarsi import *

class analizador:
    def __init__(self):
        self.numero_linea = 1
        self.numero_columna = 1

        self.lista_lexema = []
        self.lista_instrucciones = []
        self.lista_errores_lexicos = []
        self.lista_errores_sintacticos = []
        self.lista_tokens = []

        self.claves = []
        self.registros = []

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

        self.tipo_tokens = {
            'Claves': 'CLAVES',
            'imprimir': 'IMPRIMIR',
            'imprimirln': 'IMPRIMIRLN',
            'Registros': 'REGISTROS',
            'conteo': 'CONTEO',
            'promedio': 'PROMEDIO',
            'contarsi': 'CONTARSI',
            'datos': 'DATOS',
            'sumar': 'SUMAR',
            'min': 'MIN',
            'max': 'MAX',
            'exportarReporte': 'EXPORTARREPORTE',
            '=': 'IGUAL',
            '(': 'PARINI',
            ')': 'PARFIN',
            '[': 'CORCHETEIN',
            ']': 'CORCHETEFIN',
            ';': 'PUNTOYCOMA',
            ',': 'COMA',
            '"': 'COMILLA',
            '{': 'LLAVEIN',
            '}': 'LLAVEFIN'
        }

        self.palabras = list(self.palabra_reservadas.values())

    def analizador_lexico(self, cadena):
        # print("aqui")
        lexema = ''
        puntero = 0

        while cadena:
            char = cadena[puntero]
            puntero += 1

            
            if char == '#':
                lexema, cadena = self.comentario(cadena[puntero:])
                if lexema and cadena :
                    self.numero_linea += 1

                    print("Comentario:", lexema)
                    # self.numero_columna = 1
                    puntero = 0
            elif char == '\'':
                lexema, cadena = self.comentario(cadena[puntero:])
                if lexema and cadena :
                    self.numero_linea += 1
                    # self.numero_columna = 1

                    print("Comentario Multiple:", lexema)
                    # self.numero_columna += len(lexema)+1
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

                if numero and cadena:

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
                # self.numero_linea += 1
                self.numero_columna += 4
                cadena = cadena[4:]
                puntero = 0
            else:
                cadena = cadena[1:]
                puntero = 0
                # print("Errro:1", char)
                error = Errores((len(self.lista_errores_lexicos)+1), char , "Error lexico", self.numero_linea, self.numero_columna)
                self.numero_columna += 1
                self.lista_errores_lexicos.append(error)

        # for lexema in self.lista_lexema:
        #     print(lexema.lexema)

        print("------------")
        for error in self.lista_errores_lexicos:
            print("Error Lexico:",error.lexema,"fila:",error.obtener_Fila(),"columna:",error.obtener_Columna())
        print("------------")
        print("Lexemas:")
        for lex_todos in self.lista_lexema:
            print("Lexema:",lex_todos.lexema,'Token:', lex_todos.tipo,"fila:",lex_todos.obtener_Fila(),"columna:",lex_todos.obtener_Columna())
        # for lexema in self.lista_lexema:
        #     print("{}-lin-{} -col-{}".format(lexema.lexema, lexema.obtener_Fila(), lexema.obtener_Columna()))
        # print("ERRORES")
        # for error in self.lista_errores:
        #     print(error.lexema)

        self.lista_tokens = self.lista_lexema.copy()

        return self.lista_lexema

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
                        self.numero_linea += 1
                        return lexema, cadena[len(puntero)+1:]
                    
                    if char == '\'':
                        cont += 1
                    elif char == '\n':
                        self.numero_linea += 1
                    else:
                        cont = 0
                        lexema += char
        else:
            # print("aqu")
            for char in cadena:
                puntero += char
                if char == '\n':
                    self.numero_linea += 1
                    self.numero_columna = 1
                    return lexema, cadena[len(puntero)+1:]
                else :
                    lexema += char
                    
                    

        return None, None
    
    def analizador_sintactico(self):
        palabra = ''
        sig_igual= ''
        corchete_in = ''
        corchete_fin = ''
        llave_in = ''
        comilla = ''

        while self.lista_lexema:
            
            if len(self.lista_errores_sintacticos) == 0:
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
                                            return Imprimirln(texto.lexema, lexema.obtener_Fila(), lexema.obtener_Columna())
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

                    elif lexema.operar(None) == "conteo":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            parentesis = self.lista_lexema.pop(0)
                            if parentesis.operar(None) == ')':
                                punto_coma = self.lista_lexema.pop(0)
                                if punto_coma.operar(None) == ';':
                                    return Conteo(self.get_conteo(), lexema.obtener_Fila(), lexema.obtener_Columna())
                                else:
                                    error = Errores((len(self.lista_errores_sintacticos)+1), punto_coma.operar(None), "Error sintactico", punto_coma.obtener_Fila(), punto_coma.obtener_Columna())
                                    self.lista_errores_sintacticos.append(error)
                            else:
                                error = Errores((len(self.lista_errores_sintacticos)+1), parentesis.operar(None), "Error sintactico", parentesis.obtener_Fila(), parentesis.obtener_Columna())
                                self.lista_errores_sintacticos.append(error)
                        else:
                            error = Errores((len(self.lista_errores_sintacticos)+1), lexema.operar(None), "Error sintactico", lexema.obtener_Fila(), lexema.obtener_Columna())
                            self.lista_errores_sintacticos.append(error)
                                
                    elif lexema.operar(None) == "promedio":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            comillas = self.lista_lexema.pop(0)
                            if comillas.operar(None) == '"':
                                campo = self.lista_lexema.pop(0)
                                comillas = self.lista_lexema.pop(0)
                                if comillas.operar(None) == '"':
                                    parentesis = self.lista_lexema.pop(0)
                                    if parentesis.operar(None) == ')':
                                        punto_coma = self.lista_lexema.pop(0)
                                        if punto_coma.operar(None) == ';':

                                            resultado = self.promedio(campo.lexema)

                                            return Promedio(resultado, lexema.obtener_Fila(), lexema.obtener_Columna())
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

                    elif lexema.operar(None) == "datos":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            parentesis = self.lista_lexema.pop(0)
                            if parentesis.operar(None) == ')':
                                punto_coma = self.lista_lexema.pop(0)
                                if punto_coma.operar(None) == ';':

                                    return Datos(self.get_datos(), lexema.obtener_Fila(), lexema.obtener_Columna())
                                else:
                                    error = Errores((len(self.lista_errores_sintacticos)+1), punto_coma.operar(None), "Error sintactico", punto_coma.obtener_Fila(), punto_coma.obtener_Columna())
                                    self.lista_errores_sintacticos.append(error)
                            else:
                                error = Errores((len(self.lista_errores_sintacticos)+1), parentesis.operar(None), "Error sintactico", parentesis.obtener_Fila(), parentesis.obtener_Columna())
                                self.lista_errores_sintacticos.append(error)
                        else:
                            error = Errores((len(self.lista_errores_sintacticos)+1), lexema.operar(None), "Error sintactico", lexema.obtener_Fila(), lexema.obtener_Columna())
                            self.lista_errores_sintacticos.append(error)
                                
                    elif lexema.operar(None) == "sumar":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            comillas = self.lista_lexema.pop(0)
                            if comillas.operar(None) == '"':
                                campo = self.lista_lexema.pop(0)
                                comillas = self.lista_lexema.pop(0)
                                if comillas.operar(None) == '"':
                                    parentesis = self.lista_lexema.pop(0)
                                    if parentesis.operar(None) == ')':
                                        punto_coma = self.lista_lexema.pop(0)
                                        if punto_coma.operar(None) == ';':

                                            resultado = self.sumar(campo.lexema)

                                            return Suma(resultado, lexema.obtener_Fila(), lexema.obtener_Columna())
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
                    
                    elif lexema.operar(None) == "max":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            comillas = self.lista_lexema.pop(0)
                            if comillas.operar(None) == '"':
                                campo = self.lista_lexema.pop(0)
                                comillas = self.lista_lexema.pop(0)
                                if comillas.operar(None) == '"':
                                    parentesis = self.lista_lexema.pop(0)
                                    if parentesis.operar(None) == ')':
                                        punto_coma = self.lista_lexema.pop(0)
                                        if punto_coma.operar(None) == ';':

                                            resultado = self.get_max(campo.lexema)

                                            return MaxMin(resultado, lexema.obtener_Fila(), lexema.obtener_Columna())
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
                                        
                    elif lexema.operar(None) == "min":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            comillas = self.lista_lexema.pop(0)
                            if comillas.operar(None) == '"':
                                campo = self.lista_lexema.pop(0)
                                comillas = self.lista_lexema.pop(0)
                                if comillas.operar(None) == '"':
                                    parentesis = self.lista_lexema.pop(0)
                                    if parentesis.operar(None) == ')':
                                        punto_coma = self.lista_lexema.pop(0)
                                        if punto_coma.operar(None) == ';':

                                            resultado = self.get_min(campo.lexema)

                                            return MaxMin(resultado, lexema.obtener_Fila(), lexema.obtener_Columna())
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
                    
                    elif lexema.operar(None) == "exportarReporte":
                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            comillas = self.lista_lexema.pop(0)
                            if comillas.operar(None) == '"':
                                titulo = self.lista_lexema.pop(0)
                                comillas = self.lista_lexema.pop(0)
                                if comillas.operar(None) == '"':
                                    parentesis = self.lista_lexema.pop(0)
                                    if parentesis.operar(None) == ')':
                                        punto_coma = self.lista_lexema.pop(0)
                                        if punto_coma.operar(None) == ';':

                                            self.generar_reporte(titulo.lexema)

                                            return Reporte(titulo.lexema, lexema.obtener_Fila(), lexema.obtener_Columna())
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

                    elif lexema.operar(None) == "contarsi":

                        lexema = self.lista_lexema.pop(0)
                        if lexema.operar(None) == '(':
                            comillas = self.lista_lexema.pop(0)
                            if comillas.operar(None) == '"':
                                campo = self.lista_lexema.pop(0)
                                comillas = self.lista_lexema.pop(0)
                                if comillas.operar(None) == '"':
                                    coma = self.lista_lexema.pop(0)
                                    if coma.operar(None) == ',':
                                        sig = self.lista_lexema.pop(0)
                                        if sig.operar(None) == '"':
                                            valor = self.lista_lexema.pop(0)
                                            comillas = self.lista_lexema.pop(0)
                                            if comillas.operar(None) == '"':
                                                parentesis = self.lista_lexema.pop(0)
                                                if parentesis.operar(None) == ')':
                                                    punto_coma = self.lista_lexema.pop(0)
                                                    if punto_coma.operar(None) == ';':

                                                        resultado = self.contar_si(campo.operar(None), valor.operar(None))

                                                        return Contarsi(resultado, lexema.obtener_Fila(), lexema.obtener_Columna())
                                                    else:
                                                        error = Errores((len(self.lista_errores_sintacticos)+1), punto_coma.operar(None), "Error sintactico", punto_coma.obtener_Fila(), punto_coma.obtener_Columna())
                                                        self.lista_errores_sintacticos.append(error)
                                                else:
                                                    error = Errores((len(self.lista_errores_sintacticos)+1), parentesis.operar(None), "Error sintactico", parentesis.obtener_Fila(), parentesis.obtener_Columna())
                                                    self.lista_errores_sintacticos.append(error)
                                            else:
                                                error = Errores((len(self.lista_errores_sintacticos)+1), comillas.operar(None), "Error sintactico", comillas.obtener_Fila(), comillas.obtener_Columna())
                                                self.lista_errores_sintacticos.append(error)
                                        elif str(sig.operar(None)).isdigit():
                                            parentesis = self.lista_lexema.pop(0)
                                            if parentesis.operar(None) == ')':
                                                punto_coma = self.lista_lexema.pop(0)
                                                if punto_coma.operar(None) == ';':

                                                    resultado = self.contar_si(campo.operar(None), sig.operar(None))

                                                    return Contarsi(resultado, lexema.obtener_Fila(), lexema.obtener_Columna())
                                                else:
                                                    error = Errores((len(self.lista_errores_sintacticos)+1), punto_coma.operar(None), "Error sintactico", punto_coma.obtener_Fila(), punto_coma.obtener_Columna())
                                                    self.lista_errores_sintacticos.append(error)
                                            else:
                                                error = Errores((len(self.lista_errores_sintacticos)+1), parentesis.operar(None), "Error sintactico", parentesis.obtener_Fila(), parentesis.obtener_Columna())
                                                self.lista_errores_sintacticos.append(error)
                                        else:
                                            error = Errores((len(self.lista_errores_sintacticos)+1), sig.operar(None), "Error sintactico", sig.obtener_Fila(), sig.obtener_Columna())
                                            self.lista_errores_sintacticos.append(error)
                                    else:
                                        error = Errores((len(self.lista_errores_sintacticos)+1), coma.operar(None), "Error sintactico", coma.obtener_Fila(), coma.obtener_Columna())
                                        self.lista_errores_sintacticos.append(error)
                                else:
                                    error = Errores((len(self.lista_errores_sintacticos)+1), comillas.operar(None), "Error sintactico", comillas.obtener_Fila(), comillas.obtener_Columna())
                                    self.lista_errores_sintacticos.append(error)
                            else :
                                error = Errores((len(self.lista_errores_sintacticos)+1), comillas.operar(None), "Error sintactico", comillas.obtener_Fila(), comillas.obtener_Columna())
                                self.lista_errores_sintacticos.append(error)
                        else :
                            error = Errores((len(self.lista_errores_sintacticos)+1), lexema.operar(None), "Error sintactico", lexema.obtener_Fila(), lexema.obtener_Columna())
                            self.lista_errores_sintacticos.append(error)
                    else :
                        error = Errores((len(self.lista_errores_sintacticos)+1), lexema.operar(None), "Error sintactico", lexema.obtener_Fila(), lexema.obtener_Columna())
                        self.lista_errores_sintacticos.append(error)
                else:
                    error = Errores((len(self.lista_errores_sintacticos)+1), lexema.operar(None), "Error sintactico", lexema.obtener_Fila(), lexema.obtener_Columna())
                    self.lista_errores_sintacticos.append(error)

                    return "MALOOOO"
            else :

                for er in self.lista_errores_sintacticos:
                    print("ERROr", er.lexema)
                return None

        return None
            
    def recursivo_operar(self):
        while True:
            operacion = self.analizador_sintactico()
            if operacion:
                self.lista_instrucciones.append(operacion)
            else :
                break

        # for instur in self.lista_instrucciones:
        #     print(instur.tipo.operar(None))
        
        return self.lista_instrucciones
    
    def armar_registros(self):
        comilla = ''
        llave_in = ''
        llave_cierre = ''
        regis = ''

        llave_in = self.lista_lexema.pop(0)

        lista_temp = []

        while llave_cierre != "]":

            if llave_in.operar(None) == "{":

                sig = self.lista_lexema.pop(0)
                while sig.operar(None) != "}":

                    if sig.operar(None) == "\"":

                        regis = self.lista_lexema.pop(0)
                        comilla = self.lista_lexema.pop(0)

                        if comilla.operar(None) == "\"":
                            lista_temp.append(regis.operar(None))
                    elif sig.operar(None) == ",":

                        sig = self.lista_lexema.pop(0)
                        continue
                    else:
                        # error = Errores((len(self.lista_errores_sintacticos)+1), sig.operar(None), "Error sintactico", sig.obtener_Fila(), sig.obtener_Columna())
                        # self.lista_errores_sintacticos.append(error)
                        lista_temp.append(sig.operar(None))

                    sig = self.lista_lexema.pop(0)

                self.registros.append(lista_temp)
                lista_temp = []
            else:
                error = Errores((len(self.lista_errores_sintacticos)+1), llave_in.operar(None), "Error sintactico", llave_in.obtener_Fila(), llave_in.obtener_Columna())
                self.lista_errores_sintacticos.append(error)

            llave_cierre = self.lista_lexema.pop(0).operar(None)    

    def get_conteo(self):
        return str(len(self.registros))
    
    def contar_si(self, campo, valor):
        cont = 0

        index = self.claves.index(campo)

        for registros in self.registros:
            if str(registros[index]) == str(valor):
                cont += 1

        return str(cont)

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
            
    def armar_claves(self):
        sig2 = ""
        prueba = self.lista_lexema.pop(0)

        if prueba.operar(None) == "\"":
            col = self.lista_lexema.pop(0)

            sig = self.lista_lexema.pop(0)

            if sig.operar(None) == "\"":
                self.claves.append(col.operar(None))
                sig2 = self.lista_lexema.pop(0)

            else:
                error = Errores((len(self.lista_errores_sintacticos)+1), sig.operar(None), "Error sintactico", sig.obtener_Fila(), sig.obtener_Columna())
                self.lista_errores_sintacticos.append(error)
                return print("ERRROE1")
            
            if sig2.operar(None) == ",":
                    self.armar_claves()

            elif sig2.operar(None) == "]":
                pass
            else:
                error = Errores((len(self.lista_errores_sintacticos)+1), sig2.operar(None), "Error sintactico", sig2.obtener_Fila(), sig2.obtener_Columna())
                self.lista_errores_sintacticos.append(error)
                return print("ERRROE2")

        else:
            error = Errores((len(self.lista_errores_sintacticos)+1), prueba.operar(None), "Error sintactico", prueba.obtener_Fila(), prueba.obtener_Columna())
            self.lista_errores_sintacticos.append(error)
            return print("ERROR")
        
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
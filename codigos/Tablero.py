if __name__ == 'codigos.Tablero':
	from codigos import jugar#NO SE QUE TAN BIEN ESTÁ ESTO
import json

class Tablero():
    def __init__(self, nivel, letras=None, confirmadas=None, coloreadas=None):
        '''Seteamos el tamaño por nivel, las casillas especiales e inicializamos el tablero como vacio'''
        self.__nivel = nivel
        if self.__nivel == "Facil":
            self.__tamanio = 23
            self.__especiales = {"uno": (('b_0_6'), ('b_1_7'), ('b_2_8'), ('b_3_9'), ('b_4_10'), ('b_5_11'), ('b_6_12'), ('b_7_13'), ('b_8_14'), ('b_9_15'), ('b_10_16'), ('b_11_17'), ('b_12_18'), ('b_13_19'), ('b_14_20'), ('b_15_21'), ('b_16_22')),
                                 "dos": (('b_6_0'), ('b_7_1'), ('b_8_2'), ('b_9_3'), ('b_10_4'), ('b_11_5'), ('b_12_6'), ('b_13_7'), ('b_14_8'), ('b_15_9'), ('b_16_10'), ('b_17_11'), ('b_18_12'), ('b_19_13'), ('b_20_14'), ('b_21_15'), ('b_22_16')),
                                 "tres": (('b_0_17'), ('b_1_16'), ('b_2_15'), ('b_3_14'), ('b_4_13'), ('b_5_12'), ('b_6_11'), ('b_7_10'), ('b_8_9'), ('b_9_8'), ('b_10_7'), ('b_11_6'), ('b_12_5'), ('b_13_4'), ('b_14_3'), ('b_15_2'), ('b_16_1'), ('b_17_0')),
                                 "cuatro": (('b_6_22'), ('b_7_21'), ('b_8_20'), ('b_9_19'), ('b_10_18'), ('b_11_17'), ('b_12_16'), ('b_13_15'), ('b_14_14'), ('b_15_13'), ('b_16_12'), ('b_17_11'), ('b_18_10'), ('b_19_9'), ('b_20_8'), ('b_21_7'), ('b_22_6')),
                                 "cinco": (('b_1_5'), ('b_2_4'), ('b_3_3'), ('b_4_2'), ('b_5_1'), ('b_1_18'), ('b_2_19'), ('b_3_20'), ('b_4_21'), ('b_5_22'), ('b_18_1'), ('b_19_2'), ('b_20_3'), ('b_21_4'), ('b_22_5'), ('b_17_22'), ('b_18_21'), ('b_19_20'), ('b_20_19'), ('b_21_18'), ('b_22_17')),
                                 "seis": (('b_6_5'), ('b_17_5'),  ('b_6_17'), ('b_17_17'), ('b_0_0'), ('b_11_0'), ('b_22_0'), ('b_0_11'), ('b_22_11'), ('b_0_22'), ('b_11_22'), ('b_22_22'))
                                 }
        elif self.__nivel == "Medio":
            self.__tamanio = 19
            self.__especiales = {"uno": (('b_0_0'), ('b_0_9'), ('b_0_18'), ('b_9_0'), ('b_9_18'), ('b_18_0'), ('b_18_9'), ('b_18_18')),
                                 "dos": (('b_1_1'), ('b_2_2'), ('b_3_3'), ('b_4_4'), ('b_5_5'), ('b_6_6'), ('b_7_7'), ('b_8_8'), ('b_10_10'), ('b_11_11'), ('b_12_12'), ('b_13_13'), ('b_14_14'), ('b_15_15'), ('b_16_16'), ('b_17_17'), ('b_17_1'), ('b_16_2'), ('b_15_3'), ('b_14_4'), ('b_13_5'), ('b_12_6'), ('b_11_7'), ('b_10_8'), ('b_8_10'), ('b_7_11'), ('b_6_12'), ('b_5_13'), ('b_4_14'), ('b_3_15'), ('b_2_16'), ('b_1_17')),
                                 "tres": (('b_4_9'), ('b_9_4'), ('b_14_9'), ('b_9_14'))
                                 }
        else:
            self.__tamanio = 15
            self.__especiales = {"uno": (('b_0_0'), ('b_7_0'), ('b_14_0'), ('b_0_7'), ('b_14_7'), ('b_0_14'), ('b_7_14'), ('b_14_14')),
                                 "dos": (('b_1_1'),   ('b_2_2'), ('b_3_3'), ('b_4_4'), ('b_1_13'), ('b_2_12'), ('b_3_11'), ('b_4_10'), ('b_13_1'), ('b_12_2'), ('b_11_3'), ('b_10_4'), ('b_13_13'), ('b_12_12'), ('b_11_11'), ('b_10_10')),
                                 "tres": (('b_1_5'), ('b_1_9'), ('b_5_1'), ('b_5_5'), ('b_5_9'), ('b_5_13'), ('b_9_1'), ('b_9_5'), ('b_9_9'), ('b_9_13'), ('b_13_5'), ('b_13_9')),
                                 "cuatro": (('b_0_3'), ('b_0_11'), ('b_2_6'), ('b_2_8'), ('b_3_0'), ('b_3_7'), ('b_3_14'), ('b_6_2'), ('b_6_6'), ('b_6_8'), ('b_6_12'), ('b_7_3'), ('b_7_11'), ('b_8_2'), ('b_8_6'), ('b_8_8'), ('b_8_12'), ('b_11_0'), ('b_11_7'), ('b_11_14'), ('b_12_6'), ('b_12_8'), ('b_14_3'), ('b_14_11'))
                                 }
        if letras == None:
            self.__letras = [["" for i in range(self.__tamanio)] for j in range(self.__tamanio)]
        else:
            self.__letras = letras
        if confirmadas == None:
            self.__confirmadas = [[False for i in range(self.__tamanio)] for j in range(self.__tamanio)]
        else:
            self.__confirmadas = confirmadas
        if coloreadas == None:
            self.__coloreadas = [["None" for i in range(self.__tamanio)] for j in range(self.__tamanio)]
        else:
            self.__coloreadas = coloreadas

    def get_especiales(self):
        return self.__especiales

    def get_tamanio(self):
        return self.__tamanio

    def get_letras(self):
        return self.__letras

    def get_letra(self, x, y):
        return self.__letras[x][y]

    def set_letra(self, l, x, y):
        self.__letras[x][y] = l

    def get_confirmadas(self):
        return self.__confirmadas

    def get_coloreadas(self):
        return self.__coloreadas

    def get_no_confirmadas(self):
        '''con esto se obtienen las casillas no ocupadas por letras a través de una lista de tuplas'''
        fichas = []
        for x in range(self.__tamanio):
            for y in range(self.__tamanio):
                if ((not self.__confirmadas[x][y]) and (self.__letras[x][y] != "")):
                    fichas.append((x, y))
        return fichas

    def buscar_palabra(self, jugador):
        fichas = []
        for x in range(self.__tamanio):
            for y in range(self.__tamanio):
                if ((not self.__confirmadas[x][y]) and (self.__letras[x][y] != "")):
                    fichas.append((self.__letras[x][y], x, y))

        es_palabra = True

        # Verifico que tenga las letras en una sola linea horizontal o vertical
        es_vertical = True
        for i in range(len(fichas)):
            if (fichas[i][1] != fichas[0][1]):
                es_vertical = False
        if not es_vertical:
            es_horizontal = True
            for i in range(len(fichas)):
                if (fichas[i][2] != fichas[0][2]):
                    es_horizontal = False

        # Verifico que no tenga espacios
        if(len(fichas) > 1):
            if es_vertical:
                fichas = sorted(fichas, key=lambda item: item[2])
                x = fichas[0][2]
                for y in range(len(fichas)):
                    if (x != fichas[y][2]):
                        es_palabra = False
                    x += 1
            elif es_horizontal:
                fichas = sorted(fichas, key=lambda item: item[1])
                y = fichas[0][1]
                for x in range(len(fichas)):
                    if (y != fichas[x][1]):
                        es_palabra = False
                    y += 1
            else:
                es_palabra = False
        else:
            es_palabra = False
    	
        medio=True
    	#Verifico si el primer turno es del jugador y si es así, si la palbra introducida pasa por el medio del tablero
        if(jugador.get_primer_turno()) and (self.__letras[self.__tamanio//2][self.__tamanio//2] == "★"):
            es_palabra = False
            medio=False

        # Armo la palabra
        if es_palabra:
            palabra = ""
            for i in range(len(fichas)):
                palabra = palabra+fichas[i][0]
            palabra = palabra.lower()
        else:
            palabra = "No es palabra"

        return palabra,medio

    def confirmar_letras(self, win, turno):
        '''Confirmo las letras ingresadas y calculo el puntaje dependiendo el nivel'''
        puntaje = 0
        puntaje_letras = {}
        claves = []
        for x in range(self.__tamanio):
            for y in range(self.__tamanio):
                if ((not self.__confirmadas[x][y]) and (self.__letras[x][y] != "")):
                    self.__confirmadas[x][y] = True
                    letra = self.__letras[x][y]
                    claves.append((letra, x, y))
                    if turno:
                        win["b_"+str(x)+"_"+str(y)].update(button_color=('white', '#6a354c'))
                        self.__coloreadas[x][y]="IA"
                    else:
                        win["b_"+str(x)+"_"+str(y)].update(button_color=('white', '#498269'))
                        self.__coloreadas[x][y]="Jugador"
        if self.__nivel == "Facil":
            puntaje = self.__calcular_puntaje_Facil(claves)
        elif self.__nivel == "Medio":
            puntaje = self.__calcular_puntaje_Medio(claves)
        else:
            puntaje = self.__calcular_puntaje_dificil(claves)

        return puntaje

    def insertar_palabra(self, palabra, window, jugador, IA,lista):# no lo entiendo bien
        casillas = []
        ok = False
        pal=palabra.replace(' ','')
        if(not IA.get_primer_turno()):
            for i in range(self.__tamanio):
                for j in range(self.__tamanio):
                    if(not self.__confirmadas[j][i]):
                        casillas.append((j, i))
                        if(len(casillas) == len(palabra.split())):
                            ok = True
                            break
                    else:
                        casillas = []
                if(ok):
                    break
                else:
                    casillas = []

            if(not ok):
                for i in range(self.__tamanio):
                    for j in range(self.__tamanio):
                        if(not self.__confirmadas[i][j]):
                            casillas.append((i, j))
                            if(len(casillas) == len(palabra.split())):
                                ok = True
                                break
                        else:
                            casillas = []
                    if(ok):
                        break
                    else:
                        casillas = []
        else:
            for i in range(len(palabra.split())):
                casillas.append((i+self.__tamanio//2, self.__tamanio//2))
            ok = True

        if(ok):
            i = 0
            for c in casillas:
                self.__letras[c[0]][c[1]] = palabra.split()[i]
                window["b_"+str(c[0])+"_"+str(c[1])].update(palabra.split()[i])
                i += 1
            jugar.confirmar(window, self, jugador, IA,pal,lista)

        return ok 

    def __calcular_puntaje_Facil(self, claves):
        '''Calculo el puntaje del nivel fácil teniendo en cuenta si pasa por las casillas especiales del nivel'''
        rojo = self.__especiales["uno"]
        azul = self.__especiales["dos"]
        amarillo = self.__especiales["tres"]
        verde = self.__especiales["cuatro"]
        celeste = self.__especiales["cinco"]
        anaranjado = self.__especiales["seis"]

        puntaje = 0
        puntaje_letras = {}
        duplicar=False
        triplicar=False

        for i in claves:
            try:
                with open("archivos/config.json", "r") as c:
                    config = json.load(c)
                puntaje_letras = config["puntaje_fichas"]
                if ("b_"+str(i[1])+"_"+str(i[2])) in rojo:
                    # Duplica el valor de la letra
                    puntaje = puntaje + (puntaje_letras[i[0]]*2)
                elif ("b_"+str(i[1])+"_"+str(i[2])) in azul:
                    # Triplica el valor de la letra
                    puntaje = puntaje+(puntaje_letras[i[0]]*3)
                elif ("b_"+str(i[1])+"_"+str(i[2])) in amarillo:
                    # Duplica el valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]
                    triplicar=True
                elif("b_"+str(i[1])+"_"+str(i[2])) in verde:
                    # Triplica el valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]
                    duplicar=True
                elif("b_"+str(i[1])+"_"+str(i[2])) in celeste:
                    # Resta 2 al valor de la palabra"
                    puntaje = puntaje+puntaje_letras[i[0]]-2
                elif("b_"+str(i[1])+"_"+str(i[2])) in anaranjado:
                    # Resta 3 al valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]-3
                else:
                    # incrementa los pts en caso que no haya caido en una casilla especial
                    puntaje = puntaje+puntaje_letras[i[0]]
            except FileNotFoundError as ex:
                sg.popup("No se encontro el archivo config.json",title='')

        if triplicar:
            puntaje*=3
        elif duplicar:
            puntaje*=2

        return puntaje

    def __calcular_puntaje_Medio(self, claves):
        '''Calculo el puntaje del nivel medio teniendo en cuenta si pasa por las casillas especiales del nivel'''
        verde = self.__especiales["uno"]
        rosa = self.__especiales["dos"]
        dorado = self.__especiales["tres"]

        puntaje = 0
        puntaje_letras = {}

        for i in claves:
            try:
                with open("archivos/config.json", "r") as c:
                    config = json.load(c)
                puntaje_letras = config["puntaje_fichas"]
                if("b_"+str(i[1])+"_"+str(i[2])) in rosa:
                    # Duplica el valor de la letra
                    puntaje = puntaje + (puntaje_letras[i[0]]*2)
                elif ("b_"+str(i[1])+"_"+str(i[2])) in dorado:
                    # Resta 2 al valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]-2
                elif ("b_"+str(i[1])+"_"+str(i[2])) in verde:
                    # Resta 3 al valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]-3
                else:
                    # incrementa los pts en caso que no haya caido en una casilla especial
                    puntaje = puntaje + puntaje_letras[i[0]]
            except FileNotFoundError as ex:
                sg.popup("No se encontro el archivo config.json",title='')
        return puntaje

    def __calcular_puntaje_dificil(self, claves):
        '''Calculo el puntaje del nivel difícil teniendo en cuenta si pasa por las casillas especiales del nivel'''
        Anaranjado = self.__especiales["uno"]
        Amarillo = self.__especiales["dos"]
        Verde = self.__especiales["tres"]
        Celeste = self.__especiales["cuatro"]
        puntaje = 0
        puntaje_letras = {}
        
        for i in claves:
            try:
                with open("archivos/config.json", "r") as c:
                    config = json.load(c)
                puntaje_letras = config["puntaje_fichas"]
                if ("b_"+str(i[1])+"_"+str(i[2])) in Celeste:
                    # Duplica el valor de la letra
                    puntaje = puntaje + (puntaje_letras[i[0]]*2)
                elif("b_"+str(i[1])+"_"+str(i[2])) in Anaranjado:
                    # Triplica el valor de la letra
                    puntaje = puntaje+(puntaje_letras[i[0]]*3)
                elif ("b_"+str(i[1])+"_"+str(i[2])) in Verde:
                    # Resta 2 al valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]-2
                elif ("b_"+str(i[1])+"_"+str(i[2])) in Amarillo:
                    # Resta 3 al valor de la palabra
                    puntaje = puntaje+puntaje_letras[i[0]]-3
                else:
                    # incrementa los pts en caso que no haya caido en una casilla especial
                    puntaje = puntaje+puntaje_letras[i[0]]
            except FileNotFoundError as ex:
                sg.popup("No se encontro el archivo config.json",title='')

        return puntaje
        


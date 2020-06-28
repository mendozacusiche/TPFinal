import PySimpleGUI as sg
from string import ascii_uppercase as up
import random, sys, time, json, threading, ventana_bienvenida, Fichas, Tablero, IA
from pattern.es import parse, conjugate, INFINITIVE

def evaluar(palabra, dificultad):
    ok=False
    if palabra != "No es palabra":
        if (dificultad == "Facil") and (parse(palabra).split("/")[1] in ("JJ","NN","VB")):
            ok=True
        elif (dificultad == "Medio") and (parse(palabra).split("/")[1] in ("JJ","VB")):
            ok=True
        elif (dificultad == "DificilVerbos") and (parse(palabra).split("/")[1] in ("VB")):
            ok=True
        elif (dificultad == "DificilAdjetivos") and (parse(palabra).split("/")[1] in ("JJ")):
            ok=True
    return ok

def terminar():
    pass

def recargar_fichas(fichas, bolsa, window, turnoIA=False):
    usadas=fichas.get_usadas()
    for i in range(7):
        if usadas[i]:
            l=sacar_letra_bolsa(bolsa)
            if not turnoIA:
                window["-letra"+str(i)+"-"].update(l)
            fichas.set_letra(l,i)
            usadas[i]=False

def pasar(tablero,fichas,tiempos,tiempo_turno,Intel,bolsa,window,turnoIA=False):
    window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
    devolver_fichas(window,tablero,fichas)
    recargar_fichas(fichas,bolsa,window,turnoIA)
    tiempos[1]=tiempo_turno
    Intel.set_mi_turno(not turnoIA)

def segundo(tablero,fichas_jugador, Intel, tiempo_turno, bolsa, window, t):
    while (t[0]>0):
        time.sleep(1)
        t[0]-=1
        t[1]-=1
        if(t[1]== 0):
            if Intel.get_mi_turno():
                pasar(tablero,Intel.get_fichas(),t,tiempo_turno,Intel,bolsa,window,True)
            else:
                pasar(tablero,fichas_jugador,t,tiempo_turno,Intel,bolsa,window)
                Intel.turno()
                pasar(tablero,Intel.get_fichas(),t,tiempo_turno,Intel,bolsa,window,True)
    terminar()

def contar_letras_bolsa(bolsa):
    cant=0
    for letra in bolsa.keys():
        cant=cant+bolsa[letra]
    return cant

def sacar_letra_bolsa(bolsa):
    letra=random.choice(list(bolsa.keys()))
    while (bolsa[letra] == 0):
        letra=random.choice(list(bolsa.keys()))
    bolsa[letra]-=1
    return letra

def iniciar(iniciado, t, window, config, tiempo_turno, tablero):
    bolsa=config["cant_fichas"]
    Inteligencia = IA.IA (bolsa)
    nuevas=[]
    for i in range(7):
        l=sacar_letra_bolsa(bolsa)
        nuevas.append(l)
        window["-letra"+str(i)+"-"].update(l)
    fichas_jugador= Fichas.Fichas(nuevas)
    timers= threading.Thread(target= segundo, args=(tablero,fichas_jugador,Inteligencia,tiempo_turno,bolsa,window,t))
    if __name__ == 'jugar':
        timers.start()
    window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
    return True, fichas_jugador, bolsa, Inteligencia

def crear_botones(n, tablero):
    return [[sg.Button(" ",font=("Impact", 9),size=(3,0),pad=(0,0),key=("b_"+str(n)+"_"+str(i)))]for i in range(tablero.get_tamanio())]

def crear_layout(tablero, tiempos, jugador):

    layout_fichasIA=[[sg.Button("#",font=("Impact",14), button_color=color_button, key=("-letraIA"+str(i)+"-")) for i in range(7)]]
    layout_fichas_jugador=[[sg.Button(" ",font=("Impact",14), button_color=color_button, key=("-letra"+str(i)+"-")) for i in range(7)]]

    columna_1 = [
                [sg.Frame('FICHAS COMPUTADORA',layout_fichasIA)],
                [sg.Column(crear_botones(i, tablero), pad=(0,0)) for i in range(tablero.get_tamanio())],
                [sg.Frame('FICHAS JUGADOR',layout_fichas_jugador),sg.Button('CAMBIAR',font=("Impact",12))]
            ]


    Tiempo_juego= [
                    [sg.Text(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}",size=(10, 2), font=('Helvetica', 20), justification='center', key='-TURNO-')],
                  ]

    T_turno = [
                [sg.Text(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}",size=(10, 2), font=('Helvetica', 20), justification='center', key='-DURACION-')],
              ]

    columna_2 = [
                [sg.Button('INICIAR',font=("Impact",14))],
                [sg.Frame('DURACION DEL JUEGO',Tiempo_juego, pad=(10,10), relief= 'solid'), sg.Frame('DURACION DEL TURNO',T_turno, pad= (10, 10), relief= 'solid')],
                [sg.Image(filename='imagenes/playerlogo.png', pad=(5, 0)), sg.Text(jugador)],
                [sg.Text('PUNTAJE'), sg.Text('0000000',key=("-puntos-")) ],
                [sg.Image(filename='imagenes/computerlogo.png', pad=(5, 0)), sg.Text('PC')],
                [sg.Text('PUNTAJE'), sg.Text('0000000',key=("-puntosIA-"))],
                [sg.Text('FICHAS EN BOLSA:'), sg.Text("000", key=("-CantFichas-"))],
                [sg.Button('Pasar',font=("Impact",10))],
                [sg.Button("Evaluar Palabra",font=("Impact",10))], 
                [sg.Button('Posponer',font=("Impact",10))],
                [sg.Button('Terminar',font=("Impact",10))],
                [sg.Button('Exit',font=("Impact",10))]
                ]

    layout = [  
                [sg.Column(columna_1, pad=(0,0)), sg.Frame('CONFIGURACION', columna_2, pad=(20, 50), relief= 'solid')],
             ]
    return layout     

def checkear_ficha(event, fichas, window, n):
    if (fichas.get_checked()[n]==False):
        fichas.descheckear_todas(window)
        fichas.checkear(n)
        window["-letra"+str(n)+"-"].update(button_color=('white','blue'))
    else:
        fichas.descheckear(n)
        window["-letra"+str(n)+"-"].update(button_color=('white','OrangeRed3'))


def clickear_ficha(event, fichas, window):

    if event == ("-letra0-"):
        checkear_ficha(event,fichas,window,0)
        return 0
    elif event == ("-letra1-"):
        checkear_ficha(event,fichas,window,1)
        return 1
    elif event == ("-letra2-"):
        checkear_ficha(event,fichas,window,2)
        return 2
    elif event == ("-letra3-"):
        checkear_ficha(event,fichas,window,3)
        return 3
    elif event == ("-letra4-"):
        checkear_ficha(event,fichas,window,4)
        return 4
    elif event == ("-letra5-"):
        checkear_ficha(event,fichas,window,5)
        return 5
    elif event == ("-letra6-"):
        checkear_ficha(event,fichas,window,6)
        return 6

def devolver_letra(window,tablero,fichas,x,y):
    pos=0
    while (fichas.get_letras()[pos]!= ""):
        pos+=1
    window["-letra"+str(pos)+"-"].update(tablero.get_letra(x,y))
    fichas.set_letra(tablero.get_letra(x,y), pos)
    fichas.desusar(pos)
    tablero.set_letra("",x,y)

def devolver_fichas(window,tablero,fichas):
    coordenadas=tablero.get_no_confirmadas()
    for c in coordenadas:
        devolver_letra(window,tablero,fichas,c[0],c[1])
        window["b_"+str(c[0])+"_"+str(c[1])].update("")

def colocar_letra(event,fichas,tablero,window,pos):
    if True in (fichas.get_checked()):
        b,x,y = str(event).split("_")
        x= int (x)
        y= int (y)
        if not fichas.get_usadas()[pos]:
            if (not tablero.get_confirmadas()[x][y]):
                if (tablero.get_letra(x,y)!=""):
                    devolver_letra(window,tablero,fichas,x,y)
                tablero.set_letra(fichas.get_letras()[pos],x,y)
                window[event].update(fichas.get_letras()[pos])
                window["-letra"+str(pos)+"-"].update("")
                fichas.set_letra("",pos)
                fichas.usar(pos)
        else:
            if (not tablero.get_confirmadas()[x][y]):
                if (tablero.get_letra(x,y)!=""):
                    devolver_letra(window,tablero,fichas,x,y)
                    window[event].update("")

def confirmar(window,tablero,puntos,turnoIA=False):
    nuevos_puntos=tablero.confirmar_letras()
    puntos=puntos+nuevos_puntos
    if turnoIA:
        window["-puntosIA-"].update(puntos)
    else:
        window["-puntos-"].update(puntos)
    return puntos

def juego(cargar=False):
    if cargar:
        archivo= open("guardado.txt","r")
        config = json.load(archivo)
        jugador = config["jugador"]
        ventana_bienvenida.ventana(jugador) 
        puntos=config["puntos"]
        puntosIA=config["puntosIA"]
    else:
        archivo= open("config.txt","r")
        config = json.load(archivo)
        jugador = ventana_bienvenida.ventana()
        puntos=0
        puntosIA=0

    tiempo_total= int(config["tiempo_total"]) * 60
    tiempo_turno= int(config["tiempo_turno"]) * 60
    tiempos=[tiempo_total,tiempo_turno]

    dificultad=config["dificultad"]
    if dificultad == "Dificil":
        opciones=["Adjetivos", "Verbos"]
        dificultad = dificultad+random.choice(opciones)

    tablero = Tablero.Tablero(dificultad)

    layout = crear_layout(tablero, tiempos, jugador)    

    window = sg.Window('ScrabbleAR',resizable= True,).Layout(layout).Finalize()

    iniciado=False
    pos_letra= -1

    while True:                    
        event, values = window.Read(timeout=250)
        print(event, values)
        if event in (None,'Exit'):
            break
        elif event == "INICIAR":
            if not iniciado:
                iniciado, fichas_jugador, bolsa, Inteligencia = iniciar(iniciado, tiempos, window, config, tiempo_turno, tablero)
        elif event == sg.TIMEOUT_KEY:
            window["-TURNO-"].update(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}")
            window["-DURACION-"].update(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}")
        elif event in ("-letra0-","-letra1-","-letra2-","-letra3-","-letra4-","-letra5-","-letra6-"):
            if iniciado:
            	pos_letra = clickear_ficha(event, fichas_jugador, window)
        elif event == "CAMBIAR":
            pass
        elif event == "Posponer":
            pass
        elif event == "Terminar":
            pass
        elif event in ("-letraIA0-","-letraIA1-","-letraIA2-","-letraIA3-","-letraIA4-","-letraIA5-","-letraIA6-"):
            pass
        elif event == "Evaluar Palabra":
            if iniciado:
                palabra = tablero.buscar_palabra()
                ok = evaluar(palabra, dificultad)
                if ok:
                    puntos=confirmar(window,tablero,puntos)
                    pasar(tablero,fichas_jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
                    Inteligencia.turno()
                    pasar(tablero,Inteligencia.get_fichas(),tiempos,tiempo_turno,Inteligencia,bolsa,window,True)
                else:
                    devolver_fichas(window,tablero,fichas_jugador)
        elif event == "Pasar":
            if iniciado and not Inteligencia.get_mi_turno():
                pasar(tablero,fichas_jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
                Inteligencia.turno()
                pasar(tablero,Inteligencia.get_fichas(),tiempos,tiempo_turno,Inteligencia,bolsa,window,True)
        else:
        	if iniciado:
        		colocar_letra(event,fichas_jugador,tablero,window,pos_letra)

    window.close()


color_button = ('white','OrangeRed3')

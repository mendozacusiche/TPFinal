import PySimpleGUI as sg
from string import ascii_uppercase as up
import random, sys, time, json, threading, ventana_bienvenida
from Tablero_juego import *
from pattern.es import parse, conjugate, INFINITIVE

def evaluar(palabra, dificultad):
    ok=False
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

def pasar():
    pass

def segundo(t):
    while (t[0]>0):
        time.sleep(1)
        t[0]-=1
        t[1]-=1
        if(t[1]== 0):
            pasar()
    terminar()

def iniciar(iniciado, t):
    if not iniciado:
        timers= threading.Thread(target= segundo, args=(t,))
        if __name__ == 'jugar':
            timers.start()
    return True  

def crear_layout(tablero, tiempos, jugador):


    #tema del la ventana
    sg.theme('DarkTeal8')
    letrasRandom = lambda : [random.choice(up) for i in range(7)]
    a=letrasRandom()

    # tablero del ScrabbleAR
    color_button = ('white','OrangeRed3')
    #instanciamos el tablero del juego

    columna_1 = tablero.columna(sg)
    Tiempo_juego= [
                    [sg.Text(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}",size=(10, 2), font=('Helvetica', 20), justification='center', key='-TURNO-')],
                  ]

    T_turno = [
                [sg.Text(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}",size=(10, 2), font=('Helvetica', 20), justification='center', key='-DURACION-')],
              ]

    columna_2 = [
                  [sg.Frame('DURACION DEL JUEGO',Tiempo_juego, pad=(10,10), relief= 'solid'), sg.Frame('DURACION DEL TURNO',T_turno, pad= (10, 10), relief= 'solid')],
                  [sg.Image(filename='imagenes/playerlogo.png', pad=(5, 0)), sg.Text(jugador)],
                  [sg.Text('PUNTAJE'), sg.Text('Caja de Pts') ],
                  [sg.Image(filename='imagenes/computerlogo.png', pad=(5, 0)), sg.Text('PC')],
                  [sg.Text('PUNTAJE'), sg.Text('Caja de pts')],
                  [sg.Text('CANTIDAD DE FICHAS'), sg.Text('cant fichas en la bolsa')],
                  [sg.Button('INICIAR')],
                  [sg.Button('PASAR')],
                  [sg.Button('CAMBIAR PALABRA')],
                  [sg.Text('ORIENTACIÓN DE LA PALABRA')],
                  [sg.Button('▲', pad=(102, 10))],
                  [sg.Text(' '*10), sg.Button('◀', pad=(5, 0)), sg.Button('■', pad=(5, 0)), sg.Button('▶', pad=(5, 0))],
                  [sg.Button('▼',pad=(102, 10))],
                ]
    #suken, solid, ridge, raised

    layout = [  [sg.Text(' '*43), sg.Text('FICHAS COMPUTADORA')],
                [sg.Column(columna_1, background_color= 'grey40'), sg.Frame('CONFIGURACION', columna_2, pad=(20, 50), relief= 'solid')],
                [sg.Text(' '*43), sg.Text('FICHAS JUGADOR')],
                [sg.Button("Evaluar Palabra"),sg.Button('Exit'), sg.Button('Guardar Partida',  pad=(230, 0))]
             ]
    return layout

def juego(cargar=False):


    if cargar:
        archivo= open("guardado.txt","r")
    else:
        archivo= open("config.txt","r")
        jugador = ventana_bienvenida.ventana()
    config = json.load(archivo)
    if cargar:
        
    tiempo_total= int(config["tiempo_total"]) * 60
    tiempo_turno= int(config["tiempo_turno"]) * 60
    tiempos=[tiempo_total,tiempo_turno]

    dificultad=config["dificultad"]
    if dificultad == "Dificil":
        opciones=["Adjetivos", "Verbos"]
        dificultad = dificultad+random.choice(opciones)

    tablero = Tablero("dificil", 'SkyBlue3')

    tam_celda =25

    layout = crear_layout(tablero, tiempos, jugador)    

    window = sg.Window('ScrabbleAR',resizable= True,).Layout(layout).Finalize()
    g = window.FindElement('_GRAPH_')

    #metodos del tablero 
    tablero.mostrar_tablero(g)
    tablero.diseño_tablero(g) 
    tablero.Crear_Matriz()
    matriz = tablero.get_matriz()
    text_box = tablero.get_text_box()
    selected = tablero.get_selected()


    Check_box = lambda x,y : g.TKCanvas.itemconfig(matriz[box_y][box_x], fill="#CFF5E3")
    Uncheck_box = lambda x,y: g.TKCanvas.itemconfig(matriz[box_y][box_x], fill="white")
    despintar = lambda x: g.TKCanvas.itemconfig(x, fill="white")

    Check_button = lambda x: window.FindElement(x).Update(button_color=('white','blue'))
    Uncheck_button = lambda x: window.FindElement(x).Update(button_color=('white','green'))
    current_Check_button = ''

    word=''

    button_selected = False
    current_button_selected = ''
    Tiempo, duracion = True, 0
    Turno, turn_cont = True, 0
    iniciado=False

    while True:                    
        event, values = window.Read(timeout=300)
        print(values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '_GRAPH_':
            if iniciado:
                if values['_GRAPH_'] == (None,None):
                    continue
                mouse = values["_GRAPH_"]
                box_x = mouse[0]//tam_celda
                box_y = mouse[1]//tam_celda
                if mouse == (None, None) or box_x > 15 or box_y > 15:
                    continue
                if button_selected:
                    current_Check_button  = box_x, box_y
                    Check_box(box_x, box_y)
                    selected[box_x][box_y] = True
                    
                    if(text_box[box_x][box_y]== ""):
                        text_box[box_x][box_y] = g.DrawText(current_button_selected, (box_x * tam_celda + 18, box_y * tam_celda + 17),font='Courier 12')
                        word+=current_button_selected
                    else:
                        # aca iria la actualizacion del cuadrado pero no me sale
                        print(text_box[box_x][box_y])
                        g.TKCanvas.itemconfig(text_box[box_y][box_x],text="")
                        print((g.TKCanvas.itemconfigure(text_box[box_y][box_x])))
        elif event == "INICIAR":
            iniciado= iniciar(iniciado, tiempos)
        elif event == sg.TIMEOUT_KEY:
            window["-TURNO-"].update(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}")
            window["-DURACION-"].update(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}")
        else:
            if button_selected:
                if event == current_button_selected:
                    Uncheck_button(event)
                    button_selected = False
                    current_button_selected = ''
            else:
                Check_button(event)
                button_selected = True
                current_button_selected = event

    window.close()

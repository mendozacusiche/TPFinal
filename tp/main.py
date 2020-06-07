import PySimpleGUI as sg
from string import ascii_uppercase as up
from random import choice
import random
from Tablero_juego import*
#tema del la ventana
sg.theme('DarkTeal8')
letrasRandom = lambda : [choice(up) for i in range(7)]
a=letrasRandom()

# tablero del ScrabbleAR
tam_celda =25
color_button = ('white','OrangeRed3')
#instanciamos el tablero del juego
tablero = Tablero("Medio", "blue", 15)

columna_1 = tablero.columna(sg, a)
Tiempo_juego= [
                [sg.Text(size=(10, 2), font=('Helvetica', 20), justification='center', key='-TURNO-')],
              ]

T_turno = [
            [sg.Text(size=(10, 2), font=('Helvetica', 20), justification='center', key='-DURACION-')],
          ]

columna_2 = [
              [sg.Frame('DURACION DEL JUEGO',Tiempo_juego, pad=(10,10), relief= 'solid'), sg.Frame('DURACION DEL TURNO',T_turno, pad= (10, 10), relief= 'solid')],
              [sg.Image(filename='imagenes/playerlogo.png', pad=(5, 0)), sg.Text('JUGADOR'), sg.Text('Nombre')],
              [sg.Text('PUNTAJE'), sg.Text('Caja de Pts') ],
              [sg.Image(filename='imagenes/computerlogo.png', pad=(5, 0)), sg.Text('PC')],
              [sg.Text('PUNTAJE'), sg.Text('Caja de pts')],
              [sg.Button('CONFIGURACION')],
              [sg.Button('PASAR')],
              [sg.Button('CAMBIAR PALABRA')],
              [sg.Text('ORIENTACIÓN DE LA PALABRA')],
              [sg.Button('▲', pad=(102, 10))],
              [sg.Text(' '*10), sg.Button('◀', pad=(5, 0)), sg.Button('■', pad=(5, 0)), sg.Button('▶', pad=(5, 0))],
              [sg.Button('▼',pad=(102, 10))],
            ]
#suken, solid, ridge, raised


layout = [ [sg.Text(' '*43), sg.Text('FICHAS COMPUTADORA')],
           [sg.Column(columna_1, background_color= 'grey40'), sg.Frame('CONFIGURACION', columna_2, pad=(20, 50), relief= 'solid')],
           [sg.Text(' '*43), sg.Text('FICHAS JUGADOR')],
           [sg.Button("Evaluar Palabra"),sg.Button('Exit'), sg.Button('Guardar Partida',  pad=(230, 0))]
         ]

window = sg.Window('ScrabbleAR',resizable= True,) .Layout(layout) .Finalize()
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

while True:                    
    event, values = window.Read()
    
    while True:
     # Event Loop
        event, values = window.read(timeout=10) # Please try and use as high of a timeout value as you can
        if Tiempo:
            window['-DURACION-'].update('{:02d}:{:02d}.{:02d}'.format((duracion // 100) // 60, (duracion // 100) % 60, duracion % 100))
            duracion += 1
        if Turno:
            window['-TURNO-'].update('{:02d}:{:02d}.{:02d}'.format((turn_cont // 100) // 60, (turn_cont // 100) % 60, turn_cont % 100))
            turn_cont +=1
        
        if duracion == 3000:
            break

        #if turn_cont == 120:
        #    turn_cont = 0
       
    print(values)
    if event is None or 'tipo' == 'Exit':
        break
    if event == '_GRAPH_':
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
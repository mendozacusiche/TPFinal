import PySimpleGUI as sg
import sys
from tkinter import *

if __name__ == 'codigos.Layout':
    from codigos import records,Tablero
    
def definir_descripcion(dif,opcion=None):
    if dif=="Facil":
        descr= "Nivel Fácil. Palabras permitidas: sustantivos, adjetivos y verbos." 
        
    elif dif=="Medio":
        descr="Nivel Medio. Palabras permitidas: adjetivos y verbos. "
    else:
        descr="Nivel Difícil. Palabras permitidas: "+opcion
    return descr

def definir_especiales(dif):
    if dif=='Facil':
        lay=[
            [sg.Button(button_color=(None, 'red'),size=(2,1),disabled=True),sg.Text("Duplica el valor de la letra")],
            [sg.Button(button_color=(None, 'blue'),size=(2,1),disabled=True),sg.Text("Triplica el valor de la letra")],
            [sg.Button(button_color=(None, 'green'),size=(2,1),disabled=True),sg.Text("Duplica el valor de la palabra")],
            [sg.Button(button_color=(None, 'yellow'),size=(2,1),disabled=True),sg.Text("Triplica el valor de la palabra")],
            [sg.Button(button_color=(None, '#ff8c00'),size=(2,1),disabled=True),sg.Text("Resta 2 al valor de la palabra")],
            [sg.Button(button_color=(None, '#00b7ff'),size=(2,1),disabled=True),sg.Text("Resta 3 al valor de la palabra")]
        ]
    elif dif=='Medio':
        lay=[
            [sg.Button(button_color=(None,'IndianRed1'),size=(2,1),disabled=True),sg.Text("Duplica el valor de la letra")],
            [sg.Button(button_color=(None,'orange3'),size=(2,1),disabled=True),sg.Text("Resta 2 al valor de la palabra")],
            [sg.Button(button_color=(None,'green'),size=(2,1),disabled=True),sg.Text("Resta 3 al valor de la palabra")]
        ]
    else:
        lay=[
            [sg.Button(button_color=(None,'#007eb0'),size=(2,1),disabled=True),sg.Text("Duplica el valor de la letra")],
            [sg.Button(button_color=(None,'#fc2a00'),size=(2,1),disabled=True),sg.Text("Triplica el valor de la letra")],
            [sg.Button(button_color=(None,'#4fb304'),size=(2,1),disabled=True),sg.Text("Resta 2 al valor de la palabra")],
            [sg.Button(button_color=(None,'#f09605'),size=(2,1),disabled=True),sg.Text("Resta 3 al valor de la palabra")]
        ]
    return lay

def crear_botones(tablero, dificultad):
    if sys.platform == "win32":
        if (dificultad == "Medio" or dificultad == "Facil"):
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(2,0), pad=(0, 0),font=('Current',9,'bold'), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
        else:
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(4,2), pad=(0, 0),font=('Current',9,'bold'), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
    else:
        if (dificultad == "Medio" or dificultad == "Facil"):
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(1,1), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
        else:
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(2,2), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]

def crear_layout(tablero, tiempos, jugador, dificultad,cambios,opcion=None,cargar=False):
    '''Creación de la ventana de juego'''
    descr=definir_descripcion(dificultad,opcion)
    lay=definir_especiales(dificultad)
    
    
        
    layout_fichasIA=[[sg.Button("#",font=("Current",9,'bold'),size=(2,1), pad=(20, 0), button_color=color_button, key=("-letraIA"+str(i)+"-")) for i in range(7)]]
    layout_fichas_jugador=[[sg.Button(" ",font=("Current",9,'bold'),size=(2,1), pad=(20, 0), button_color=color_button, key=("-letra"+str(i)+"-"), disabled=True) for i in range(7)]]
    
    columna_0 = [
                    [sg.Column(lay)],
                    [sg.Text('Mensajes del sistema: ',font=("Current",9,'bold')),sg.Text('',key='-turno-',font=("Current",10), size=(10, 0))], 
                    [sg.Text('Palabras ingresadas:',font=("Current",9,'bold'))],
                    [sg.Text('TURNO',font=("Current",9,'bold'),justification='lleft'),sg.Text('PALABRA',font=("Current",9,'bold'),justification='center'),sg.Text('PUNTOS',font=("Current",9,'bold'),justification='lright')],
                    [sg.Listbox( values={}, key='PALABRAS',size= (30,20), pad=(0,0), background_color="#b7c9e7",font=("Current",10))],
                    ]
    
    columna_1 = [
                [sg.Frame('FICHAS COMPUTADORA',layout_fichasIA)],
                [sg.Column(crear_botones(tablero, dificultad), background_color= 'grey40', justification='center')],
                [sg.Frame('FICHAS JUGADOR',layout_fichas_jugador)]
                ]

    Tiempo_juego=[       
                [sg.Text(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}",size=(10, 2), text_color='white',font=('Digital-7',20), justification='center', key='-TURNO-')],
                ]

    T_turno = [
                [sg.Text(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}",size=(10, 2), font=('Digital-7', 20), text_color='white',justification='center', key='-DURACION-')],
                ]

    fila_1 = [
                [sg.Text(descr,font=("Current",9,'bold'))],
                [sg.T(' '*4),sg.Button('INICIAR',key=("INICIAR"),font=("Current",10), size=(10, 0),pad=(0, 0)),sg.Button('POSPONER',key='Posponer',font=("Current",10),pad=(0, 0),size=(15, 0),disabled=True), sg.Button('TERMINAR',key='TERMINAR',font=("Current",10),size=(10, 0), pad=(0, 0),disabled=True)],
                [sg.Frame('DURACION DEL JUEGO',Tiempo_juego, pad=(10,10), relief= 'solid'), sg.Frame('DURACION DEL TURNO',T_turno, pad= (10, 10), relief= 'solid')],
                [sg.Image(filename='imagenes/playerlogo.png', pad=(5, 0)), sg.Text(jugador), sg.Image(filename='imagenes/greendot.png',visible=False, key="-dot-")],
                [sg.Text('PUNTAJE'), sg.Text('0000000',key=("-puntos-")) ],
                [sg.Image(filename='imagenes/computerlogo.png', pad=(5, 0)), sg.Text('PC'), sg.Image(filename='imagenes/greendot.png',visible=False, key="-dotIA-")],
                [sg.Text('PUNTAJE'), sg.Text('0000000',key=("-puntosIA-"))],
                [sg.Text('FICHAS EN BOLSA:'), sg.Text("000", key=("-CantFichas-"))],
                [sg.Button('Pasar',key='Pasar',font=("Current",10),size=(15, 0),disabled=True)],
                [sg.Button("Evaluar Palabra",key="Evaluar Palabra",font=("Current",10),size=(15, 0),disabled=True)], 
                [sg.Button('Cambiar letras',key='Cambiar letras',font=("Current",10),size=(15, 0),disabled=True),sg.Text('Cambios disponibles: '),sg.Text(cambios,key='-cambios-',visible=False)]
                ]

    
    if cargar:
        fila_1[1][1]=sg.Button('RETOMAR',key=("RETOMAR"),font=("Current",10), size=(10, 0),pad=(0, 0))

    columna_2=[
                [sg.Text(' '*80),sg.Button('Ayuda (?)',key='AYUDA',font=("Current",10,'bold'),size=(10, 0))],
                [sg.Text(' '*80),sg.Button('Ver puntajes',key='PUNTAJES',font=("Current",10,'bold'),size=(10, 0))],                 
                [sg.Frame('CONFIGURACION', fila_1, pad=(20, 50), relief= 'solid')],
                ]

    layout = [  
                [sg.Column(columna_0),sg.Column(columna_1, pad=(0,0)),sg.Column(columna_2, pad=(0,0))],
                ]

    return layout 
    
def mostrar_fichas(window,Inteligencia,jugador,config):
    '''Al finalizar la partida se muestran las fichas de la IA y se descuentan los puntos correspondientes a las letras de los atriles'''
    ptsIA=0
    for i in range(len(Inteligencia.get_fichas().get_letras())):
        if (not Inteligencia.get_fichas().get_usadas()[i]):
            window["-letraIA"+str(i)+"-"].update(Inteligencia.get_fichas().get_letra(i))
            ptsIA=ptsIA+config["puntaje_fichas"][Inteligencia.get_fichas().get_letra(i)]
        else:
            window["-letraIA"+str(i)+"-"].update("")
    Inteligencia.set_puntos(Inteligencia.get_puntos()-ptsIA)
    window["-puntosIA-"].update(Inteligencia.get_puntos())
    pts=0
    for i in range(len(jugador.get_fichas().get_letras())):
        if (not jugador.get_fichas().get_usadas()[i]):
            pts=pts+config["puntaje_fichas"][jugador.get_fichas().get_letra(i)]
    jugador.set_puntos(jugador.get_puntos()-pts)
    window["-puntos-"].update(jugador.get_puntos())
        
def terminar(window,Inteligencia,tiempos,jugador,dif,fecha,config):
    '''Se utiliza cuando el jugador oprime el botón terminar'''
    layout1=[
            [sg.Text("¿Seguro que quiere terminar el juego?")],
            [sg.Button('Salir',key='SALIR'), sg.Button('Cancelar',key='CANCELAR')] 
            ]
    wind= sg.Window('',layout1)
    event,values=wind.Read()
    wind.close()
    if event== 'SALIR':
        tiempos[2] = False
        mostrar_fichas(window,Inteligencia,jugador,config)
        layout2=[
            [sg.Text('FIN DEL JUEGO')],
            [sg.Text('Puntos jugador: '),sg.Text(jugador.get_puntos())],
            [sg.Text('Puntos computadora: '),sg.Text(Inteligencia.get_puntos())],
            [sg.Ok()]
            ]
        wind2=sg.Window("",layout2)
        event,values=wind2.Read()
        wind2.close()
        if dif in ("Facil","Medio"):
            records.actualizar(jugador.get_nombre(),jugador.get_puntos(),dif,fecha)
        else:
            records.actualizar(jugador.get_nombre(),jugador.get_puntos(),"Dificil",fecha)
        return True
    elif event=='CANCELAR':
        return False
        
def terminar_por_otros(window,Inteligencia,jugador,dif,tiempos,fecha,config):
    '''Se utiliza cuando la partida termina por el tiempo o porque no hay más 
    fichas en la bolsa.'''
    tiempos[2] = False
    mostrar_fichas(window,Inteligencia,jugador,config)
    layout1=[
                [sg.Text('FIN DEL JUEGO')],
                [sg.Text('Puntos jugador: '),sg.Text(jugador.get_puntos())],
                [sg.Text('Puntos computadora: '),sg.Text(Inteligencia.get_puntos())],
                [sg.Button('OK')]
                ]
    wind= sg.Window('',layout1)
    event,values=wind.Read()
    wind.close()
    dic={jugador.get_nombre():jugador.get_puntos()}
    records.actualizar(jugador.get_nombre(),jugador.get_puntos(),dif,fecha)
    
def diseño_facil(window,tablero):
    '''Se ubican las casillas especiales en el tablero del nivel fácil'''
    for i in range(len(tablero.get_especiales()["uno"])):
        window[tablero.get_especiales()["uno"][i]].update(button_color=(None, 'red'))
    for j in range(len(tablero.get_especiales()["dos"])):
        window[tablero.get_especiales()["dos"][j]].update(button_color=(None, 'blue'))
    for y in range(len(tablero.get_especiales()["tres"])):
        window[tablero.get_especiales()["tres"][y]].update(button_color=(None, 'yellow'))
    for z in range(len(tablero.get_especiales()["cuatro"])):
        window[tablero.get_especiales()["cuatro"][z]].update(button_color=(None, 'green'))
    for w in range(len(tablero.get_especiales()["cinco"])):
        window[tablero.get_especiales()["cinco"][w]].update(button_color=(None, '#00b7ff'))
    for x in range(len(tablero.get_especiales()["seis"])):
        window[tablero.get_especiales()["seis"][x]].update(button_color=(None, '#ff8c00'))
    
def diseño_medio(window,tablero):
    '''Se ubican las casillas especiales en el tablero del nivel medio'''
    for i in range(len(tablero.get_especiales()["uno"])):
         window[tablero.get_especiales()["uno"][i]].update(button_color=(None, 'green'))
    for j in range(len(tablero.get_especiales()["dos"])):
         window[tablero.get_especiales()["dos"][j]].update(button_color=(None, 'IndianRed1'))
    for x in range(len(tablero.get_especiales()["tres"])):
         window[tablero.get_especiales()["tres"][x]].update(button_color=(None, 'orange3'))

def diseño_dificil(window,tablero):
    '''Se ubican las casillas especiales en el tablero del nivel dificil'''
    for i in range(len(tablero.get_especiales()["uno"])):
        window[tablero.get_especiales()["uno"][i]].update(button_color=(None, '#fc2a00'))
    for j in range(len(tablero.get_especiales()["dos"])):
        window[tablero.get_especiales()["dos"][j]].update(button_color=(None, '#f09605'))
    for x in range(len(tablero.get_especiales()["tres"])):
        window[tablero.get_especiales()["tres"][x]].update(button_color=(None,'#4fb304'))
    for y in range(len(tablero.get_especiales()["cuatro"])):
        window[tablero.get_especiales()["cuatro"][y]].update(button_color=(None, '#007eb0'))

def cargar_tablero(window,tablero):
    '''Se utiliza para cargar la parte gráfica del tablero del juego guardado '''
    for i in range(tablero.get_tamanio()):
        for j in range(tablero.get_tamanio()):
            if (tablero.get_confirmadas()[i][j]):
                window["b_"+str(i)+"_"+str(j)].update(tablero.get_letras()[i][j])
                if(tablero.get_coloreadas()[i][j]=="IA"):
                    window["b_"+str(i)+"_"+str(j)].update(button_color=('white', '#6a354c'))
                else:
                    window["b_"+str(i)+"_"+str(j)].update(button_color=('white', '#498269'))

        
color_button = ('white','OrangeRed3')
if __name__ == '__main__':
    sg.theme('BlueMono')
    sg.popup('Por favor ejecute ScrabbleAR.py',title='')

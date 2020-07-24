import PySimpleGUI as sg
import sys,records,Tablero


def definir_descripcion(dif,opcion=None):
	if dif=="Facil":
		descr= "Palabras permitidas: sustantivos, adjetivos y verbos." 
		
	elif dif=="Medio":
		descr="Palabras permitidas: adjetivos y verbos. "
	else:
		descr="Palabras permitidas: "+opcion
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
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(2,0), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
        else:
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(4,2), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
    else:
        if (dificultad == "Medio" or dificultad == "Facil"):
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(0,0), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
        else:
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(2,2), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]



def crear_layout(tablero, tiempos, jugador, dificultad,cambios,opcion=None):

	descr=definir_descripcion(dificultad,opcion)
	lay=definir_especiales(dificultad)
		
	layout_fichasIA=[[sg.Button("#",font=("Current",9),size=(0,0), pad=(20, 0), button_color=color_button, key=("-letraIA"+str(i)+"-")) for i in range(7)]]#,sg.Text('',key='-PC-')]]
	layout_fichas_jugador=[[sg.Button(" ",font=("Current",9),size=(2,1), pad=(20, 0), button_color=color_button, key=("-letra"+str(i)+"-"), disabled=True) for i in range(7)]]#,sg.Text('',key='-Jug-')]]
   
	columna_0 = [
					[sg.Column(lay)],#no se si está bien esto
					[sg.Text('Mensajes del sistema: ')], 
					[sg.Text('',key='-turno-',font=("Current",10), size=(10, 0),pad=(0, 0))]
					]
    
	columna_1 =	[
				[sg.Frame('FICHAS COMPUTADORA',layout_fichasIA)],
				[sg.Column(crear_botones(tablero, dificultad), background_color= 'grey40', justification='center')],
				[sg.Frame('FICHAS JUGADOR',layout_fichas_jugador)]
				]

	Tiempo_juego=[       
				[sg.Text(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}",size=(10, 2), text_color='white',font=('Digital-7',20), justification='center', key='-TURNO-')],
				]

	T_turno = [                                                                  #'Helvetica'
				[sg.Text(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}",size=(10, 2), font=('Digital-7', 20), text_color='white',justification='center', key='-DURACION-')],
				]

	columna_2 = [
				[sg.Text(descr)],
				[sg.T(' '*4),sg.Button('INICIAR',key=("INICIAR"),font=("Current",10), size=(10, 0),pad=(0, 0)), sg.Button('TERMINAR',key='TERMINAR',font=("Current",10),size=(10, 0), pad=(0, 0),disabled=True),sg.Button('EXIT',font=("Current", 10), size=(10, 0), pad=(0, 0))],
				[sg.Frame('DURACION DEL JUEGO',Tiempo_juego, pad=(10,10), relief= 'solid'), sg.Frame('DURACION DEL TURNO',T_turno, pad= (10, 10), relief= 'solid')],
				[sg.Image(filename='imagenes/playerlogo.png', pad=(5, 0)), sg.Text(jugador), sg.Image(filename='imagenes/greendot.png',visible=False, key="-dot-")],
				[sg.Text('PUNTAJE'), sg.Text('0000000',key=("-puntos-")) ],
				[sg.Image(filename='imagenes/computerlogo.png', pad=(5, 0)), sg.Text('PC'), sg.Image(filename='imagenes/greendot.png',visible=False, key="-dotIA-")],
				[sg.Text('PUNTAJE'), sg.Text('0000000',key=("-puntosIA-"))],
				[sg.Text('FICHAS EN BOLSA:'), sg.Text("000", key=("-CantFichas-"))],
				[sg.Button('Pasar',key='Pasar',font=("Current",10),size=(15, 0),disabled=True)],
				[sg.Button("Evaluar Palabra",key="Evaluar Palabra",font=("Current",10),size=(15, 0),disabled=True)], 
				[sg.Button('Posponer',key='Posponer',font=("Current",10), size=(15, 0),disabled=True)],
				[sg.Button('Cambiar letras',key='Cambiar letras',font=("Current",10),size=(15, 0),disabled=True),sg.Text('Cambios disponibles: '),sg.Text(cambios,key='-cambios-',visible=False)]
				]
    
	layout = [  
				[sg.Column(columna_0),sg.Column(columna_1, pad=(0,0)), sg.Frame('CONFIGURACION', columna_2, pad=(20, 50), relief= 'solid')],
				]
	return layout   


def terminar(Inteligencia,tiempos,jugador,dif): #CONCURRENCIA
	tiempos[2] = False
	
	layout0=[
			[sg.Text('¿Está seguro que desea salir?')],
			[sg.Button('SI'),sg.Button('NO')]
			]
    
	win=sg.Window('',layout0)
	ev,val=win.Read()
    
	if ev=='SI':
		layout1=[
				[sg.Text('FIN DEL JUEGO')],
				[sg.Text('Puntos jugador: '),sg.Text(jugador.get_puntos())],
				[sg.Text('Puntos computadora: '),sg.Text(Inteligencia.get_puntos())],
				[sg.Button('Guardar partida', key='GUARDAR'),sg.Button('Salir sin guardar',key='SALIR')] #si apreta sin guardar se debe verificar si corresponde guardar o no el puntaje
				]
		wind= sg.Window('TERMINAR',layout1)
		event,values=wind.Read()
		if event== 'SALIR':
			#dic={jugador:puntos[0]}
			records.actualizar(jugador.get_nombre(),jugador.get_puntos(),dif)
			wind.close()
			win.close()
		return True
	else:
		win.close()
		return False
		
def terminar_por_otros(Inteligencia,jugador,dif):
	layout1=[
				[sg.Text('FIN DEL JUEGO')],
				[sg.Text('Puntos jugador: '),sg.Text(jugador.get_puntos())],
				[sg.Text('Puntos computadora: '),sg.Text(Inteligencia.get_puntos())],
				[sg.Button('OK')]
				]
	wind= sg.Window('',layout1)
	event,values=wind.Read()
	print('FIN DEL JUEGO')
	dic={jugador.get_nombre():jugador.get_puntos()}
	records.actualizar(jugador.get_nombre(),jugador.get_puntos(),dif)
	if event=='OK':
		wind.close()

def diseño_facil(window,tablero):
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
    for i in range(len(tablero.get_especiales()["uno"])):
         window[tablero.get_especiales()["uno"][i]].update(button_color=(None, 'green'))
    for j in range(len(tablero.get_especiales()["dos"])):
         window[tablero.get_especiales()["dos"][j]].update(button_color=(None, 'IndianRed1'))
    for x in range(len(tablero.get_especiales()["tres"])):
         window[tablero.get_especiales()["tres"][x]].update(button_color=(None, 'orange3'))

def diseño_dificil(window,tablero):
    for i in range(len(tablero.get_especiales()["uno"])):
        window[tablero.get_especiales()["uno"][i]].update(button_color=(None, '#fc2a00'))
    for j in range(len(tablero.get_especiales()["dos"])):
        window[tablero.get_especiales()["dos"][j]].update(button_color=(None, '#f09605'))
    for x in range(len(tablero.get_especiales()["tres"])):
        window[tablero.get_especiales()["tres"][x]].update(button_color=(None,'#4fb304'))
    for y in range(len(tablero.get_especiales()["cuatro"])):
        window[tablero.get_especiales()["cuatro"][y]].update(button_color=(None, '#007eb0'))
		
color_button = ('white','OrangeRed3')

import PySimpleGUI as sg
from string import ascii_uppercase as up
import random, sys, time, json, threading, ventana_bienvenida, Fichas, Tablero, IA
from pattern.es import *   #parse, conjugate, INFINITIVE

def evaluar(palabra, dificultad):
    ok=False
    analisis = parse(palabra).split('/')
    if palabra != "No es palabra":
        if (dificultad == "Facil") and (analisis[1] in ("JJ","NN","VB")):
            ok=True
        elif (dificultad == "Medio") and (analisis[1] in ("JJ","VB")):
            ok=True
        elif (dificultad == "DificilVerbos") and (analisis[1] in ("VB")):
            ok=True
        elif (dificultad == "DificilAdjetivos") and (analisis[1] in ("JJ")):
            ok=True
    else:
        sg.popup("La Palapra Ingresada No es Valida")
    return ok

def terminar(puntos,tiempos):
    tiempos[2] = False
    layout1=[
            [sg.Text('FIN DEL JUEGO')],
            [sg.Text('Puntos jugador: '),sg.Text(puntos[0])],
            [sg.Text('Puntos computadora: '),sg.Text(puntos[1])]
            ]
    wind= sg.Window('TERMINAR',layout1)
    event,values=wind.Read()

def recargar_fichas(fichas, bolsa, window, turnoIA=False):
    usadas=fichas.get_usadas()
    for i in range(7):
        if usadas[i]:
            l=sacar_letra_bolsa(bolsa)
            if not turnoIA:
                window["-letra"+str(i)+"-"].update(l)
            fichas.set_letra(l,i)
            usadas[i]=False

def pasar(tablero,fichas,tiempos,tiempo_turno,Intel,bolsa,window,turnoIA=False,timer=False):
    if not timer:
        window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
    devolver_fichas(window,tablero,fichas)
    recargar_fichas(fichas,bolsa,window,turnoIA)
    tiempos[1]=tiempo_turno
    Intel.set_mi_turno(not turnoIA)

def segundo(tablero,fichas_jugador, Intel, tiempo_turno, bolsa, window, t, puntos):
    while (t[0]>0 and t[2]):
        time.sleep(1)
        t[0]-=1
        t[1]-=1
        if(t[1]== 0):
            if Intel.get_mi_turno():
                pasar(tablero,Intel.get_fichas(),t,tiempo_turno,Intel,bolsa,window,True,True)
            else:
                pasar(tablero,fichas_jugador,t,tiempo_turno,Intel,bolsa,window,timer=True)
                threading.Thread(target= Intel.turno, args=(bolsa,window,tablero,puntos)).start()
    if (t[2]):
        terminar(puntos,t)

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

def cambiar_fichas(window,fichas,bolsa,tablero,turnoIA=False):
    if(not turnoIA):
        devolver_fichas(window,tablero,fichas)
    for i in range(7):
        bolsa[fichas.get_letras()[i]]+=1
        fichas.set_letra(sacar_letra_bolsa(bolsa),i)
        if(not turnoIA):
            window["-letra"+str(i)+"-"].update(fichas.get_letra(i))

def iniciar(iniciado, t, window, config, tiempo_turno, tablero, dificultad, puntos):
    bolsa=config["cant_fichas"]
    Inteligencia = IA.IA (bolsa,dificultad,puntos[1])
    nuevas=[]
    for i in range(7):
        l=sacar_letra_bolsa(bolsa)
        nuevas.append(l)
        window["-letra"+str(i)+"-"].update(l)
    fichas_jugador= Fichas.Fichas(nuevas)
    timers= threading.Thread(target= segundo, args=(tablero,fichas_jugador,Inteligencia,tiempo_turno,bolsa,window,t,puntos))
    if __name__ == 'jugar':
        timers.start()
    window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
    return True, fichas_jugador, bolsa, Inteligencia

#def crear_botones(n, tablero):
def crear_botones(tablero, dificultad):
    if sys.platform == "win32":
        if (dificultad == "Medio" or dificultad == "Facil"):
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(2,0), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
        else:
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(4,2), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
    else:
        if (dificultad == "Medio" or dificultad == "Facil"):
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(1,1), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]
        else:
            return [[sg.Button(" ", button_color=(None, '#a6a3a2'), size=(2,2), pad=(0, 0), key=("b_"+str(x)+"_"+str(y))) for x in range(tablero.get_tamanio())] for y in range(tablero.get_tamanio())]

def diseño_facil(window):
    # Agrega todos los cuadrados premium que influyen en la puntuación de la palabra.
    uno= (('b_0_6'), ('b_1_7'), ('b_2_8'), ('b_3_9'), ('b_4_10'), ('b_5_11'), ('b_6_12'), ('b_7_13'),('b_8_14'), ('b_9_15'), ('b_10_16'),('b_11_17'), ('b_12_18'), ('b_13_19'),('b_14_20'),('b_15_21'),('b_16_22'))
    dos= (('b_6_0'), ('b_7_1'), ('b_8_2'), ('b_9_3'), ('b_10_4'),('b_11_5'), ('b_12_6'), ('b_13_7'), ('b_14_8'), ('b_15_9'),('b_16_10'), ('b_17_11'), ('b_18_12'),('b_19_13'), ('b_20_14'), ('b_21_15'),('b_22_16'))
    tres= (('b_0_17'), ('b_1_16'), ('b_2_15'), ('b_3_14'), ('b_4_13'), ('b_5_12'), ('b_6_11'), ('b_7_10'), ('b_8_9'), ('b_9_8'), ('b_10_7'),('b_11_6'), ('b_12_5'),('b_13_4'), ('b_14_3'), ('b_15_2'),('b_16_1'), ('b_17_0'))
    cuatro = (('b_6_22'), ('b_7_21'), ('b_8_20'), ('b_9_19'), ('b_10_18'), ('b_11_17'), ('b_12_16'),('b_13_15'), ('b_14_14'), ('b_15_13'), ('b_16_12'), ('b_17_11'), ('b_18_10'), ('b_19_9'), ('b_20_8'), ('b_21_7'), ('b_22_6'))
    cinco = (('b_1_5'), ('b_2_4'), ('b_3_3'), ('b_4_2'), ('b_5_1'), ('b_1_18'), ('b_2_19'),('b_3_20'), ('b_4_21'), ('b_5_22'), ('b_18_1'), ('b_19_2'), ('b_20_3'), ('b_21_4'), ('b_22_5'), ('b_17_22'), ('b_18_21'),('b_19_20'), ('b_20_19'),('b_21_18'), ('b_22_17'))
    seis = (('b_6_5'), ('b_17_5'), ('b_11_11'), ('b_6_17'),('b_17_17'),('b_0_0'), ('b_11_0'), ('b_22_0'),('b_0_11'), ('b_22_11'), ('b_0_22'),('b_11_22'),('b_22_22'))
    
    for i in range(len(uno)):
        window[uno[i]].update(button_color=(None, 'red'))
    for j in range(len(dos)):
        window[dos[j]].update(button_color=(None, 'blue'))
    for y in range(len(tres)):
        window[tres[y]].update(button_color=(None, 'yellow'))
    for z in range(len(cuatro)):
        window[cuatro[z]].update(button_color=(None, 'green'))
    for w in range(len(cinco)):
        window[cinco[w]].update(button_color=(None, '#00b7ff'))
    for x in range(len(seis)):
        window[seis[x]].update(button_color=(None, '#ff8c00'))
    

def diseño_medio(window):
    # Agrega todos los cuadrados premium que influyen en la puntuación de la palabra.
    uno =(('b_0_0'), ('b_0_9'), ('b_0_18'), ('b_9_0'), ('b_9_9'), ('b_9_18'), ('b_18_0'), ('b_18_9'), ('b_18_18'))
    dos =(('b_1_1'), ('b_2_2'), ('b_3_3'), ('b_4_4'), ('b_5_5'), ('b_6_6'), ('b_7_7'), ('b_8_8'), ('b_10_10'), ('b_11_11'), ('b_12_12'), ('b_13_13'), ('b_14_14'), ('b_15_15'), ('b_16_16'), ('b_17_17'),
          ('b_17_1'), ('b_16_2'), ('b_15_3'), ('b_14_4'), ('b_13_5'), ('b_12_6'), ('b_11_7'), ('b_10_8'), ('b_8_10'), ('b_7_11'), ('b_6_12'), ('b_5_13'), ('b_4_14'), ('b_3_15'), ('b_2_16'), ('b_1_17'))
    tres =(('b_4_9'),('b_9_4'),('b_14_9'),('b_9_14'))
    
    for i in range(len(uno)):
         window[uno[i]].update(button_color=(None, 'green'))
    for j in range(len(dos)):
         window[dos[j]].update(button_color=(None, 'IndianRed1'))
    for x in range(len(tres)):
         window[tres[x]].update(button_color=(None, 'orange3'))

def diseño_dificil(window):
    # Agrega todos los cuadrados premium que influyen en la puntuación de la palabra.
    uno= (('b_0_0'), ('b_7_0'), ('b_14_0'), ('b_0_7'), ('b_14_7'), ('b_0_14'), ('b_7_14'), ('b_14_14'))
    dos= (('b_1_1'),   ('b_2_2'), ('b_3_3'), ('b_4_4'), ('b_1_13'),('b_2_12'), ('b_3_11'), ('b_4_10'), ('b_13_1'), ('b_12_2'),('b_11_3'), ('b_10_4'), ('b_13_13'),('b_12_12'), ('b_11_11'), ('b_10_10'))
    tres= (('b_1_5'), ('b_1_9'), ('b_5_1'), ('b_5_5'), ('b_5_9'), ('b_5_13'), ('b_9_1'), ('b_9_5'), ('b_9_9'), ('b_9_13'), ('b_13_5'), ('b_13_9'), ('b_7_7'))
    cuatro = (('b_0_3'), ('b_0_11'), ('b_2_6'), ('b_2_8'), ('b_3_0'), ('b_3_7'), ('b_3_14'),('b_6_2'), ('b_6_6'), ('b_6_8'), ('b_6_12'), ('b_7_3'), ('b_7_11'), ('b_8_2'), ('b_8_6'), ('b_8_8'), ('b_8_12'), ('b_11_0'), ('b_11_7'), ('b_11_14'), ('b_12_6'), ('b_12_8'), ('b_14_3'), ('b_14_11'))

    for i in range(len(uno)):
        window[uno[i]].update(button_color=(None, '#fc2a00'))
    for j in range(len(dos)):
        window[dos[j]].update(button_color=(None, '#f09605'))
    for x in range(len(tres)):
        window[tres[x]].update(button_color=(None,'#4fb304'))
    for y in range(len(cuatro)):
        window[cuatro[y]].update(button_color=(None, '#007eb0'))
    

def cambiar_colores(window, dificultad):
    
    if(dificultad == "Facil"):
        diseño_facil(window)
    elif(dificultad == "Medio"):
        diseño_medio(window)
    else:
        diseño_dificil(window)

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
			[sg.Button(button_color=(None, 'red'),size=(2,1)),sg.Text("Duplica el valor de la letra")],
			[sg.Button(button_color=(None, 'blue'),size=(2,1)),sg.Text("Triplica el valor de la letra")],
			[sg.Button(button_color=(None, 'green'),size=(2,1)),sg.Text("Duplica el valor de la palabra")],
			[sg.Button(button_color=(None, 'yellow'),size=(2,1)),sg.Text("Triplica el valor de la palabra")],
			[sg.Button(button_color=(None, '#ff8c00'),size=(2,1)),sg.Text("Resta 2 al valor de la palabra")],
			[sg.Button(button_color=(None, '#00b7ff'),size=(2,1)),sg.Text("Resa 3 al valor de la palabra")]
		]
	elif dif=='Medio':
		lay=[
			[sg.Button(button_color=(None,'IndianRed1'),size=(2,1)),sg.Text("Duplica el valor de la letra")],
			[sg.Button(button_color=(None,'orange3'),size=(2,1)),sg.Text("Resta 2 al valor de la palabra")],
			[sg.Button(button_color=(None,'green'),size=(2,1)),sg.Text("Resta 3 al valor de la palabra")]
		]
	else:
		lay=[
			[sg.Button(button_color=(None,'#007eb0'),size=(2,1)),sg.Text("Duplica el valor de la letra")],
			[sg.Button(button_color=(None,'#fc2a00'),size=(2,1)),sg.Text("Triplica el valor de la letra")],
			[sg.Button(button_color=(None,'#4fb304'),size=(2,1)),sg.Text("Resta 2 al valor de la palabra")],
			[sg.Button(button_color=(None,'#f09605'),size=(2,1)),sg.Text("Resta 3 al valor de la palabra")]
		]
	return lay

def crear_layout(tablero, tiempos, jugador, dificultad,cambios,opcion=None):

	descr=definir_descripcion(dificultad,opcion)
	lay=definir_especiales(dificultad)
		
	layout_fichasIA=[[sg.Button("#",font=("Current",9),size=(0,0), pad=(20, 0), button_color=color_button, key=("-letraIA"+str(i)+"-")) for i in range(7)]]#,sg.Text('',key='-PC-')]]
	layout_fichas_jugador=[[sg.Button(" ",font=("Current",9),size=(2,1), pad=(20, 0), button_color=color_button, key=("-letra"+str(i)+"-")) for i in range(7)]]#,sg.Text('',key='-Jug-')]]
   
	columna_0 = [
					[sg.Column(lay)],#no se si está bien esto
					[sg.Text('Mensajes del sistema: ')], 
					[sg.Text('',key='-turno-',font=("Current",10), size=(10, 0),pad=(0, 0))]
					]
    
	columna_1 =	[
				[sg.Frame('FICHAS COMPUTADORA',layout_fichasIA)],
				#[sg.Column(crear_botones(i, tablero), pad=(0,0)) for i in range(tablero.get_tamanio())],
				[sg.Column(crear_botones(tablero, dificultad), background_color= 'grey40', justification='center', )],
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
				#[sg.Button('Terminar',font=("Current",9),size=(10, 0))],
				#[sg.Button('Exit',font=("Current", 9), size=(10, 0))]
				[sg.Button('Cambiar letras',key='Cambiar letras',font=("Current",10),size=(15, 0),disabled=True),sg.Text('Cambios disponibles: '),sg.Text(cambios,key='-cambios-',visible=False)]
				]

    
	layout = [  
				[sg.Column(columna_0),sg.Column(columna_1, pad=(0,0)), sg.Frame('CONFIGURACION', columna_2, pad=(20, 50), relief= 'solid')],
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
    if turnoIA:
        puntos[1]=puntos[1]+nuevos_puntos
        window["-puntosIA-"].update(puntos[1])
    else:
        puntos[0]=puntos[0]+nuevos_puntos
        window["-puntos-"].update(puntos[0])
def deshabilitar_habilitar_botones(window,b,cambios):
	for i in range(7):
		window["-letra"+str(i)+"-"].update(disabled=b)
	window["Evaluar Palabra"].update(disabled=b)
	window['Pasar'].update(disabled=b)
	if (cambios>0):
		window['Cambiar letras'].update(disabled=b)

def juego(cargar=False):
	if cargar:
		try:
			archivo= open("guardado.txt","r")
			config = json.load(archivo)
			jugador = config["jugador"]
			ventana_bienvenida.ventana(jugador)
			puntos=[config["puntos"],config["puntosIA"]] # puntos[0] son los del jugador, puntos[1] de la IA
			cambios=config["cambios"]
		except FileNotFoundError as ex:
			print('No se encontro el  archivo.......')
	else:
		try:
			archivo= open("config.txt","r")
			config = json.load(archivo)
		except FileNotFoundError as ex:
			print(ex)
			print('No se encontro el archivo')

		jugador = ventana_bienvenida.ventana()
		puntos=[0,0] # puntos[0] son los del jugador, puntos[1] de la IA
		cambios=3
        
	tiempo_total= int(config["tiempo_total"]) * 60
	tiempo_turno= int(config["tiempo_turno"]) * 60
	tiempos=[tiempo_total,tiempo_turno,True]

	dificultad=config["dificultad"]
	# if dificultad == "Dificil":
		# opciones=["Adjetivos", "Verbos"]
		# opcion=random.choice(opciones)

	tablero = Tablero.Tablero(dificultad)
	
	if dificultad == "Dificil":
		opciones=["Adjetivos", "Verbos"]
		opcion=random.choice(opciones)
		dificultad=dificultad+opcion
		layout = crear_layout(tablero, tiempos, jugador, dificultad,cambios,opcion)    
	else:
		layout = crear_layout(tablero, tiempos, jugador, dificultad,cambios)    

	window = sg.Window('ScrabbleAR',resizable= True,element_justification='center',).Layout(layout).Finalize()

	iniciado=False
	pos_letra= -1

    


	while True:                    
		event, values = window.Read(timeout=250)
		print(event, values)
		if event in (None,'EXIT'):
			tiempos[2]=False #se deberían guardar los puntajes acá?
			break
		elif event == "INICIAR":
			if not iniciado:
				window["INICIAR"].update(disabled=True)
				window['TERMINAR'].update(disabled=False)
				window['Pasar'].update(disabled=False)
				window["Evaluar Palabra"].update(disabled=False)
				window['Posponer'].update(disabled=False)
				window["Cambiar letras"].update(disabled=False)
				window['-cambios-'].update(visible=True)
				iniciado, fichas_jugador, bolsa, Inteligencia = iniciar(iniciado, tiempos, window, config, tiempo_turno, tablero, dificultad, puntos)
				jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,puntos))
				#actualiza el tablero con las casillas de primio  por nivel
				cambiar_colores(window,dificultad)
		elif event == sg.TIMEOUT_KEY:
			window["-TURNO-"].update(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}")
			window["-DURACION-"].update(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}")
		elif event in ("-letra0-","-letra1-","-letra2-","-letra3-","-letra4-","-letra5-","-letra6-") and not Inteligencia.get_mi_turno():
			if iniciado:
				pos_letra = clickear_ficha(event, fichas_jugador, window)
		elif event == "Cambiar letras" and not Inteligencia.get_mi_turno():
			if iniciado:
				cambiar_fichas(window,fichas_jugador,bolsa,tablero)
				cambios-=1
				pasar(tablero,fichas_jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
				jugar_IA.start()
				window['-cambios-'].update(cambios)
				if cambios==0:
					window["Cambiar letras"].update(disabled=True)
		elif event == "Posponer":
			pass
		elif event == "TERMINAR":
			terminar(puntos,puntosIA)
			break
		elif event in ("-letraIA0-","-letraIA1-","-letraIA2-","-letraIA3-","-letraIA4-","-letraIA5-","-letraIA6-"):
			pass
		elif event == "Evaluar Palabra" and not Inteligencia.get_mi_turno():
			if iniciado:
				palabra = tablero.buscar_palabra()
				ok = evaluar(palabra, dificultad)
				if ok:
					confirmar(window,tablero,puntos)
				else:
					devolver_fichas(window,tablero,fichas_jugador)
				pasar(tablero,fichas_jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
				jugar_IA.start()
		elif event == "Pasar":
			if iniciado and not Inteligencia.get_mi_turno():
				pasar(tablero,fichas_jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
				jugar_IA.start()
		else:
			if iniciado:
				colocar_letra(event,fichas_jugador,tablero,window,pos_letra)
		if(iniciado and not Inteligencia.get_procesando() and Inteligencia.get_mi_turno()):
			jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,puntos))
			pasar(tablero,Inteligencia.get_fichas(),tiempos,tiempo_turno,Inteligencia,bolsa,window,True)
		if (iniciado) and (tiempos[1]==60):
			if Inteligencia.get_mi_turno():
				window['-turno-'].update('Turno PC')
				window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)
				window["-dot-"].update(filename='imagenes/greendot.png',visible=False)
			else:
				window['-turno-'].update('Tu turno')
				window["-dotIA-"].update(filename='imagenes/greendot.png',visible=False)
				window["-dot-"].update(filename='imagenes/greendot.png',visible=True)

	window.close()


color_button = ('white','OrangeRed3')

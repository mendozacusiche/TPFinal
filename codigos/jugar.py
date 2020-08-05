import PySimpleGUI as sg
from string import ascii_uppercase as up
import random, sys, time, json, threading
if __name__ == 'codigos.jugar':
	from codigos import ventana_bienvenida, Layout,Fichas, Tablero, IA, Jugador,cambiar_letras
from pattern.es import *   #parse, conjugate, INFINITIVE
from datetime import date

def evaluar(palabra, dificultad):
    '''Se evalúa si el tipo de palabra ingresada corresponde a alguno de los tipos aceptados en el nivel que se está jugando'''
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
   
    return ok


def recargar_fichas(jugador, bolsa, window): 
    '''Repone las fichas usadas'''
    usadas=jugador.get_fichas().get_usadas()
    for i in range(7):
        if usadas[i]:
            l=sacar_letra_bolsa(bolsa)
            window["-letra"+str(i)+"-"].update(l)
            jugador.get_fichas().set_letra(l,i)
            jugador.get_fichas().desusar(i)

def pasar(jugador,tiempos,tiempo_turno,Intel):#CONCURRENCIA
	'''Pasa el turno'''
	if(jugador.get_mi_turno()):
		Intel.set_procesando(True)
		Intel.set_mi_turno(True)
		jugador.set_jugado(True)
	else:
		jugador.set_jugado(False)
		jugador.set_mi_turno(True)
	tiempos[1]=tiempo_turno


def segundo(tablero,jugador,Intel,tiempo_turno,window,t,lista): #CONCURRENCIA
	'''Va restando de a 1 segundo los contadores de tiempo, y si llega a 0 el tiempo del turno, pasa el turno, hasta que se llega a 0 en el 
	tiempo total de la partida o se termine por otros motivos'''
	while (t[0]>0 and t[2]):
		time.sleep(1)
		t[0]-=1
		t[1]-=1
		if(t[1]== 0):
			pasar(jugador,t,tiempo_turno,Intel)
			if not jugador.get_mi_turno():
				threading.Thread(target= Intel.turno, args=(bolsa,window,tablero,jugador,t,tiempo_turno,lista)).start()

def contar_letras_bolsa(bolsa):
    '''Cuenta la cantidad de letras que hay en la bolsa'''
    cant=0
    for letra in bolsa.keys():
        cant=cant+bolsa[letra]
    return cant

def sacar_letra_bolsa(bolsa):
    '''Saca una letra aleatoria de la bolsa'''
    letra=random.choice(list(bolsa.keys()))
    while (bolsa[letra] == 0):
        letra=random.choice(list(bolsa.keys()))
    bolsa[letra]-=1
    return letra

def cambiar_fichas(window, jugador, claves,bolsa,tablero):
    ''''''
    for i in range(7):
        if claves[i][1]:
            bolsa[jugador.get_fichas().get_letras()[i]]+=1
            jugador.get_fichas().set_letra(sacar_letra_bolsa(bolsa),i)
            window["-letra"+str(i)+"-"].update(jugador.get_fichas().get_letra(i))

def iniciar(t, window, config, tiempo_turno, tablero, dificultad, nombre,lista):
	'''Define qué sucede cuando se oprime el botón iniciar'''
	window["INICIAR"].update(disabled=True)
	window['TERMINAR'].update(disabled=False)
	window['Posponer'].update(disabled=False)
	window['-cambios-'].update(visible=True)
	bolsa=config["cant_fichas"]
	nuevas=[]
	for i in range(7):
		l=sacar_letra_bolsa(bolsa)
		nuevas.append(l)
	turno=random.choice([True,False])
	Inteligencia = IA.IA (Fichas.Fichas(nuevas),True,dificultad,0,mi_turno=turno,procesando=turno)
	nuevas=[]
	for i in range(7):
		l=sacar_letra_bolsa(bolsa)
		nuevas.append(l)
		window["-letra"+str(i)+"-"].update(l)
	jugador=Jugador.Jugador(nombre,Fichas.Fichas(nuevas),not Inteligencia.get_mi_turno())
	if (Inteligencia.get_mi_turno()):
		window['-turno-'].update('Turno PC')
		window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)#Hay que poner manejo de excepciones??
	else:
		window['Pasar'].update(disabled=False)
		window["Evaluar Palabra"].update(disabled=False)
		window["Cambiar letras"].update(disabled=False)
		for i in range(7):
			window["-letra"+str(i)+"-"].update(disabled=False)
		window['-turno-'].update('Tu turno')
		window["-dot-"].update(filename='imagenes/greendot.png',visible=True)#Hay que poner manejo de excepciones??
	timers= threading.Thread(target= segundo, args=(tablero,jugador,Inteligencia,tiempo_turno,window,t,lista))
	if __name__ == 'codigos.jugar':
		timers.start()
	window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
	return True, jugador, bolsa, Inteligencia

def retomar(window,jugador,tablero,Inteligencia,tiempo_turno,bolsa,t,dificultad,lista):
	'''Define qué sucede cuando se oprime el botón retomar'''
	Layout.cargar_tablero(window,tablero)
	window["RETOMAR"].update(disabled=True)
	window['TERMINAR'].update(disabled=False)
	window['Posponer'].update(disabled=False)
	window['-cambios-'].update(visible=True)
	window["-puntos-"].update(jugador.get_puntos())
	window["-puntosIA-"].update(Inteligencia.get_puntos())
	window['PALABRAS'].update(map(lambda x: " {}  {}  {} ".format(x[0], x[1], x[2]),lista))
	for i in range(7):
		window["-letra"+str(i)+"-"].update(jugador.get_fichas().get_letra(i))
	if (Inteligencia.get_mi_turno()):
		window['-turno-'].update('Turno PC')
		window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)#Hay que poner manejo de excepciones??
	else:
		window['Pasar'].update(disabled=False)
		window["Evaluar Palabra"].update(disabled=False)
		window["Cambiar letras"].update(disabled=False)
		for i in range(7):
			window["-letra"+str(i)+"-"].update(disabled=False)
		window['-turno-'].update('Tu turno')
		window["-dot-"].update(filename='imagenes/greendot.png',visible=True)#Hay que poner manejo de excepciones??
	timers= threading.Thread(target= segundo, args=(tablero,jugador,Inteligencia,tiempo_turno,window,t,lista))
	if __name__ == 'codigos.jugar':
		timers.start()
	window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
	
	return True
    
def cambiar_colores(window, dificultad, tablero):   
    '''Actualiza las casillas especiales de tablero dependiendo del nivel'''
    window["b_"+str(tablero.get_tamanio()//2)+"_"+str(tablero.get_tamanio()//2)].update('★',button_color=(None,'pink'))#★
    if(dificultad == "Facil"):
        Layout.diseño_facil(window,tablero)
    elif(dificultad == "Medio"):
        Layout.diseño_medio(window,tablero)
    else:
        Layout.diseño_dificil(window,tablero)
 
def checkear_ficha(event, jugador, window, n):  
    '''Cambia el estado de las fichas del atril del jugador'''
    if (jugador.get_fichas().get_checked()[n]==False):
        jugador.get_fichas().descheckear_todas(window)
        jugador.get_fichas().checkear(n)
        window["-letra"+str(n)+"-"].update(button_color=('white','blue'))
    else:
        jugador.get_fichas().descheckear(n)
        window["-letra"+str(n)+"-"].update(button_color=('white','OrangeRed3'))

def clickear_ficha(event, jugador, window):
	
    if event == ("-letra0-"):
        checkear_ficha(event,jugador,window,0)
        return 0
    elif event == ("-letra1-"):
        checkear_ficha(event,jugador,window,1)
        return 1
    elif event == ("-letra2-"):
        checkear_ficha(event,jugador,window,2)
        return 2
    elif event == ("-letra3-"):
        checkear_ficha(event,jugador,window,3)
        return 3
    elif event == ("-letra4-"):
        checkear_ficha(event,jugador,window,4)
        return 4
    elif event == ("-letra5-"):
        checkear_ficha(event,jugador,window,5)
        return 5
    elif event == ("-letra6-"):
        checkear_ficha(event,jugador,window,6)
        return 6

def devolver_letra(window,tablero,fichas,x,y):
    '''Devuelve una letra desde el tablero hacia el atril'''
    pos=0
    while (fichas.get_letras()[pos]!= ""):
        pos+=1
    window["-letra"+str(pos)+"-"].update(tablero.get_letra(x,y))
    fichas.set_letra(tablero.get_letra(x,y), pos)
    fichas.desusar(pos)
    tablero.set_letra("",x,y)

def devolver_fichas(window,tablero,fichas):
	'''Devuelve todas las letras desde el tablero, no confirmadas, hacía el atril '''
	coordenadas=tablero.get_no_confirmadas()
	for c in coordenadas:
		devolver_letra(window,tablero,fichas,c[0],c[1])
		if c==(tablero.get_tamanio()//2,tablero.get_tamanio()//2):
			window["b_"+str(c[0])+"_"+str(c[1])].update("★")
		else:
			window["b_"+str(c[0])+"_"+str(c[1])].update("")

def colocar_letra(event,jugador,tablero,window,pos):
    '''Coloca una letra en el tablero'''
    if True in (jugador.get_fichas().get_checked()):
        b,x,y = str(event).split("_")
        x= int (x)
        y= int (y)
        if not jugador.get_fichas().get_usadas()[pos]:
            if (not tablero.get_confirmadas()[x][y]):
                if (tablero.get_letra(x,y)!=""):
                    devolver_letra(window,tablero,jugador.get_fichas(),x,y)
                tablero.set_letra(jugador.get_fichas().get_letras()[pos],x,y)
                window[event].update(jugador.get_fichas().get_letras()[pos])
                window["-letra"+str(pos)+"-"].update("")
                jugador.get_fichas().set_letra("",pos)
                jugador.get_fichas().usar(pos)
        else:
            if (not tablero.get_confirmadas()[x][y]):
                if (tablero.get_letra(x,y)!=""):
                    devolver_letra(window,tablero,jugador.get_fichas(),x,y)
                    if (x==tablero.get_tamanio()//2 and y==tablero.get_tamanio()//2):
                    	window[event].update("★")
                    else:
                    	window[event].update("")

def confirmar(window,tablero,jugador,IA,palabra,lista):
	'''Confirma las letras en el tablero'''
	nuevos_puntos=tablero.confirmar_letras(window, IA.get_mi_turno())
	if (IA.get_primer_turno() or jugador.get_primer_turno()):
		IA.set_primer_turno(False)
		jugador.set_primer_turno(False)
	if IA.get_mi_turno():
		turno='PC'
		IA.set_puntos(IA.get_puntos()+nuevos_puntos)
		window["-puntosIA-"].update(IA.get_puntos())
	else:
		turno=jugador.get_nombre()
		jugador.set_puntos(jugador.get_puntos()+nuevos_puntos)
		window["-puntos-"].update(jugador.get_puntos())
	lista.append((turno.upper(),palabra.upper(),nuevos_puntos))
	lista.append(('','',''))
	window['PALABRAS'].update(map(lambda x: " {}  {}  {} ".format(x[0], x[1], x[2]),lista))
	

def deshabilitar_habilitar_botones(window,b,jugador):
	'''Se habilitan y deshabilitan los distintos botones del juego'''
	for i in range(7):
		window["-letra"+str(i)+"-"].update(disabled=b)
	window["Evaluar Palabra"].update(disabled=b)
	window['Pasar'].update(disabled=b)
	if (jugador.get_cambios()>0):
		window['Cambiar letras'].update(disabled=b)

def posponer(config,tablero,bolsa,Inteligencia,jugador,tiempos,dificultad,lista,opcion=None):
	'''Se guardan los datos para posponer el juego'''
	#config["tablero_tamanio"]=tablero.get_tamanio()
	#config["tablero_especiales"]=tablero.get_especiales()
	config["tablero_letras"]=tablero.get_letras()
	config["tablero_confirmadas"]=tablero.get_confirmadas()
	config["tablero_coloreadas"]=tablero.get_coloreadas()
	config["bolsa"]=bolsa
	config["tiempos"]=tiempos
	config["dificultad"]=dificultad
	config["opcion"]=opcion
	config["Inteligencia_fichas_letras"]=Inteligencia.get_fichas().get_letras()
	config["Inteligencia_fichas_usadas"]=Inteligencia.get_fichas().get_usadas()
	config["Inteligencia_fichas_checked"]=Inteligencia.get_fichas().get_checked()
	config["Inteligencia_mi_turno"]=Inteligencia.get_mi_turno()
	config["Inteligencia_procesando"]=Inteligencia.get_procesando()
	config["Inteligencia_dificultad"]=Inteligencia.get_dificultad()
	#config["Inteligencia_cambios_letras"]=Inteligencia.get_cambios_letras()
	config["Inteligencia_puntos"]=Inteligencia.get_puntos()
	config["Inteligencia_primer_turno"]=Inteligencia.get_primer_turno()
	config["jugador_fichas_letras"]=jugador.get_fichas().get_letras()
	config["jugador_fichas_usadas"]=jugador.get_fichas().get_usadas()
	config["jugador_fichas_checked"]=jugador.get_fichas().get_checked()
	config["jugador_puntos"]=jugador.get_puntos()
	config["jugador_nombre"]=jugador.get_nombre()
	config["jugador_cambios"]=jugador.get_cambios()
	config["jugador_mi_turno"]=jugador.get_mi_turno()
	config["jugador_primer_turno"]=jugador.get_primer_turno()
	config["jugador_jugado"]=jugador.get_jugado()
	config["lista"]=lista
	archivo=open("archivos/guardado.json","w") 
	json.dump(config,archivo)
	tiempos[2]=False
	sg.popup('Partida guardada con éxito',title='')

def juego(cargar=False):
	'''Creación de la ventana de juego'''
	try:
		if cargar:
			with open("archivos/guardado.json","r") as archivo:
				config = json.load(archivo) #se podria cambiar el nombre a guardado de la var
			nombre = config["jugador_nombre"]
			fichas=Fichas.Fichas(config["jugador_fichas_letras"],config["jugador_fichas_usadas"],config["jugador_fichas_checked"])
			jugador= Jugador.Jugador(nombre,fichas,config["jugador_mi_turno"],config["jugador_mi_turno"],config["jugador_cambios"],config["jugador_puntos"],config["jugador_jugado"])
			ventana_bienvenida.ventana(nombre)
			tiempos= config["tiempos"]
			tiempo_total=int(config["tiempo_total"]) * 60
			tiempo_turno=int(config["tiempo_turno"]) * 60
			dificultad=config["dificultad"]
			opcion=config["opcion"]
			bolsa=config["bolsa"]
			tablero=Tablero.Tablero(dificultad,config["tablero_letras"],config["tablero_confirmadas"],config["tablero_coloreadas"])
			fichasIA=Fichas.Fichas(config["Inteligencia_fichas_letras"],config["Inteligencia_fichas_usadas"],config["Inteligencia_fichas_checked"])
			Inteligencia=IA.IA(fichasIA,config["Inteligencia_primer_turno"],config["Inteligencia_dificultad"],config["Inteligencia_puntos"],config["Inteligencia_mi_turno"],config["Inteligencia_procesando"])#,config["Inteligencia_cambios_letras"])
			layout = Layout.crear_layout(tablero, tiempos, nombre, dificultad, jugador.get_cambios(), opcion, True)
			window = sg.Window('ScrabbleAR',resizable= True,element_justification='center',).Layout(layout).Finalize()
			iniciado = False
			lista=config["lista"]
		else:
			with open("archivos/config.json","r") as archivo:
				config = json.load(archivo)
			nombre = ventana_bienvenida.ventana()  
			tiempo_total= int(config["tiempo_total"]) * 60
			tiempo_turno= int(config["tiempo_turno"]) * 60
			tiempos=[tiempo_total,tiempo_turno,True]
			dificultad=config["dificultad"]
			tablero = Tablero.Tablero(dificultad)
			if dificultad == "Dificil":
				opciones=["Adjetivos", "Verbos"]
				opcion=random.choice(opciones)
				dificultad=dificultad+opcion
				layout = Layout.crear_layout(tablero, tiempos, nombre, dificultad, 3, opcion)    
			else:
				layout = Layout.crear_layout(tablero, tiempos, nombre, dificultad, 3)    
			window = sg.Window('ScrabbleAR',resizable= True,element_justification='center').Layout(layout).Finalize()
			iniciado=False
			lista=[]

		pos_letra= -1 #se actualiza al clickear ficha y se utiliza en colocar letra

		while True:                    
			event, values = window.Read(timeout=200)
			#print(event, values)
			if event == None:
				tiempos[2]=False 
				break
			elif event == "INICIAR":
				if not iniciado:
					iniciado, jugador, bolsa, Inteligencia = iniciar(tiempos, window, config, tiempo_turno, tablero, dificultad, nombre,lista)
					jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,jugador,tiempos,tiempo_turno,lista))			
					cambiar_colores(window,dificultad,tablero) #actualiza el tablero con las casillas de premio  por nivel
					if Inteligencia.get_mi_turno():
						jugar_IA.start()
			elif event == "RETOMAR":
				if not iniciado:			
					cambiar_colores(window,dificultad,tablero) #actualiza el tablero con las casillas de premio  por nivel
					iniciado = retomar(window,jugador,tablero,Inteligencia,tiempo_turno,bolsa,tiempos,dificultad,lista)
					jugar_IA = threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,jugador,tiempos,tiempo_turno,lista))
					if Inteligencia.get_mi_turno():
						jugar_IA.start()
			elif event == sg.TIMEOUT_KEY:
				if(iniciado):
					window["-TURNO-"].update(f"{tiempos[0] // 60}:{tiempos[0]%60:02d}")
					window["-DURACION-"].update(f"{tiempos[1] // 60}:{tiempos[1]%60:02d}")
					window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
			elif event in ("-letra0-","-letra1-","-letra2-","-letra3-","-letra4-","-letra5-","-letra6-") and not Inteligencia.get_mi_turno():
				if iniciado:
					pos_letra = clickear_ficha(event, jugador, window)
			elif event == "Cambiar letras" and not Inteligencia.get_mi_turno():
				if iniciado:
					devolver_fichas(window,tablero,jugador.get_fichas())
					ok=cambiar_letras.ventana(window, jugador, bolsa, tablero)
					if ok:
						jugador.set_cambios(jugador.get_cambios()-1)
						window['-cambios-'].update(jugador.get_cambios())
						if jugador.get_cambios()==0:
							window["Cambiar letras"].update(disabled=True)
						pasar(jugador,tiempos,tiempo_turno,Inteligencia)
			elif event == "Posponer":
				if (iniciado):
					devolver_fichas(window,tablero,jugador.get_fichas())
					if (dificultad in ("Facil","Medio")):
						posponer(config,tablero,bolsa,Inteligencia,jugador,tiempos,dificultad,lista)
						break
					else:
						posponer(config,tablero,bolsa,Inteligencia,jugador,tiempos,dificultad,lista,opcion)
						break
			elif event == "TERMINAR":
				devolver_fichas(window,tablero,jugador.get_fichas())
				fecha=date.today()
				if Layout.terminar(window,Inteligencia,tiempos,jugador,dificultad,fecha,config):
					break
			elif event in ("-letraIA0-","-letraIA1-","-letraIA2-","-letraIA3-","-letraIA4-","-letraIA5-","-letraIA6-"):
				pass #Usamos esto porque si no al clickear una ficha de la IA se traba el programa y si las deshabilitamos cambia el color, por lo tanto no nos sirve
			elif event == "Evaluar Palabra" and not Inteligencia.get_mi_turno():
				if iniciado:
					palabra,medio = tablero.buscar_palabra(jugador)
					ok = evaluar(palabra, dificultad)
					if ok:
						confirmar(window,tablero,jugador,Inteligencia,palabra,lista)
						
					else:
						devolver_fichas(window,tablero,jugador.get_fichas())
						if not medio:
							sg.popup('En la primer jugada la palabra debe pasar por el medio',title='')
						else:
							sg.popup("La palabra ingresada no es valida",title='')
					if (len(jugador.get_fichas().get_usadas())>contar_letras_bolsa(bolsa)):
						fecha=date.today()
						Layout.terminar_por_otros(window,Inteligencia,jugador,dificultad,tiempos,fecha,config)
						break
					else:
						pasar(jugador,tiempos,tiempo_turno,Inteligencia)
			elif event == "Pasar":
				if iniciado and not Inteligencia.get_mi_turno():
					pasar(jugador,tiempos,tiempo_turno,Inteligencia)
			else:
				if iniciado:
					colocar_letra(event,jugador,tablero,window,pos_letra)
			
			'''Por problemas de compatibilidad de PySimpleGUI con Threading, se busco la manera con booleanos de hacer las tareas que requerian
			de actualización gráfica por fuera de los procesos cuando estos hayan indicado su finalización.
			Las ultimas versiones de PySimpleGUI incorporaron una instruccion "write_event_value" que permite levantar eventos que son leidos
			con window.Read(), pero no nos pareció indicado usar versiones posteriores que pudieran generar problemas al correr en computadoras
			donde no este actualizado.'''
			if(iniciado and not Inteligencia.get_procesando() and Inteligencia.get_mi_turno()): 
				if Inteligencia.get_terminar(): 
					fecha=date.today()
					Layout.terminar_por_otros(window,Inteligencia,jugador,dificultad,tiempos,fecha,config)
					break
				else:
					Inteligencia.set_mi_turno(False)
					jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,jugador,tiempos,tiempo_turno,lista))
					window['-turno-'].update('Tu turno')
					window["-dotIA-"].update(filename='imagenes/greendot.png',visible=False)
					window["-dot-"].update(filename='imagenes/greendot.png',visible=True)
					deshabilitar_habilitar_botones(window,False,jugador)
			elif (iniciado and jugador.get_jugado() and jugador.get_mi_turno()):
				jugador.set_mi_turno(False)
				deshabilitar_habilitar_botones(window,True,jugador)
				devolver_fichas(window,tablero,jugador.get_fichas())
				recargar_fichas(jugador,bolsa,window)
				window['-turno-'].update('Turno PC')
				window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)
				window["-dot-"].update(filename='imagenes/greendot.png',visible=False)
				jugar_IA.start()

			if tiempos[0]==0:
				devolver_fichas(window,tablero,jugador.get_fichas())
				fecha=date.today()
				Layout.terminar_por_otros(window,Inteligencia,jugador,dificultad,tiempos,fecha,config)
				break
		window.close()

	except FileNotFoundError:
		if cargar:
			sg.popup('No se encontro el archivo guardado.json',title='')
		else:
			sg.popup('No se encontro el archivo config.json',title='')
		

if __name__ == '__main__':
	sg.theme('BlueMono')
	sg.popup('Por favor ejecute ScrabbleAR.py',title='')

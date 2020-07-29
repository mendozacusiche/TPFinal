import PySimpleGUI as sg
from string import ascii_uppercase as up
import random, sys, time, json, threading, ventana_bienvenida, Fichas, Tablero, IA, Layout, Jugador
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
    # else:
        # sg.popup("La Palapra Ingresada No es Valida")
    return ok


def recargar_fichas(jugador, bolsa, window, turnoIA=False):
    usadas=jugador.get_fichas().get_usadas()
    for i in range(7):
        if usadas[i]:
            l=sacar_letra_bolsa(bolsa)
            if not turnoIA:
                window["-letra"+str(i)+"-"].update(l)
            jugador.get_fichas().set_letra(l,i)
            usadas[i]=False

def pasar(tablero,jugador,tiempos,tiempo_turno,Intel,bolsa,window):#CONCURRENCIA
	devolver_fichas(window,tablero,jugador.get_fichas())
	recargar_fichas(jugador,bolsa,window,Intel.get_mi_turno())
	tiempos[1]=tiempo_turno
	if Intel.get_mi_turno()==False:
		Intel.set_mi_turno(True)
		window['-turno-'].update('Turno PC')
		window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)
		window["-dot-"].update(filename='imagenes/greendot.png',visible=False)
		deshabilitar_habilitar_botones(window,True,jugador)
	jugador.set_mi_turno(not jugador.get_mi_turno())


def segundo(tablero,jugador,Intel,tiempo_turno,bolsa,window,t,dif): #CONCURRENCIA
	while (t[0]>0 and t[2]):
		time.sleep(1)
		t[0]-=1
		t[1]-=1
		if(t[1]== 0):
			pasar(tablero,jugador,t,tiempo_turno,Intel,bolsa,window)
			if not Intel.get_mi_turno():
				threading.Thread(target= Intel.turno, args=(bolsa,window,tablero,jugador,t,tiempo_turno)).start()

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

def iniciar(t, window, config, tiempo_turno, tablero, dificultad, nombre):
	window["INICIAR"].update(disabled=True)
	window['TERMINAR'].update(disabled=False)
	window['Posponer'].update(disabled=False)
	window['-cambios-'].update(visible=True)
	bolsa=config["cant_fichas"]
	nuevas=[]
	for i in range(7):
		l=sacar_letra_bolsa(bolsa)
		nuevas.append(l)
	Inteligencia = IA.IA (Fichas.Fichas(nuevas),True,dificultad,0,mi_turno=random.choice([True,False]))
	nuevas=[]
	for i in range(7):
		l=sacar_letra_bolsa(bolsa)
		nuevas.append(l)
		window["-letra"+str(i)+"-"].update(l)
	jugador=Jugador.Jugador(nombre,Fichas.Fichas(nuevas),not Inteligencia.get_mi_turno())
	if (Inteligencia.get_mi_turno()):
		window['-turno-'].update('Turno PC')
		window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)
	else:
		window['Pasar'].update(disabled=False)
		window["Evaluar Palabra"].update(disabled=False)
		window["Cambiar letras"].update(disabled=False)
		for i in range(7):
			window["-letra"+str(i)+"-"].update(disabled=False)
		window['-turno-'].update('Tu turno')
		window["-dot-"].update(filename='imagenes/greendot.png',visible=True)
	timers= threading.Thread(target= segundo, args=(tablero,jugador,Inteligencia,tiempo_turno,bolsa,window,t,dificultad))
	if __name__ == 'jugar':
		timers.start()
	window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
	return True, jugador, bolsa, Inteligencia

def retomar(window,jugador,tablero,Inteligencia,tiempo_turno,bolsa,t,dificultad):
	Layout.cargar_tablero(window,tablero)
	window["RETOMAR"].update(disabled=True)
	window['TERMINAR'].update(disabled=False)
	window['Posponer'].update(disabled=False)
	window['-cambios-'].update(visible=True)
	window["-puntos-"].update(jugador.get_puntos())
	window["-puntosIA-"].update(Inteligencia.get_puntos())
	for i in range(7):
		window["-letra"+str(i)+"-"].update(jugador.get_fichas().get_letra(i))
	if (Inteligencia.get_mi_turno()):
		window['-turno-'].update('Turno PC')
		window["-dotIA-"].update(filename='imagenes/greendot.png',visible=True)
	else:
		window['Pasar'].update(disabled=False)
		window["Evaluar Palabra"].update(disabled=False)
		window["Cambiar letras"].update(disabled=False)
		for i in range(7):
			window["-letra"+str(i)+"-"].update(disabled=False)
		window['-turno-'].update('Tu turno')
		window["-dot-"].update(filename='imagenes/greendot.png',visible=True)
	timers= threading.Thread(target= segundo, args=(tablero,jugador,Inteligencia,tiempo_turno,bolsa,window,t,dificultad))
	if __name__ == 'jugar':
		timers.start()
	window["-CantFichas-"].update(str(contar_letras_bolsa(bolsa)))
	return True
    
def cambiar_colores(window, dificultad, tablero):   
    window["b_"+str(tablero.get_tamanio()//2)+"_"+str(tablero.get_tamanio()//2)].update('★')#★
    if(dificultad == "Facil"):
        Layout.diseño_facil(window,tablero)
    elif(dificultad == "Medio"):
        Layout.diseño_medio(window,tablero)
    else:
        Layout.diseño_dificil(window,tablero)
 
def checkear_ficha(event, jugador, window, n):  
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
		if c==(tablero.get_tamanio()//2,tablero.get_tamanio()//2):
			window["b_"+str(c[0])+"_"+str(c[1])].update("★")
		else:
			window["b_"+str(c[0])+"_"+str(c[1])].update("")

def colocar_letra(event,jugador,tablero,window,pos):
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
                    window[event].update("")

def confirmar(window,tablero,jugador,IA):
	nuevos_puntos=tablero.confirmar_letras(window, IA.get_mi_turno())
	if (IA.get_primer_turno() or jugador.get_primer_turno()):
		IA.set_primer_turno(False)
		jugador.set_primer_turno(False)
	if IA.get_mi_turno():
		IA.set_puntos(IA.get_puntos()+nuevos_puntos)
		window["-puntosIA-"].update(IA.get_puntos())
	else:
		jugador.set_puntos(jugador.get_puntos()+nuevos_puntos)
		window["-puntos-"].update(jugador.get_puntos())

def deshabilitar_habilitar_botones(window,b,jugador):
	for i in range(7):
		window["-letra"+str(i)+"-"].update(disabled=b)
	window["Evaluar Palabra"].update(disabled=b)
	window['Pasar'].update(disabled=b)
	if (jugador.get_cambios()>0):
		window['Cambiar letras'].update(disabled=b)

def posponer(config,tablero,bolsa,Inteligencia,jugador,tiempos,dificultad,opcion=None):
	#config["tablero_tamanio"]=tablero.get_tamanio()
	#config["tablero_especiales"]=tablero.get_especiales()
	config["tablero_letras"]=tablero.get_letras()
	config["tablero_confirmadas"]=tablero.get_confirmadas()
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
	config["Inteligencia_cambios_letras"]=Inteligencia.get_cambios_letras()
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
	archivo=open("archivos/guardado.json","w") 
	json.dump(config,archivo)
	sg.popup('Partida guardada con éxito')

def juego(cargar=False):
	try:
		if cargar:
			archivo= open("archivos/guardado.json","r")#falta crear archivo #poner manejo excepciones #fijarse si está vacio el archivo también 
			config = json.load(archivo) #se podria cambiar el nombre a guardado de la var
			nombre = config["jugador_nombre"]
			fichas=Fichas.Fichas(config["jugador_fichas_letras"],config["jugador_fichas_usadas"],config["jugador_fichas_checked"])
			jugador= Jugador.Jugador(nombre,fichas,config["jugador_mi_turno"],config["jugador_mi_turno"],config["jugador_cambios"],config["jugador_puntos"])
			ventana_bienvenida.ventana(nombre)
			tiempos= config["tiempos"]
			tiempo_total=int(config["tiempo_total"]) * 60
			tiempo_turno=int(config["tiempo_turno"]) * 60
			dificultad=config["dificultad"]
			opcion=config["opcion"]
			bolsa=config["bolsa"]
			tablero=Tablero.Tablero(dificultad,config["tablero_letras"],config["tablero_confirmadas"])
			fichasIA=Fichas.Fichas(config["Inteligencia_fichas_letras"],config["Inteligencia_fichas_usadas"],config["Inteligencia_fichas_checked"])
			Inteligencia=IA.IA(fichasIA,config["Inteligencia_primer_turno"],config["Inteligencia_dificultad"],config["Inteligencia_puntos"],config["Inteligencia_mi_turno"],config["Inteligencia_procesando"],config["Inteligencia_cambios_letras"])
			layout = Layout.crear_layout(tablero, tiempos, nombre, dificultad, jugador.get_cambios(), opcion, True)
			window = sg.Window('ScrabbleAR',resizable= True,element_justification='center',).Layout(layout).Finalize()
			iniciado = False
		else:
			archivo= open("archivos/config.json","r") #manejo excepciones
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
			window = sg.Window('ScrabbleAR',resizable= True,element_justification='center',).Layout(layout).Finalize()
			iniciado=False

		pos_letra= -1 #que es esto?

		while True:                    
			event, values = window.Read(timeout=200)
			print(event, values)
			if event in (None,'EXIT'):
				tiempos[2]=False #se deberían guardar los puntajes acá?
				break
			elif event == "INICIAR":
				if not iniciado:
					iniciado, jugador, bolsa, Inteligencia = iniciar(tiempos, window, config, tiempo_turno, tablero, dificultad, nombre)
					jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,jugador,tiempos,tiempo_turno))			
					cambiar_colores(window,dificultad,tablero) #actualiza el tablero con las casillas de premio  por nivel
					if Inteligencia.get_mi_turno():
						jugar_IA.start()
			elif event == "RETOMAR":
				if not iniciado:
					iniciado = retomar(window,jugador,tablero,Inteligencia,tiempo_turno,bolsa,tiempos,dificultad)
					jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,jugador,tiempos,tiempo_turno))			
					cambiar_colores(window,dificultad,tablero) #actualiza el tablero con las casillas de premio  por nivel
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
					cambiar_fichas(window,jugador.get_fichas(),bolsa,tablero)
					jugador.set_cambios(jugador.get_cambios()-1)
					pasar(tablero,jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
					jugar_IA.start()
					window['-cambios-'].update(jugador.get_cambios())
					if jugador.get_cambios()==0:
						window["Cambiar letras"].update(disabled=True)
			elif event == "Posponer":
				if (iniciado):
					if (dificultad in ("Facil","Medio")):
						posponer(config,tablero,bolsa,Inteligencia,jugador,tiempos,dificultad)
						break
					else:
						posponer(config,tablero,bolsa,Inteligencia,jugador,tiempos,dificultad,opcion)
						break
			elif event == "TERMINAR":
				if Layout.terminar(Inteligencia,tiempos,jugador,dificultad):
					break
			elif event in ("-letraIA0-","-letraIA1-","-letraIA2-","-letraIA3-","-letraIA4-","-letraIA5-","-letraIA6-"):
				pass #es necesario poner este evento si no hace nada?
			elif event == "Evaluar Palabra" and not Inteligencia.get_mi_turno():
				if iniciado:
					palabra,medio = tablero.buscar_palabra(jugador)
					ok = evaluar(palabra, dificultad)
					if ok:
						confirmar(window,tablero,jugador,Inteligencia)
					else:
						devolver_fichas(window,tablero,jugador.get_fichas())
						
						if not medio:
							sg.popup('En la primer jugada la palabra debe pasar por el medio')
						else:
							sg.popup("La palabra ingresada no es valida")
					pasar(tablero,jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
					jugar_IA.start()
			elif event == "Pasar":
				if iniciado and not Inteligencia.get_mi_turno():
					pasar(tablero,jugador,tiempos,tiempo_turno,Inteligencia,bolsa,window)
					jugar_IA.start()
			else:
				if iniciado:
					colocar_letra(event,jugador,tablero,window,pos_letra)
			if(iniciado and not Inteligencia.get_procesando() and Inteligencia.get_mi_turno()):
				Inteligencia.set_mi_turno(False)
				jugar_IA= threading.Thread(target= Inteligencia.turno, args=(bolsa,window,tablero,jugador,tiempos,tiempo_turno))
				window['-turno-'].update('Tu turno')
				window["-dotIA-"].update(filename='imagenes/greendot.png',visible=False)
				window["-dot-"].update(filename='imagenes/greendot.png',visible=True)
				deshabilitar_habilitar_botones(window,False,jugador)
			if tiempos[0]==0:#acá no deberiamos preguntar si se quedo sin fichas la bolsa también?
				Layout.terminar_por_otros(Inteligencia,jugador,dificultad)
				break
		window.close()

	except FileNotFoundError as ex: #raro manejo de excepciones
		print('No se encontro el  archivo.......')

color_button = ('white','OrangeRed3')

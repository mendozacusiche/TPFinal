import PySimpleGUI as sg
import json

def aplicar(vals, punts, cants,wind):
	'''Se define qué sucede cuando se da click en aplicar en la ventana de configuración'''
	try:
		archivo=open("archivos/config.json","r+")

		config=json.load(archivo)

		config["tiempo_total"] = int(vals["-tot-"])
		config["tiempo_turno"] = int(vals["-turn-"])
		config["dificultad"] = vals["-dif-"]
		for p in punts:
			config["puntaje_fichas"][p]=punts[p]
		for c in cants:
			config["cant_fichas"][c]=cants[c]

		archivo.seek(0)
		json.dump(config,archivo)
		archivo.truncate()
		if config["dificultad"]=="Facil":
			wind["-imagen-"].update(filename='imagenes/tabfacil.png')
			wind["-descr-"].update("""Nivel fácil: 
Palabras permitidas: sustantivos, adjetivos y verbos. 
Tamaño del tablero: 23x23.""")
		elif config["dificultad"]=="Medio":
			wind["-imagen-"].update(filename='imagenes/tabmedio.png')
			wind["-descr-"].update("""Nivel medio: 
Palabras permitidas: adjetivos y verbos. 
Tamaño del tablero: 19x19.""")
		else:
			wind["-imagen-"].update(filename='imagenes/tabdificil.png')
			wind["-descr-"].update("""Nivel dificil: 
Palabras permitidas: son elegidas al azar entre adjetivos y verbos. 
Tamaño del tablero: 15x15.""")
		archivo.close()
	except FileNotFoundError as ex:
		sg.popup('No se encontro el archivo "config.json" en el directorio actual',title='')
		
  		
def restaurar(win):
	'''Se define qué sucede cuando se da click en restaurar en la ventana de configuración'''
	try:
		archivo=open("archivos/config.json","w")#acá creo que no es necesario, porque siempre va a poder abrirlo por ser en modo w

		puntaje_fichas= { 'A' : 1 ,   'B' : 3 ,   'C' : 2 , 'D' : 2 ,
					      'E' : 1 ,   'F' : 4 ,   'G' : 2 , 'H' : 4 ,
					      'I' : 1 ,   'J' : 6 , 'K' : 7 , 'L' : 1 ,'LL': 7,
					      'M' : 3 ,   'N' : 1 ,'Ñ': 7,   'O' : 1 , 'P' : 3 ,
					      'Q' : 7 , 'R' : 1 ,'RR': 7,   'S' : 1 , 'T' : 1 ,
					      'U' : 1 ,   'V' : 4 ,   'W' : 7 , 'X' : 7 ,
					      'Y' : 4 ,   'Z' : 10 }

		cant_fichas= { 'A' : 23 ,   'B' : 4 ,   'C' : 6 , 'D' : 6 ,
					   'E' : 23 ,   'F' : 3 ,   'G' : 3 , 'H' : 3 ,
					   'I' : 23 ,   'J' : 3 , 'K' : 1 , 'L' : 6 ,'LL': 1,
					   'M' : 4 ,   'N' : 8 ,'Ñ': 1,   'O' : 23 , 'P' : 3 ,
					   'Q' : 1 , 'R' : 6 ,'RR': 1,   'S' : 10 , 'T' : 6 ,
					   'U' : 23 ,   'V' : 3  ,   'W' : 1 , 'X' : 1 ,
					   'Y' : 1 ,   'Z' : 1 }

		j={"tiempo_total":"20","tiempo_turno":"1","dificultad":"Medio","puntaje_fichas":puntaje_fichas,"cant_fichas":cant_fichas}

		json.dump(j,archivo)

		archivo.close()

		win["-tot-"].update(j["tiempo_total"])
		win["-turn-"].update(j["tiempo_turno"])
		win["-dif-"].update(j["dificultad"])
		win["-desc-"].update("")
		win["-l1-"].update("")
		win["-l2-"].update("")
		win["-t1-"].update("")
		win["-t2-"].update("")
	except FileNotFoundError as ex:
		sg.popup("No se encontro el archivo config.json",title='')

def actualizar_descripcion(win,val):
	'''Se actualiza la descripción en la ventana dependiendo del nivel elegido'''
	if(val["-dif-"]=="Facil"):
		win["-desc-"].update("Facil: sustantivos, adjetivos y verbos. Tablero 23x23.")
		win["-max-"].update("(max: 25)")
	elif (val["-dif-"]=="Medio"):
		win["-desc-"].update("Medio: adjetivos y verbos. Tablero 19x19.")
		win["-max-"].update("(max: 20)")
	elif (val["-dif-"]=="Dificil"):
		win["-desc-"].update("Dificil: al azar adjetivos o verbos. Tablero 15x15.")
		win["-max-"].update("(max: 15)")

def ventana(wind):
	'''Creación ventana de configuración'''
	try:
		with open("archivos/config.json","r") as archivo:
			config= json.load(archivo)
		letras=["A","B","C","D","E","F","G","H","I","J","K","L","LL","M","N","Ñ","O","P","Q","R","RR","S","T","U","V","W","X","Y","Z"]
		
		layout=[
			[sg.Text("Tiempo: ",font=("Arial Black",10))],
			[sg.Text("Total:"), sg.InputText(config["tiempo_total"],size=(3,1),key="-tot-"), sg.Text("Turno "), sg.InputText(config["tiempo_turno"],size=(3,1),key="-turn-")],
			[sg.Text("(max: 15)",key="-max-")],
			[sg.Text("Dificultad: ",font=("Arial Black",10))], 
			[sg.Combo(["Facil","Medio","Dificil"],config["dificultad"], enable_events=True, key="-dif-")],
			[sg.Text("", size=(50,1) , key=("-desc-"))],
			[sg.Text("Puntaje: ",font=("Arial Black",10))], 
			[sg.Text("Letra "),sg.Combo(letras,letras[0],size=(3,1), enable_events=True, key="-l1-"),sg.Text("Puntos "),sg.InputText(config["puntaje_fichas"][letras[0]],size=(3,1), enable_events=True, key="-t1-")],
			[sg.Text("Cantidad: ",font=("Arial Black",10))],
			[sg.Text("Letra "),sg.Combo(letras,letras[0],size=(3,1), enable_events=True, key="-l2-"),sg.Text("Cantidad "),sg.InputText(config["cant_fichas"][letras[0]],size=(3,1), enable_events=True, key="-t2-")],
			[sg.Button("Aplicar",font=("Arial Black",11),size=(15, 0),pad=(0, 0)),sg.Button("Restaurar",font=("Arial Black",11), size=(15, 0),pad=(0, 0)),sg.Button("Atrás",key="Atras",font=("Arial Black",11), size=(15, 0),pad=(0, 0))]
			]
		if config["dificultad"]=="Facil":
			layout[2][0]=sg.Text("(max: 25)",key="-max-")
		elif config["dificultad"]=="Medio":
			layout[2][0]=sg.Text("(max: 20)",key="-max-")

		window= sg.Window("Configuración",layout)

		nuevos_puntajes={}
		nuevas_cantidades={}

		while True:
			evento,valores = window.read()
	
			if evento == "Aplicar":
				try:
					if (int(valores["-tot-"])<=25 and valores["-dif-"]=="Facil") or (int(valores["-tot-"])<=20 and valores["-dif-"]=="Medio") or (int(valores["-tot-"])<=15 and valores["-dif-"]=="Dificil"):
						if (int(valores["-turn-"])<=int(valores["-tot-"]))and((int(valores["-turn-"])!=0) and (int(valores["-tot-"])!=0)): #no se si está bien poner el igual acá o deberia ir en el elif
							if(int(valores["-t2-"])>0)and (int(valores["-t1-"])>0):
								aplicar(valores, nuevos_puntajes, nuevas_cantidades,wind)
								sg.popup('Configuración guardada con éxito!',title='')
								break
							else:
								sg.popup('Ingrese valores mayores a 0!',title='')
						elif ((int(valores["-turn-"])==0) or (int(valores["-tot-"])==0)):
							sg.popup('Ingrese valores mayores a 0!',title='')
						elif (int(valores["-turn-"])>int(valores["-tot-"])):
							sg.popup("El tiempo de turno supera al tiempo de partida!",title="")

					else:
						sg.popup("El tiempo de partida supera el maximo!",title="")
				except ValueError:
					sg.popup('Ingrese un valor válido!',title='')
			elif evento == "Restaurar":
				restaurar(window)
				nuevos_puntajes={}
				nuevas_cantidades={}
	
			elif evento == "Atras" or evento == sg.WIN_CLOSED:
				break
	
			elif evento == "-dif-":
				actualizar_descripcion(window, valores)
	
			elif evento == "-l1-":
				if (valores["-l1-"] in nuevos_puntajes):
					window["-t1-"].update(nuevos_puntajes[valores["-l1-"]])
				else:
					window["-t1-"].update(config["puntaje_fichas"][valores["-l1-"]])
				
			elif evento == "-l2-":
				
				if (valores["-l2-"] in nuevos_puntajes):
					window["-t2-"].update(nuevos_puntajes[valores["-l2-"]])
				else:
					window["-t2-"].update(config["cant_fichas"][valores["-l2-"]])
				
			elif evento == "-t1-":
				try:
					if int(valores["-t1-"])>0:
						nuevos_puntajes[valores["-l1-"]]=int(valores["-t1-"])
					else:
						sg.popup('Ingrese valores mayores a 0!',title='')
				except ValueError:
					sg.popup('Ingrese un valor válido!',title='')
			elif evento == "-t2-":
				try:
					if int(valores["-t2-"])>0:
						nuevas_cantidades[valores["-l2-"]]=int(valores["-t2-"])
					else:
						sg.popup('Ingrese valores mayores a 0!',title='')
				except ValueError:
					sg.popup('Ingrese un valor válido!',title='')
	
		window.Close()
	except FileNotFoundError as ex:
		sg.popup("No se encontro el archivo config.json",title='')
	


if __name__ == '__main__':
	sg.theme('BlueMono')
	sg.popup('Por favor ejecute ScrabbleAR.py',title='')


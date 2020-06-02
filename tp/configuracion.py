import PySimpleGUI as sg
import json

def aplicar(vals, punts, cants):
	archivo=open("config.txt","r+")

	config=json.load(archivo)

	config["tiempo_total"] = vals["-tot-"]
	config["tiempo_turno"] = vals["-turn-"]
	config["dificultad"] = vals["-dif-"]
	for p in punts:
		config["puntaje_fichas"][p]=punts[p]
	for c in cants:
		config["cant_fichas"][c]=cants[c]

	archivo.seek(0)
	json.dump(config,archivo)
	archivo.truncate()

	archivo.close()

def restaurar(win):
	archivo=open("config.txt","w")

	puntaje_fichas= { 'A' : 1 ,   'B' : 3 ,   'C' : 2 , 'D' : 2 ,
					'E' : 1 ,   'F' : 4 ,   'G' : 2 , 'H' : 4 ,
					'I' : 1 ,   'J' : 6 , 'K' : 7 , 'L' : 1 ,'LL': 7,
					'M' : 3 ,   'N' : 1 ,'Ñ': 7,   'O' : 1 , 'P' : 3 ,
					'Q' : 7 , 'R' : 1 ,'RR': 7,   'S' : 1 , 'T' : 1 ,
					'U' : 1 ,   'V' : 4 ,   'W' : 7 , 'X' : 7 ,
					'Y' : 4 ,   'Z' : 10 }

	cant_fichas= { 'A' : 15 ,   'B' : 4 ,   'C' : 6 , 'D' : 6 ,
				'E' : 15 ,   'F' : 3 ,   'G' : 3 , 'H' : 3 ,
				'I' : 10 ,   'J' : 3 , 'K' : 1 , 'L' : 6 ,'LL': 1,
				'M' : 4 ,   'N' : 8 ,'Ñ': 1,   'O' : 14 , 'P' : 3 ,
				'Q' : 1 , 'R' : 6 ,'RR': 1,   'S' : 10 , 'T' : 6 ,
				'U' : 10 ,   'V' : 3  ,   'W' : 1 , 'X' : 1 ,
				'Y' : 1 ,   'Z' : 1 }

	j={"tiempo_total":"30","tiempo_turno":"1","dificultad":"Medio","puntaje_fichas":puntaje_fichas,"cant_fichas":cant_fichas}

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


def actualizar_descripcion(win,val):
	if(val["-dif-"]=="Facil"):
		win["-desc-"].update("Facil: sustantivos, adjetivos y verbos. Tablero 15x15.")
	elif (val["-dif-"]=="Medio"):
		win["-desc-"].update("Medio: sustantivos y verbos. Tablero NxN.")
	elif (val["-dif-"]=="Dificil"):
		win["-desc-"].update("Dificil: tipo palabra al azar. Tablero NxN.")

def ventana():

	archivo= open("config.txt","r")

	config= json.load(archivo)

	letras=["A","B","C","D","E","F","G","H","I","J","K","L","LL","M","N","Ñ","O","P","Q","R","RR","S","T","U","V","W","X","Y","Z"]

	layout=[
		[sg.Text("Tiempo: ")],
		[sg.Text("Total "), sg.InputText(config["tiempo_total"],size=(3,1),key="-tot-"), sg.Text("Turno "), sg.InputText(config["tiempo_turno"],size=(3,1),key="-turn-")],
		[sg.Text("Dificultad: ")], 
		[sg.Combo(["Facil","Medio","Dificil"],config["dificultad"], enable_events=True, key="-dif-")],
		[sg.Text("", size=(40,1) , key=("-desc-"))],
		[sg.Text("Puntaje: ")],
		[sg.Text("Letra "),sg.Combo(letras,size=(3,1), enable_events=True, key="-l1-"),sg.Text("Puntos "),sg.InputText("",size=(3,1), enable_events=True, key="-t1-")],
		[sg.Text("Cantidad: ")],
		[sg.Text("Letra "),sg.Combo(letras,size=(3,1), enable_events=True, key="-l2-"),sg.Text("Cantidad "),sg.InputText("",size=(3,1), enable_events=True, key="-t2-")],
		[sg.Button("Aplicar"),sg.Button("Restaurar"),sg.Button("Atras")]
		]

	window= sg.Window("Configuracion",layout)

	archivo.close()

	nuevos_puntajes={}
	nuevas_cantidades={}

	while True:
		evento,valores = window.read()

		if evento == "Aplicar":
			aplicar(valores, nuevos_puntajes, nuevas_cantidades)

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
			nuevos_puntajes[valores["-l1-"]]=valores["-t1-"]

		elif evento == "-t2-":
			nuevas_cantidades[valores["-l2-"]]=valores["-t2-"]


	window.Close()
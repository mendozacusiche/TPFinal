import json
import PySimpleGUI as sg
	
def  ventana ():
	opciones=('Facil','Medio','Dificil')
	layout=[
		[sg.Text('Elija el nivel para ver el TOP TEN: ')],
		[sg.Combo(["Facil","Medio","Dificil"], enable_events=True, key='-dif-')],
		[sg.Listbox( values={}, key='RECORDS', size= (60,10), pad=(0,0))],
		[sg.Button('Salir')]
		]
	window=sg.Window('record',layout)
	while True:
		event,values=window.Read()
		if event == "-dif-":
			imprimir(values["-dif-"],window)
		if event in (None,'Salir'):
			break
	window.close()


def crear():
	datos={'Facil':{},'Medio':{},'Dificil':{}}
	with open('archivos/topten.json','w') as p:
		json.dump(datos,p,indent=4)
	return datos
	
def actualizar(nombre,puntaje,nivel):
	'''actualizo los records en el nivel que corresponda'''
	try:
		with open('archivos/topten.json','r') as p:
			datos=json.load(p)
		if nivel in datos.keys():
			if (nombre in datos[nivel].keys()):
				if puntaje> datos[nivel][nombre]:
					datos[nivel][nombre]=puntaje
			else:
				if (len(datos[nivel])<10):
					datos[nivel][nombre]=puntaje
				else:
					print(len(datos[nivel]))
					minimo=min(datos[nivel], key=datos[nivel].get)
					datos[nivel].pop(minimo)
					datos[nivel][nombre]=puntaje
					
		else :
			datos[nivel]=dic
		guardarDatos(datos)
	except FileNotFoundError:
		sg.popup('No se encontro el archivo topten.json')

def guardarDatos(datos): #no uso manejo de excepciones porque ya las uso cuando lo llamo 
	with open('archivos/topten.json','w') as p:
		json.dump(datos,p,indent=4)

def imprimir(nivel,win):
	try:
		with open('archivos/topten.json','r') as p:
			datos=json.load(p)
		try:
			lista = sorted(datos[nivel].items(), key=lambda x: x[1],reverse=True)
			win['RECORDS'].update(map(lambda x: "{}. {}: {}".format(lista.index(x)+1,x[0], x[1]),lista))
		except KeyError:
			sg.popup('No hay registros del nivel seleccionado')
	except FileNotFoundError:
		sg.popup('No se encontro el archivo topten.json')
		#win.close()#se puede poner o no

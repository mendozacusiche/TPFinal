import json
import PySimpleGUI as sg

def  ventana ():
	opciones=('Facil','Medio','Dificil')
	layout=[
		[sg.Text('Elija el nivel para ver el TOP TEN: ')],
		[sg.Listbox(opciones,size=(15,len(opciones)))],
		[sg.Button('OK')]
		]
	window=sg.Window('record',layout)
	event,values=window.Read()
	if event=='OK':
		#print(values[0][0])
		imprimir(values[0][0])
		window.close()


def crear():
	datos={'Facil':{},'Medio':{},'Dificil':{}}
	with open('topten.txt','w') as p:
		json.dump(datos,p,indent=4)
	return datos
	
def actualizar(dic,nivel):
	'''actualizo los records en el nivel que corresponda'''
	with open('topten.txt','r') as p:
		datos=json.load(p)
	if nivel in datos.keys():
		if  len(datos[nivel])<10 :
			datos[nivel].update(dic)
		elif datos[nivel][datos.keys()[-1]]< dic[1]:
			datos[nivel].pop(datos.keys()[-1])
			datos[nivel]=dic
	else :
		datos[nivel]=dic
	return datos

def guardarDatos(datos):
	with open('topten.txt','w') as p:
		json.dump(datos,p,indent=4)

def imprimir(nivel):
	with open('topten.txt','r') as p:
		datos=json.load(p)
		try:
			print(json.dumps(datos[nivel],indent=4))
		except KeyError:
			print('No hay registros del nivel seleccionado')

#nom='pepe'
#punt=0
#dic={nom:punt}
#nivel='Dificil'
#datos=crear() #ojo que cada vez que ejecuta borra todo
#datos={}
#datos=actualizar(dic,nivel)
#guardarDatos(datos)
#imprimir(nivel)

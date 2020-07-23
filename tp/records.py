import json
import PySimpleGUI as sg
	
def  ventana ():
	opciones=('Facil','Medio','Dificil')
	# frase=''' 1.
 # 2.
 # 3.
 # 4.
 # 5.
 # 6.
 # 7.
 # 8.
 # 9.
# 10.'''
	layout=[
		[sg.Text('Elija el nivel para ver el TOP TEN: ')],
		#[sg.Combo(opciones,key='-dif-')],
		[sg.Listbox(opciones,size=(15,len(opciones))),sg.Button('OK')],
		[sg.Column([sg.Text(str(i+1)+".",font=("Current",8),pad=(0,0))]for i in range(10)),sg.Listbox( values={}, key='RECORDS', size= (60,10), pad=(0,0))],
		#[sg.Text(frase,pad=(0,0),font=('Current',11)),sg.Listbox( values={}, key='RECORDS', size= (60,10),pad=(0,0) )],
		[sg.Button('Salir')]
		]
	window=sg.Window('record',layout)
	while True:
		event,values=window.Read()
		# if event=='-dif-':
			# print(event,values)
			# imprimir(values,window)
		if event=='OK':
			#print(values[0][0])
			imprimir(values[0][0],window)
		if event=='Salir':
			break
	window.close()


def crear():
	datos={'Facil':{},'Medio':{},'Dificil':{}}
	with open('archivos/topten.json','w') as p:
		json.dump(datos,p,indent=4)
	return datos
	
def actualizar(nombre,puntaje,nivel):
	'''actualizo los records en el nivel que corresponda'''
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
				print('hola')
	else :
		datos[nivel]=dic
	guardarDatos(datos)

def guardarDatos(datos):
	with open('archivos/topten.json','w') as p:
		json.dump(datos,p,indent=4)

def imprimir(nivel,win):
	with open('archivos/topten.json','r') as p:
		datos=json.load(p)
	try:
		lista = sorted(datos[nivel].items(), key=lambda x: x[1],reverse=True)
		
		win['RECORDS'].update(map(lambda x: " {}: {}".format(x[0], x[1]),lista))
	except KeyError:
		sg.popup('No hay registros del nivel seleccionado')




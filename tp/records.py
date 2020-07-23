import json
import PySimpleGUI as sg

def  ventana ():
	opciones=('Facil','Medio','Dificil')
	frase='''1.
2.
3.
4.
5.
6.
7.
8.
9.
10.'''
	layout=[
		[sg.Text('Elija el nivel para ver el TOP TEN: ')],
		#[sg.Combo(opciones,key='-dif-')],
		[sg.Listbox(opciones,size=(15,len(opciones))),sg.Button('OK')],
		[sg.Text(frase,pad=(0,0),font=('Current',11)),sg.Listbox( values={}, key='RECORDS', size= (60,10),pad=(0,0) )],
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
			#print(datos[nivel])
		else:
			minimo=min(d, key=d.get)
			datos[nivel].pop(minimo)
			datos[nivel]=dic
		# elif datos[nivel][datos.keys()[-1]]< dic[1]:
			# datos[nivel].pop(datos.keys()[-1])
			# datos[nivel]=dic
	else :
		datos[nivel]=dic
	guardarDatos(datos)

def guardarDatos(datos):
	with open('topten.txt','w') as p:
		json.dump(datos,p,indent=4)

def imprimir(nivel,win):
	with open('topten.txt','r') as p:
		datos=json.load(p)
	try:
		lista = sorted(datos[nivel].items(), key=lambda x: x[1],reverse=True)
		
		# l=[]
		# tup=()
		# for elem in datos[nivel]:
			# tup=(elem,datos[nivel][elem])
			# l.append(tup)
		# num=[]
		# n=1
		# for elem in lista:
			# num.append(str(n))
			# n=n+1
		# num=1
		# for elem in lista:
			# win['RECORDS'].update(str(num)+'. '+elem)
			# num+=1
		
		win['RECORDS'].update(map(lambda x: " {}: {}".format(x[0], x[1]),lista))
	except KeyError:
		sg.popup('No hay registros del nivel seleccionado')

			


#nom='pepe'
#punt=0
#dic={nom:punt}
#nivel='Dificil'
#datos=crear() #ojo que cada vez que ejecuta borra todo
#datos={}
#datos=actualizar(dic,nivel)
#guardarDatos(datos)
#imprimir(nivel)

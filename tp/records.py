import json

#def  ventana ():
#	pass

def crear():
	datos={'Facil':{},'Medio':{},'Dificil':{}}
	with open('topten.txt','w') as p:
		json.dump(datos,p,indent=4)
	return datos
	
def actualizar(dic,nivel):
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
		print(json.dumps(datos,indent=4))
		

#nom='pepe'
#punt=0
#dic={nom:punt}
#nivel='Dificil'
#datos=crear() #ojo que cada vez que ejecuta borra todo
#datos={}
#datos=actualizar(dic,nivel)
#guardarDatos(datos)
#imprimir(nivel)

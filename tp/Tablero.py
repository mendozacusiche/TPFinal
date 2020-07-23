import jugar
import json

class Tablero():
	def __init__(self, nivel):
		'''Seteamos el tamaño por nivel e inicializamos el tablero como vacio'''
		if nivel == "Facil":
			self.__tamanio=23
		elif nivel == "Medio":
			self.__tamanio=19
		else:
			self.__tamanio=15
		self.__letras = [["" for i in range(self.__tamanio)] for j in range(self.__tamanio)]
		self.__confirmadas = [[False for i in range(self.__tamanio)] for j in range(self.__tamanio)]

	def get_tamanio(self):
		return self.__tamanio

	def get_letras(self):
		return self.__letras

	def get_letra(self,x,y):
		return self.__letras[x][y]

	def set_letra(self,l,x,y):
		self.__letras[x][y]=l

	def get_confirmadas(self):
		return self.__confirmadas

	def get_no_confirmadas(self):
		'''con esto se obtienen las casillas no ocupadas por letras a traves de una lista de tuplas'''
		fichas=[]
		for x in range(self.__tamanio):
			for y in range(self.__tamanio):
				if ((not self.__confirmadas[x][y]) and (self.__letras[x][y]!="")):
					fichas.append((x,y))
		return fichas

	def buscar_palabra(self):
		fichas=[]
		for x in range(self.__tamanio):
			for y in range(self.__tamanio):
				if ((not self.__confirmadas[x][y]) and (self.__letras[x][y]!="")):
					fichas.append((self.__letras[x][y],x,y))

		es_palabra=True

		#Verifico que tenga las letras en una sola linea horizontal o vertical
		es_vertical=True
		for i in range(len(fichas)):
			if (fichas[i][1] != fichas[0][1]):
				es_vertical=False
		if not es_vertical:
			es_horizontal=True
			for i in range(len(fichas)):
				if (fichas[i][2] != fichas[0][2]):
					es_horizontal=False

		#Verifico que no tenga espacios
		if(len(fichas)>0):
			if es_vertical:
				fichas=sorted(fichas, key = lambda item: item[2])
				x=fichas[0][2]
				for y in range(len(fichas)):
					if (x != fichas[y][2]):
						es_palabra=False
					x+=1
			elif es_horizontal:
				fichas=sorted(fichas, key = lambda item: item[1])
				y=fichas[0][1] 
				for x in range(len(fichas)):
					if (y != fichas[x][1]):
						es_palabra=False
					y+=1
			else:
				es_palabra=False
		else:
			es_palabra=False

		#Armo la palabra
		if es_palabra:
			palabra=""
			for i in range(len(fichas)):
				palabra=palabra+fichas[i][0]
			palabra=palabra.lower()
		else:
			palabra= "No es palabra"
		
		return palabra

	def confirmar_letras(self):
		puntaje=0
		puntaje_letras={}
		for x in range(self.__tamanio):
			for y in range(self.__tamanio):
				if ((not self.__confirmadas[x][y]) and (self.__letras[x][y]!="")):
					self.__confirmadas[x][y]=True
					letra=self.__letras[x][y]
					print(letra)
					try:
						with open ("archivos/config.json","r") as c:
							config= json.load(c)
						puntaje_letras=config["puntaje_fichas"]
						if letra in puntaje_letras.keys():
							puntaje=puntaje+puntaje_letras[letra]
					except FileNotFoundError as ex:
						print("No se encontro el archivo config.txt")
					#puntaje=calcular_puntaje(letra,puntaje)
		return puntaje 

	def insertar_palabra(self,palabra,window,puntos):
		casillas=[]
		ok=False
		for i in range(self.__tamanio):
			for j in range(self.__tamanio):
				if(not self.__confirmadas[j][i]):
					casillas.append((j,i))
					if(len(casillas)==len(palabra.split())):
						ok=True
						break
				else:
					casillas=[]
			if(ok):
				break
			else:
				casillas=[]

		if(not ok):
			for i in range(self.__tamanio):
				for j in range(self.__tamanio):
					if(not self.__confirmadas[i][j]):
						casillas.append((i,j))
						if(len(casillas)==len(palabra.split())):
							ok=True
							break
					else:
						casillas=[]
				if(ok):
					break
				else:
					casillas=[]

		if(ok):
			i=0
			for c in casillas:
				self.__letras[c[0]][c[1]]=palabra.split()[i]
				window["b_"+str(c[0])+"_"+str(c[1])].update(palabra.split()[i])
				i+=1
			jugar.confirmar(window,self,puntos,True)

		return ok

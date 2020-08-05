from codigos import jugar, Layout
from clases import Fichas, Tablero

class IA():

	def __init__(self,fichas,primer_turno,dificultad,puntos,mi_turno=False,procesando=False):#,cambios_letras=3):
		'''Constructor de la clase IA'''
		self.__fichas=fichas
		self.__mi_turno=mi_turno
		self.__primer_turno=primer_turno
		self.__procesando=procesando
		self.__dificultad=dificultad
		# self.__cambios_letras=cambios_letras
		self.__puntos=puntos
		self.__terminar=False

	def combinaciones(self,combs,pal,marcas,letras,largo):
		'''Busca las combinaciones posibles para armar una palabra con las fichas que tiene en el atril'''
		if (largo>0):
			for i in range(len(letras)):
				if(not marcas[i]):
					marcas[i]=True
					self.combinaciones(combs,pal+letras[i]+" ",marcas,letras,largo-1)
					marcas[i]=False
		else:
			combs.append(pal)

	def buscar_palabra(self):
		'''Busca una palabra válida'''
		palabra=""
		n=len(self.__fichas.get_letras())
		marcas=[False for i in range(n)]
		while(palabra=="" and n>1):
			combs=[]
			self.combinaciones(combs,palabra,marcas,self.__fichas.get_letras(),n)
			for i in range(len(combs)):
				pal=""
				for letra in combs[i].split():
					pal=pal+letra.lower()
				if (jugar.evaluar(pal, self.__dificultad)):
					palabra=combs[i]
					break
			n-=1
		return palabra

	def turno(self,bolsa,window,tablero,jugador,tiempos,tiempo_turno,lista):
		'''Acciones que realiza la IA cuando es su turno'''
		palabra=self.buscar_palabra()
		if (palabra!=""):
			ok = tablero.insertar_palabra(palabra,window,jugador,self,lista)
			#
			if(ok):
				for l in palabra.split():
					i=0
					while((l != self.__fichas.get_letras()[i]) or (self.__fichas.get_usadas()[i])):
						i+=1
					self.__fichas.usar(i)
				if (len(palabra.split())<=jugar.contar_letras_bolsa(bolsa)):
					for i in range(7):
						if (self.__fichas.get_usadas()[i]):
							self.__fichas.set_letra(jugar.sacar_letra_bolsa(bolsa),i)
							self.__fichas.desusar(i)
				else:
					self.__terminar=True
		# else:
			# if self.__cambios_letras > 0:
				# jugar.cambiar_fichas(window,self.__fichas,bolsa,tablero,True)
				# self.__cambios_letras-=1
		self.__procesando=False
		jugar.pasar(jugador,tiempos,tiempo_turno,self)

	def get_procesando(self):
		return self.__procesando

	def set_procesando(self, b):
		self.__procesando=b

	def get_primer_turno(self):
		return self.__primer_turno

	def set_primer_turno(self,b):
		self.__primer_turno=b
		
	def get_mi_turno(self):
		return self.__mi_turno

	def set_mi_turno(self, b):
		self.__mi_turno=b

	def get_fichas(self):
		return self.__fichas

	def get_dificultad(self):
		return self.__dificultad

	def get_puntos(self):
		return self.__puntos

	def set_puntos(self, p):
		self.__puntos=p

	# def get_cambios_letras(self):
		# return self.__cambios_letras

	def get_terminar(self):
		return self.__terminar

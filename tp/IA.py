import jugar, Fichas, Tablero

class IA():

	def __init__(self,bolsa,dificultad):
		nuevas=[]
		for i in range(7):
			l=jugar.sacar_letra_bolsa(bolsa)
			nuevas.append(l)
		self.__fichas=Fichas.Fichas(nuevas)
		self.__mi_turno=False
		self.__dificultad=dificultad
		self.__cambios_letras=3
		self.__puntos=0

	def combinaciones(self,combs,pal,marcas,letras,largo):
		if (largo>0):
			for i in range(len(letras)):
				if(not marcas[i]):
					marcas[i]=True
					self.combinaciones(combs,pal+letras[i]+" ",marcas,letras,largo-1)
					marcas[i]=False
		else:
			combs.append(pal)

	def buscar_palabra(self):
		palabra=""
		marcas=[False for i in range(len(self.__fichas.get_letras()))]
		n=7
		while(palabra=="" and n>0):
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

	def turno(self,bolsa,window,tablero):
		palabra=self.buscar_palabra()

		if (palabra!=""):
			ok, self.__puntos = tablero.insertar_palabra(palabra,window,self.__puntos)
			if(ok):
				for l in palabra.split():
					i=0
					while((l != self.__fichas.get_letras()[i]) or (self.__fichas.get_usadas()[i])):
						i+=1
					self.__fichas.usar(i)
					self.__fichas.set_letra(jugar.sacar_letra_bolsa(bolsa),i)
			for i in range(7):
				self.__fichas.desusar(i)
		else:
			if self.__cambios_letras > 0:
				jugar.cambiar_fichas(window,self.__fichas,bolsa,tablero,True)
				self.__cambios_letras-=1

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

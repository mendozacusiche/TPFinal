if __name__=='codigos.Jugador':
	from codigos import jugar,Fichas
	

class Jugador():

	def __init__ (self,nombre,fichas,mi_turno,primer_turno=True,cambios=3,puntos=0,jugado=False):
		'''Constructor de la clase Jugador'''
		self.__nombre=nombre
		self.__fichas= fichas
		self.__mi_turno=mi_turno
		self.__primer_turno=primer_turno
		self.__cambios=cambios
		self.__puntos=puntos
		self.__jugado=jugado

	def get_nombre(self):
		return self.__nombre

	def get_fichas(self):
		return self.__fichas

	def get_mi_turno(self):
		return self.__mi_turno

	def set_mi_turno(self,mi_turno):
		self.__mi_turno=mi_turno

	def get_primer_turno(self):
		return self.__primer_turno

	def set_primer_turno(self,b):
		self.__primer_turno=b

	def get_cambios(self):
		return self.__cambios

	def set_cambios(self,c):
		self.__cambios=c

	def get_puntos(self):
		return self.__puntos

	def set_puntos(self,puntos):
		self.__puntos=puntos

	def get_jugado(self):
		return self.__jugado

	def set_jugado(self,b):
		self.__jugado=b

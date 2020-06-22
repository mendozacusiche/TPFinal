import jugar, Fichas

class IA():

	def __init__(self,bolsa):
		nuevas=[]
		for i in range(7):
			l=jugar.sacar_letra_bolsa(bolsa)
			nuevas.append(l)
		self.__fichas=Fichas.Fichas(nuevas)
		self.__mi_turno=False

	def turno(self):
		pass

	def get_mi_turno(self):
		return self.__mi_turno

	def set_mi_turno(self, b):
		self.__mi_turno=b

	def get_fichas(self):
		return self.__fichas

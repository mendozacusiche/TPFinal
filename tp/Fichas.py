class Fichas():
	
	def __init__(self, nuevas):
		self.__letras=[]
		self.__usadas=[]
		self.__checked=[]
		for i in range(7):
			self.__letras.append(nuevas[i])
			self.__usadas.append(False)
			self.__checked.append(False)

	def get_letras(self):
		return self.__letras

	def set_letra(self, l, i):
		self.__letras[i] = l

	def get_usadas(self):
		return self.__usadas

	def get_checked(self):
		return self.__checked

	def usar(self, i):
		self.__usadas[i]=True

	def desusar(self, i):
		self.__usadas[i]=False

	def checkear(self, i):
		self.__checked[i]=True

	def descheckear(self, i):
		self.__checked[i]=False

	def descheckear_todas(self, window):
		for i in range(7):
			self.__checked[i]=False
		window["-letra0-"].update(button_color=('white','OrangeRed3'))
		window["-letra1-"].update(button_color=('white','OrangeRed3'))
		window["-letra2-"].update(button_color=('white','OrangeRed3'))
		window["-letra3-"].update(button_color=('white','OrangeRed3'))
		window["-letra4-"].update(button_color=('white','OrangeRed3'))
		window["-letra5-"].update(button_color=('white','OrangeRed3'))
		window["-letra6-"].update(button_color=('white','OrangeRed3'))

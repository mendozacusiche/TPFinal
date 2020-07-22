import PySimpleGUI as sg
import configuracion, jugar
import json

def ventana():
	
	try:
		archivo= open("config.txt","r")
		config= json.load(archivo)
	
		dificultad=config["dificultad"]
		if dificultad=='Facil':
			imag=sg.Image(filename='imagenes/tabfacil.png',key='-imagen-')
			descr="""Nivel fácil: 			
Palabras permitidas: sustantivos, adjetivos y verbos. 
Tamaño del tablero: 23x23."""
		elif dificultad=='Medio':
			imag=sg.Image(filename='imagenes/tabmedio.png',key='-imagen-')
			descr="""Nivel medio: 			
Palabras permitidas: adjetivos y verbos. 
Tamaño del tablero: 19x19."""
		else:
			imag=sg.Image(filename='imagenes/tabdificil.png',key='-imagen-')
			descr="""Nivel dificil: 			
Palabras permitidas: son elegidas al azar entre adjetivos y verbos. 
Tamaño del tablero: 15x15."""

		columna1=[[imag]]
		
		
	except FileNotFoundError as ex:
		print("No se encontro el archivo config.txt")
		columna1=[[sg.Text('No hay tablero actual')]]
				
	columna2=[[sg.Text(descr,key='-descr-',font=("Current",10), size = (30, 0),justification='ljust')],
			[sg.Button('Configuracion',font=("Current",10), size =(29, 0))],
			[sg.Button('Jugar',font=("Current",10), size=(12, 0)), sg.Button('Atras',font=("Current",10), size=(12,0))]
			]
	
	layout=[[sg.Column(columna1),sg.Column(columna2)]]
	
	window=sg.Window('Scrabble',layout)
	

	while True:
		event,values=window.Read()
		
		if (event== 'Jugar'):
			window.close()
			jugar.juego()
		elif (event=='Configuracion'):
			window.Hide()
			configuracion.ventana(window)
			window.UnHide()
		elif (event == sg.WIN_CLOSED or event == "Atras"):
			window.close()
			break

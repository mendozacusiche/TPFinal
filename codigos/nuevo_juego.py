import PySimpleGUI as sg
if __name__ == 'codigos.nuevo_juego':
	from codigos import configuracion, jugar
import json
from tkinter import *

def ventana():	
	'''Creación de la ventana de nuevo juego'''
	try:
		try:
			with open("archivos/config.json","r") as archivo:
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
			sg.popup("No se encontro el archivo config.json",title='')
			columna1=[[sg.Text('No hay tablero actual')]]
			descr='No hay descripción del nivel actual'
		
		columna2=[
				[sg.Text(descr,key='-descr-',font=("Arial Black",10), size = (35, 0), justification='ljust')],
				[sg.Button('Configuración',key='Configuracion',font=("Arial Black",12), size =(29, 0))],
				[sg.Button('Jugar',font=("Arial Black",12), size=(13, 0)), sg.Button('Atrás',key='Atras',font=("Arial Black",12), size=(13,0),pad=(20,0))]
				]
	
		layout=[[sg.Column(columna1),sg.Column(columna2)]]
	
		window=sg.Window('ScrabbleAR',layout)
	
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
	except TclError:
		sg.popup("Lo sentimos a ocurrido un error inesperado",title='')
if __name__ == '__main__':
	sg.theme('BlueMono')
	sg.popup('Por favor ejecute ScrabbleAR.py',title='')

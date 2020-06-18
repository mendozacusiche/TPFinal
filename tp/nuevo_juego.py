import PySimpleGUI as sg
import configuracion, jugar, json


def ventana():
	columna1=[[sg.Text("tablero")]]
				
	columna2=[[sg.Text("descripción configuración predeterminada")],
			[sg.Button('Configuracion')],
			[sg.Button('Iniciar'), sg.Button('Atras')]
			]
	
	layout=[[sg.Column(columna1),sg.Column(columna2)]]
	
	window=sg.Window('Scrabble',layout)
	

	while True:
		event,values=window.Read()
		
		if (event== 'Iniciar'):
			window.close()
			jugar.juego()
		elif (event=='Configuracion'):
			window.Hide()
			configuracion.ventana()
			window.UnHide()
		elif (event == sg.WIN_CLOSED or event == "Atras"):
			window.close()
			break

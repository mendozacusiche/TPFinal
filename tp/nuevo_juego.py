import PySimpleGUI as sg
import configuracion, jugar


def ventana():
	columna1=[[sg.Text("tablero")]]
				
	columna2=[[sg.Text("descripción configuración predeterminada")],
			[sg.Button('Configuracion',font=("Current ",9), size=(29,0))],
			[sg.Button('Jugar',font=("Current ",9),size=(12,0)), sg.Button('Atras',font=("Current ",9), size=(12,0))]
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
			configuracion.ventana()
			window.UnHide()
		elif (event == sg.WIN_CLOSED or event == "Atras"):
			window.close()
			break

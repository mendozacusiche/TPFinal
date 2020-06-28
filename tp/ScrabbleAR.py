import PySimpleGUI as sg
import configuracion, nuevo_juego, records, jugar


def main(args):
	sg.theme('DarkTeal8')

	layout=[[sg.Button('Nuevo Juego',font=("Impact",16))],
			[sg.Button('Cargar Juego',font=("Impact",16))],
			[sg.Button("Records",font=("Impact",16))],
			[sg.Button('Salir',font=("Impact",16))]]
	
	window=sg.Window('Scrabble',layout)
	

	while True:
		event,values=window.Read()
		
		if (event== 'Nuevo Juego'):
			window.Hide()
			nuevo_juego.ventana()
			window.UnHide()
		elif (event=='Cargar Juego'):
			window.Hide()
			#jugar.juego(True)
			window.UnHide()
		elif (event=="Records"):
			window.Hide()
			records.ventana()
			window.UnHide()
		elif (event == sg.WIN_CLOSED or event == "Salir"):
			break
			
	window.close()
	
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

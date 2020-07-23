import PySimpleGUI as sg
import configuracion, nuevo_juego, records, jugar


def main(args):
	#sg.theme('DarkTeal8') #'BlueMono' 'BluePurple' 'DarkAmber'
	sg.theme('BlueMono')
	layout=[[sg.Button('Nuevo Juego',font=("Current",10), size=(20, 0))],
			[sg.Button('Cargar Juego',font=("Current",10), size=(20, 0))],
			[sg.Button("Records",font=("Current",10), size=(20, 0))],
			[sg.Button('Salir',font=("Current",10),size=(20, 0))]]
	
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

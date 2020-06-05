import PySimpleGUI as sg
import configuracion, main2  
import json


def main(args):
	columna1=[[sg.Text("tablero")]]
				
	columna2=[[sg.Text("descripción configuración predeterminada")],
			[sg.Button('Cambiar configuración')],
			[sg.Button('Iniciar Nuevo')],
			[sg.Button('Cargar Juego')],
			[sg.Button('Top Ten')]]
	
	layout=[[sg.Column(columna1),sg.Column(columna2)]]
	
	window=sg.Window('Scrabble',layout)
	

	while True:  #agregue el bucle para que se pueda volver al menu si queremos volver atras
		event,values=window.Read()
		#window.close() #comente esta linea para poder usarla en el elif, aunque crearia conflicto con el if. 
		
		if (event== 'Iniciar Nuevo'):
			window.Hide()
			main2.juego()
			window.UnHide()
			#columna3=[[sg.Text("tablero")]]
			#columna4=[[sg.Text("descripción configuración predeterminada")],
			#		[sg.Button('Confirmar')],
			#		[sg.Button('Cambiar fichas')],
			#		[sg.Button('Top Ten')],
			#		[sg.Button('Terminar')]]
			#layout1=[[sg.Column(columna3),sg.Column(columna4)]]
			#window=sg.Window('Scrabble',layout1)
			#while True:
			#	events,value=window.Read()
			#	if events=='Terminar':
			#		break
		elif (event == 'Cargar Juego'):
			window.Hide()
			main2.juego(True)
			window.UnHide()
		elif (event=='Cambiar configuración'):
			window.Hide()
			configuracion.ventana()
			window.UnHide()
		# elif (event=='Top Ten'):
			# with open('topten.txt','r') as t:
				# datos=json.load(t)
				# print(json.dumps(datos,sort_keys=True,indent=4))	
			
	window.close()
	
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

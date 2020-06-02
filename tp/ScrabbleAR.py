import PySimpleGUI as sg
import configuracion  # importe el .py que hice
import json


def main(args):
	columna1=[[sg.Text("tablero")]]
				
	columna2=[[sg.Text("descripción configuración predeterminada")],
			[sg.Button('Cambiar configuración')],
			[sg.Button('Iniciar')],
			[sg.Button('Top Ten')]]
	
	layout=[[sg.Column(columna1),sg.Column(columna2)]]
	
	window=sg.Window('Scrabble',layout)
	

	while True:  #agregue el bucle para que se pueda volver al menu si queremos volver atras
		event,values=window.Read()
		#window.close() #comente esta linea para poder usarla en el elif, aunque crearia conflicto con el if. 
		
		if (event== 'Iniciar'): #consideraria hacer esta parte en un .py aparte, por el conflicto al modificar window y por legibilidad
			columna3=[[sg.Text("tablero")]]
			columna4=[[sg.Text("descripción configuración predeterminada")],
					[sg.Button('Confirmar')],
					[sg.Button('Cambiar fichas')],
					[sg.Button('Top Ten')],
					[sg.Button('Terminar')]]
			layout1=[[sg.Column(columna3),sg.Column(columna4)]]
			window=sg.Window('Scrabble',layout1)
			while True:
				events,value=window.Read()
				if events=='Terminar':
					break
		elif (event=='Cambiar configuración'):
			window.Hide()
			configuracion.ventana()
			window.UnHide()
			#lay=[[sg.Text('Ingrese que nivel quiere jugar')],
			#	[sg.Combo(['Nivel 1','Nivel 2','Nivel 3'])],
			#	[sg.Button('OK')]]
			#wind=sg.Window('config',lay)
			#event,value=wind.Read()
			#if value=='Nivel 1':
			#	print('abro juego nivel 1')
			#elif value=='Nivel 2':
			#	print('abro juego nivel 2')
			#else:
			#	print( 'abro juego  nivel 3')
		# elif (event=='Top Ten'):
			# with open('topten.txt','r') as t:
				# datos=json.load(t)
				# print(json.dumps(datos,sort_keys=True,indent=4))	
			
	window.close()
	
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
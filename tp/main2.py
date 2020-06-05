import PySimpleGUI as sg
import sys, Tablero_juego

def juego(cargar=False): #hay que agregar en algun lugar despues que pasaria si se pasa como parametro True, que seria agregar las palabras al tablero y cambiar los timers con la informacion del archivo del guardado

	tablero = Tablero_juego.Tablero("Medio", "blue", 15)

	col1 = [
			[sg.Text("00:00"),sg.Text("texto",size=(50,1),justification="center"),sg.Text("0:00")],
			[sg.Column(tablero.columna())]
			]

	layout=[[sg.Column(col1)]]

	if sys.platform == "win32":
		col2= [
				[sg.Text("",pad=(0,10))],
				[sg.Button("Iniciar",size=(15,2),font=("Impact", 12))],
				[sg.Text("",pad=(0,10))],
				[sg.Image(sys.path[0]+"\imagenes\playerlogo.png",pad=(20,5)),sg.Text("9999")],
				[sg.Image(sys.path[0]+"\imagenes\computerlogo.png",pad=(20,5)),sg.Text("9999")],
				[sg.Text("",pad=(0,40))],
				[sg.Button("Confirmar",size=(15,2),font=("Impact", 12))],
				[sg.Button("Pasar",size=(15,2),font=("Impact", 12))],
				[sg.Button("Posponer",size=(15,2),font=("Impact", 12))],
				[sg.Button("Terminar",size=(15,2),font=("Impact", 12))],
				[sg.Text("",pad=(0,30))],
				[sg.Button("Cambiar",size=(15,2),font=("Impact", 12))]
			]		

		layout[0].append(sg.Column(col2))
	elif sys.platform == "linux":
		col2= [
				[sg.Text("",pad=(0,10))],
				[sg.Button("Iniciar",size=(15,2),font=("Impact", 12))],
				[sg.Text("",pad=(0,10))],
				[sg.Image(sys.path[0]+"/imagenes/playerlogo.png",pad=(20,5)),sg.Text("9999")],
				[sg.Image(sys.path[0]+"/imagenes/computerlogo.png",pad=(20,100)),sg.Text("9999")],
				[sg.Text("",pad=(0,40))],
				[sg.Button("Confirmar",size=(15,2),font=("Impact", 12))],
				[sg.Button("Pasar",size=(15,2),font=("Impact", 12))],
				[sg.Button("Posponer",size=(15,2),font=("Impact", 12))],
				[sg.Button("Terminar",size=(15,2),font=("Impact", 12))],
				[sg.Text("",pad=(0,30))],
				[sg.Button("Cambiar",size=(15,2),font=("Impact", 12))]
			]		

		layout[0].append(sg.Column(col2))
	else:
		col2= [
				[sg.Text("",pad=(0,10))],
				[sg.Button("Iniciar",size=(15,2),font=("Impact", 12))],
				[sg.Text("",pad=(0,10))],
				[sg.Text("Player",pad=(20,5)),sg.Text("9999")],
				[sg.Text("Computer",pad=(20,100)),sg.Text("9999")],
				[sg.Text("",pad=(0,40))],
				[sg.Button("Confirmar",size=(15,2),font=("Impact", 12))],
				[sg.Button("Pasar",size=(15,2),font=("Impact", 12))],
				[sg.Button("Posponer",size=(15,2),font=("Impact", 12))],
				[sg.Button("Terminar",size=(15,2),font=("Impact", 12))],
				[sg.Text("",pad=(0,30))],
				[sg.Button("Cambiar",size=(15,2),font=("Impact", 12))]
			]		

		layout[0].append(sg.Column(col2))

	layout.append([sg.Text("Letras en Bolsa: N")])
	
	window = sg.Window('ScrabbleAR', ).Layout(layout).Finalize()



	g = window.FindElement('_GRAPH_')
	tablero.mostrar_tablero(g)
	tablero.diseño_tablero(g)
	tablero.Crear_Matriz()
	matriz = tablero.get_matriz()
	text_box = tablero.get_text_box()
	selected = tablero.get_selected()

	
	Check_box = lambda x,y : g.TKCanvas.itemconfig(matriz[box_y][box_x], fill="#CFF5E3")
	Uncheck_box = lambda x,y: g.TKCanvas.itemconfig(matriz[box_y][box_x], fill="white")
	despintar = lambda x: g.TKCanvas.itemconfig(x, fill="white")
	Check_button = lambda x: window.FindElement(x).Update(button_color=('white','blue'))
	Uncheck_button = lambda x: window.FindElement(x).Update(button_color=('white','green'))
	current_Check_button = ''

	word=''
	tam_celda =25
	button_selected = False
	current_button_selected = ''
	iniciado= False
	while True:
		event, values = window.Read()
		print(values)
		if event == sg.WIN_CLOSED:
			break
		elif event == '_GRAPH_':
			if iniciado: # aca agregue la condicion de que tenga que haberse iniciado previamente para colocar letras
				if values['_GRAPH_'] == (None,None):
					continue
				mouse = values["_GRAPH_"]
				box_x = mouse[0]//tam_celda
				box_y = mouse[1]//tam_celda
				if mouse == (None, None) or box_x > 15 or box_y > 15:
					continue
				if button_selected:
					current_Check_button  = box_x, box_y
					Check_box(box_x, box_y)
					selected[box_x][box_y] = True

					if(text_box[box_x][box_y]== ""):
						text_box[box_x][box_y] = g.DrawText(current_button_selected, (box_x * tam_celda + 18, box_y * tam_celda + 17),font='Courier 12')
						word+=current_button_selected
					else:
		                # aca iria la actualizacion del cuadrado pero no me sale
						print(text_box[box_x][box_y])
						g.TKCanvas.itemconfig(text_box[box_y][box_x],text="")
						print((g.TKCanvas.itemconfigure(text_box[box_y][box_x])))
		elif event == "Iniciar":
			iniciado = True
			#muchas mas cosas tienen que pasar aca, y probablemente lo mejor sea modularizar
		elif event == "Confirmar":
			pass
		elif event == "Pasar":
			pass
		elif event == "Posponer":
			pass
		elif event == "Terminar":
			pass
		elif event == "Cambiar":
			pass
		else:
			if button_selected:
				if event == current_button_selected:
					Uncheck_button(event)
					button_selected = False
					current_button_selected = ''
			else:
				Check_button(event)
				button_selected = True
				current_button_selected = event 
	




	window.Close()

#juego()

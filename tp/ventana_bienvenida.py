import PySimpleGUI as sg 

def ventana(jugador="None"):

  if jugador != "None":
    layout = [
              [sg.Text('Bienvenido a ScrabbleAR! ',size=(40, 1), justification='center', font='Courier 15')],
              [sg.Image(filename='imagenes/icons.png', pad=(215, 0))],
              [sg.Text('Bienvenido de nuevo ',size=(40, 1), justification='center', font='Courier 15')],
              [sg.Ok()]
            ]
    window = sg.Window('ScrabbleAR',element_justification='center', resizable= True).Layout(layout)
    event, values= window.read()
    window.close()

  else:
    layout = [
              [sg.Text('Bienvenido a ScrabbleAR! ',size=(40, 1), justification='center', font='Courier 15')],
              [sg.Image(filename='imagenes/icons.png', pad=(215, 0))],
              [sg.Text('Por favor, introduzca su nombre ',size=(40, 1), justification='center', font='Courier 15')],
              [sg.InputText(size=(50, 1),justification='left', font="Helvetica",key="-Nombre-")],
              [sg.Button('Confirmar'), sg.Button('Salir')],
            ]
    window = sg.Window('ScrabbleAR',element_justification='center', resizable= True).Layout(layout)
    while True:             # Event Loop
        event, values = window.read()
        if event in (None, 'Salir'):
          window.close()
          return jugador
        elif (event =="Confirmar") and (values["-Nombre-"] not in ("","Olvido el nombre!")):
          window.close()
          return values["-Nombre-"]
        else:
          window["-Nombre-"].update("Olvido el nombre!")

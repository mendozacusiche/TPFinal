import PySimpleGUI as sg 

def ventana():
  #sg.theme('Dark Brown 1')
  sg.ChangeLookAndFeel('LightGreen')

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
        return "None"
      elif (event =="Confirmar") and (values["-Nombre-"] not in ("","Olvido el nombre!")):
        window.close()
        return values["-Nombre-"]
      else:
        window["-Nombre-"].update("Olvido el nombre!")

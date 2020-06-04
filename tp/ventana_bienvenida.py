import PySimpleGUI as sg 

#sg.theme('Dark Brown 1')
sg.ChangeLookAndFeel('LightGreen')

layout = [
          [sg.Text('Bienvenido a ScrabbleAR! ',size=(40, 1), justification='center', font='Courier 15')],
          [sg.Image(filename='imagenes/icons.png', pad=(215, 0))],
          [sg.Text('Por favor, introduzca su nombre ',size=(40, 1), justification='center', font='Courier 15')],
          [sg.Text('  '),sg.InputText(size=(50, 1),justification='left', font="Helvetica")],
          [sg.Text(' '*40), sg.Button('Jugar'), sg.Button('Salir')],
        ]
window = sg.Window('ScrabbleAR').Layout(layout)
while True:             # Event Loop
    event, values = window.read()
    if event in (None, 'Salir'):
        break
    else:
         # llama al la ventana  del juego 
         pass
import PySimpleGUI as sg
#import jugar
from codigos import jugar
def sacar_letras( win, jugador):
    ''' saca todas las letras del atril del jugador'''
    fichas = []
    fichas_f = []
    for i in range(7):
        fichas.append(jugador.get_fichas().get_letras()[i])
        fichas_f.append(True)
        win["-letra"+str(i)+"-"].update("")

    return False, fichas, fichas_f

def clickear_ficha(event, jugador, window, win, fichas):
    '''confirma que letras el jugador desea cambiar y preservar en el atril'''
    if event == ("-c0-"):
        window[event].update("?")
        win["-letra0-"].update(jugador.get_fichas().get_letras()[0])
        fichas[0] = False
    elif event == ("-c1-"):
        window[event].update("?")
        win["-letra1-"].update(jugador.get_fichas().get_letras()[1])
        fichas[1] = False
    elif event == ("-c2-"):
        window[event].update("?")
        win["-letra2-"].update(jugador.get_fichas().get_letras()[2])
        fichas[2] = False
    elif event == ("-c3-"):
        window[event].update("?")
        win["-letra3-"].update(jugador.get_fichas().get_letras()[3])
        fichas[3] = False
    elif event == ("-c4-"):
        window[event].update("?")
        win["-letra4-"].update(jugador.get_fichas().get_letras()[4])
        fichas[4] = False
    elif event == ("-c5-"):
        window[event].update("?")
        win["-letra5-"].update(jugador.get_fichas().get_letras()[5])
        fichas[5] = False
    elif event == ("-c6-"):
        window[event].update("?")
        win["-letra6-"].update(jugador.get_fichas().get_letras()[6])
        fichas[6] = False

    return fichas

def unirlis(lista1, listas2):
    '''Une en una tupla las listas de letras y  de booleanos que representan las fichas a cambiar  y conservar en el atril'''
    claves = []
    for i in range(7):
        claves.append((lista1[i], listas2[i]))
    return claves

def ventana(win, jugador ,bolsa, tablero):
    ''' ventana de  Cambiar Fichas'''
    layout = [
              [sg.Text('CAMBIAR LETRAS',size=(40, 1), justification='center', font='Courier 15')],
              [sg.T('has click en las letras que desea conservar', justification='center')],
              [sg.Button(jugador.get_fichas().get_letras()[i], size=(2,1), pad=(1, 0), button_color=('white','#5e82bf'), key=("-c"+str(i)+"-")) for i in range(7)],
              #[sg.Column(lista = crear_botones(win, jugador))],
              #[sg.Button("?",font=("Current",9),size=(2,1), pad=(1, 0), button_color=('white','#5e82bf'), key=("-c"+str(i)+"-")) for i in range(7)],
              [sg.Button('CONFIMAR CAMBIO')]
             ]
    #auto_close_duration = 1,
    window = sg.Window('CAMBIAR LETRAS',element_justification='center', no_titlebar=True, keep_on_top= True).Layout(layout)
    ok = True
    cambio = False
    cambiar_F  = []
    while True:             # Event Loop
        event, values = window.read()
        if ok:
            ok, cambiar_fichas,fichas_b = sacar_letras(win, jugador)
        elif event in ("-c0-", "-c1-", "-c2-", "-c3-", "-c4-", "-c5-", "-c6-"):
            cambiar_F = clickear_ficha(event, jugador, window, win, fichas_b)
            cambio = True
        elif (event =="CONFIMAR CAMBIO"):
            if cambio:
                #entra y cambia las fichas eligidas
                claves = unirlis(cambiar_fichas, cambiar_F)
            else:
                #entra por si cambia todos las fichas
                claves = unirlis(cambiar_fichas, fichas_b)
            #se llama a cambiar fichas de  jugar.py
            jugar.cambiar_fichas(win,jugador,claves,bolsa,tablero)
            # print(claves)
            #window.UnHide()
            break
    window.close()
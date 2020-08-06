import PySimpleGUI as sg
if __name__=='codigos.cambiar_letras':
    from codigos import jugar

def sacar_letras( win, jugador):
    ''' Saca todas las letras del atril del jugador'''
    fichas=[]
    fichas_f=[]
    for i in range(7):
        fichas.append(jugador.get_fichas().get_letras()[i])
        fichas_f.append(True)
        win["-letra"+str(i)+"-"].update("")

    return fichas, fichas_f

def clickear_ficha(event, jugador, window, win, fichas):
    '''Confirma que letras el jugador desea cambiar y preservar en el atril'''
    if event==("-c0-"):
        if(fichas[0]):
            window[event].update("?")
            win["-letra0-"].update(jugador.get_fichas().get_letra(0))
            fichas[0]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(0))
            win["-letra0-"].update("")
            fichas[0]=True
    elif event==("-c1-"):
        if(fichas[1]):
            window[event].update("?")
            win["-letra1-"].update(jugador.get_fichas().get_letra(1))
            fichas[1]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(1))
            win["-letra1-"].update("")
            fichas[1]=True
    elif event==("-c2-"):
        if(fichas[2]):
            window[event].update("?")
            win["-letra2-"].update(jugador.get_fichas().get_letra(2))
            fichas[2]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(2))
            win["-letra2-"].update("")
            fichas[2]=True
    elif event==("-c3-"):
        if(fichas[3]):
            window[event].update("?")
            win["-letra3-"].update(jugador.get_fichas().get_letra(3))
            fichas[3]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(3))
            win["-letra3-"].update("")
            fichas[3]=True
    elif event==("-c4-"):
        if(fichas[4]):
            window[event].update("?")
            win["-letra4-"].update(jugador.get_fichas().get_letra(4))
            fichas[4]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(4))
            win["-letra4-"].update("")
            fichas[4]=True
    elif event==("-c5-"):
        if(fichas[5]):
            window[event].update("?")
            win["-letra5-"].update(jugador.get_fichas().get_letra(5))
            fichas[5]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(5))
            win["-letra5-"].update("")
            fichas[5]=True
    elif event==("-c6-"):
        if(fichas[6]):
            window[event].update("?")
            win["-letra6-"].update(jugador.get_fichas().get_letra(6))
            fichas[6]=False
        else:
            window[event].update(jugador.get_fichas().get_letra(6))
            win["-letra6-"].update("")
            fichas[6]=True

def unirlis(lista1, listas2):
    '''Une en una tupla las listas de letras y  de booleanos que representan las 
    fichas a cambiar  y conservar en el atril.'''
    claves=[]
    for i in range(7):
        claves.append((lista1[i], listas2[i]))
    return claves

def devolver(win,jugador):
    for i in range(7):
        win["-letra"+str(i)+"-"].update(jugador.get_fichas().get_letra(i))

def ventana(win, jugador ,bolsa, tablero):
    ''' Ventana de cambiar_letras'''
    layout = [
              [sg.Text('CAMBIAR LETRAS',size=(40, 1), justification='center', font='Courier 15')],
              [sg.T('Haga click en las letras que desea conservar', justification='center')],
              [sg.Button(jugador.get_fichas().get_letras()[i], size=(2,1), pad=(1, 0), button_color=('white','#5e82bf'), key=("-c"+str(i)+"-")) for i in range(7)],
              [sg.Button('CONFIRMAR CAMBIO')]
             ]
    window=sg.Window('CAMBIAR LETRAS',element_justification='center', keep_on_top= True).Layout(layout)

    ok=False
    cambiar_fichas,fichas_b=sacar_letras(win, jugador)

    while True:             # Event Loop
        event, values=window.read()
        if event==None:
            if not ok:
                devolver(win,jugador)
            break
        elif event in ("-c0-", "-c1-", "-c2-", "-c3-", "-c4-", "-c5-", "-c6-"):
            clickear_ficha(event, jugador, window, win, fichas_b)
        elif (event=="CONFIRMAR CAMBIO"):
            claves=unirlis(cambiar_fichas, fichas_b)
            jugar.cambiar_fichas(win,jugador,claves,bolsa,tablero)
            ok=True
            break
    window.close()
    return ok


if __name__=='__main__':
    sg.theme('BlueMono')
    sg.popup('Por favor ejecute ScrabbleAR.py',title='')

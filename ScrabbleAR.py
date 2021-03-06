import PySimpleGUI as sg
import os
from codigos import configuracion,nuevo_juego,jugar,records


def main(args):
    '''Bienvenidos al ScrabbleAR'''
    
    '''Programa principal'''
    
    sg.theme('BlueMono')
    layout=[[sg.Button('Nuevo Juego',font=("Arial Black",12), size=(20, 0))],
            [sg.Button('Cargar Juego',font=("Arial Black",12), size=(20, 0), disabled=True)],
            [sg.Button("Records",font=("Arial Black",12), size=(20, 0))],
            [sg.Button('Salir',font=("Arial Black",12),size=(20, 0))]]
    if os.path.isfile("archivos/guardado.json"):  #si existe un juego guardado se habilita el botón cargar juego
        layout[1]=[sg.Button('Cargar Juego',font=("Arial Black",12), size=(20, 0), disabled=False)]

    window=sg.Window('Scrabble',layout)

    while True:
        event,values=window.Read()

        if (event== 'Nuevo Juego'):
            window.Hide()
            nuevo_juego.ventana()
            if os.path.isfile("archivos/guardado.json"):
                window["Cargar Juego"].update(disabled=False)  #si luego de jugar se guarda la partida se habilita el botón Cargar Juego
            window.UnHide()
        elif (event=='Cargar Juego'):
            window.Hide()
            jugar.juego(True)
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

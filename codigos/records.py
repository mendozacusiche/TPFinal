import json
import PySimpleGUI as sg
    
def  ventana ():
    '''Creación de la ventana de los records'''
    opciones=('Facil','Medio','Dificil')
    layout=[
        [sg.Text('Elija el nivel para ver el TOP TEN: ')],
        [sg.Combo(["Facil","Medio","Dificil"], enable_events=True, key='-dif-')],
        [sg.Listbox( values={}, key='RECORDS', size= (60,10), pad=(0,0))],
        [sg.Button('Salir')]
        ]
    window=sg.Window('record',layout)
    while True:
        event,values=window.Read()
        if event=="-dif-":
            imprimir(values["-dif-"],window)
        if event in (None,'Salir'):
            break
    window.close()


def actualizar(nombre,puntaje,nivel,fecha):
    '''actualizo los records en el nivel que corresponda'''
    try:
        with open('archivos/topten.json','r') as p:
            datos=json.load(p)
        f='{}/{}/{}'.format(fecha.day,fecha.month,fecha.year)
        if nivel in datos.keys():
            if (nombre in datos[nivel].keys()):
                if puntaje> datos[nivel][nombre][0]:
                    datos[nivel][nombre]=(puntaje,f)
            else:
                if (len(datos[nivel])<10):
                    datos[nivel][nombre]=(puntaje,f)
                else:
                    minimo=min(datos[nivel], key=datos[nivel].get)
                    if puntaje>datos[nivel][minimo][0]:
                        datos[nivel].pop(minimo)
                        datos[nivel][nombre]=(puntaje,f)
                    
        else :
            datos_nivel={nombre:(puntaje,f)}
            datos[nivel]=datos_nivel
        guardarDatos(datos)
    except FileNotFoundError:
        sg.popup('No se encontro el archivo topten.json')

def guardarDatos(datos):   #no uso manejo de excepciones porque ya las uso cuando lo llamo 
    '''Guardo los datos en topten.son que fueron generados en actualizar, ya 
    que es el método que llama a guardarDatos.'''
    with open('archivos/topten.json','w') as p:
        json.dump(datos,p,indent=4)

def imprimir(nivel,win):
    '''Imprimo el registro de records del nivel seleccionado en la ventana '''
    try:
        with open('archivos/topten.json','r') as p:
            datos=json.load(p)

        try:
            lista=sorted(datos[nivel].items(), key=lambda x: x[1][0],reverse=True)

            win['RECORDS'].update(map(lambda x: "{}. {} {}: {}".format(lista.index(x)+1,x[1][1],x[0], x[1][0]),lista))
        except KeyError:
            sg.popup('No hay registros del nivel seleccionado')
    except FileNotFoundError:
        sg.popup('No se encontro el archivo topten.json')
        
if __name__=='__main__':
    sg.theme('BlueMono')
    sg.popup('Por favor ejecute ScrabbleAR.py',title='')

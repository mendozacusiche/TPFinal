class Tablero():

    
    def __init__(self, nivel, color, tamanio):
       
        self.__tamanio  = tamanio
        self.__nivel = nivel
        self.__color = color
        self.__matriz=[]
        self.__selected=[]
        self.__text_box=[]
        
    def Crear_Matriz(self):
        
        for i in range(0, self.__tamanio):
            self.__matriz.append([0]* self.__tamanio)
            self.__selected.append([False]*self.__tamanio)
            self.__text_box.append([""]*self.__tamanio)
    
    def get_matriz(self):
        return self.__matriz
    
    def get_selected(self):
        return self.__selected
 
    def get_text_box(self):
        return self.__text_box
            
    def columna(self, sg, a):
        
        columna_1 = [
                    [sg.Button("#", pad=(20, 0), button_color=('white','OrangeRed3')) for i in a],
                    [sg.Graph((500,500),(0,385),(385,0), key='_GRAPH_', background_color='grey70',change_submits=True, drag_submits=False)],
                    [sg.Button(i, pad=(20, 0), button_color=('white','OrangeRed3')) for i in a]
                 ]
        
        return columna_1
            
        
    def mostrar_tablero(self, obj):
        BOX_SIZE = 25
        
        for row in range(0, self.__tamanio):
            for col in range(0, self.__tamanio):

                obj.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3),line_color='yellow' ,fill_color='SkyBlue3')
 
 
    def diseño_tablero(self, obj):
        BOX_SIZE = 25
        diag = self.__tamanio -1
        
        for row in range(0, self.__tamanio):
            for col in range(0, self.__tamanio): 
                if row == col:
                    obj.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3),line_color='yellow' ,fill_color='IndianRed1')
                
                if (col == diag):
                    obj.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3),line_color='yellow' ,fill_color='IndianRed1')
                    diag -= 1
                    

                if (row % 7 == 0) and (col % 7 == 0):
                    obj.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3),line_color='yellow' ,fill_color='medium sea green')
               
    def imprimir(self):

        print("Color: {} Nivel del juego: {}".format(self.__color, self.__nivel))
        
    
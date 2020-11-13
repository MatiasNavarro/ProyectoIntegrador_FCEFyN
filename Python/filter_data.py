"""
Obtiene informacion relevante de la RdP. Luego de haber convertido los archivos extraidos del Petrinator 
se analizan en este script para obtener: 
    - Cantidad estados
    - Cantidad plazas
    - Cantidad transiciones
    - Matriz [estados x transiciones]
    - Matriz [estados x plazas]
    - Estados en deadlock


Autores: 
- Izquierdo, Agustina Nahir
- Navarro, Matias Alejandro 
- Salvatierra, Andres
"""

import numpy as np
import os

def main():
    """
    Obtiene informacion relevante de la RdP. \n 

    Returns \n
    -------
        Cantidad estados
        Cantidad plazas
        Cantidad transiciones
        Matriz [estados x transiciones]
        Matriz [estados x plazas]
        Estados en deadlock
    """
    cantidad_estados=0
    cantidad_transiciones=0
    cantidad_plazas=0
    state_file = open("./state.txt","r")
    filtrado_prueba_file = open ("filtrado_prueba.txt", "w")
    plaza_tmp_file = open("plaza.txt","w")

    #Obtenemos la cantidad de estados y filtramos la informacion
    for lineas in state_file.readlines() :
        if(len(lineas)>2):
            if(lineas.find("R")!=-1): #Estado
                indice = lineas.find("S")
                estado = lineas[indice:lineas.find(" [")]
                cantidad_estados = cantidad_estados +1
                indice = lineas.find("[")
                plaza_tmp_file.write(lineas[indice+1:lineas.find("]")] + "\n") #Nos quedamos con el marcado para ese estado
                filtrado_prueba_file.write(estado)
                filtrado_prueba_file.write("\n")
            elif (lineas.find("D")!=-1): #Deadlock
                indice = lineas.find("S")
                estado = lineas[indice:lineas.find(" [")]
                cantidad_estados=cantidad_estados +1
                filtrado_prueba_file.write(estado)
                filtrado_prueba_file.write("\n")
                indice = lineas.find("[")
                plaza_tmp_file.write(lineas[indice+1:lineas.find("]")] + "\n") #Nos quedamos con el marcado para ese estado
            elif (lineas.find("p")!=-1 or lineas.find("t")!=-1):   
                if(lineas.find("p")!=-1): #Obtenemos el numero de plazas
                    cantidad_plazas= int(lineas[lineas.find("p ")+1:lineas.find("\n")])
                else:                     #Obtenemos el numero de transiciones
                    cantidad_transiciones= int(lineas[lineas.find("t ")+1:lineas.find("\n")])
            else:   
                indice = lineas.find("T")
                transicion=lineas[indice:lineas.find(" [")]
                transicion=transicion.replace(" => "," ")
                filtrado_prueba_file.write(transicion)
                filtrado_prueba_file.write("\n")


    #Cierre de archivos
    state_file.close()
    filtrado_prueba_file.close()
    plaza_tmp_file.close()

    #Matriz de estados-transiciones
    matriz_es_tr = np.zeros((cantidad_estados,cantidad_transiciones)) - 1

    #Matriz de estados-plazas (Marcado)
    plaza_file = open('plaza.txt', 'r')
    matriz_es_pl = np.loadtxt('plaza.txt',delimiter=", ",dtype=int)
    plaza_file.close

    #Elimina archivo temporal
    os.remove("plaza.txt")

    """
    Inicializacion de matriz a partir de la información filtrada de la RdP.
    Cargando en la misma, para cada Estado(fila) en su respectiva interseccion con Transicion(columna)
    el estado siguiente al que se llega a partir del disparo de dicha transicion.
    Con: 
        un -1 si la transicion no esta sensibilizada para dicho estado,
        el estado_siguiente(nro!=-1) al que se llega a partir del disparo
    
    Ademas se detectan aquellos estados que poseen Deadlock

    Apertura de archivo ya filtrado segun nuestro interes de detectar caminos que lleven al Deadlock
    luego el archivo se cierra para evitar inconvenientes.
    """
    
    archivo = open("./filtrado_prueba.txt","r")
    cont_estados=0
    maq_estado = 0
    flag_deadlock = 1


    for lineas in archivo.readlines() :
        if(maq_estado==0):        
            if(lineas.find("S")!=-1):
                maq_estado=1             
        else:
            if(lineas.find("T")!=-1):
                indice_t=lineas[lineas.find("T")+1:lineas.find(" ")]
                indice_s=lineas[lineas.find("S")+1:lineas.find("\n")]
                matriz_es_tr[cont_estados][int(indice_t)-1]=int(indice_s)
                flag_deadlock=0
            else:
                maq_estado=0 #Fin de codigo
                if(lineas.find("S")!=-1):
                    maq_estado=1
                if(cont_estados!=cantidad_estados):
                    cont_estados=cont_estados+1

    archivo.close()

    state_deadlock = []

    #Nos quedamos con los estados que estan en deadlock
    archivo = open("./deadlock.txt","r")

    for lineas in archivo.readlines():
        indice=lineas.find("S")
        if(indice!=-1):
            state_deadlock.append(int(lineas[indice+1:len(lineas)]))

    return cantidad_estados, cantidad_plazas, cantidad_transiciones, matriz_es_tr, matriz_es_pl, state_deadlock
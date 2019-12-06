import os
import numpy as np
import time

def fun_deadlock (matriz,estado,cantidad_estados,cantidad_transiciones):
    """ Apartir de matriz de Estados x Transiciones = [proximo estado(Tx)] 
        se inicia la busqueda recursiva de disparos que llevan a Deadlock 
        editando dichos valores en la matriz con un valor de -1, de esta forma
        se deshabilitan impidiendo llegar al estado de bloqueo.
    Parametros: \n
        matriz -- EstadosxTransiciones = [proximo estado en funcion de la transicion que se dispara(Tx)].
        estado -- Estado que posee Deadlock.
        cantidad_estados -- cantidad de estados que posee dicha RdP.
        cantidad_transiciones -- cantidad de transiciones que posee la RdP."""
    
    for i in range (0,cantidad_estados):
        cont_transiciones=0
        flag_path_deadlock=0

        for j in range (0,cantidad_transiciones):
            if(matriz[i][j]==estado):
                flag_path_deadlock=1
                matriz[i][j]=-1

            if(matriz[i][j]!=-1):
                cont_transiciones=cont_transiciones+1
                
        if(cont_transiciones==0 and flag_path_deadlock==1):
            fun_deadlock(matriz,i,cantidad_estados,cantidad_transiciones)       
            #print("Post recursion",estado)

#Apertura de archivos resultantes de la conversion de archivos .html to .txt 
# obtenidos del SW Petrinator, para su siguiente manipulacion y filtrado.
archivo = open("./state.txt","r")
f = open ("filtrado_prueba.txt", "w")


# Inicializacion de parametros globales
cantidad_estados=0
cantidad_transiciones=8

#Obtenemos la cantidad de estados y filtramos la informacion
for lineas in archivo.readlines() :
    if(len(lineas)>2):
        if(lineas.find("R")!=-1):
            indice = lineas.find("S")
            estado = lineas[indice:lineas.find(" [")]
            cantidad_estados = cantidad_estados +1
            f.write(estado)
            f.write("\n")
        elif (lineas.find("D")!=-1):
            indice = lineas.find("S")
            estado = lineas[indice:lineas.find(" [")]
            cantidad_estados=cantidad_estados +1
            f.write(estado)
            f.write("\n")
        else:
            indice = lineas.find("T")
            transicion=lineas[indice:lineas.find(" [")]
            transicion=transicion.replace(" => "," ")
            f.write(transicion)
            f.write("\n")

#Cierre de archivos
archivo.close()
f.close()

#Matriz de estados-transiciones
matriz =np.zeros((cantidad_estados,cantidad_transiciones)) - 1

#Inicializacion de matriz a partir de la información filtrada de la RdP.
#Cargando en la misma, para cada Estado(fila) en su respectiva interseccion con Transicion(columna)
#el estado siguiente al que se llega a partir del disparo de dicha transicion.
#Con: 
#   un -1 si la transicion no esta sensibilizada para dicho estado,
#   el estado_siguiente(nro!=-1) al que se llega a partir del disparo
#
# Ademas se detectan aquellos estados que poseen Deadlock

#Apertura de archivo ya filtrado segun nuestro interes de detectar caminos que lleven al Deadlock
#luego el archivo se cierra para evitar inconvenientes.
archivo = open("./filtrado_prueba.txt","r")

cont_estados=0
maq_estado = 0
flag_deadlock = 1
state_deadlock = []

for lineas in archivo.readlines() :

    if(maq_estado==0):        
        if(lineas.find("S")!=-1):
            maq_estado=1             
    else:
        if(lineas.find("T")!=-1):
           indice_t=lineas[lineas.find("T")+1:lineas.find(" ")]
           indice_s=lineas[lineas.find("S")+1:lineas.find("\n")]
           matriz[cont_estados][int(indice_t)-1]=int(indice_s)
           flag_deadlock=0
        else:
            maq_estado=0 #Fin de codigo
            if(flag_deadlock==1):
                state_deadlock.append(cont_estados)
            if(lineas.find("S")!=-1):
                maq_estado=1
                flag_deadlock = 1
            if(cont_estados!=cantidad_estados):
                cont_estados=cont_estados+1

archivo.close()

# print("Estados con deadlock",state_deadlock)
# print("\n")
# print("Estados alcanzables a partir de las respectivas transiciones:")
# print("Transiciones sensibilizadas con deadlock")
# print(matriz)
# print("\n")

#Llamada recursiva a fun_deadlock en busqueda de caminos que dirigen al deadlock
for i in range (0, len(state_deadlock)):
    fun_deadlock(matriz,state_deadlock[i],cantidad_estados,cantidad_transiciones)

# print("Estados alcanzables a partir de las respectivas transiciones, sin deadlock")
# print (matriz)
# print("\n")

#Obtencion final de la matriz con los respectivos vectores de sensibilizado por cada estado
for i in range (0,cantidad_estados):
    for j in range (0,cantidad_transiciones):
        if(matriz[i][j]==-1):
            matriz[i][j]=0
        else:
            matriz[i][j]=1
%time 
#Almacenamiento de matriz final en un archivo .txt y posterior cierre del mismo evitando inconvenientes
f = open("matriz.txt","w")
for i in range (0,cantidad_estados):
    f.write("[  ")
    for j in range (0,cantidad_transiciones):
        f.write(str(int(matriz[i][j])))
        f.write("  ")
    f.write("] \n")
f.close()
os.remove("filtrado_prueba.txt")

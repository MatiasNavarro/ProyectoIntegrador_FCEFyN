import os
import numpy as np
import time
import re
import sys

def fun_deadlock (matriz_es_tr,estado,cantidad_estados,cantidad_transiciones):
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
            if(matriz_es_tr[i][j]==estado):
                flag_path_deadlock=1
                matriz_es_tr[i][j]=-1

            if(matriz_es_tr[i][j]!=-1):
                cont_transiciones=cont_transiciones+1
                
        if(cont_transiciones==0 and flag_path_deadlock==1):
            fun_deadlock(matriz_es_tr,i,cantidad_estados,cantidad_transiciones)       
            #print("Post recursion",estado)

def fun_sifones(estado,matriz_sifones,matriz_es_pl,cantidad_sifones,cantidad_plazas):
    """ Apartir de matriz de Estados x Plazas = [Marcado] 
        se recorre la fila de la matriz donde se encuentra el estado deadlock, 
        colocando un "1" en aquellas plazas donde el marcado sea >=1.
        Se realiza un and entre esa fila de la matriz y el sifon, si la and = 0 implica que ese sifon
        se encuentra vacio para ese estado de deadlock.
    Parametros: \n
        estado -- Estado que posee Deadlock.
        matriz_sifones -- [Marcado de plazas que componen el sifon]
        matriz_es_pl -- EstadosxPlazas = [Marcado para ese estado].
        cantidad_plazas -- cantidad de plazas que posee la RdP.
        cantidad_estados -- cantidad de estados que posee dicha RdP."""

    print("Sifones que no se cumplen en el estado deadlock ",estado,"\n")
    aux=np.zeros(cantidad_plazas)
    for j in range(0,cantidad_plazas):
        if(matriz_es_pl[estado][j]>=1):
            aux[j]=1
 
    for i in range(0,cantidad_sifones):
        cont=0
        for j in range(0,cantidad_plazas):
            if(int(matriz_sifones[i][j] and aux[j])==1):
                cont=cont+1
        if(cont==0):
            print("Sifon numero",i)
            print(matriz_sifones[i])
        


#Apertura de archivos resultantes de la conversion de archivos .html to .txt 
# obtenidos del SW Petrinator, para su siguiente manipulacion y filtrado.
state_file = open("./state.txt","r")
filtrado_prueba_file = open ("filtrado_prueba.txt", "w")
plaza_tmp_file = open("plaza.txt","w")

# Inicializacion de parametros globales
cantidad_estados=0
cantidad_transiciones=0 #Panama 14,21,22,32
cantidad_plazas=0       #Prueba2 4,4,1,1
cantidad_sifones=74      #POPN 20,26,74,130
cantidad_traps=130

#Obtenemos la cantidad de estados y filtramos la informacion
for lineas in state_file.readlines() :
    if(len(lineas)>2):
        if(lineas.find("R")!=-1):
            indice = lineas.find("S")
            estado = lineas[indice:lineas.find(" [")]
            cantidad_estados = cantidad_estados +1
            indice = lineas.find("[")
            plaza_tmp_file.write(lineas[indice+1:lineas.find("]")] + "\n") #Nos quedamos con el marcado para ese estado
            filtrado_prueba_file.write(estado)
            filtrado_prueba_file.write("\n")
        elif (lineas.find("D")!=-1):
            indice = lineas.find("S")
            estado = lineas[indice:lineas.find(" [")]
            cantidad_estados=cantidad_estados +1
            filtrado_prueba_file.write(estado)
            filtrado_prueba_file.write("\n")
            indice = lineas.find("[")
            plaza_tmp_file.write(lineas[indice+1:lineas.find("]")] + "\n") #Nos quedamos con el marcado para ese estado
        elif (lineas.find("p")!=-1 or lineas.find("t")!=-1):    #VER
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
matriz_es_tr =np.zeros((cantidad_estados,cantidad_transiciones)) - 1

#Matriz de estados-plazas
plaza_file = open('plaza.txt', 'r')
matriz_es_pl = np.loadtxt('plaza.txt',delimiter=", ",dtype=int)
plaza_file.close
#Elimina archivo temporal
os.remove("plaza.txt")

#print (matriz_es_pl)

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
           matriz_es_tr[cont_estados][int(indice_t)-1]=int(indice_s)
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

#print("Estados con deadlock",state_deadlock)
# print("\n")
# print("Estados alcanzables a partir de las respectivas transiciones:")
# print("Transiciones sensibilizadas con deadlock")
# print(matriz)
# print("\n")

#Creamos la matriz que representa por fila la cantidad de sifones o traps y por columna plazas
#hay un 1 en las plazas que conforman esos sifones o traps
matriz_sifones =np.zeros((cantidad_sifones,cantidad_plazas))
matriz_traps =np.zeros((cantidad_traps,cantidad_plazas))

#Flag en 0 significa que es trap, en 1 que es un sifon
flag_siphones=0
sifones_file = open("./siphons_traps.txt","r")
indice_sifon=-1
indice_traps=-1

#Llena las matrices de sifones y traps
for lineas in sifones_file.readlines() :
    if(len(lineas)>2):
        if(lineas.find("siphons")!=-1):
            flag_siphones=1
        elif(lineas.find("traps")!=-1):
            flag_siphones=0
        else:
            if(flag_siphones==1):
                inicio=lineas.find("\n")
                indice_sifon=indice_sifon+1
                for i in range (0,inicio+1):
                    if(lineas[i].find("P")!=-1):
                        indice1=i
                    if(lineas[i].find(" ")!=-1 or lineas[i].find("\n")!=-1):
                        indice2=i
                        matriz_sifones[indice_sifon][int(lineas[indice1+1:indice2])-1]=1
            if(flag_siphones==0):
                inicio=lineas.find("\n")
                indice_traps=indice_traps+1
                for i in range (0,inicio+1):
                    if(lineas[i].find("P")!=-1):
                        indice1=i
                    if(lineas[i].find(" ")!=-1 or lineas[i].find("\n")!=-1):
                        indice2=i
                        matriz_traps[indice_traps][int(lineas[indice1+1:indice2])-1]=1

sifones_file.close()

#Llamada recursiva a fun_deadlock en busqueda de caminos que dirigen al deadlock
for i in range (0, len(state_deadlock)):
    fun_deadlock(matriz_es_tr,state_deadlock[i],cantidad_estados,cantidad_transiciones)
    fun_sifones(state_deadlock[i],matriz_sifones,matriz_es_pl,cantidad_sifones,cantidad_plazas)
# print("Estados alcanzables a partir de las respectivas transiciones, sin deadlock")
# print (matriz)
# print("\n")

#Obtencion final de la matriz con los respectivos vectores de sensibilizado por cada estado
for i in range (0,cantidad_estados):
    for j in range (0,cantidad_transiciones):
        if(matriz_es_tr[i][j]==-1):
            matriz_es_tr[i][j]=0
        else:
            matriz_es_tr[i][j]=1

#Almacenamiento de matriz final en un archivo .txt y posterior cierre del mismo evitando inconvenientes
f = open("matriz_es_tr.txt","w")
for i in range (0,cantidad_estados):
    f.write("[  ")
    for j in range (0,cantidad_transiciones):
        f.write(str(int(matriz_es_tr[i][j])))
        f.write("  ")
    f.write("] \n")
f.close()

#Elimina archivo temporal
os.remove("filtrado_prueba.txt")
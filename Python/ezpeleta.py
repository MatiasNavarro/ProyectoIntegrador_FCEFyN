import os
import numpy as np
import time
import re
import sys

# Inicializacion de parametros globales
cantidad_estados=0
cantidad_transiciones=0 #Panama 14,21,22,32
cantidad_plazas=0       #Prueba2 4,4,1,1
cantidad_sifones=22      #POPN 20,26,74,130
cantidad_traps=32        #Prueba3 8,7,2,1

def supervisor(sifon):
    #Marcado del supervisor
    print("Marcado del supervisor",sifon[2]-1) #Es la posicion 2 debido que el sifon esta declarado estado deadlock[0], numero sifon[1], marcado sifon[2]

    #Transiciones que salen del estado idle, le quitan tokens a los supervisores
    #estas se encuentran en el estado inicial (0) y son las transiciones
    #que son distintan de -1 en la matriz matriz_es_tr (estado-transicion)
    for ii in range(cantidad_transiciones):
        if(matriz_es_tr[0][ii]!=-1):
            print("Transicion: ",ii+1)


def fun_sifones_deadlock(estado,matriz_sifones,matriz_es_pl,idle):
    """ Devuelve los sifones que se vacian en ese estado de deadlock
        Apartir de matriz de Estados x Plazas = [Marcado] 
        se recorre la fila de la matriz donde se encuentra el estado deadlock, 
        colocando un "1" en aquellas plazas donde el marcado sea >=1.
        Se realiza un and entre esa fila de la matriz y el sifon, si la and = 0 implica que ese sifon
        se encuentra vacio para ese estado de deadlock.
    Parametros: \n
        estado -- Estado que posee Deadlock.
        matriz_sifones -- [Marcado de plazas que componen el sifon]
        matriz_es_pl -- EstadosxPlazas = [Marcado para ese estado]."""

    print("Sifones que no se cumplen en el estado deadlock ",estado)
    aux=np.zeros(cantidad_plazas)
    flag_sifon_idle=0
    for j in range(0,cantidad_plazas):
        if(matriz_es_pl[estado][j]>=1): #Obtenemos las plazas(marcadas) del estado deadlock
            aux[j]=1

    for i in range(0,cantidad_sifones):
        cont=0
        for j in range(0,cantidad_plazas):
            if(int(matriz_sifones[i][j] and aux[j])==1): 
                cont=cont+1             #Si el contador es distinto de cero, el sifon no esta vacio
        if(cont==0):
            marcado=0
            print("Sifon numero",i,matriz_sifones[i])
            for j in range(0,cantidad_plazas):
                if(matriz_sifones[i][j]==1):
                    marcado=marcado+matriz_es_pl[0][j] #Es 0 en fila, porque es el estado inicial en el que se encontraban las plazas de los sifones
            if(idle==0):
                for jj in range(0,len(sifon_idle)):
                    if(sifon_idle[jj]==i): #El sifon vacio en deadlock esta vacio en idle?
                        flag_sifon_idle=1
                if(flag_sifon_idle==0): #El sifon no estaba vacio en idle
                    sifon_deadlock.append([estado,i,marcado]) #Devuelve el sifon y su marcado inicial, para ese estado deadlock
            else:
                sifon_idle.append[i]

#Apertura de archivos resultantes de la conversion de archivos .html to .txt 
# obtenidos del SW Petrinator, para su siguiente manipulacion y filtrado.
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
matriz_es_tr =np.zeros((cantidad_estados,cantidad_transiciones)) - 1

#Matriz de estados-plazas (Marcado)
plaza_file = open('plaza.txt', 'r')
matriz_es_pl = np.loadtxt('plaza.txt',delimiter=", ",dtype=int)
plaza_file.close

#Elimina archivo temporal
os.remove("plaza.txt")

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
                length=lineas.find("\n")
                indice_sifon=indice_sifon+1
                for i in range (0,length+1):
                    if(lineas[i].find("P")!=-1):
                        indice1=i
                    if(lineas[i].find(" ")!=-1 or lineas[i].find("\n")!=-1):
                        indice2=i
                        matriz_sifones[indice_sifon][int(lineas[indice1+1:indice2])-1]=1
            if(flag_siphones==0):
                length=lineas.find("\n")
                indice_traps=indice_traps+1
                for i in range (0,length+1):
                    if(lineas[i].find("P")!=-1):
                        indice1=i
                    if(lineas[i].find(" ")!=-1 or lineas[i].find("\n")!=-1):
                        indice2=i
                        matriz_traps[indice_traps][int(lineas[indice1+1:indice2])-1]=1
sifones_file.close()

print(matriz_es_pl)

print(matriz_es_tr)

print(matriz_sifones)

print(state_deadlock)

sifon_idle=[] #Estado_idle sifon
sifon_deadlock=[] #Estado_deadlock-sifon-marcado

idle=1 #Sifones vacios estado inicial
fun_sifones_deadlock(0,matriz_sifones,matriz_es_pl,idle)
print("Sifones vacios en idle",sifon_idle)

#Llamada recursiva a fun_deadlock en busqueda de caminos que dirigen al deadlock
idle=0 #Sifones en estado deadlock
for i in range (0, len(state_deadlock)):
    fun_sifones_deadlock(state_deadlock[i],matriz_sifones,matriz_es_pl,idle)
print("Estados con deadlock",state_deadlock)
print("Estado deadlock, sifon asociado al deadlock y su marcado",sifon_deadlock)

#Nos quedamos con un solo sifon
sifon=sifon_deadlock[0]

#AGREGADO DE SUPERVISOR
supervisor(sifon)

#Elimina archivo temporal
os.remove("filtrado_prueba.txt")
import os
import numpy as np
import time

def fun_deadlock (matriz,estado,cantidad_estados,cantidad_transiciones):
    for i in range (0,cantidad_estados):
        #if(estado==82):
         #   print (i)
        cont_transiciones=0
        flag_path_deadlock=0
        # print i
        for j in range (0,cantidad_transiciones):
            if(matriz[i][j]==estado):
                #print i
                # print j
                flag_path_deadlock=1
                matriz[i][j]=-1
            if(matriz[i][j]!=-1):
                cont_transiciones=cont_transiciones+1
        # print "cont trnsiciones",cont_transiciones
        if(cont_transiciones==0 and flag_path_deadlock==1):
           # if(estado==82):
            #    print ("Recursion",i)
            # print "Estado nuevo", estado
            # print matriz
            fun_deadlock(matriz,i,cantidad_estados,cantidad_transiciones)       
            #print("Post recursion",estado)
archivo = open("./state.txt","r")
f = open ("filtrado_prueba.txt", "w")

cantidad_estados=0
cantidad_transiciones=20

#Obtenemos la cantidad de estados y filtramos la informacion
for lineas in archivo.readlines() :
    if(len(lineas)>2):
        if(lineas.find("R")!=-1):
            indice = lineas.find("S")
            estado = lineas[indice:lineas.find(" [")]
            cantidad_estados = cantidad_estados +1
            #print(estado)
            f.write(estado)
            f.write("\n")
        elif (lineas.find("D")!=-1):
            indice = lineas.find("S")
            estado = lineas[indice:lineas.find(" [")]
            cantidad_estados=cantidad_estados +1
            #print(estado)
            f.write(estado)
            f.write("\n")
        else:
            indice = lineas.find("T")
            transicion=lineas[indice:lineas.find(" [")]
            transicion=transicion.replace(" => "," ")
            #print(transicion)
            f.write(transicion)
            f.write("\n")

archivo.close()
f.close() 
##Matriz de transicion-estados
matriz =np.zeros((cantidad_estados,cantidad_transiciones)) - 1

#Modificar matriz a partir de los estados en los que estamos
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
  #         print "indice t",indice_t
           indice_s=lineas[lineas.find("S")+1:lineas.find("\n")]
 #          print "indice s",indice_s
#           print "cont_estados", cont_estados
           matriz[cont_estados][int(indice_t)-1]=int(indice_s)
           flag_deadlock=0
        else:
            maq_estado=0 #Fin de coodigo
            if(flag_deadlock==1):
                state_deadlock.append(cont_estados)
            if(lineas.find("S")!=-1):
                maq_estado=1
                flag_deadlock = 1
            if(cont_estados!=cantidad_estados):
                cont_estados=cont_estados+1
archivo.close()

print("Estados con deadlock",state_deadlock)
print("\n")
print("Estados alcanzables a partir de las respectivas transiciones:")
print("Transiciones sensibilizadas con deadlock")
print(matriz)
print("\n")

for i in range (0, len(state_deadlock)):
    fun_deadlock(matriz,state_deadlock[i],cantidad_estados,cantidad_transiciones)

print("Estados alcanzables a partir de las respectivas transiciones, sin deadlock")
print (matriz)
print("\n")
for i in range (0,cantidad_estados):
    for j in range (0,cantidad_transiciones):
        if(matriz[i][j]==-1):
            matriz[i][j]=0
        else:
            matriz[i][j]=1

print("Transiciones sensibilizadas sin deadlock")
print (matriz)

f = open("matriz.txt","w")
for i in range (0,cantidad_estados):
    f.write("[  ")
    for j in range (0,cantidad_transiciones):
        f.write(str(int(matriz[i][j])))
        f.write("  ")
    f.write("] \n")
f.close()
os.remove("filtrado_prueba.txt")
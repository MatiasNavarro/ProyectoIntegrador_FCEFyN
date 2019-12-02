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
            print("Post recursion",estado)
archivo = open("./state.txt","r")
f = open ("filtrado_prueba.txt", "w")

cantidad_estados=0
cantidad_transiciones=14

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
# print("82",matriz[82])
# print("46",matriz[46])
# print("81",matriz[81])
# print("168",matriz[168])
# print("80",matriz[80])
# print("167",matriz[167])
# print("540",matriz[540])
# print("866",matriz[866])
# print("539",matriz[539])
# print("557",matriz[557])
# print("540",matriz[540])
# print("872",matriz[872])
# print("50",matriz[50])
# print("556",matriz[556])
# print("928",matriz[928])
# print("132",matriz[132])
# print("535",matriz[535])
# print("167",matriz[167])
# print("534",matriz[534])
# print("1417",matriz[1417])
# print("431",matriz[431])
# print("533",matriz[533])
# print("430",matriz[430])
# print("532",matriz[532])
# print("537",matriz[537])
# print("166",matriz[166])
# print("539",matriz[539])
# print("538",matriz[538])
# print("542",matriz[542])
# print("556",matriz[556])
# print("634",matriz[634])
# print("537",matriz[537])
# print("541",matriz[541])
# print("555",matriz[555])
# print("538",matriz[538])
# print("554",matriz[554])
# print("464",matriz[464])
# print("536",matriz[536])
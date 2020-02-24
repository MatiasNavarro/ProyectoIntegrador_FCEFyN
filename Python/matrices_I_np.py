import os
import numpy as np
import time
import re
import sys

# Inicializacion de parametros globales
cantidad_estados=0
cantidad_transiciones=14     #Panama 14,21,22,32
cantidad_plazas=21           #Prueba2 4,4,1,1
cantidad_sifones=22         #POPN 20,26,74,130
cantidad_traps=32           #Prueba3 8,7,2,1

#Apertura de archivos resultantes de la conversion de archivos .html to .txt 
# obtenidos del SW Petrinator, para su siguiente manipulacion y filtrado.
matriz_I = open("./matricesI.txt","r")
matriz_I_pos = np.loadtxt(matriz_I,delimiter=' '' ',skiprows=3,max_rows=21, dtype=bytes).astype(str)
matriz_I_neg = np.loadtxt(matriz_I,delimiter=' '' ',skiprows=2,max_rows=22, dtype=bytes).astype(str)

aux_pos = []
aux_neg = []
for i in range(cantidad_plazas):
    aux_pos.append(matriz_I_pos[i].split(" "))

for i in range(cantidad_plazas):
    aux_neg.append(matriz_I_neg[i].split(" "))

aux_pos = np.delete(aux_pos,0,1)
aux_neg = np.delete(aux_neg,0,1)
aux_pos = np.delete(aux_pos,14,1)
aux_neg = np.delete(aux_neg,14,1)

matriz_I_pos = aux_pos
matriz_I_neg = aux_neg
print ("I+\n",matriz_I_pos)
print("I-\n",matriz_I_neg)

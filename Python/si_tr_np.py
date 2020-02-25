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
pasi = open("./siphons_traps.txt","r")
i = 0 
aux_s = 0
aux_t = 0
sif = 0
trp = 0

for line in pasi:
    i=i+1
    if(i>1):
        aux_s = aux_s + 1
        aux_t = aux_t + 1 
        if(line.find("Minimal traps")==1):
            sif = aux_s - 1
            aux_t = 0
        if(line.find("Analysis")==1):
            trp = aux_t -1

pasi.seek(0)
print("Sifones = ",sif)
print("Trampas = ",trp)

siphons = np.loadtxt(pasi,delimiter=' '' ',skiprows=1,max_rows=sif, dtype=bytes).astype(str)
traps = np.loadtxt(pasi,delimiter=' '' ',skiprows=1,max_rows=trp, dtype=bytes).astype(str)

aux_si = []
aux_tr = []
for i in range(len(siphons)):
    aux_si.append(siphons[i].split(" "))

for i in range(len(traps)):
    aux_tr.append(traps[i].split(" "))

siphons = aux_si
traps = aux_tr
print("Sifones")
for i in range(0,len(siphons)):
    print(siphons[i])

print("Trampas")
for i in range(0,len(traps)):
    print(traps[i])

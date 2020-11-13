"""
Funciones adicionales para agregar el supervidor (plaza, arcos y marcado correspondiente) de la red de Petri (.pflow) creadas con el software Petrinator. 

Autores: 
- Izquierdo, Agustina Nahir
- Navarro, Matias Alejandro 
- Salvatierra, Andres
"""

import os
import numpy as np
import time
import re
import sys

def main(p_vs, token_vs, t_in, t_out, file_name):
    """
    Funcion encargada de agregar el supervisor (Vs) con sus correspondiente marcados y los arcos de entrada y salidas.  \n

    Parameters \n 
    ----------
        p_vs        -- Id de la nueva plaza (Vs) a agregar. Ej: P5.  \n
        token_vs    -- Marcado del supervisor. \n
        t_in        -- Arcos de entrada al supervisor. \n
        t_out       -- Arcos de salida del supervisor. \n
        file_name   -- Nombre del archivo de la Rdp (.pflow). \n
    """

    f = open(file_name,"r")
    archivo = f.readlines()
    archivo_sin_espacio=[]

    x=np.random.randint(-300, 300)
    y=np.random.randint(-300, 300)

    flag_place=1
    flag_arco=1
    for i in range(len(archivo)):
        archivo_sin_espacio.append(archivo[i].strip()) #Elimina los espacios contenidos en el archivo y los guarda en 'archivo_sin_espacio'
        if(archivo_sin_espacio[len(archivo_sin_espacio)-1]=="</place>" and flag_place==1): #Busca el lugar del archivo donde se debe agregar la plaza con el marcado
            archivo_sin_espacio.append('<place>\n<id>'+ p_vs + '</id>\n<x>' + str(x) + '</x>\n<y>'+ str(y) +'</y>\n<label>'+ p_vs + '</label>\n<tokens>'+ token_vs + '</tokens>\n<isStatic>false</isStatic>\n</place>')
            flag_place=0

        if(archivo_sin_espacio[len(archivo_sin_espacio)-1]=="</arc>" and flag_arco==1): #Busca el lugar del archivo donde se debe agregar los arcos 
            for i in range(len(t_in)): #Arco desde una transicion a la plaza supervisor (arcos de entrada a Vs)
                archivo_sin_espacio.append('<arc>\n<type>regular</type>\n<sourceId>'+ t_in[i] + '</sourceId>\n<destinationId>'+ p_vs + '</destinationId>\n<multiplicity>1</multiplicity>\n</arc>')
            
            for i in range(len(t_out)): #Arco desde la plaza supervisor a una transicion (arcos de salida de Vs)
                archivo_sin_espacio.append('<arc>\n<type>regular</type>\n<sourceId>'+ p_vs + '</sourceId>\n<destinationId>'+ t_out[i] +'</destinationId>\n<multiplicity>1</multiplicity>\n</arc>')
            
            flag_arco=0
    f.close()

    with open(file_name, 'w') as f: #Se reescribe el archivo '.pflow'
        for item in archivo_sin_espacio:
            f.write("%s\n" % item)

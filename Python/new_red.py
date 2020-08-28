import os
import numpy as np
import time
import re
import sys




def main(p_vs, token_vs, t_in, t_out, file_name):
    f = open(file_name,"r")
    archivo = f.readlines()
    archivo_sin_espacio=[]

    x=np.random.randint(-300, 300)
    y=np.random.randint(-300, 300)

    flag_place=1
    flag_arco=1
    for i in range(len(archivo)):
        archivo_sin_espacio.append(archivo[i].strip())
        if(archivo_sin_espacio[len(archivo_sin_espacio)-1]=="</place>" and flag_place==1):
            archivo_sin_espacio.append('<place>\n<id>'+ p_vs + '</id>\n<x>' + str(x) + '</x>\n<y>'+ str(y) +'</y>\n<label>'+ p_vs + '</label>\n<tokens>'+ token_vs + '</tokens>\n<isStatic>false</isStatic>\n</place>')
            flag_place=0

        if(archivo_sin_espacio[len(archivo_sin_espacio)-1]=="</arc>" and flag_arco==1):
            for i in range(len(t_in)):
                archivo_sin_espacio.append('<arc>\n<type>regular</type>\n<sourceId>'+ t_in[i] + '</sourceId>\n<destinationId>'+ p_vs + '</destinationId>\n<multiplicity>1</multiplicity>\n</arc>')
            for i in range(len(t_out)):
                archivo_sin_espacio.append('<arc>\n<type>regular</type>\n<sourceId>'+ p_vs + '</sourceId>\n<destinationId>'+ t_out[i] +'</destinationId>\n<multiplicity>1</multiplicity>\n</arc>')
            flag_arco=0

    f.close()

    with open(file_name, 'w') as f:
        for item in archivo_sin_espacio:
            f.write("%s\n" % item)

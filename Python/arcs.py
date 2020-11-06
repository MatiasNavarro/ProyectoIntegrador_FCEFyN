'''
Funciones adicionales para modificar agregar/eliminar arcos de las redes de Petri (.pflow) creadas 
con el software Petrinator
'''

#--------------------------------------------------------------------------------------------
# Eliminar Arco
#--------------------------------------------------------------------------------------------
def eliminararco(name_pflow, aS, aD): #Archivo pflow a ser modificado - dS: Source del arco a eliminar - dD: Destino del arco a eliminar
    aS = str(f'P{aS}')
    aD = str(f'T{aD}')
    
    pos = 0
    arco_eliminado = [] 

    f = open(name_pflow,"r")
    archivo = f.readlines()
    f.close()

    for i in range(len(archivo)):
        arco_eliminado.append(archivo[i].strip())

    for i in range (len(arco_eliminado)):
        if(arco_eliminado[i] == ('<sourceId>'+aS+'</sourceId>') and arco_eliminado[i+1] == ('<destinationId>'+aD+'</destinationId>')):
            pos = i-2

    arc = 1 
    while(arc):
        if(arco_eliminado[pos] != '</arc>'):
            arco_eliminado.pop(pos)
        else:
            arco_eliminado.pop(pos)
            arc = 0

    with open(name_pflow, 'w') as f:
        for item in arco_eliminado:
            f.write("%s\n" % item)
    f.close()


#--------------------------------------------------------------------------------------------
# Agregar Arco
#--------------------------------------------------------------------------------------------
def agregararco(name_pflow, aS, aD): #Archivo pflow a ser modificado - dS: Source del arco a agregar - dD: Destino del arco a agregar
    aS = str(f'T{aS}')
    aD = str(f'P{aD}')
    
    flag = 0
    archivo_sin_espacio=[]

    f = open(name_pflow,"r")
    archivo = f.readlines()
    f.close()

    for i in range(len(archivo)):
        archivo_sin_espacio.append(archivo[i].strip())

        if(archivo_sin_espacio[i] == '</arc>' and flag == 0):
            archivo_sin_espacio.append('<arc>\n<type>regular</type>\n<sourceId>'+ aS + '</sourceId>\n<destinationId>'+ aD +'</destinationId>\n<multiplicity>1</multiplicity>\n</arc>')
            flag = 1

    with open(name_pflow, 'w') as f:
        for item in archivo_sin_espacio:
            f.write("%s\n" % item)
    f.close()
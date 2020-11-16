"""
Funciones adicionales para agregar/eliminar arcos de las redes de Petri (.pflow) creadas 
con el software Petrinator

Autores: 
- Izquierdo, Agustina Nahir
- Navarro, Matias Alejandro 
- Salvatierra, Andres
"""

#--------------------------------------------------------------------------------------------
# Eliminar Arco
#--------------------------------------------------------------------------------------------
def eliminararco(name_pflow, aS, aD):
    """
    Elimina un arco de la red. Desde una plaza supervisor hasta una transición. \n
    
    Parameters \n
    ----------
        name_pflow  -- Nombre del la red  a modificar (.pflow) creada con el software Petrinator. \n
        aS          -- Fuente del arco a eliminar. \n
        aD          -- Destino del arco a eliminar. \n
    """
    aS = str(f'P{aS}')  #Al arco fuente se le agrega una 'P' (plaza) para conformar la nomenclatura. Ej: P5 
    aD = str(f'T{aD}')  #Al arco destino se le agrega una 'T' (transicion) para conformar la nomenclatura. Ej: T9
    
    arc = 0 
    pos = 0
    arco_eliminado = [] 

    f = open(name_pflow,"r")
    archivo = f.readlines()
    f.close()

    for i in range(len(archivo)):   #Elimina los espacios contenidos en el archivo y los guarda en 'arco_eliminado'
        arco_eliminado.append(archivo[i].strip())

    for i in range (len(arco_eliminado)): #Busca el arco a eliminar y guarda la posición para eliminarlo
        if(arco_eliminado[i] == ('<sourceId>'+aS+'</sourceId>') and arco_eliminado[i+1] == ('<destinationId>'+aD+'</destinationId>')):
            pos = i-2
            arc = 1 

    
    while(arc): #Si se encuentra el arco a el arco a eliminar modifica el archivo, de no ser así, no se realiza ninguna acción 
        if(arco_eliminado[pos] != '</arc>'):
            arco_eliminado.pop(pos)
        else:
            arco_eliminado.pop(pos)
            arc = 0

    with open(name_pflow, 'w') as f:  #Se reescribe el archivo '.pflow' 
        for item in arco_eliminado:
            f.write("%s\n" % item)
    f.close()


#--------------------------------------------------------------------------------------------
# Agregar Arco
#--------------------------------------------------------------------------------------------
def agregararco(name_pflow, aS, aD): 
    """
    Agrega un arco de la red. Desde una transición hasta una plaza supervisor. \n
    
    Parameters \n
    ----------
        name_pflow  -- Nombre del la red a modificar (.pflow) creada con el software Petrinator. \n
        aS          -- Fuente del arco a agregar \n
        aD          -- Destino del arco a agregar \n
    """
    aS = str(f'T{aS}') #Al arco fuente se le agrega una 'T' (transicion) para conformar la nomenclatura. Ej: T9
    aD = str(f'P{aD}') #Al arco destino se le agrega una 'P' (plaza) para conformar la nomenclatura. Ej: P5 
    
    flag = 0
    archivo_sin_espacio=[]

    f = open(name_pflow,"r")
    archivo = f.readlines()
    f.close()

    for i in range(len(archivo)): #Elimina los espacios contenidos en el archivo y los guarda en 'archivo_sin_espacio'
        archivo_sin_espacio.append(archivo[i].strip())

        if(archivo_sin_espacio[i] == '</arc>' and flag == 0): #Busca el lugar del archivo donde se debe agregar el arco
            archivo_sin_espacio.append('<arc>\n<type>regular</type>\n<sourceId>'+ aS + '</sourceId>\n<destinationId>'+ aD +'</destinationId>\n<multiplicity>1</multiplicity>\n</arc>')
            flag = 1

    with open(name_pflow, 'w') as f: #Se reescribe el archivo '.pflow' 
        for item in archivo_sin_espacio:
            f.write("%s\n" % item)
    f.close()
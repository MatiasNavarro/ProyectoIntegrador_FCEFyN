import os
import numpy as np
import time
import re
import sys
import html_txt_all as hta 

# Inicializacion de parametros globales
cantidad_estados=0
cantidad_transiciones=0 #Panama 14,21,22,32
cantidad_plazas=0       #Prueba2 4,4,1,1
cantidad_sifones=0      #POPN 20,26,74,130
cantidad_traps=0        #Prueba3 8,7,2,1

def siphones_traps(cantidad_plazas):
    """ Devuelve una matriz de [sifones x plazas] y otra de [trampas x plazas]. Tambien devuelve cantidad de sifones y de trampas
    Parametros:\n
        cantidad_plazas
    """
    #Apertura de archivos resultantes de la conversion de archivos .html to .txt 
    # obtenidos del SW Petrinator, para su siguiente manipulacion y filtrado.
    pasi = open("./siphons_traps.txt","r")
    i = 0 
    aux_s = 0
    aux_t = 0

    for line in pasi:
        i=i+1
        if(i>1):
            aux_s = aux_s + 1
            aux_t = aux_t + 1 
            if(line.find("Minimal traps")==1):
                cantidad_sifones = aux_s - 1
                aux_t = 0
            if(line.find("Analysis")==1):
                cantidad_traps = aux_t -1

    pasi.seek(0)

    siphons = np.loadtxt(pasi,delimiter=' '' ',skiprows=1,max_rows=cantidad_sifones, dtype=bytes).astype(str)
    traps = np.loadtxt(pasi,delimiter=' '' ',skiprows=1,max_rows=cantidad_traps, dtype=bytes).astype(str)

    aux_si = []
    aux_tr = []
    for i in range(len(siphons)):
        aux_si.append(siphons[i].split(" "))

    for i in range(len(traps)):
        aux_tr.append(traps[i].split(" "))

    siphons = aux_si
    traps = aux_tr

    #Creamos la matriz que representa por fila la cantidad de sifones o traps y por columna plazas
    #hay un 1 en las plazas que conforman esos sifones o traps
    matriz_sifones =np.zeros((cantidad_sifones,cantidad_plazas))
    matriz_traps =np.zeros((cantidad_traps,cantidad_plazas))

    for i in range(0,len(siphons)):
        for j in range(0,len(siphons[i])):
            matriz_sifones[i][int(siphons[i][j])-1]=1
        
    for i in range(0,len(traps)):
        for j in range(0,len(traps[i])):
            matriz_traps[i][int(traps[i][j])-1]=1

    return matriz_sifones,matriz_traps,cantidad_sifones,cantidad_traps

def invariantes(cantidad_transiciones):
    """ Devuelve la matriz de invariantes de transicion, mediante la apertura de un archivo txt previamente convertido.
    Parametros:\n
        cantidad_transiciones
    """
    file = open('invariante.txt', 'r')
    cont = 0
    TInvariantes = []
    PInvariantes = []
    for line in file:
        if(cont==0):
            TInvariantes = line
            cont = cont + 1
        elif(cont==1):
            PInvariantes = line
            cont = cont + 1

    aux_I = TInvariantes.split(' ')
    TInvariantes = [] 
    for i in range (cantidad_transiciones, len(aux_I)-2):
        TInvariantes.append(aux_I[i])

    M_TI = np.zeros((int(len(TInvariantes)/cantidad_transiciones), cantidad_transiciones))
    m = 0
    for i in range ((int(len(TInvariantes)/cantidad_transiciones))):
        for j in range (cantidad_transiciones):
            M_TI[i][j] = TInvariantes[m]
            m = m + 1
    
    return M_TI


def matriz_pre_pos(cantidad_plazas,cantidad_transiciones):
    """ Obtiene la matriz pre y post a partir de un archivo txt previamente convertido
    Parametros: \n
        cantidad_plazas 
        cantidad_transiciones
    """
    #Apertura de archivos resultantes de la conversion de archivos .html to .txt 
    # obtenidos del SW Petrinator, para su siguiente manipulacion y filtrado.
    matriz_I = open("./matricesI.txt","r")
    matriz_I_pos = np.loadtxt(matriz_I,delimiter=' '' ',skiprows=3,max_rows=cantidad_plazas, dtype=bytes).astype(str)
    matriz_I_neg = np.loadtxt(matriz_I,delimiter=' '' ',skiprows=2,max_rows=cantidad_plazas+1, dtype=bytes).astype(str)

    aux_pos = []
    aux_neg = []
    for i in range(cantidad_plazas):
        aux_pos.append(matriz_I_pos[i].split(" "))

    for i in range(cantidad_plazas):
        aux_neg.append(matriz_I_neg[i].split(" "))

    aux_pos = np.delete(aux_pos,0,1)
    aux_neg = np.delete(aux_neg,0,1)
    aux_pos = np.delete(aux_pos,cantidad_transiciones,1)
    aux_neg = np.delete(aux_neg,cantidad_transiciones,1)

    matriz_I_pos = aux_pos
    matriz_I_neg = aux_neg

    return matriz_I_pos,matriz_I_neg

def supervisor(cantidad_transiciones,cantidad_plazas,sifon,matriz_es_tr,matriz_pos,matriz_pre,matriz_sifones,t_invariant):
    """ Define el supervisor que va a controlar el bad-sifon. Esta funcion define las transiciones de entrada y salida de esta plaza
    Parametros: \n
        cantidad_transiciones
        cantidad_plazas 
        sifon -- bad sifon a controlar. Compuesto por 3 elementos: estado deadlock[0], numero sifon[1], marcado sifon[2]
        matriz_es_tr -- [estado x transiciones]
        matriz_pos
        matriz_pre
        matriz_sifones
        t_invariant 
    """
    trans_idle=[]
    #Marcado del supervisor
    print("Sifon a controlar: ",sifon[1])
    print("Marcado del supervisor",sifon[2]-1) #Es la posicion 2 debido que el sifon esta declarado estado deadlock[0], numero sifon[1], marcado sifon[2]

    #Transiciones que salen del estado idle, le quitan tokens a los supervisores
    #estas se encuentran en el estado inicial (0) y son las transiciones
    #que son distintan de -1 en la matriz matriz_es_tr (estado-transicion) --> Transiciones 1 de Ezpeleta
    for ii in range(cantidad_transiciones):
        if(matriz_es_tr[0][ii]!=-1):
            print("Transicion output: ",ii+1) #+1 Por problemas de indice en petrinator empieza en 1
            trans_idle.append(ii)

    tran_sifon=np.zeros(cantidad_transiciones) #Vector que indica que transiciones sacan/ponen tokens en el sifon

    plazas_sifon=np.copy(matriz_sifones[sifon[1]]) #Las plazas que componen nuestro sifon

    #Localizamos transiciones que colocan tokens al supervisor-->Transiciones 2 de Ezpeleta
    for i in range(0,cantidad_plazas):
        if(plazas_sifon[i]==1): #Es una plaza del sifon
            for j in range(0,cantidad_transiciones):
                if(int(matriz_pre[i][j])==1):
                    tran_sifon[j]=tran_sifon[j]-1 #Le quita tokens al sifon
                if(int(matriz_pos[i][j])==1):
                    tran_sifon[j]=tran_sifon[j]+1 #Le agrega tokens al sifon
    
    for i in range(0,cantidad_transiciones):
        if(tran_sifon[i]>0):
            print("Transicion input:", i+1) #Petrinator empieza en 1 y no en cero por eso el +1
    
    plazas_sifon_complemento=np.copy(plazas_sifon) #Usado para calcular la 3er transicion de Ezpeleta

    #Obtenemos los complementos
    for i in range(0,len(tran_sifon)):
        if(tran_sifon[i]>0):
            for j in range(0,cantidad_plazas):
                if(int(matriz_pre[j][i])==1):#son las plazas que habilitan transiciones que agregan mas 
                                             #tokens de los que sacan del sifon.
                    plazas_sifon_complemento[j]=1

    trans_pla_idle=[] #Transicion idle y la/s plaza/s a la/s que le pone tokens
    for i in range(0,len(trans_idle)):
        p_idle=[]
        for j in range (0,cantidad_plazas):
            if(int(matriz_pos[j][trans_idle[i]])!=0):
                p_idle.append(int(j))
        trans_pla_idle.append([trans_idle[i],p_idle])
    
    #print("Transicion idle y la/s plaza/s a la/s que le pone tokens", trans_pla_idle)
    for i in range(0,len(trans_pla_idle)):
        pla_trans=[]
        for j in range(0,len(trans_pla_idle[i][1])):
            for k in range(0,cantidad_transiciones):
                if((int(matriz_pre[trans_pla_idle[i][1][j]][k])==1)):
                    pla_trans.append(k) #transiciones a la que la plaza habilita
        if(len(pla_trans)>1): #Esta en conflicto, ya que habilita a mas de 1 transicion
            #print("Plaza", trans_pla_idle[i][1]) #Petrinator empieza en 1 y no en cero por eso el +1
            #print("Transiciones en conflicto que plaza esa habilita: ",pla_trans) #Petrinator empieza en 1 y no en cero por eso el +1
            for ii in range(0,len(pla_trans)):
                flag_sifon=0
                for jj in range(0,len(t_invariant)):
                    if(int(t_invariant[jj][pla_trans[ii]])==1): #La T en conflicto forma parte del T invariante?
                        aux_t=np.copy(t_invariant[jj])  #Guardamos el T invatiante
                        for aa in range(0,len(aux_t)):
                            if(int(aux_t[aa])==1): #Buscamos la T que forma parte del T-invariante
                                for bb in range(0,len(matriz_pos)):
                                    if(int(matriz_pos[bb][aa])==1):
                                        if(int(plazas_sifon_complemento[bb])==1): #La T alimenta a alguna plaza del sifon'
                                            flag_sifon=1

                if(flag_sifon==0):                                 
                    print("Transicion input:",int(pla_trans[ii])+1)
                #else:
                 #   print("ESTA TRANSICION FORMA PARTE DEL CAMINO DEL SIFON:",int(pla_trans[ii])+1)

        #else:
         #   print("Plaza", trans_pla_idle[i][1]) #Petrinator empieza en 1 y no en cero por eso el +1
          #  print("Transiciones que no estan en conflicto que plaza esa habilita: ",pla_trans)


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

   # print("Sifones que no se cumplen en el estado deadlock ",estado)
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
            #print("Sifon numero",i,matriz_sifones[i])
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

#Conversion de archivos html a txt
hta.main()

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
##   un -1 si la transicion no esta sensibilizada para dicho estado,
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

(matriz_sifones,matriz_traps,cantidad_sifones,cantidad_traps)=siphones_traps(cantidad_plazas)

(matriz_pos,matriz_pre)=matriz_pre_pos(cantidad_plazas,cantidad_transiciones)

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

sifones_not_bad=np.zeros(len(matriz_sifones))
for ii in range (0, len(matriz_traps)):
    for kk in range(0,len(matriz_sifones)):
        indice_plazas=0
        for jj in range (0,cantidad_plazas):
            if(matriz_traps[ii][jj]==1):
                if(matriz_sifones[kk][jj]==1):
                    indice_plazas=indice_plazas+1
        if(indice_plazas==np.sum(matriz_traps[ii])):
            sifones_not_bad[kk]=1

for i in range(0, len(sifones_not_bad)):
    flag=0
    if(sifones_not_bad[i]==0): #Es un bad siphon
        for j in range(0, len(sifon_deadlock)):
            if(flag!=1):
                if(i==sifon_deadlock[j][1]): #Este bad siphon se vacia en deadlock? No hace falta agregarlo ya lo tenemos, en caso de no tenerlo agregarlo para controlarlo
                    flag=1
        if(flag==0): #No estaba incluido antes
            marcado=0
            for j in range(0,cantidad_plazas):
                if(matriz_sifones[i][j]==1):
                    marcado=marcado+matriz_es_pl[0][j] #Es 0 en fila, porque es el estado inicial en el que se encontraban las plazas de los sifones
            if(marcado!=0):
                sifon_deadlock.append(["inanicion",i,marcado])

print(sifon_deadlock)
#Nos quedamos con un solo sifon
sifon=np.copy(sifon_deadlock[0])

#Obtenemos T-invariantes
t_invariant=invariantes(cantidad_transiciones)

#Agregamos el supervisor del bad-sifon
supervisor(cantidad_transiciones,cantidad_plazas,sifon,matriz_es_tr,matriz_pos,matriz_pre,matriz_sifones,t_invariant)

#Elimina archivo temporal
os.remove("filtrado_prueba.txt")
exit()


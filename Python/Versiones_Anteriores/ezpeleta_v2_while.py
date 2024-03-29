import os
import numpy as np
import time
import re
import sys
import html_txt_all as hta
import filter_data as filterdata


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

    pasi.close()
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

    file.close()
    return M_TI.astype(int)

def matriz_pre_pos(cantidad_plazas,cantidad_transiciones):
    """ Devuelve la matriz pre y post a partir de un archivo txt previamente convertido
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

    matriz_I_pos = aux_pos.astype(int)
    matriz_I_neg = aux_neg.astype(int)

    matriz_I.close()

    return matriz_I_pos,matriz_I_neg

def conflict_t_invariante(t_conflict,t_invariant,matriz_pos,plazas_sifon_complemento):
    for ii in range(0,len(t_conflict)):
        flag_sifon=0
        for jj in range(0,len(t_invariant)):
            if(int(t_invariant[jj][t_conflict[ii]])==1): #La T en conflicto forma parte del T invariante?
                aux_t=np.copy(t_invariant[jj])  #Guardamos el T invariante
                for aa in range(0,len(aux_t)):
                    if(int(aux_t[aa])==1): #Buscamos la T que forma parte del T-invariante
                        for bb in range(0,len(matriz_pos)):
                            if(int(matriz_pos[bb][aa])==1):
                                if(int(plazas_sifon_complemento[bb])==1): #La T alimenta a alguna plaza del sifon'
                                    flag_sifon=1

        if(flag_sifon==0):
            print("Transicion input:",int(t_conflict[ii])+1)

def path_conflict(t_idle,t_analizar,flag_idle,plazas_sifon_complemento,matriz_pre,matriz_pos,cantidad_plazas,cantidad_transiciones,t_invariant):
    if(t_idle!=t_analizar or flag_idle==1):
        flag_idle=0
        p_idle=[] #Plaza a las que le pone tokens la transicion
        for jj in range (0,cantidad_plazas):
            if(int(matriz_pos[jj][t_analizar])!=0): #A que plazas esta alimentando esa transicion(t_analizar)
                p_idle.append(int(jj))
        #print(p_idle)
        for ii in range (0,len(p_idle)):
            t_conflict=[] #Plaza que alimenta a las transiciones en conflicto
            for mm in range (0,cantidad_transiciones):
                if(matriz_pre[p_idle[ii]][mm]==1):
                    t_conflict.append(mm)             #Transiciones en conflicto sensibilizadas por esa plaza
            if(len(t_conflict)>1): #La plaza sensibiliza a mas de una transicion? Hay conflicto

                file_t_conflict_orig = open('t_conflict_red_original.txt', 'w')
                for ij in range (0, len(t_conflict)):
                    file_t_conflict_orig.write(str(t_conflict[ij]) + ' ')
                file_t_conflict_orig.close()

                conflict_t_invariante(t_conflict,t_invariant,matriz_pos,plazas_sifon_complemento)

            else: #no hay conflicto
                path_conflict(t_idle,t_conflict[0],flag_idle,plazas_sifon_complemento,matriz_pre,matriz_pos,cantidad_plazas,cantidad_transiciones,t_invariant)

def supervisor(cantidad_transiciones,cantidad_plazas,sifon,matriz_es_tr,matriz_pos,matriz_pre,matriz_sifones,t_invariant):
    """ Define el supervisor que va a controlar el bad-siphon. Esta funcion define el marcado de la plaza supervisor y las transiciones de entrada y salida del mismo
    Parametros: \n
        cantidad_transiciones
        cantidad_plazas
        sifon -- bad siphon a controlar. Compuesto por 3 elementos: estado deadlock[0], numero sifon[1], marcado sifon[2]
        matriz_es_tr -- [estado x transiciones]
        matriz_pos
        matriz_pre
        matriz_sifones
        t_invariant
    """
    trans_idle=[] #Transiciones habilitadas en el marcado inicial
    #Marcado del supervisor
    print("Sifon a controlar: ",sifon[1]+1)
    print("Marcado del supervisor",sifon[2]-1) #Es la posicion 2 debido que el sifon esta declarado estado deadlock[0], numero sifon[1], marcado sifon[2]

    #Transiciones que salen del estado idle, le quitan tokens a los supervisores
    #estas se encuentran sensibilizadas en el estado inicial (0) y son las transiciones
    #que son distintan de -1 en la matriz matriz_es_tr (estado-transicion) --> Transiciones 1 de Ezpeleta
    for ii in range(cantidad_transiciones):
        if(matriz_es_tr[0][ii]!=-1):
            trans_idle.append(ii)
            print("Transicion output: ",ii+1) #+1 Por problemas de indice en petrinator empieza en 1


    tran_sifon=np.zeros(cantidad_transiciones) #Vector que indica que transiciones sacan/ponen tokens en el sifon

    plazas_sifon=np.copy(matriz_sifones[sifon[1]]) #Vectors de todas las plazas del sistema, en 1 se encuentran las plazas que componen nuestro sifon
    #print(plazas_sifon)
    #Localizamos transiciones que colocan tokens al supervisor-->Transiciones 2 de Ezpeleta
    for i in range(0,cantidad_plazas):
        if(plazas_sifon[i]==1): #Es una plaza del sifon
            for j in range(0,cantidad_transiciones):
                if(int(matriz_pre[i][j])==1):
                    tran_sifon[j]=tran_sifon[j]-1 #Le quita tokens al sifon
                if(int(matriz_pos[i][j])==1):
                    tran_sifon[j]=tran_sifon[j]+1 #Le agrega tokens al sifon

    for i in range(0,cantidad_transiciones):
        if(tran_sifon[i]>0): #Si es mayor a 0 significa que esta transicion coloca mas tokens a los sifones de los que le quitan
            print("Transicion input:", i+1) #Petrinator empieza en 1 y no en cero por eso el +1
    plazas_sifon_complemento=np.copy(plazas_sifon) #Usado para calcular la 3er transicion de Ezpeleta

    #Obtenemos los complementos
    for i in range(0,len(tran_sifon)):
        if(tran_sifon[i]>0):
            for j in range(0,cantidad_plazas):
                if(int(matriz_pre[j][i])==1):#son las plazas que habilitan transiciones que agregan mas
                                             #tokens de los que sacan del sifon.
                    plazas_sifon_complemento[j]=1

    for tt in range (0,len(trans_idle)):
        cont_t_invariante=0 #indica en cuantos T-invariantes aparece la Transiciones habilitadas en estado idle
                        #de ser =>2 implica que esta en conflicto
        for yy in range (0,len(t_invariant)):
            if(t_invariant[yy][trans_idle[tt]]==1):
                cont_t_invariante=cont_t_invariante+1
        if(cont_t_invariante>=2):
           # print("Transicion iddle que esta en dos T:",tt)
            path_conflict(trans_idle[tt],trans_idle[tt],1,plazas_sifon_complemento,matriz_pre,matriz_pos,cantidad_plazas,cantidad_transiciones,t_invariant) #El 1 indica que es flag_idle

def fun_sifones_deadlock(estado,matriz_sifones,matriz_es_pl,idle,cantidad_plazas,cantidad_sifones,sifon_idle,sifon_deadlock):
    """ Devuelve los sifones que se vacian en ese estado de deadlock
        Apartir de matriz de Estados x Plazas = [Marcado]
        se recorre la fila de la matriz donde se encuentra el estado deadlock,
        colocando un "1" en aquellas plazas donde el marcado sea >=1.
        Se realiza un and entre esa fila de la matriz y el sifon, si la and = 0 implica que ese sifon
        se encuentra vacio para ese estado de deadlock.
    Parametros: \n
        estado -- Estado que posee Deadlock.
        matriz_sifones -- [Marcado de plazas que componen el sifon]
        matriz_es_pl -- EstadosxPlazas = [Marcado para ese estado].
        idle -- Indica si se agrega a la lista de sifon_idle o sifon_deadlock"""

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

def main():
    print("--------------------------------------------------------------------------")
    print("Algoritmo para la solucion de deadlock para redes de petri tipo S3PR")
    print("--------------------------------------------------------------------------")
    #Conversion de archivos html a txt
    hta.main()

    #Filtrado de archivos provenientes del Petrinator
    (cantidad_estados, cantidad_plazas , cantidad_transiciones, matriz_es_tr, matriz_es_pl, state_deadlock) = filterdata.main()

    #Matrices
    (matriz_sifones,matriz_traps,cantidad_sifones,cantidad_traps)=siphones_traps(cantidad_plazas)

    (matriz_pos,matriz_pre)=matriz_pre_pos(cantidad_plazas,cantidad_transiciones)

    #T-invariantes
    t_invariant=invariantes(cantidad_transiciones)

    print("\nIngrese: ")
    print("1 - Primer analisis de la red")
    print("2 - Segundo analisis analisis de la red")
    print("3 - Red con supervisores, tratamiento de conflicto y t_idle")
    #print("4 - Red con supervisores y tratamiento de t_idle")
    analisis= input("\nOpcion: ")
    print("\n")
    #analisis= input("Primer analisis de la red -> 1\nSub red de la red original ->2\n Red con supervisores y tratamiento de conflicto -> 3\nRed con supervisores y tratamiento de t_idles -> 4")

    if(analisis=="1"):
        #Obtenemos la cantidad de plazas de la red original
        file_plazas = open('cantidad_plazas_red_original.txt', 'w')
        file_plazas.write(str(len(matriz_es_pl[0])))
        file_plazas.close()

        #Guardamos los T-invariantes de la red original
        file_t_inv_orig = open('invariante_red_original.txt', 'w')
        for i in range (0, len(t_invariant)):
            for j in range(0, len(t_invariant[0])):
                file_t_inv_orig.write(str(t_invariant[i][j]) + ' ')
            file_t_inv_orig.write("\n")
        file_t_inv_orig.close()


    if(analisis=="2" or analisis=="1"):
        sifon_idle=[] #Estado_idle sifon
        sifon_deadlock=[] #Estado_deadlock-sifon-marcado

        idle=1 #Sifones vacios estado inicial
        fun_sifones_deadlock(0,matriz_sifones,matriz_es_pl,idle,cantidad_plazas,cantidad_sifones,sifon_idle,sifon_deadlock)
        print("Sifones vacios en idle",sifon_idle)

        #Llamada recursiva a fun_deadlock en busqueda de caminos que dirigen al deadlock
        idle=0 #Sifones en estado deadlock
        for i in range (0, len(state_deadlock)):
            fun_sifones_deadlock(state_deadlock[i],matriz_sifones,matriz_es_pl,idle,cantidad_plazas,cantidad_sifones,sifon_idle,sifon_deadlock)
        print("Estados con deadlock",state_deadlock)
        print("Cantidad de estados con deadlock", len(state_deadlock))
        print("Estado deadlock, sifon asociado al deadlock y su marcado",sifon_deadlock)
        print("Cantidad de sifones vacios:", len(sifon_deadlock))

        ###################################
                ### ESTO SOLUCIONABA LO DE INANICION SI SIRVE INCLUIR
        #sifones_not_bad=np.zeros(len(matriz_sifones)) #Todos los que tengan 0 son bad siphon
        # for ii in range (0, len(matriz_traps)):
        #     for kk in range(0,len(matriz_sifones)):
        #         indice_plazas=0
        #         for jj in range (0,cantidad_plazas):
        #             if(matriz_traps[ii][jj]==1):
        #                 if(matriz_sifones[kk][jj]==1):
        #                     indice_plazas=indice_plazas+1
        #         if(indice_plazas==np.sum(matriz_traps[ii])):
        #             sifones_not_bad[kk]=1
        # #print(sifones_not_bad)
        # for i in range(0, len(sifones_not_bad)):
        #     flag=0
        #     if(sifones_not_bad[i]==0): #Es un bad siphon
        #         for j in range(0, len(sifon_deadlock)):
        #             if(flag!=1):
        #                 if(i==sifon_deadlock[j][1]): #Este bad siphon se vacia en deadlock? No hace falta agregarlo ya lo tenemos, en caso de no tenerlo agregarlo para controlarlo
        #                     flag=1
        #         if(flag==0): #No estaba incluido antes
        #             marcado=0
        #             for j in range(0,cantidad_plazas):
        #                 if(matriz_sifones[i][j]==1):
        #                     marcado=marcado+matriz_es_pl[0][j] #Es 0 en fila, porque es el estado inicial en el que se encontraban las plazas de los sifones
        #             if(marcado!=0):
        #                 sifon_deadlock.append([-1,i,marcado]) #El -1 indica que no es deadlock si no que es inanicion

        # print(sifon_deadlock)

        ##################################################

        listita=[]
        for i in range(0, len(sifon_deadlock)):
            #Nos quedamos con un solo sifon
            flag=0
            for j in range(0,len(listita)):
                if(sifon_deadlock[i][1]==listita[j]):
                    flag=1

            if(flag==0):
                listita.append(sifon_deadlock[i][1])
            print('\n')

            sifon=np.copy(sifon_deadlock[i])

            #Agregamos el supervisor del bad-sifon
            supervisor(cantidad_transiciones,cantidad_plazas,sifon,matriz_es_tr,matriz_pos,matriz_pre,matriz_sifones,t_invariant)

        print("sifones vacios sin repetir",listita)
        print("Cantidad de sifones vacios sin repetir",len(listita))

        #Elimina archivo temporal
        os.remove("filtrado_prueba.txt")


    elif(analisis=="3"):   #se obtienen los supervisores (3) o Anular brazos de idle a supervisores (4)


        file_plazas = open('cantidad_plazas_red_original.txt', 'r')
        cantidad_plazas_red_original=int(file_plazas.read())
        # print(cantidad_plazas_red_original)
        # print(len(matriz_es_pl[0]))
        array_supervisor =[]
        for i in range (cantidad_plazas_red_original,len(matriz_es_pl[0])):
            array_supervisor.append(i)
        #print(array_supervisor)


        trans_idle=[] #Transiciones habilitadas en el marcado inicial
        #Transiciones que salen del estado idle
        for ii in range(cantidad_transiciones):
            if(matriz_es_tr[0][ii]!=-1):
                trans_idle.append(ii)
                #print("Transicion Idle: ",ii+1) #+1 Por problemas de indice en petrinator empieza en 0

        #Guardamos los T-invariantes de la red original
        file_t_invariant_red_original = open("./invariante_red_original.txt","r")
        t_invariant_red_original = np.loadtxt(file_t_invariant_red_original,delimiter=' '' ',skiprows=0,max_rows=cantidad_transiciones, dtype=bytes).astype(str)

        aux_t_inv = []

        for i in range(len(t_invariant_red_original)):
                aux_t_inv.append(t_invariant_red_original[i].split(" "))

        aux_t_inv = np.delete(aux_t_inv,cantidad_transiciones,1)

        t_invariant_red_original = aux_t_inv
        #print(t_invariant_red_original)

        #Guardamos los conflictos de la red original
        file_t_conflict_red_original = open("./t_conflict_red_original.txt","r")
        t_conflict_red_original = np.loadtxt(file_t_conflict_red_original,delimiter=' ',skiprows=0,max_rows=1, dtype=bytes).astype(str)


        aux_conflic = []

        for i in range(len(t_conflict_red_original)):
            if(t_conflict_red_original[i]!=""):
                aux_conflic.append(t_conflict_red_original[i].split(" "))

        t_conflict_red_original= aux_conflic

        #print(t_conflict_red_original)

        #if(analisis=="3"):
            # #Buscamos los T-invariantes en los que esta presenta la transicion en conflictos
            # #lo recorremos sin tener en cuenta la T-idle dado que esta afecta a todos los supervisores
            # #todo aquel supervisor que no afecte el camino del T-invariante la T-conflicto le debe dar token
            # for i in range(len(t_conflict_red_original)):
            #     aux = int(t_conflict_red_original[i][0])
            #     for j in range(len(t_invariant_red_original)): #cantidad de t-invariantes
            #         if(int(t_invariant_red_original[j][aux])==1): #La transicion en conflicto forma parte del T-invariantes
            #             for m in range(len(array_supervisor)):
            #                 contador=0                           #Para verificar si alguna transicion del T-invariante le devuelve al supervisor
            #                 for k in range(len(t_invariant_red_original[j])): #Cantidad de transiciones del t-invariante
            #                     if(int(t_invariant_red_original[j][k])==1):
            #                         if(int(matriz_pos[array_supervisor[m]][k])==1): #Le devuelve token al supervisores
            #                             contador = contador + 1
            #                 #print("Supervisor ",array_supervisor[m]+1, " Contador ",contador)
            #                 if(contador==0):
            #                     print("La transicion en conflicto ", aux+1," le tiene que devolver un token al supervisor ", array_supervisor[m]+1)

        # else:
        #Buscamos eliminar los arcos de las transiciones idle cuyo T-invariante al que pertenece no le devuelve token al supervisor. (i.e arcos innecesarios)
        for i in range(len(trans_idle)): #Cantidad de trans_idle
            for j in range(len(t_invariant_red_original)): #cantidad de t-invariantes
                if(int(t_invariant_red_original[j][trans_idle[i]])==1): #La transicion idle forma parte del t-invariantes
                    for m in range(len(array_supervisor)):
                        cont_sup = 0
                        for l in range(len(t_invariant_red_original[j])):
                            if(int(t_invariant_red_original[j][l])==1):
                                if(int(matriz_pos[array_supervisor[m]][l])==1): #El T-invariante de la transicion idle le devuelve token al supervisor?
                                    cont_sup = 1 # si devuelve
                        if(cont_sup==0): #no devuelve
                            cont=0
                            for k in range(len(t_conflict_red_original)):
                                aux = int(t_conflict_red_original[k][0])
                                if(int(t_invariant_red_original[j][aux])==1): #La transicion en conflicto forma parte del T-invariante
                                    cont = cont + 1
                                    print("La transicion en conflicto ", aux+1," le tiene que devolver un token al supervisor ", array_supervisor[m]+1)

                            if(cont == 0):
                                if(int(matriz_pre[int(array_supervisor[m])][int(trans_idle[i])])==1):
                                    print("Eliminar arco desde ", array_supervisor[m]+1, "hasta ", trans_idle[i]+1)

    else:
        print("Opcion erronea")
        exit()

while(1):
    flag = 0
    main()
    print("\n-------------------------------------------------------------")
    print("Ingrese:")
    print("1 - Deadlock = true  - Volver a ejecutar el Algoritmo")
    print("0 - Deadlock = false - Finalizar ejecucion")
    flag = input("Opcion: ")
    print("-------------------------------------------------------------")

    if(flag=="0"):
        exit()

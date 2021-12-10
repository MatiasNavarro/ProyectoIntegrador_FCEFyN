<center><h1> Determinación automática del control de una red de Petri. </h1> <center>

<center> <h3>
Proyecto Integrador - Ingenería en Computación  <br>
Facultad de Ciencias Exactas Físicas y Naturales - UNC 
</h3>
</center>
   
El tema a abarcar es principalmente el análisis de redes de Petri que presentan estados de deadlock, teniendo como objetivo desarrollar y documentar un algoritmo que permita el control de las mismas, restringiendo el alcance de estos estados. 

- Autores: 
    * Izquierdo, Agustina
    * Navarro, Matias
    * Salvatierra, Andres

En la carpeta **Videos** se encuentran los videos demostrativos correspondientes a cada uno de los algoritmos. También se puede acceder a los videos mediante el siguiente enlace: 
[Determinación automática para control de una RdP](https://www.youtube.com/channel/UCfxSAAWuko0kU51Ncw-RGPA?view_as=subscriber)

En la carpeta **Informe** se encuentran los PDF correspondientes, y en cada uno, en el *Anexo B* se encuentra la forma detallada de como ejecutar cada uno de los algotimos. 

En la carpeta **Redes de Petri** se encuentran las redes utilizadas en ambos proyectos integradores. La red a controlar lleva el nombre de la carpeta junto con la palabra original (Por ejemplo: ezpeleta_original.pflow), mientras que la red ya controlada dependiendo con que versión del algoritmo fue resuelta será especificado en su nombre junto con la palabra controlada (Por ejemplo: controlada_pi_parte1.pflow, controlada_pi_parte2.pflow, controlada.pflow (en caso que coincidan las soluciones)).

Ejecición del **algoritmo PI-Parte 1**:
``` bash
$ cd Python/
$ python3 algoritmo-v3.py
```

Ejecución del **algoritmo PI-Parte 2**:
``` bash
$ cd Python/
$ python3 tesis.py
```
Ejecución del software **Petrinator**:
``` bash
$ cd Redes_de_Petri/
$ ./Petrinator.sh
```

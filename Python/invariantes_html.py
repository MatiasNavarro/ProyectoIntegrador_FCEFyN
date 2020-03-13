import os
import numpy as np
from bs4 import BeautifulSoup

"""Elimina los salto de linea, espacios y palabras sobrantes en el archivo para luego ser procesado 
correctamente en otro script de python. \n
Crea un archivo temporal para trabajar y al final lo elimina.

Parámetros: \n
    text -- Archivo html que fue convertido a txt.
"""
def clean_file(text):
    # En las siguiente lineas de código se abren y se cierran dos archivos, los cuales 
    # son leídos y escritos para dejar el archivo "limpio" para el próximo script. 
    f = open ("invariante.txt", "w")
    f.write(text)
    f.close()

    f1 = open('invariante.txt', 'r')
    f2 = open('invariante.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace('\n', ' '))
    f1.close()
    f2.close()

    f1 = open('invariante.txt.tmp', 'r')
    f2 = open('invariante.txt', 'w')
    for line in f1:
        f2.write(line.replace('Petri Net Invariant Analysis T-Invariants ', ''))
    f1.close()
    f2.close()

    f1 = open('invariante.txt', 'r')
    f2 = open('invariante.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace('The net is covered by positive T-Invariants, therefore it might be bounded and live. P-Invariants.', ''))
    f1.close()
    f2.close()

    f1 = open('invariante.txt.tmp', 'r')
    f2 = open('invariante.txt', 'w')
    for line in f1:
        f2.write(line.replace('The net is covered by positive P-Invariants, therefore it is bounded. P-Invariant equations.', ''))
    f1.close()
    f2.close()

    f1 = open('invariante.txt', 'r')
    f2 = open('invariante.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace('The net is not covered by positive T-Invariants, therefore we do not know if it is bounded and live.', ''))
    f1.close()
    f2.close()

    f1 = open('invariante.txt.tmp', 'r')
    f2 = open('invariante.txt', 'w')
    for line in f1:
        f2.write(line.replace('The net is not covered by positive P-Invariants, therefore we do not know if it is bounded.', ''))
    f1.close()
    f2.close()
    
    
    f1 = open('invariante.txt', 'r')
    f2 = open('invariante.txt.tmp', 'w')
    for line in f1:
            f2.write(line.replace('P', '\nP',1))
    f1.close()
    f2.close()

    f1 = open('invariante.txt.tmp', 'r')
    f2 = open('invariante.txt', 'w')
    for line in f1:
        f2.write(line.replace('M', '\nM',1))
    f1.close()
    f2.close()
    
    #Elimina archivo temporal
    os.remove("invariante.txt.tmp")

def main():
    # Abre un archivo html a partir del path indicado por consola, y lo carga en un archivo
    # BeatifulSoup para extraer los datos html de dicho archivo.
    archivo = input("Path del archivo de invariantes (html): ")
    html = open(archivo,'r')
    soup = BeautifulSoup(html,'lxml')

    # Elimina todos elementos de estilo
    for script in soup(["style"]):
        script.extract()

    # Obtener texto del archivo BeautifulSoup
    text = soup.get_text(separator='\n', strip=True)


    # break into lines and remove leading and trailing space on each
    # Elimina los saltos de lina y los espacios al principio y al final de cada línea
    lines = (line.strip() for line in text.split("\n"))

    # break multi-headlines into a line each
    # Separa varios encabezados en cada linea
    chunks = (phrase.strip() for line in lines for phrase in line.split("\n"))

    # drop blank lines
    # Elimina líneas en blanco
    text = '\n'.join(chunk for chunk in chunks if chunk)

    #Llamada a la funcion clean_file()
    clean_file(text)
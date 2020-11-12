"""
Convierte el archivo de SIFONES Y TRAMPAS extraido del Petrinator (.html) a un archivo '.txt' que luego será utilizado en el algoritmo

Autores: 
- Izquierdo, Agustina Nahir
- Navarro, Matias Alejandro 
- Salvatierra, Andres
"""

import os
from bs4 import BeautifulSoup

def clean_file(text):
    """Elimina los salto de linea, espacios y palabras sobrantes en el archivo para luego ser procesado 
    correctamente en otro script de python. \n
    Crea un archivo temporal para trabajar y al final lo elimina.

    Parámetros: \n
        text -- Archivo html que fue convertido a txt.
    """

    # En las siguiente lineas de código se abren y se cierran dos archivos, los cuales 
    # son leídos y escritos para dejar el archivo "limpio" para el próximo script. 
    f = open ("siphons_traps.txt", "w")
    f.write(text)
    f.close()
    
    f1 = open('siphons_traps.txt', 'r')
    f2 = open('siphons_traps.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace('\n', ' '))
    f1.close()
    f2.close()

    f1 = open('siphons_traps.txt.tmp', 'r')
    f2 = open('siphons_traps.txt', 'w')
    for line in f1:
        f2.write(line.replace(' }', '\n'))
    f1.close()
    f2.close()
    f1 = open('siphons_traps.txt', 'r')
    f2 = open('siphons_traps.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace("siphons", "siphons \n"))
    f1.close()
    f2.close()

    f1 = open('siphons_traps.txt.tmp', 'r')
    f2 = open('siphons_traps.txt', 'w')
    for line in f1:
        f2.write(line.replace("traps", "traps \n"))
    f1.close()
    f2.close()

    f1 = open('siphons_traps.txt', 'r')
    f2 = open('siphons_traps.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace(',', ''))
    f1.close()
    f2.close()
    
    f1 = open('siphons_traps.txt.tmp', 'r')
    f2 = open('siphons_traps.txt', 'w')
    for line in f1:
        f2.write(line.replace('Siphons and Traps', ''))
    f1.close()
    f2.close()

    f1 = open('siphons_traps.txt', 'r')
    f2 = open('siphons_traps.txt.tmp', 'w')
    for line in f1:
        f2.write(line.replace(' {', ''))
    f1.close()
    f2.close()

    f1 = open('siphons_traps.txt.tmp', 'r')
    f2 = open('siphons_traps.txt', 'w')
    for line in f1:
        f2.write(line.replace('P', ''))
    f1.close()
    f2.close()

    #Elimina archivo temporal
    os.remove("siphons_traps.txt.tmp")

def main():
    # Abre un archivo html a partir del path indicado por consola, y lo carga en un archivo
    # BeatifulSoup para extraer los datos html de dicho archivo.
    archivo = input("Path del archivo de Sifones(html): ")
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
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    # Elimina líneas en blanco
    text = '\n'.join(chunk for chunk in chunks if chunk)

    #Llamada a la funcion clean_file()
    clean_file(text)

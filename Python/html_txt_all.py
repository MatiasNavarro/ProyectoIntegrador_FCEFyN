"""
Este script se encarga de llamar a los demás para realizar la conversión de los archivos extraidos del Petrinator

Autores: 
- Izquierdo, Agustina Nahir
- Navarro, Matias Alejandro 
- Salvatierra, Andres
"""

import state_deadlock as sd
import matricesI_html as mih
import siphons_traps as st
import invariantes_html as inv

def main():
    sd.main()
    mih.main()
    st.main()
    inv.main()
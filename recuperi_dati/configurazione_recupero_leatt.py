import sys
from configurazione_webdriver import *
from selenium.common.exceptions import *
listasku=[]
opzioni.add_argument("window-size=1920,1080")
cartella_attuale=os.path.dirname(os.path.abspath(__file__))
file_listasku=os.path.join(cartella_attuale, '../storage/LEATT/listasku.csv')
with open(file_listasku,'r') as file:
 for riga in file:
  listasku.append(riga.strip())     

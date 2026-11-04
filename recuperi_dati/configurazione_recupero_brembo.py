listacodici=[]
from configurazione_webdriver import *
from selenium.common.exceptions import *
cartella_attuale=os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(cartella_attuale, '../storage/BREMBO/listasku.csv')
opzioni.add_argument('start-maximized')
with open(file_listasku,'r') as file:
 for riga in file:
  listacodici.append(riga.strip())

from configurazione_webdriver import *
from bs4 import BeautifulSoup
from selenium.common.exceptions import *
opzioni.add_argument('start-maximized')
listasku=[]
cartella_attuale = os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(cartella_attuale, '../storage/QUADLOCK/listasku.csv')
with open(file_listasku,'r') as file:
 for riga in file:
  listasku.append(riga.strip())

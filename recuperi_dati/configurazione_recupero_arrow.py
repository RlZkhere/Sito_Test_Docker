from configurazione_webdriver import *
from bs4 import BeautifulSoup
base_dir = os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(base_dir, '../storage/ARROW/listasku.csv')
listasku=[]
with open(file_listasku,'r') as file:
 for riga in file:
  listasku.append(riga.strip())
opzioni.add_argument('window-size=1920,1080')

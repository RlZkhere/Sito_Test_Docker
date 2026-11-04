from configurazione_webdriver import *
from selenium.common.exceptions import *
opzioni.add_argument("window-size=1920,1080")
listasku=[]
base_dir = os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(base_dir, '../storage/GPR/listasku.csv')
with open(file_listasku,'r') as file:
 for riga in file:
  listasku.append(riga.strip())

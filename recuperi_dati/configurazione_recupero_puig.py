from configurazione_webdriver import *
from selenium.common.exceptions import *
opzioni.add_argument('start-maximized')
listasku=[]
base_dir = os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(base_dir, '../storage/PUIG/listasku.csv')
with open(file_listasku,'r') as file:
 for riga in file:
  listasku.append(riga.strip())
browser=webdriver.Chrome(options=opzioni)

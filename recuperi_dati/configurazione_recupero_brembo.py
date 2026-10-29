import os
import traceback
import time
import selenium
listacodici=[]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
cartella_attuale=os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(cartella_attuale, '../storage/BREMBO/listasku.csv')
opzioni=Options()
opzioni.add_argument('headless')
opzioni.add_argument("--no-sandbox")
opzioni.add_argument('start-maximized')
opzioni.add_argument("--disable-dev-shm-usage")
opzioni.add_argument("--disable-gpu")
service=Service(executable_path="/usr/bin/chromedriver")
opzioni.binary_location = "/usr/bin/chromium-browser"
browser=webdriver.Chrome(service=service,options=opzioni)
with open(file_listasku,'r') as file:
 for riga in file:
  listacodici.append(riga.strip())

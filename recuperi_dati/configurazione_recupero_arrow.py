import os
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
base_dir = os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(base_dir, '../storage/ARROW/listasku.csv')
listasku=[]
with open(file_listasku,'r') as file:
 for riga in file:
  listasku.append(riga.strip())
service=Service(executable_path="/usr/bin/chromedriver")
opzioni=Options()
opzioni.binary_location = "/usr/bin/chromium-browser"
opzioni.add_argument('headless')
opzioni.add_argument('window-size=1920,1080')
opzioni.add_argument("--no-sandbox")
opzioni.add_argument("--disable-dev-shm-usage")
opzioni.add_argument("--disable-gpu")
browser=webdriver.Chrome(service=service,options=opzioni)

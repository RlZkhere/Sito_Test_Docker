import os
import time
import traceback
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
opzioni=Options()
opzioni.add_argument('headless')
opzioni.add_argument('start-maximized')
opzioni.add_argument("--no-sandbox")
opzioni.add_argument("--disable-dev-shm-usage")
opzioni.add_argument("--disable-gpu")
service=Service(executable_path="/usr/bin/chromedriver")
opzioni.binary_location = "/usr/bin/chromium-browser"
browser=webdriver.Chrome(service=service,options=opzioni)
listacodici=[]
lista_categorie=[
"ABBIGLIAMENTO - ACCESSORI", "ACCENSIONI / CENTRALINE", "ACCENSIONI / CENTRALINE - RICAMBI", "ADESIVI", "ALBERI A CAMME", "ALBERI MOTORE", "ALBERI MOTORE - KIT REVISIONE - RICAMBI", "ALIMENTAZIONE - RICAMBI", "AMMORTIZZATORE RIALZI", 
"AMMORTIZZATORI / FORCELLA", "ATTREZZI OFFICINA", "CAMPANE FRIZIONE", "CAPPUCCI CANDELA", "CARBURATORI", "CARBURATORI - RICAMBI", "CARTER MOTORE", "CARTER TRASMISSIONE", "CEPPI FRENO", "CERCHI", "CINGHIE VARIATORE", "COLLETTORI ASPIRAZIONE", 
"COLLETTORI SCARICO", "COMANDO STARTER ARIA", "CORNETTI D'ASPIRAZIONE", "CROCIERA CAMBIO", "CUSCINETTI", "DISCHI FRENO", "E-BIKE - HI-SPEED", "E-BIKE E-P3 RICAMBI", "FILTRI ARIA", "FILTRI CARBURANTE", "FILTRI FLANGE", "FILTRI OLIO", "FORCELLONI (TORSEN WD)", 
"FRIZIONI", "GABBIE SPINOTTO", "GAZEBO", "GETTI CARBURATORE", "GIUNTO FLESSIBILE", "GUARNIZIONI", "IMPIANTI ALIMENTAZIONE", "KIT GRUPPI TERMICI", "KIT GRUPPI TERMICI - RICAMBI", "KIT RAPPORTI - INGRANAGGI", "LAMELLE - LASTRE FIBRA DI CARBONIO", 
"MANOPOLE - COMANDI GAS", "MARMITTE", "MARMITTE - RICAMBI", "MINIBIKE", "MINIBIKE - RICAMBI", "MINICROSS/MINIMOTARD/XP4T - RICAMBI", "MISURINO OLIO", "MOLLE DI CONTRASTO", "MOLLE FRIZIONE", "MOLLE MARMITTA", "MOTORE THOR", "MOTORE THOR - RICAMBI", "PARALEVE", 
"PARAOLI (ANELLI DI TENUTA)", "PASTIGLIE FRENO", "PISTONI PER KIT POLINI", "PNEUMATICI", "POLMONE STABILIZZATORE RECUPERO GAS", "POMPE ACQUA", "PORTATARGA", "RICAMBI", "RULLI VARIATORE", "RULLI VARIATORE - KIT", "SEGMENTI", "SEMIPULEGGE CONDOTTE", 
"SEMIPULEGGE FISSE", "SILENZIATORI - LANA DI VETRO", "SISTEMI FRENANTI - ACCESSORI", "SKATE", "SPILLI CARBURATORE", "STRUMENTI ELETTRONICI", "SUPPORTI ANTIVIBRANTI", "TESTE", "TRASMISSIONI - RICAMBI", "VALVOLE LAMELLARE", "VARIATORI"
]
cartella_attuale = os.path.dirname(os.path.abspath(__file__))
file_listasku = os.path.join(cartella_attuale, '../storage/POLINI/listasku.csv')
with open(file_listasku,'r') as file:
 for riga in file:
  listacodici.append(riga.strip())

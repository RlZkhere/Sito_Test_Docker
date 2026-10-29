from configurazione_recupero_brembo import *
from bs4 import BeautifulSoup
cartella_attuale=os.path.dirname(os.path.abspath(__file__))
file_foto=os.path.join(cartella_attuale, '../storage/BREMBO/foto.csv')
file_dati=os.path.join(cartella_attuale, '../storage/BREMBO/dati.csv')
file_log=os.path.join(cartella_attuale, '../storage/BREMBO/log.csv')
def recupera_immagini(sku_foto):
 lista_scrivi_foto=[]
 conta_foto=int(0)
 try: 
  browser.find_elements(By.XPATH,"//button[contains(@class,'is-selected') and contains(@class,'carousel')]")[0].click()
  time.sleep(1.5)
  lista_foto=browser.find_elements(By.CLASS_NAME,'f-thumbs__viewport.is-draggable')[0].find_elements(By.TAG_NAME,'div')
  for foto in lista_foto:
   try:
    numero_foto=foto.get_attribute('index')
    numero_foto=int(numero_foto)+1 
    link_foto=foto.find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
    riga_scrivi=sku_foto+';'+link_foto+';'+str(numero_foto)
    lista_scrivi_foto.append(riga_scrivi)
   except Exception:
    traceback.print_exc()      
  browser.find_elements(By.XPATH,"//button[@class='f-button' and @title='Close']")[0].click()
  time.sleep(2)  
 except Exception:
  lista_scrivi_foto=[]    
 return lista_scrivi_foto
def recupera_dati(sku):   
 lista_dati_foto=[]
 dati_tecnici=''   
 try: #BLOCCO_DATI_TECNICI
  tabella_dati_html=browser.find_elements(By.XPATH,"//div[contains(@class,'main-abstract') and text()='Specifiche tecniche']")[0].find_element(By.XPATH,"..").find_elements(By.XPATH,".//div[@class='data mrg']")[0].get_attribute('innerHTML')
  tabella_dati_tecnici=BeautifulSoup(tabella_dati_html, 'html.parser')
 except Exception:
  traceback.print_exc()   
  tabella_dati_tecnici=''     
 try: 
  for elemento_dato in tabella_dati_tecnici.find_all('div', class_='item'):
   nome_elemento=elemento_dato.find_all('div', class_='label')[0].get_text().strip()
   valore_elemento=elemento_dato.find_all('div', class_='detail')[0].get_text().strip()
   dati_tecnici=dati_tecnici+'$'+nome_elemento+': '+valore_elemento   
 except Exception:
  pass 
 try: #DESCRIZIONE
  descrizione=browser.find_elements(By.CLASS_NAME,'description')[0].get_attribute('innerText').replace('\n','$')   
 except Exception:
  descrizione=''
  f=open(file_log,'a')
  f.write(str(sku) + ': DESCRIZIONE MANCANTE'+"\n")
  f.close()
 try: #NOME
  nome_prodotto=browser.find_elements(By.CLASS_NAME,'main-title')[0].get_attribute('innerText').strip()
 except Exception:
  nome_prodotto=''
  f=open(file_log,'a')
  f.write('NOME non trovato per '+str(sku)+"\n") 
  f.close()  
 try: #LINEA
  browser.find_elements(By.CLASS_NAME,'cluster-tag.inline.big')[0].get_attribute('innerText').strip()   
 except Exception:
  linea=''     
 try: #LISTA_IMMAGINI
  lista_dati_foto=recupera_immagini(sku)
  if lista_dati_foto:
   f=open(file_foto,'a')
   for x in lista_dati_foto:   
    f.write(x+"\n")
   f.close()
 except Exception:
  traceback.print_exc()
 riga_dati='MQ-'+sku+';'+nome_prodotto+';'+linea+';'+descrizione+';'+dati_tecnici 
 f=open(file_dati,'a')
 f.write(riga_dati+"\n")
 f.close()
def pagina_caricata(tempo,tipo):
 try:
  elemento=WebDriverWait(browser,tempo).until(EC.presence_of_element_located((tipo)))
 except Exception:
  traceback.print_exc()
note_unisci=''
valori_uniti='' 
browser=webdriver.Chrome(options=opzioni)
browser.get('https://www.bremboparts.com/europe/it')
pagina_caricata(10,(By.CLASS_NAME,'cookie-toast'))
try:
 try:
  browser.find_elements(By.CLASS_NAME,'cookie-toast')[0].find_elements(By.XPATH,".//button[@data-border and text()='Solo cookie tecnici']")[0].click()
  time.sleep(2)
 except NoSuchElementException:
  pass    
except Exception:
 traceback.print_exc()    
try:
 browser.find_elements(By.XPATH,"//button[@class='button' and text()='Confirm']")[0].click()
 time.sleep(2)
except Exception:
 pass    
try:
 pagina_caricata(10,(By.XPATH,"//button[text()='Rifiuta']"))
 browser.find_elements(By.XPATH,"//button[text()='Rifiuta']")[0].click()
 time.sleep(2)
except Exception:
 pass    
browser.find_elements(By.XPATH,"//button[contains(@class,'button') and @aria-label='Moto']")[0].click()
time.sleep(1.5)
browser.find_elements(By.CLASS_NAME,'icon.vehicle.icon-code')[0].find_element(By.XPATH,"..").click()
newsletter=int(0)
for codice in listacodici:
 codice_trovato=''
 browser.find_element(By.ID,'CodePrefix').clear()
 browser.find_element(By.ID,'CodePrefix').send_keys(codice+Keys.ENTER)
 if newsletter == 0:
  try:
   pagina_caricata(3,(By.XPATH,"//button[@class='button' and text()='Iscriviti subito']"))
   browser.find_elements(By.XPATH,"//button[@class='button' and text()='Iscriviti subito']")[0]
   browser.find_elements(By.CLASS_NAME,'content')[3].find_elements(By.XPATH,".//button[@class='close']")[0].click()
   time.sleep(2)
   newsletter=1
  except Exception:
   pass
 try:
  codice_trovato=browser.find_elements(By.XPATH,"//nav[@class='list' and @aria-label='Catalogo']")[0].find_elements(By.CLASS_NAME,'item')[2].get_attribute('innerText').replace('\n','').strip()
  if codice_trovato != codice:
   continue 
  else:
   recupera_dati(codice)      
 except Exception:
  f=open(file_log,'a')
  f.write('CODICE NON TROVATO '+str(codice)+"\n")
  f.close()  

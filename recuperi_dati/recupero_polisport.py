from configurazione_recupero_polisport import *
base_dir = os.path.dirname(os.path.abspath(__file__))
file_log = os.path.join(base_dir, '../storage/POLISPORT/log.csv')
cartella_foto=os.path.join(base_dir, '../storage/POLISPORT/FOTO') 
try:
 os.mkdir(cartella_foto)   
except Exception:     
 pass
def scrivi_errore(nome_file,riga):
 f=open(nome_file,'a')
 f.write(riga+"\n")
 f.close() 
def recupera_foto(sku):
 try:
  browser.find_elements(By.CLASS_NAME,'slick-track')[0].find_elements(By.XPATH,".//div[contains(@class,'slick-active')]")[0].find_elements(By.TAG_NAME,'a')[0].click()
  link=browser.find_elements(By.CLASS_NAME,'imageExtraZoom')[0].get_attribute('src')
 except Exception:
  link=''
  scrivi_errore(file_log,'ERRORE RECUPERO FOTO PER CODICE '+sku) 
 try:
  browser.execute_script("document.getElementsByClassName('mfp-close rdc-mfp-icon-svg')[0].click()") #PROVA A CHIUDERE A PRIORI LA FOTO
  time.sleep(1)
 except Exception:
  pass     
 return link
def elemento_caricato(tempo,tipo):
 try:
  caricato=WebDriverWait(browser,tempo).until(EC.presence_of_element_located(tipo))    
  return 0
 except Exception:
  return 1
browser.get('https://www.polisport.com/es')
pagina_caricata=int(0)
pagina_caricata=elemento_caricato(10,(By.ID,'concentPopup'))
if pagina_caricata == 0: #ESISTE IL POPUP
 try: #CHIUDE I COOKIES
  browser.find_element(By.ID,'concentPopup').find_elements(By.CLASS_NAME,'rdc-aceptbuttons')[0].find_elements(By.XPATH,".//button[contains(text(),'necesarios')]")[0].click()
  time.sleep(2)
 except Exception:
  sys.exit(0)
for codice in listasku:
 link_foto=''
 browser.find_elements(By.XPATH,"//li[@class='search']")[0].click()
 time.sleep(1) 
 browser.find_element(By.ID,'search').clear()
 browser.find_element(By.ID,'search').send_keys(codice+Keys.ENTER)
 pagina_caricata=elemento_caricato(2,(By.XPATH,"//h1[@class='title-heading-titles' and contains(text(),'no ha tenido')]"))
 if pagina_caricata == 0:
  scrivi_errore(file_log,'CODICE '+str(codice)+' NON TROVATO')
  continue 
 pagina_caricata=elemento_caricato(5,(By.XPATH,"//a[@title='Productos']"))
 if pagina_caricata == 0:
  browser.find_elements(By.TAG_NAME,'article')[0].click() #PIU VOLTE STESSO ARTICOLO IN BASE A COMPATIBILITA MA VA BENE APRIRE UNO QUALSIASI
 pagina_caricata=elemento_caricato(5,(By.XPATH,"//div[@class='name']"))
 if pagina_caricata != 0:
  scrivi_errore(file_log,'ERRORE DURANTE RICERCA '+str(codice))
  continue        
 time.sleep(1)
 link_foto=recupera_foto(codice)
 if link_foto != '':
  data_foto = requests.get(link_foto).content
  with open(cartella_foto+'/MM-'+codice+'_1.jpg', 'wb') as scrivi:
   scrivi.write(data_foto)       
 time.sleep(3) 
browser.quit() 

from configurazione_recupero_leatt import *
risultato=int(2)
cartella_attuale = os.path.dirname(os.path.abspath(__file__))
file_log = os.path.join(cartella_attuale, '../storage/LEATT/log.csv')
file_dati = os.path.join(cartella_attuale, '../storage/LEATT/dati.csv')
def scrivi_file(nome,stringa):
 f=open(nome,'a',encoding='utf-8')
 f.write(stringa+"\n")
 f.close() 
def pagina_caricata(tempo,tipo):
 try:
  pagina_caricata=WebDriverWait(browser,tempo).until(EC.presence_of_element_located(tipo))
  return 0
 except Exception:
  return 1  
def recupero_dati(link):
 riga_scrivi=''
 loghi_uniti=''
 browser.execute_script("window.open(arguments[0])",link)
 time.sleep(0.5)
 browser.switch_to.window(browser.window_handles[1])
 time.sleep(1)
 risultato=pagina_caricata(10,(By.CLASS_NAME,'sku__value'))
 if risultato == 1:
  scrivi_file(file_log,'ARTICOLO NON CARICATO CORRETTAMENTE: '+str(codice_cerca))
 else:
  try:
   sku=browser.find_elements(By.CLASS_NAME,'sku__value')[0].get_attribute('innerText').strip()
   try:
    descrizione=browser.find_elements(By.XPATH,"//summary[contains(@class,'cc-accordion') and text()='Descrizione']")[0].find_element(By.XPATH,"..").find_elements(By.TAG_NAME,'div')[0].get_attribute('innerHTML').replace(';',',').replace('\n','').strip()
    if descrizione.startswith('<div'):
     descrizione=descrizione.split('>',1)[1].replace('</div>','')
   except Exception:
    descrizione=''
    scrivi_file(file_log,'DESCRIZIONE NON TROVATA PER : '+str(sku)) 
   try:
    specifiche=browser.find_elements(By.XPATH,"//summary[contains(@class,'cc-accordion') and text()='Specifiche']")[0].find_element(By.XPATH,"..").find_elements(By.CLASS_NAME,'metafield-rich_text_field')[0].get_attribute('innerHTML').replace(';',',').replace('\n','').strip()
    if specifiche.startswith('<ul>') and specifiche.endswith('</ul>'):
     specifiche=specifiche.replace('</li>','$').replace('<li>','').replace('<ul>','').replace('</ul>','') #NORMALIZZO I DATI TECNICI     
     if specifiche.endswith('$'):
      specifiche=specifiche[:-1]   
   except Exception:
    specifiche=''   
    scrivi_file(file_log,'NON TROVATI DATI TECNICI PER : '+str(sku))
   try: #SOTTOTITOLO
    sottotitolo=browser.find_elements(By.CLASS_NAME,'product-info-block')[0].get_attribute('innerText').replace(';',',').strip()
   except Exception:
    sottotitolo=''
    scrivi_file(file_log,'SOTTOTITOLO NON TROVATO PER : '+str(sku))    
   try: #GUIDA TAGLIE  
    pulstante_guida_taglie=browser.find_elements(By.XPATH,"//span[text()='Guida alle taglie' and contains(@class,'chart')]")[0] #SE ESISTE ESISTE ANCHE LA GUIDA TAGLIE
    guida_taglie=browser.find_elements(By.CLASS_NAME,'size-chart')[0].find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
   except Exception:
    scrivi_file(file_log,'NON TROVATA GUIDA TAGLIE PER : '+str(sku))
    guida_taglie=''
   try: #LISTA DATI LOGHI
    lista_loghi=browser.find_elements(By.CLASS_NAME,'logo-list-container')[0].find_elements(By.XPATH,".//div[@data-cc-animate]")
    for logo in lista_loghi:
     nome_logo=logo.find_elements(By.XPATH,".//*[contains(@class,'title') and contains(@class,'logo')]")[0].get_attribute('innerText').replace(';',',').strip()
     loghi_uniti=loghi_uniti+nome_logo+'$'
    if loghi_uniti.endswith('$'):
     loghi_uniti=loghi_uniti[:-1]   
   except Exception:
    scrivi_file(file_log,'NESSUN LOGO PRESENTE PER : '+str(sku))  
   riga_scrivi=sku+';'+sottotitolo+';'+specifiche+';'+descrizione+';'+guida_taglie+';'+loghi_uniti 
  except Exception as e:
   print(e)   
 browser.close()
 browser.switch_to.window(browser.window_handles[0]) 
 return riga_scrivi
browser.get('https://leatt.it/')
time.sleep(2)
try: #RIFIUTA COOKIE
 browser.find_elements(By.XPATH,"//button[text()='Declina' and contains(@id,'shopify')]")[0].click()
 time.sleep(1)
except Exception:
 scrivi_file(file_log,'Errore scelta cookie')    
try: #CHIDI PULSANTE NON SEMPRE PRESENTE 
 browser.find_elements(By.XPATH,"//button[@aria-haspopup='dialog' and contains(@aria-label,'NOT LUCK')]")[0].click()
 time.sleep(1)
except Exception:
 pass 
browser.get('https://leatt.it/search')
risultato=pagina_caricata(10,(By.XPATH,"//input[contains(@placeholder,'erca nel') and @type='search']"))
if risultato == 1:
 scrivi_file(file_log,'PAGINA RICERCA NON CARICATA')
 sys.exit(1)
try: #ASPETTA SI APRA NEWSLETTER
 caricato=WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='cc-popup']/ancestor::div[5]//*[contains(@class, 'cc-popup-close')]")))
 browser.find_element(By.ID,'cc-popup').find_element(By.XPATH,"../../../../..").find_elements(By.CLASS_NAME,'cc-popup-close')[0].click()
 time.sleep(5)
except Exception:
 traceback.print_exc()   
for codice_cerca in listasku:
 browser.find_elements(By.XPATH,"//input[contains(@placeholder,'erca nel') and @type='search']")[0].clear()
 browser.find_elements(By.XPATH,"//input[contains(@placeholder,'erca nel') and @type='search']")[0].send_keys(codice_cerca+Keys.ENTER)
 risultato=pagina_caricata(2,(By.XPATH,"//div[contains(text(),' 0 risultati')]"))
 if risultato == 0: #SE TROVA SCRITTO 0 RESULTS CONTINUA IL CICLO
  scrivi_file(file_log,'PRODOTTO NON TROVATO: '+str(codice_cerca))
 else:
  lista_prodotti=browser.find_elements(By.CLASS_NAME,'filter-container')[0].find_elements(By.XPATH,"//product-block[@enable-swipe]")
  numero_prodotti=len(lista_prodotti)
  if numero_prodotti > 1:
   scrivi_file(file_log,'PIU DI UN ARTICOLO TROVATO PER '+str(codice_cerca))
  elif numero_prodotti == 1:
   url=lista_prodotti[0].find_elements(By.CLASS_NAME,'product-link')[0].get_attribute('href')
   scrivi_riga=recupero_dati(url)
   scrivi_file(file_dati,scrivi_riga)   
 browser.get('https://leatt.it/search')
 risultato=pagina_caricata(10,(By.XPATH,"//input[contains(@placeholder,'erca nel') and @type='search']"))
 if risultato == 1:
  scrivi_file(file_log,'NON CARICATA RICERCA DOPO ARTICOLO: '+str(codice_cerca))
  time.sleep(10)
  continue

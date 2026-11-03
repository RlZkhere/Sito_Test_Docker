from configurazione_recupero_mt import *
base_dir = os.path.dirname(os.path.abspath(__file__))
file_log = os.path.join(base_dir, '../storage/MT/log.csv')
file_dati = os.path.join(base_dir, '../storage/MT/dati.csv')
file_foto = os.path.join(base_dir, '../storage/MT/foto.csv')
def scrivi_errore(stringa):
 f=open(file_log,'a')
 f.write(stringa+"\n")
 f.close()
def pagina_caricata(tempo,tipo):
 try:
  pagina_caricata=WebDriverWait(browser,tempo).until(EC.presence_of_element_located(tipo))
  return 0
 except Exception:
  return 1
def recupera_foto(link):
 conta_foto=int(1)
 try:
  lista_foto=[]
  prima_foto=browser.find_element(By.ID,'gallery-viewer').find_elements(By.XPATH,".//li[contains(@class,'media-viewer') and contains(@class,'current-variant')]")[0].find_elements(By.XPATH,".//img[contains(@src,'mthelmets')]")[0].get_attribute('src')
  lista_foto.append((prima_foto,1))
  lista_immagini=browser.find_element(By.ID,'gallery-viewer').find_elements(By.XPATH,".//li[contains(@class,'media-viewer') and not (contains(@class,'current-variant'))]")
  for immagine in lista_immagini:
   conta_foto=conta_foto+1
   try:
    link_immagine=immagine.find_elements(By.XPATH,".//img[contains(@src,'mthelmets')]")[0].get_attribute('src')
    lista_foto.append((link_immagine,conta_foto))
   except Exception:
    scrivi_errore('Errore recupero foto: '+str(conta_foto)+' per link '+link)
  f=open(file_foto,'a')
  for x,y in lista_foto:
   f.write(link+';'+x+';'+str(y)+"\n")
  f.close()
 except Exception:
  #traceback.print_exc()
  scrivi_errore('Errore recupero foto per link: '+link)
def recupera_dati(url):
 descrizioni=''
 riga_scrivi=''
 correlati_uniti=''
 browser.get(url)
 controllo=pagina_caricata(10,(By.CLASS_NAME,'container'))
 if controllo == 0:
  time.sleep(1.5)
  try:
   titolo=browser.find_elements(By.CLASS_NAME,'product-info__block.product-info__block--sm.product-info__title')[0].get_attribute('innerText').replace('\n',' ').replace(';',',').strip()
  except Exception:
   titolo=''
   scrivi_errore('Titolo non trovato per link: '+url)
  try: #BLOCCO CORRELATI
   lista_correlati=browser.find_elements(By.TAG_NAME,'product-recommendations')[0].find_elements(By.XPATH,".//div[contains(@class,'accessories-section')]")
   for el_correlato in lista_correlati:
    nome_correlato=el_correlato.find_elements(By.XPATH,".//div[contains(@class,'container')]")[0].get_attribute('innerText').strip() #PRENDE IL NOME DEL TIPO CORRELATO
    correlati_uniti=correlati_uniti+'|'+nome_correlato.replace('\n',' ').replace(';',',')
    val_correlati=el_correlato.find_elements(By.XPATH,".//div[contains(@class,'container')]")[1].find_elements(By.TAG_NAME,'ul')[0].find_elements(By.TAG_NAME,'product-card')
    for valore in val_correlati:
     valore_correlato=valore.find_elements(By.XPATH,".//*[contains(@class,'card__title')]")[0].get_attribute('innerText').strip() #PRENDE I TITOLI DEI CORRELATI DI QUEL TIPO
     correlati_uniti=correlati_uniti+'$'+valore_correlato.replace('\n',' ').replace(';',',')
  except Exception:
   scrivi_errore('Errore recupero correlati per link: '+url)
  correlati_uniti=correlati_uniti.strip()
  if correlati_uniti.startswith('|'):
   correlati_uniti=correlati_uniti[1:]
  browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #SCROLLA FINO IN FONDO ALLA PAGINA PERCHE L IFRAME SI CARICA DINAMICAMENTE
  time.sleep(1.5)
  try: #RECUPERO DESCRIZIONI
   lista_descrizioni=browser.find_elements(By.CLASS_NAME,'product-info__sticky')[0].find_elements(By.XPATH,".//div[@class='product-info__block']")
   del lista_descrizioni[:3]
   for poss_descrizione in lista_descrizioni:
    try:
     poss_descrizione.find_elements(By.TAG_NAME,'button')[0].click()
     time.sleep(1)
     nome_descrizione=browser.find_elements(By.TAG_NAME,'metafield-drawer')[0].find_elements(By.TAG_NAME,'header')[0].get_attribute('innerText').replace('\n',' ').replace(' Chiudi','').replace(';',',').strip()
     valore_descrizione=browser.find_elements(By.TAG_NAME,'metafield-drawer')[0].find_elements(By.XPATH,".//div[@class='drawer__content flex-auto shrink-0']")[0].get_attribute('innerText').replace('\n',' ').replace(';',',').strip()
     descrizioni=descrizioni+'$'+nome_descrizione+'|'+valore_descrizione
     try:
      browser.find_elements(By.CLASS_NAME,'talla-close')[1].click()
      time.sleep(1)
     except Exception:
      browser.find_elements(By.TAG_NAME,'metafield-drawer')[0].find_elements(By.XPATH,".//button[@class='drawer__close-btn js-close-drawer']")[0].click()
      time.sleep(1.5)
    except Exception:
     pass #ALCUNI SONO WIDGET CHE NON POSSONO ESSERE CLICCATI
  except Exception:
   descrizioni=''
  try: #GUIDA TAGLIA
   guida_taglie=browser.find_element(By.ID,'modalTallas').find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
  except Exception:
   guida_taglie=''
  try: #VIDEO
   link_video=browser.find_elements(By.XPATH,"//iframe[contains(@src,'youtube')]")[0].get_attribute('src').split('?')[0].replace('embed/','watch?')
  except Exception:
   link_video=''
   scrivi_errore('Video non trovato per '+url)
  riga_scrivi=url+';'+titolo+';'+correlati_uniti+';'+descrizioni+';'+guida_taglie+';'+link_video
  recupera_foto(url)
 return riga_scrivi
browser.get('https://mthelmets.com/it/collections/cascos')
controllo=pagina_caricata(10,(By.ID,'main-content'))
if controllo == 0:
 lista_link_cerca=[]
 try:
  lista_pagine=browser.find_elements(By.XPATH,"//a[contains(@href,'/it/collections/cascos?page=') and contains(@class,'link')]")
  ultima_pagina=int(lista_pagine[-1].get_attribute('innerText'))
 except Exception:
  scrivi_errore('Errore recupero numero pagine, lo script girerÃ  solo sulla prima pagina')
  ultima_pagina=int(1)
 for x in range(1,ultima_pagina+1):
  conta_errori=int(0)
  lista_link=[]
  lista_link=browser.find_elements(By.CLASS_NAME,'js-pagination-result')
  for elemento_link in lista_link:
   try:
    link_articolo=elemento_link.find_elements(By.XPATH,".//a[contains(@href,'it/products')]")[0].get_attribute('href')
   except Exception:
    scrivi_errore('Errore recupero link articolo')
    continue
   lista_link_cerca.append(link_articolo)
  time.sleep(2)
  if x == ultima_pagina:
   break
  link_nuovo=browser.find_element(By.XPATH,"//a[contains(@class,'pagination') and text()='"+str(x+1)+"']").click()
  time.sleep(2)
  controllo = pagina_caricata(10, (By.ID, 'main-content'))
  while controllo != 0 and conta_errori < 5:
    conta_errori=conta_errori+1
    controllo=pagina_caricata(10,(By.ID,'main-content'))
  if conta_errori == 5:
   scrivi_errore('Errore apertura link, fermato alla pagina'+str(x))
   break
 for link_cerca in lista_link_cerca:
  try:
   scrivi_riga=recupera_dati(link_cerca)
   f=open(file_dati,'a')
   f.write(scrivi_riga+"\n")
   f.close()
  except Exception:
   scrivi_errore('Errore recupero dati per link : '+link_cerca)

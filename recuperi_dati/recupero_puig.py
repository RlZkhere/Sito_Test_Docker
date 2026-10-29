from configurazione_recupero_puig import *
base_dir = os.path.dirname(os.path.abspath(__file__))
file_dati = os.path.join(base_dir, '../storage/PUIG/dati.csv')
file_foto = os.path.join(base_dir, '../storage/PUIG/foto.csv')
file_mancanti = os.path.join(base_dir, '../storage/PUIG/mancanti.csv') 
def recupera_foto(sku):
 try:
  conta_foto=int(0)
  lista_elementi_codici=browser.find_element(By.ID,'product').find_elements(By.TAG_NAME,'div')[0].find_elements(By.XPATH,".//div[not(@class)]") #PRENDE TABELLA ELEMENTI TROVATI
  for elemento in lista_elementi_codici:
   codice_trovato=elemento.find_elements(By.CLASS_NAME,'grid.grid-cols-4')[0].get_attribute('innerText').split('REF.')[1].split('\n')[0]
   if codice_trovato == sku: #SE IL CODICE E UGUALE ALLO SKU CERCATO
    lista_foto=elemento.find_elements(By.CLASS_NAME,'grid.grid-cols-4')[0].find_elements(By.XPATH,".//a[@data-type='image']")
    for foto in lista_foto:
     try:
      link_foto=foto.get_attribute('href')
      f=open(file_foto,'a',encoding='utf-8')
      f.write(sku+';'+link_foto+';'+str(conta_foto)+"\n")
      f.close()  
     except Exception:
      continue 
     conta_foto=conta_foto+1      
 except Exception:
  traceback.print_exc()     
def recupera_allegati(sku):
 dati_allegati=''
 try:
  lista_allegati=browser.find_element(By.ID,'documentation').find_elements(By.TAG_NAME,'div')[0].find_elements(By.XPATH,".//div[not(@class)]") #PRENDE LISTA DEGLI ALLEGATI
  for allegato in lista_allegati:
   nome_allegato = allegato.find_elements(By.TAG_NAME,'a')[1].get_attribute('innerText')
   if nome_allegato != 'OMOLOGAZIONE ABE':
    link_allegato=allegato.find_elements(By.TAG_NAME,'a')[1].get_attribute('href')
    dati_allegati=dati_allegati+'$'+nome_allegato+':'+link_allegato
  if dati_allegati.startswith('$'):
   dati_allegati=dati_allegati[1:]   
 except Exception:
  traceback.print_exc()
  dati_allegati='' 
 return dati_allegati      
def pagina_caricata(tempo,tipo):
 try:
  WebDriverWait(browser,tempo).until(EC.presence_of_element_located(tipo))
 except NoSuchElementException:
  raise('ERRORE CARICAMENTO PAGINA'+str(tipo))     
browser.get('https://puighitechparts.es/it')
pagina_caricata(10,(By.ID,'btn_config'))
browser.find_element(By.ID,'btn_config').click()
time.sleep(1.5)
try:
 browser.find_element(By.ID,'location').find_elements(By.XPATH,".//option[@value='IT']")[0].click()
 time.sleep(2)
 browser.find_elements(By.XPATH,"//button[@type='button' and @*[name()='wire:click']='save' ]")[0].click()
 time.sleep(1)
except Exception:
 traceback.print_exc()
browser.get('https://puighitechparts.es/it/tuning-motos')
pagina_caricata(10,(By.ID,'q'))
for codice in listasku:
 try:
  video_uniti=''
  titolo=''
  dati_tecnici=''
  dati_specifiche=''
  descrizione=''
  lista_colonne=[]
  lista_specifiche=[]
  dati_specifiche=''
  file_allegati=''
  lista_video=[]
  browser.find_element(By.ID,'q').clear()
  browser.find_element(By.ID,'q').send_keys(codice+Keys.ENTER)
  time.sleep(2)
  if 'tuning-motos?q=' in browser.current_url: 
   f=open(file_mancanti,'a',encoding='utf-8')
   f.write(codice+"\n")
   f.close()
   continue
  else: 
   try: #TITOLO
    titolo=browser.find_elements(By.XPATH,"//h1[contains(@class,'heading1')]")[0].get_attribute('innerText').strip().replace('\n','$').replace(';',',')
   except Exception:
    titolo=''
    traceback.print_exc()
    continue     
   #print(codice+';'+titolo)   
   try: #DATI TECNICI COLONNA
    try:
     lista_colonne=browser.find_elements(By.XPATH,"//nav[@aria-label='Tabs']")[0].find_elements(By.TAG_NAME,'a') #PRENDE TUTTE LE INTESTAZIONI
    except IndexError:
     pass    
    for valore in lista_colonne:
     id_tabella=valore.get_attribute('@click.prevent').replace("tab = ","tab === ") #OGNI INTESTAZIONE HA COME ATTRIBUTO IL LINK DELLA TABELLA CHE VIENE POI RICHIAMATO DAL CLICK
     nome_colonna=valore.get_attribute('innerText').strip()
     valore_colonna=browser.find_elements(By.XPATH, f'//div[@*[name()="x-show"]="{id_tabella}"]')[0].get_attribute('innerText').strip().replace('\n',' ').replace(':',' ').replace(';',',') #CERCA LA DIV CHE HA COME ATTRIBUTO L ID DELLA TABELLA
     dati_tecnici=dati_tecnici+nome_colonna+': '+valore_colonna+'$'
    if dati_tecnici.endswith('$'):
     dati_tecnici=dati_tecnici[:-1]    
   except Exception:
    dati_tecnici=''
    traceback.print_exc()    
   try: #SOTTOTTIOLO
    sottotitolo=browser.find_element(By.ID,'product').find_elements(By.CLASS_NAME,'mb-4')[0].get_attribute('innerText').strip().replace(';',',').replace('\n','.')
   except Exception:
    sottotitolo=''   
   try: #DESCRIZIONE
    descrizione=browser.find_elements(By.CLASS_NAME,'mb-16.px-8.prose')[0].get_attribute('innerText').strip().replace(';',',').replace('\n','')  
   except Exception:
    descrizione=''      
   try: #RECUPERA LISTA_SPECIFICHE
    lista_specifiche=browser.find_element(By.ID,'specifications').find_elements(By.TAG_NAME,'div')[0].find_elements(By.TAG_NAME,'div')
    for specifiche in lista_specifiche:
     dato_specifica=specifiche.get_attribute('innerText').strip().replace('\n','$').replace('$$','$').replace('$',':').replace(';',',')
     dati_specifiche=dati_specifiche+'$'+dato_specifica
    dati_specifiche=dati_specifiche.replace('$$','$')
    if dati_specifiche.endswith('$'):
     dati_specifiche=dati_specifiche[:-1]   
   except Exception:
    dati_specifiche=''   
    traceback.print_exc()
   try: #VIDEO
    lista_video=browser.find_element(By.ID,'tunnel_videos').find_elements(By.TAG_NAME,'iframe')
    for y in lista_video:
     link_video=y.get_attribute('src')
     nome_video=y.find_element(By.XPATH,"../../..").get_attribute('innerText').replace(';',',')
     video_uniti=video_uniti+'$'+nome_video+': '+link_video   
    if video_uniti.startswith('$'):
     video_uniti=video_uniti[1:]
    if video_uniti.endswith('$'):
     video_uniti=video_uniti[:-1]        
   except Exception:
    video_uniti=''       
   recupera_foto(codice)
   file_allegati=recupera_allegati(codice)
   f=open(file_dati,'a',encoding='utf-8')
   f.write(codice+';'+titolo+';'+dati_tecnici+';'+dati_specifiche+';'+';'+sottotitolo+';'+descrizione+';'+file_allegati+';'+video_uniti+"\n")
   f.close()
 except Exception:
  traceback.print_exc()

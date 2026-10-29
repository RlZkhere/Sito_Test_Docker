from configurazione_recupero_polini import *
cartella_attuale=os.path.dirname(os.path.abspath(__file__))
file_anagrafica=os.path.join(cartella_attuale , '../storage/POLINI/dati.csv')
file_foto=os.path.join(cartella_attuale , '../storage/POLINI/foto.csv')
file_compatibilita=os.path.join(cartella_attuale , '../storage/POLINI/compatibilita.csv')
browser.get('https://catalogue.polini.com/it/home.php')
pagina_caricata=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'code_word_search')))
def recupera_dati():
 link_pdf=''
 note=''
 dati_tecnici_uniti=''
 errori=int(0)
 try:
  sku=browser.find_elements(By.XPATH,"//div[@class='spb_wrapper clearfix']")[1].find_elements(By.TAG_NAME,'h2')[0].get_attribute('innerText').strip().split(' ')[0]
 except Exception:
  sku=''    
 try: #BLOCCO FOTO
  numero_foto=len(browser.find_elements(By.XPATH,"//a[@rel='lightbox']"))
  for i in range(numero_foto):
   link_foto=browser.find_elements(By.XPATH,"//a[@rel='lightbox']")[i].get_attribute('href')
   f=open(file_foto,'a')
   f.write(sku+';'+link_foto+';'+str(i+1)+"\n")
   f.close()
 except Exception:
  pass    
 try: #DESCRIZIONE
  descrizione=browser.find_elements(By.CLASS_NAME,'descrizione')[0].get_attribute('innerText').strip()  
  for elemento in lista_categorie:
   numero_a_capo=descrizione.count('\n')
   if numero_a_capo == 1:
    if elemento.lower() in descrizione.lower():
     continue
  if not descrizione.startswith('POLINI:'): #CONTIENE COMPATIBILITA
   numero_righe=descrizione.count('\n')
   if numero_righe == 0:
    f=open(file_compatibilita,'a')
    f.write(sku+';'+descrizione.strip()+"\n")
    f.close()
   if numero_righe > 1 :
    for i in range(numero_righe):
     riga=descrizione.split('\n')[i]
     prima_parola=riga.split(' ')[0].replace(':','')
     if prima_parola != prima_parola.upper():
      continue
     else:
      f=open(file_compatibilita,'a')
      f.write(sku+';'+riga+"\n")
      f.close()      
 except Exception:
  pass
 try: #NOTE PRODOTTO
  note=browser.find_elements(By.CLASS_NAME,'note-prodotto')[0].get_attribute('innerText').replace('\n','$').replace(';',', ').strip()
  note=note.replace('$$','$')
 except Exception:
  note=''     
 try:
  link_pdf=browser.find_elements(By.CLASS_NAME,'download-pdf')[0].find_elements(By.TAG_NAME,'a')[0].get_attribute('href').replace(';',', ')
  print(link_pdf)
 except Exception:
  link_pdf=''
 try: #BLOCCO DATI TECNICI
  contenitore_dati=browser.find_elements(By.XPATH,"//div[@class='spb_wrapper clearfix']")[0]
  numero_dati=len(contenitore_dati.find_elements(By.TAG_NAME,'span'))
  if numero_dati > 0:
   for j in range(numero_dati):
    classe_singolo=contenitore_dati.find_elements(By.TAG_NAME,'span')[j].get_attribute('class').replace('col-sm-3 col-xs-6 ','').replace('box-icona ','').replace(';',', ').strip()       
    nome_singolo=contenitore_dati.find_elements(By.TAG_NAME,'span')[j].get_attribute('innerText').replace(';',', ').strip()
    dati_tecnici_uniti=dati_tecnici_uniti+'|'+classe_singolo+'$'+nome_singolo
 except Exception:
  traceback.print_exc()     
 if dati_tecnici_uniti.startswith('|'):
  dati_tecnici_uniti=dati_tecnici_uniti[1:]     
 if dati_tecnici_uniti != '' or note != '' or link_pdf != '':
  f=open(file_anagrafica,'a') 
  f.write(sku+';'+dati_tecnici_uniti+';'+note+';'+link_pdf+"\n")
  f.close() 
for codice in listacodici:
 browser.find_element(By.ID,'code_word_search').clear()   
 browser.find_element(By.ID,'code_word_search').send_keys(codice+Keys.ENTER)
 try:
  nessun_risultato=WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH,"//div[@text='Number of results: 0']")))   
  continue
 except Exception:
  pass   
 try:
  ricerca_caricata=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'row.mini-blog-item-wrap')))
 except Exception:
  continue   
 numero_articoli=len(browser.find_elements(By.XPATH,"//div[@class='row mini-blog-item-wrap']"))
 if numero_articoli == 1:
  browser.find_elements(By.CLASS_NAME,'link-ricerca')[0].click()
 if numero_articoli > 1: 
  for x in range(numero_articoli):
   codice_trovato=browser.find_elements(By.XPATH,"//div[@class='row mini-blog-item-wrap']")[x].find_elements(By.CLASS_NAME,'col-xs-10')[0].find_elements(By.TAG_NAME,'p')[0].find_elements(By.TAG_NAME,'strong')[0].get_attribute('innerText').strip()
   if codice_trovato == codice:
    browser.find_elements(By.CLASS_NAME,'link-ricerca')[x].click()
    break    
 articolo_caricato=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'container')))
 try:
  recupera_dati()
 except Exception:
  traceback.print_exc()      

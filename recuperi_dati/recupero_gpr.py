from configurazione_recupero_gpr import *
from bs4 import BeautifulSoup
base_dir = os.path.dirname(os.path.abspath(__file__))
file_log = os.path.join(base_dir, '../storage/GPR/log.csv')
file_dati = os.path.join(base_dir, '../storage/GPR/dati.csv')
file_foto = os.path.join(base_dir, '../storage/GPR/foto.csv')
file_video = os.path.join(base_dir, '../storage/GPR/video.csv')
lista_righe_scrivi=[]
def scrivi_errore(errore):
 f=open(file_log,'a')
 f.write('Elemento '+str(errore)+' non trovato'+"\n")
 f.close()
def pagina_caricata(tempo,tipo):
 try:   
  pagina_caricata=WebDriverWait(browser,tempo).until(EC.presence_of_element_located(tipo)) 
 except TimeoutException:
  scrivi_errore(tipo)
browser.get('https://www.gpr.it/')
def recupero_foto(codice):
 lista_foto=[]
 try:
  numero_foto=len(browser.find_elements(By.CLASS_NAME,'owl-stage-outer')[0].find_elements(By.XPATH,".//div[contains(@class,'owl-item not_cloned')]"))
  for x in range(numero_foto+1):
   link_foto=browser.find_elements(By.CLASS_NAME,'owl-stage-outer')[0].find_elements(By.CLASS_NAME,'owl-item.active.not_cloned')[0].find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
   lista_foto.append(codice+';'+link_foto+';'+str(x+1))
   browser.execute_script("document.getElementsByClassName('owl-next')[0].click()")
   time.sleep(1)
  f=open(file_foto,'a')
  for foto in lista_foto:
   f.write(foto+"\n")
  f.close()   
 except Exception:
  traceback.print_exc()   
def recupero_prestazioni(html):
 righe_valori=''
 riga_intestazioni=''
 lista_intestazioni=''
 tabella_finale=''
 tabella_html=BeautifulSoup(html,'html.parser') 
 intestazioni_html=tabella_html.find(class_="col_vals head").find(class_="cdata").find_all('div')
 for i in intestazioni_html:
  righe_finali=''
  intestazione=i.get_text()
  riga_intestazioni=riga_intestazioni+'<th>'+intestazione+'</th>'
  riga_intestazioni='<thead><tr>'+riga_intestazioni+'</tr></thead>'
  valori_html=tabella_html.find_all("div", {"id": "maxpower"})
 for blocco in valori_html:
  righe_tabella=blocco.find_all("div")
  conta_dati=int(0)
  conta_unita=int(0)
  valori_temporanei=''     
  for riga in righe_tabella:
   if riga.get("class",[]) == ["col_test", "text"]:
    nome_valore=riga.get_text().strip()
   if riga.get("class") == ["cval"]:
    valore_riga=riga.get_text().strip().split('A')[0].strip()
    valori_temporanei=valori_temporanei+'<td>'+valore_riga+'</td>'
    conta_dati=conta_dati+1         
    if conta_dati == 2:
     unita_misura=blocco.find_all("div", {"class": "cval first"})[conta_unita].get_text().strip()              
     righe_valori = righe_valori + '<tr><td>'+ unita_misura + '</td>' + valori_temporanei + '</tr>'
     conta_unita=conta_unita+1
     conta_dati=0
     valori_temporanei=''              
  righe_valori=righe_valori.replace('<tr><td>','<tr><td></td><td>')
  righe_valori=righe_valori.replace('<tr><td></td>','<tr><td>'+nome_valore+'</td>',1)
  tabella_finale+=righe_valori
  righe_valori=''
 riga_intestazioni='<thead><tr><th>VALORE</th><th>Unita</th><th>Stock</th><th>GPR</th></tr></thead>'
 tabella_finale='<table>'+riga_intestazioni+tabella_finale.replace('Max. Torque','<strong>Coppia Massima</strong>').replace('Max. Power','<strong>Potenza Massima</strong>')+'</table>'
 return tabella_finale
def recupera_dati(url):
 sku = ''
 sottotitolo = ''
 descrizione = ''
 dati_uniti = ''
 prestazioni = ''
 tag_uniti = ''
 lista_video=[]
 browser.execute_script("window.open(arguments[0])",url)
 time.sleep(0.5)
 browser.switch_to.window(browser.window_handles[1])
 pagina_caricata(10,(By.CLASS_NAME,'titol_article'))
 try:
  lista_dati=browser.find_elements(By.CLASS_NAME,'dades_extra')[0]
 except Exception:
  scrivi_errore(url)
  lista_dati=''
 if lista_dati != '':
  sku=lista_dati.find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'span').get_attribute('innerText').strip()
  try:
   lista_tags=lista_dati.find_elements(By.XPATH,".//*[text()='Tags:']")[0].find_element(By.XPATH,"..").find_elements(By.TAG_NAME,'a') #GUARDA TUTTI I TAG(CI POSSONO ESSERE INFORMAZIONI IMPORTANTI)
   for tag in lista_tags:
    nome_tag=tag.get_attribute('innerText')
    if len(nome_tag) > 5:
     tag_uniti=tag_uniti+'$'+nome_tag  
  except Exception:   
   scrivi_errore('Tag non presenti per '+url)
  try: #SOTTOTITOLO
   sottotitolo=browser.find_elements(By.CLASS_NAME,'subtitle_product')[0].get_attribute('innerText').replace('\n','').replace(';',',')
  except Exception:
   sottotitolo=''
   scrivi_errore('SOTTOTITOLO per '+sku)   
  try: #DATI TECNICI
   dati_uniti=''
   blocco_dati_tecnici=browser.find_elements(By.XPATH,"//p[text()='CARATTERISTICHE TECNICHE']")[0].find_element(By.XPATH,"../..").find_elements(By.XPATH,"//div[contains(@id,'ui-accordion-accordion')]")[0]
   lista_dati_tecnici=blocco_dati_tecnici.find_elements(By.XPATH,".//div[contains(@class,'bloc carac')]")
   for dato_tecnico in lista_dati_tecnici:
    nome_dato=dato_tecnico.find_elements(By.TAG_NAME,'div')[0].get_attribute('innerHTML')
    valore_dato=dato_tecnico.find_elements(By.TAG_NAME,'div')[1].get_attribute('innerHTML')
    dati_uniti=dati_uniti+nome_dato+':'+valore_dato+'$'
   dati_uniti=dati_uniti.replace(';',',')
   if dati_uniti.endswith('$'):
    dati_uniti=dati_uniti[:-1]       
  except Exception:
   scrivi_errore('DATI_TECNICI per '+sku)
  try: #DESCRIZIONE
   descrizione=browser.find_elements(By.ID,'content_text')[0].get_attribute('innerText').replace('\n',',').replace(';',',')
  except Exception:
   descrizione=''      
  try: #VIDEO NON SEMPRE PRESENTE        
   lista_video=browser.find_elements(By.XPATH,"//div[contains(@onclick,'youtube')]")
   for j in lista_video:
    video=j.get_attribute('onclick')
    if '(' in video:
     video=video.split('(')[1].split(')')[0].replace("'","")
    f=open(file_video,'a')
    f.write(sku+';'+video+"\n")
    f.close()    
  except Exception:
   traceback.print_exc()
   video=''
  try: #BLOCCO PRESTAZIONI
   tabella=browser.find_elements(By.CLASS_NAME,'gpr_vs_stock')[0].get_attribute('innerHTML')
   if tabella:
    prestazioni=recupero_prestazioni(tabella)    
  except Exception:
   scrivi_errore('SCHEDA_PRESTAZIONI per '+sku)
  try:
   recupero_foto(sku)  
  except Exception:
   scrivi_errore('FOTO per '+sku)      
 riga_scrivi=sku+';'+sottotitolo+';'+tag_uniti+';'+descrizione+';'+dati_uniti+';'+prestazioni
 browser.close() #A PRIORI DOPO TUTTO CHIUDE
 time.sleep(1)
 browser.switch_to.window(browser.window_handles[0])
 return riga_scrivi
try:
 pagina_caricata(10,(By.XPATH,"//button[@onclick='deleteAllCookies();']"))
 browser.find_elements(By.XPATH,"//button[@onclick='deleteAllCookies();']")[0].click()
 time.sleep(2)
except Exception as e:
 print('Errore: '+str(e))
try:
 barra_elementi=browser.find_element(By.ID,'camp-recerca')
except NoSuchElementException:
 try:
  barra_elementi=browser.find_elements(By.XPATH,"//input[contains(@placeholder,'Cerca')]")[0].find_element(By.XPATH,"..")
 except Exception:
  barra_elementi=''    
if barra_elementi == '':
 scrivi_errore('Barra elementi')
else:
 for valore in listasku:
  lista_codici=[]
  try:
   barra_elementi=browser.find_element(By.ID,'camp-recerca')
   print(barra_elementi.get_attribute('innerHTML'))
   barra_elementi.send_keys(valore+Keys.ENTER)
   pagina_caricata(30,(By.XPATH,"//span[contains(text(),'RISULTATI DELLA RICERCA:')]"))
   time.sleep(2)
  except Exception: 
   scrivi_errore('SKU '+str(valore))
   continue 
  try:
   lista_codici=browser.find_element(By.ID,'result_articles').find_elements(By.XPATH,".//div[@class='bloc_article']")
  except (StaleElementReferenceException,NoSuchElementException):
   scrivi_errore('SKU '+str(valore))
   lista_codici=[]  
  for x in lista_codici:
   codice=x.find_element(By.CLASS_NAME,'text_desc').find_elements(By.TAG_NAME,'span')[1].get_attribute('innerText').strip() 
   if codice == valore:
    try:
     link_articolo=x.find_elements(By.XPATH,".//link[@itemprop='url']")[0].get_attribute('href')
     output_dati=recupera_dati(link_articolo)
     lista_righe_scrivi.append(output_dati)
     if len(lista_righe_scrivi) == 50:
      with open(file_dati,'a',encoding='utf-8') as file:
       for riga_s in lista_righe_scrivi:
        file.write(riga_s+"\n")
      lista_righe_scrivi.clear()  
     time.sleep(2)   
    except Exception:
     traceback.print_exc()   
    break      
browser.quit()
if len(lista_righe_scrivi) > 0:   
 with open(file_dati,'a',encoding='utf-8') as file:   
  for riga_s in lista_righe_scrivi:
   file.write(riga_s+"\n")      

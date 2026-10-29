from configurazione_recupero_arrow import * 
base_dir = os.path.dirname(os.path.abspath(__file__))
file_foto = os.path.join(base_dir, '../storage/ARROW/foto.csv')
file_prestazioni = os.path.join(base_dir, '../storage/ARROW/prestazioni.csv')
def pagina_caricata(tempo,tipo):
 try:
  WebDriverWait(browser,tempo).until(EC.presence_of_element_located((tipo)))  
 except Exception:
  traceback.print_exc()      
def recupera_prestazioni():
 conta=int(0)
 prima_colonna=[]
 seconda_colonna=[]
 terza_colonna=[]
 quarta_colonna=[]
 tabella_finale=[]
 tabella_html=browser.find_element(By.ID,'datiMontaggio').find_elements(By.CLASS_NAME,'row')[0].get_attribute('innerHTML')
 soup=BeautifulSoup(tabella_html,'html.parser')
 parenti=soup.findAll(class_= 'row')
 for parente in parenti:
  conta=conta+1
  righe=parente.findAll('div')
  for riga in righe:
   classe=riga['class']
   if len(classe) > 1:
    tipo_valore=classe[1]
    if tipo_valore == 'subtitle' and conta == 1:
     prima_colonna.append('<td>'+riga.text+'</td>')
    if tipo_valore == 'dataMont':
     if conta == 1:
      seconda_colonna.append('<td>'+riga.text+'</td>')
     if conta == 2:
      terza_colonna.append('<td>'+riga.text+'</td>')
     if conta == 3:
      quarta_colonna.append('<td><strong>'+riga.text+'</strong></td>')   
 prima_colonna.insert(0,'<td>VALORE</td>')
 seconda_colonna.insert(0,'<td>ORIGINALE</td>')
 terza_colonna.insert(0,'<td>ARROW</td>')
 quarta_colonna.insert(0,'<td><strong>MIGLIORAMENTO</strong></td>')
 for valore in [prima_colonna,seconda_colonna,terza_colonna,quarta_colonna]:
  valore.insert(0,'<tr>')
  valore.append('</tr>')
  tabella_finale.extend(valore)
 tabella_finale="".join(tabella_finale)
 tabella_finale='<table>'+tabella_finale+'</table>'
 return tabella_finale
def recupera_dati(sku,link):
 browser.execute_script("window.open('');")
 time.sleep(0.5)
 browser.switch_to.window(browser.window_handles[1])
 time.sleep(1)
 browser.get(link)
 pagina_caricata(10,(By.ID,'montaggio-moto'))
 time.sleep(0.5)
 try:
  nome_moto=browser.find_element(By.ID,'montaggio-moto').get_attribute('innerText')
 except Exception:
  nome_moto=''   
 try: #BLOCCO_FOTO
  numero_foto=len(browser.find_elements(By.CLASS_NAME,'slick-dots')[0].find_elements(By.TAG_NAME,'li'))
  for i in range(numero_foto):
   codice_foto=browser.find_element(By.ID,'nome-montaggio').find_elements(By.TAG_NAME,'h5')[0].get_attribute('innerText')
   link_foto=browser.find_elements(By.XPATH,"//div[@class='h700-300 imgCover slick-slide slick-current slick-active']")[0].get_attribute('style').replace('background-image: url(','').split('?')[0].replace(' ','%20').replace('"','')  
   if codice_foto == sku:
    f=open(file_foto,'a')
    f.write(sku+';'+nome_moto+';'+link_foto+';'+str(i+1)+"\n")
    f.close()    
   try:  
    browser.find_elements(By.CLASS_NAME,'slick-dots')[0].find_elements(By.TAG_NAME,'li')[i+1].find_elements(By.TAG_NAME,'button')[0].click()
    time.sleep(1)
   except Exception:
    break       
 except Exception:
  pass
 try:
  tabella=recupera_prestazioni()
  f=open(file_prestazioni,'a')
  f.write(sku+';'+nome_moto+';'+tabella+"\n")
  f.close()
 except Exception:
  traceback.print_exc()     
 browser.close()
 browser.switch_to.window(browser.window_handles[0]) 
browser.get('https://www.arrow.it/it/')
pagina_caricata(10,(By.XPATH,"//button[text()='Rifiuta tutto']"))
browser.find_elements(By.XPATH,"//button[text()='Rifiuta tutto']")[0].click()
time.sleep(2)
browser.find_element(By.ID,'cookiescript_accept').click()
time.sleep(1)
browser.find_element(By.ID,'navbarSearchBike').find_elements(By.TAG_NAME,'a')[0].click()
time.sleep(1.5)
for codice in listasku:
 lista_codici=[]
 browser.find_element(By.ID,'searchInputModal').find_elements(By.XPATH,".//input[@alt='Cerca la tua moto...']")[0].clear()
 time.sleep(0.5)
 browser.find_element(By.ID,'searchInputModal').find_elements(By.XPATH,".//input[@alt='Cerca la tua moto...']")[0].send_keys(codice)
 time.sleep(2.5)
 lista_codici=browser.find_elements(By.CLASS_NAME,'ui-menu-item')
 for codice_trovato in lista_codici:
  id_pagina=codice_trovato.get_attribute('id')
  link_moto = 'https://www.arrow.it/'+browser.execute_script(f'''var item = $("#{id_pagina}").data("ui-autocomplete-item"); var testo = item.label.replace(/<[^>]*>/g, "").trim(); return "/it/assembled/" + item.value + "/" + testo.replace(/\\s+/g, "-")
  .replace(/\\//g, "-").replace(/:+/g, "-");''')
  recupera_dati(codice,link_moto)

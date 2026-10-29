from configurazione_recupero_quadlock import *
import re
cartella_attuale=os.path.dirname(os.path.abspath(__file__))
file_foto=os.path.join(cartella_attuale,'../storage/QUADLOCK/foto.csv')
file_dati=os.path.join(cartella_attuale,'../storage/QUADLOCK/dati.csv')
def pagina_caricata(tempo,tipo):
 try:
  WebDriverWait(browser,tempo).until(EC.presence_of_element_located(tipo))
 except NoSuchElementException:
  raise Exception('PAGINA NON CARICATA')
def recupera_dati(link_prodotto,sku_cercato):
 sottocategorie_unite=''
 valori_uniti=''
 lista_informazioni=[]
 lista_sottocategorie=[]
 conta_foto=int(0)
 browser.execute_script('window.open()')
 browser.switch_to.window(browser.window_handles[1])
 time.sleep(0.5)
 try:
  browser.get(link_prodotto)
  try:
   pagina_caricata(10,(By.CLASS_NAME,'product__title.mt-0.mb-1'))
   time.sleep(2)
  except Exception:
   time.sleep(5)   
  try: #BLOCCO FOTO
   lista_foto=browser.find_elements(By.XPATH,"//ul[@class='splide__list']")[0].find_elements(By.TAG_NAME,'li')
   for foto in lista_foto:
    link_foto=foto.find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
    try:
     link_foto=link_foto.split('?')[0]
    except Exception:
     pass     
    conta_foto=conta_foto+1
    f=open(file_foto,'a')
    f.write(sku_cercato+';'+link_foto+';'+str(conta_foto)+"\n")
    f.close()
  except Exception:
   pass      
  try: #ALTRE INFORMAZIONI
   lista_informazioni=browser.find_elements(By.XPATH,"//div[@class='product__info--tabs col-md-6 p-0']")[0].find_elements(By.TAG_NAME,'ul')[0].find_elements(By.TAG_NAME,'li')
   for valore in lista_informazioni:
    conta_sottocategorie=int(0)
    nome_valore=valore.find_elements(By.TAG_NAME,'button')[0].get_attribute('innerText').replace('\n','').replace(';',', ').strip()
    bottone=valore.find_elements(By.TAG_NAME,'button')[0]
    browser.execute_script("arguments[0].click();",bottone)
    time.sleep(2)
    if nome_valore == 'SPECIFICHE TECNICHE':
     lista_sottocategorie=dato_valore=browser.find_elements(By.XPATH,".//div[@class='row ' and parent::*[@class='w-100']]")[0].find_elements(By.TAG_NAME,'details')
     for sottocategoria in lista_sottocategorie:
      if conta_sottocategorie != 0:
       pulsante=sottocategoria.find_elements(By.TAG_NAME,'summary')[0]
       browser.execute_script("arguments[0].click();",pulsante)
       time.sleep(2)      
      nome_sottocategoria=sottocategoria.find_elements(By.TAG_NAME,'summary')[0].get_attribute('innerText').replace('\n',' ').replace(';',', ').strip()
      valore_sottocategoria=sottocategoria.find_elements(By.TAG_NAME,'div')[0].find_elements(By.TAG_NAME,'ul')[0].get_attribute('innerText').replace('\n',' ').replace(';',', ').strip()
      sottocategorie_unite=sottocategorie_unite+'$'+nome_sottocategoria+': '+valore_sottocategoria
      conta_sottocategorie=conta_sottocategorie+1
     if sottocategorie_unite.startswith('$'):
      sottocategorie_unite=sottocategorie_unite[1:]      
    else:
     dato_valore=browser.find_elements(By.XPATH,".//div[@class='row ' and parent::*[@class='w-100']]")[0].get_attribute('innerText').replace('\n',' ').replace(';',', ').strip()
     valori_uniti=valori_uniti+'$'+nome_valore+': '+dato_valore
    if valori_uniti.startswith('$'):
     valori_uniti=valori_uniti[1:]   
  except Exception:
   traceback.print_exc()     
  try: #PRENDI MODELLO TELEFONO
   compatibilita=browser.find_elements(By.XPATH,"//button[contains(., 'Telefono')]")[0].find_element(By.XPATH,"../..").find_elements(By.XPATH,".//li[@class='active']")[0]
   nome_telefono=compatibilita.get_attribute('innerText') 
   try:
    nome_telefono=nome_telefono.split('+')[0].strip()
   except Exception:
    pass
   nome_telefono=nome_telefono.upper()
  except Exception:
   nome_telefono=''   
  try: #PRENDI NOME CUSTODIA
   tipo_accessorio=browser.find_elements(By.XPATH,"//button[contains(., 'Telefono')]")[0].find_element(By.XPATH,"../..").find_elements(By.XPATH,".//div[starts-with(@class,'buy__variant--title')]")[0].get_attribute('innerText').replace('\n',' ').strip()
   if tipo_accessorio.upper() != nome_telefono:
    pass
   else:
    tipo_accessorio=''     
  except Exception:
   tipo_accessorio=''      
  f=open(file_dati,'a')
  f.write(sku_cercato+';'+valori_uniti+';'+sottocategorie_unite+';'+nome_telefono+';'+tipo_accessorio+"\n")
  f.close()
 except Exception:
  traceback.print_exc()
 browser.close()
 time.sleep(0.5)
 browser.switch_to.window(browser.window_handles[0]) 
browser.get('https://www.quadlockcase.eu')
time.sleep(5)
bottone_cookies = browser.find_element(By.XPATH, "//csm-cookie-consent[@class='csm-cmp-root needsclick']")
browser.execute_script(""" var host = arguments[0]; var buttons = host.shadowRoot.querySelectorAll("button"); for (var btn of buttons) { if (btn.innerText.includes("Reject")) { btn.click(); break; } } """, bottone_cookies)
time.sleep(3)
try:
 browser.find_elements(By.XPATH,"//a[@class='btn btn--link text-uppercase font-family-gotham mt-3 d-block text-center js-language-switch']")[0].click()
 time.sleep(2)
except Exception:
 pass   
try: 
 pagina_caricata(10,(By.XPATH,"//div[@role='dialog' and @aria-label='POPUP Form']"))
 browser.find_elements(By.XPATH,"//div[@role='dialog' and @aria-label='POPUP Form']")[0].click()
 time.sleep(2)
except Exception:
 pass
browser.get('https://www.quadlockcase.eu/it/pages/search-results') 
pagina_caricata(10,(By.ID,'js-search-page-input'))
for codice_cerca in listasku:
 numero_prodotti=int(0)
 browser.find_element(By.ID,'js-search-page-input').clear()
 browser.find_element(By.ID,'js-search-page-input').send_keys(codice_cerca)
 time.sleep(0.5)
 browser.find_element(By.ID,'js-search-page-input').send_keys(Keys.ENTER)
 time.sleep(1)
 pagina_caricata(10,(By.ID,'fs-product-grid-container'))
 link_articolo=browser.find_element(By.ID,'fs-product-grid-container').find_elements(By.TAG_NAME,'div')[0].find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
 recupera_dati(link_articolo,codice_cerca)

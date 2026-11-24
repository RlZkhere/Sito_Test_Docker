#!/opt/python2/bin/python2.7
# -*- coding: utf-8 -*-
from gimpfu import *
import os
import zipfile
def salva_foto(dir_immagini,file_salva):
 lista_zip=[]
 for x in os.listdir(dir_immagini):
  lista_zip.append(dir_immagini+x)
 with zipfile.ZipFile(file_salva,"w",zipfile.ZIP_DEFLATED) as zfile:
  for y in lista_zip:
   if y != 'foto_nuove.zip':
    zfile.write(y, arcname=os.path.basename(y))
def sistema_foto(foto,colore_cambia,r,g,b,ps_file):
 if r == g and g == b:
  livello=foto.active_layer
  punti=[0,0,colore_cambia,255,255,255]
  pdb.gimp_curves_spline(livello,HISTOGRAM_VALUE,len(punti),punti)
  pdb.file_jpeg_save(foto,livello,ps_file,ps_file,0.95,0,1,1,"",0,1,0,0)
def controllo(): 
 cartella='/var/www/html/storage/MODIFICA-FOTO/'
 percorso_zip=cartella+'foto_nuove.zip'
 for file in os.listdir(cartella):
  risultato=int(0)
  lista_px=[]
  percorso_file=cartella+file
  immagine=pdb.gimp_file_load(percorso_file,percorso_file)
  larghezza=immagine.width
  altezza=immagine.height
  livello=immagine.active_layer
  da=pdb.gimp_drawable_get_pixel(livello,0,0)
  sa=pdb.gimp_drawable_get_pixel(livello,(larghezza-1),0)
  db=pdb.gimp_drawable_get_pixel(livello,0,(altezza-1))
  sb=pdb.gimp_drawable_get_pixel(livello,(larghezza-1),(altezza-1))
  lista_px.append(da)
  lista_px.append(sa)
  lista_px.append(db)
  lista_px.append(sb)
  for pixel in lista_px:
   r,g,b=pixel[1]
   for colore in r,g,b:
    if colore <= 245:
     sistema_foto(immagine,colore,r,g,b,percorso_file)
     risultato=1
     break
   if risultato == 1:
    break
  pdb.gimp_image_delete(immagine)
 salva_foto(cartella,percorso_zip)   
register(
"python-fu-controlla-bordo",
"Controllo colore bordi",
"Script che controlla il colore dei bordi in modo da evitare foto a sfondo rosa",
"Khere",
"Khere",
"2026-11-24",
"Controlla bordi",
"",
[],
[],
controllo
)
main()

#!/opt/python2/bin/python2.7
# -*- coding: utf-8 -*-
from gimpfu import *
import os
import zipfile
def maggiore(x,y):
 if x >= y:
  return x
 else:
  return y   
def crea_foto_finale(immagine,dimensioni):
 larghezza = pdb.gimp_image_width(immagine)
 altezza = pdb.gimp_image_height(immagine)
 offset_x = int((dimensioni - larghezza) / 2)
 offset_y = int((dimensioni - altezza) / 2)
 pdb.gimp_context_set_background((255, 255, 255))
 pdb.gimp_image_resize(immagine,dimensioni,dimensioni,offset_x,offset_y)
 livello_sfondo = pdb.gimp_layer_new(immagine,dimensioni,dimensioni,RGB_IMAGE,"Sfondo bianco",100,NORMAL_MODE)
 pdb.gimp_image_insert_layer(immagine,livello_sfondo,None,-1)
 pdb.gimp_image_lower_item_to_bottom(immagine,livello_sfondo)
 pdb.gimp_drawable_fill(livello_sfondo,BACKGROUND_FILL)
 pdb.gimp_image_merge_visible_layers(immagine,CLIP_TO_IMAGE)
 return immagine
def scala_foto():
 lista_file=[]
 percorso='/var/www/html/storage/MODIFICA-FOTO/'
 for file in os.listdir(percorso): 
  try:
   percorso_file=percorso+file
   immagine=pdb.gimp_file_load(percorso_file,percorso_file)
   livello=pdb.gimp_image_get_active_layer(immagine)
   larghezza=pdb.gimp_image_width(immagine)
   altezza=pdb.gimp_image_height(immagine)
   if larghezza > 1800 or altezza > 1800 or (larghezza+altezza) > 3500:
    larghezza_nuova=2400
    altezza_nuova=2400
    if larghezza_nuova > larghezza and altezza_nuova > altezza:
     immagine=crea_foto_finale(immagine,2400)
    else: 
     lato_maggiore=maggiore(larghezza,altezza)
     proporzione=lato_maggiore/2400.0
     pdb.gimp_image_scale(immagine,int(larghezza/proporzione),int(altezza/proporzione))
     immagine=crea_foto_finale(immagine,2400)
   elif larghezza < 1200 and altezza < 1200: 
     lato_maggiore=maggiore(larghezza,altezza)
     proporzione=1200.0/lato_maggiore
     pdb.gimp_image_scale(immagine,int(larghezza*proporzione),int(altezza*proporzione))
     immagine=crea_foto_finale(immagine,1200)
   elif (larghezza > 1200 and altezza > 1200) or (larghezza >= 1200 and larghezza <= 1800 and altezza <=1200) or (altezza >= 1200 and altezza <= 1800 and larghezza <=1200):
     lato_maggiore=maggiore(larghezza,altezza)
     proporzione=lato_maggiore/1200.0
     altezza_nuova=altezza/proporzione
     larghezza_nuova=larghezza/proporzione
     pdb.gimp_image_scale(immagine,int(larghezza_nuova),int(altezza_nuova))
     immagine=crea_foto_finale(immagine,1200)      
   livello=pdb.gimp_image_get_active_layer(immagine)
   pdb.file_jpeg_save(immagine, livello, percorso_file, percorso_file, 0.95, 0, 1, 1, "", 0, 1, 0, 0)
   #pdb.file_png_save_defaults(immagine, livello, percorso_file, percorso_file)  
   pdb.gimp_image_delete(immagine)
   lista_file.append(percorso_file)
  except Exception:
   continue   
 with zipfile.ZipFile(percorso+"foto_nuove.zip","w") as zfile:
  for x in lista_file:
   try:
    zfile.write(x,arcname=os.path.basename(x))
   except Exception:
    continue
register(
    "python-fu-batch-scala-foto",
    "Scala la foto",
    "Scala la foto in base alla grandezza originale",
    "Khere",
    "Khere",
    "2026-10-13",
    "Scala l immagine",
    "",
    [],
    [],
    scala_foto
)
main()

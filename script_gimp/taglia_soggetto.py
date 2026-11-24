#!/opt/python2/bin/python2.7
# -*- coding: utf-8 -*-
from gimpfu import *
import os
import zipfile
percorso='/var/www/html/storage/MODIFICA-FOTO/'
def salva_foto(lista_foto):
 with zipfile.ZipFile(percorso+"foto_nuove.zip","w") as zfile:
  for x in lista_foto:
   try:
    zfile.write(x,arcname=os.path.basename(x))
   except Exception:
    continue   
def dimensioni(x,y):
 if x >= y:
  return x
 else:
  return y   
def taglia_contenuto():
 lista_file=[] 
 for file in os.listdir(percorso): 
  try:
   percorso_file=percorso+file
   immagine=pdb.gimp_file_load(percorso_file,percorso_file)
   livello=pdb.gimp_image_get_active_layer(immagine)
   pdb.plug_in_autocrop(immagine, livello)
   larghezza=immagine.width
   altezza=immagine.height
   lato_lungo=dimensioni(larghezza,altezza)
   if lato_lungo < 1100:
    rapporto=1100.0/lato_lungo
    pdb.gimp_image_scale(immagine,int(larghezza*rapporto),int(altezza*rapporto))
   livello=pdb.gimp_image_get_active_layer(immagine)
   pdb.file_png_save_defaults(immagine,livello,percorso_file,percorso_file)
   pdb.gimp_image_delete(immagine)
   lista_file.append(percorso_file)
  except Exception:
   continue 
 salva_foto(lista_file)  
register(
    "python-fu-batch-taglia-soggetto",
    "Taglia la foto al soggetto",
    "Ritaglia la foto al soggetto",
    "Khere",
    "Khere",
    "2026-10-13",
    "Taglia foto al soggetto",
    "",
    [],
    [],
    taglia_contenuto
)
main()

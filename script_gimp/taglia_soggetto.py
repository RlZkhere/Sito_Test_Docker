#!/opt/python2/bin/python2.7
# -*- coding: utf-8 -*-
from gimpfu import *
import os
import zipfile
def taglia_contenuto():
 lista_file=[]
 percorso='/var/www/html/storage/MODIFICA-FOTO/'
 for file in os.listdir(percorso): 
  try:
   percorso_file=percorso+file
   immagine=pdb.gimp_file_load(percorso_file,percorso_file)
   livello=pdb.gimp_image_get_active_layer(immagine)
   pdb.plug_in_autocrop(immagine, livello)
   livello=pdb.gimp_image_get_active_layer(immagine)
   pdb.file_png_save_defaults(immagine,livello,percorso_file,percorso_file)
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

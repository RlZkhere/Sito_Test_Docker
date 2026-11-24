#!/opt/python2/bin/python2.7
# -*- coding: utf-8 -*-
from gimpfu import *
import os
import zipfile
lista_file=[]
percorso_cartella='/var/www/html/storage/MODIFICA-FOTO'
def salva_foto(lista_immagini):
 with zipfile.ZipFile(percorso_cartella+"/foto_nuove.zip","w") as zfile:
  for x in lista_immagini:
   try:
    zfile.write(x,arcname=os.path.basename(x))
   except Exception:
    continue    
def foto_specchiata():
 for file in os.listdir('/var/www/html/storage/MODIFICA-FOTO/'): 
  try:
   if '_1' in file: 
    percorso_file=percorso_cartella+'/'+file
    percorso_terzo_file=percorso_file.replace('_1','_3')
    percorso_secondo_file=percorso_file.replace('_1','_2')
    immagine=pdb.gimp_file_load(percorso_file,percorso_file)
    livello=pdb.gimp_image_get_active_layer(immagine)
    pdb.gimp_item_transform_flip_simple(livello, ORIENTATION_HORIZONTAL, True, 0)
    livello=pdb.gimp_image_get_active_layer(immagine)
    pdb.file_png_save_defaults(immagine,livello,percorso_terzo_file,percorso_terzo_file)
    pdb.gimp_image_delete(immagine)
    os.rename(percorso_file,percorso_secondo_file)
    immagine_n_1=pdb.gimp_file_load(percorso_secondo_file,percorso_secondo_file)
    immagine_n_2=pdb.gimp_file_load(percorso_terzo_file,percorso_terzo_file)
    livello_1=pdb.gimp_image_get_active_layer(immagine_n_1) 
    pdb.plug_in_autocrop(immagine_n_1, livello_1)
    altezza_1=pdb.gimp_image_height(immagine_n_1)
    larghezza_1=pdb.gimp_image_width(immagine_n_1) 
    rapporto_1=1200.0 / altezza_1
    larghezza_max_1 = int(larghezza_1 * 1200.0 / altezza_1)
    livello_2=pdb.gimp_image_get_active_layer(immagine_n_2)
    pdb.plug_in_autocrop(immagine_n_2, livello_2)
    altezza_2=pdb.gimp_image_height(immagine_n_2)
    larghezza_2=pdb.gimp_image_width(immagine_n_2) 
    rapporto_2=1200.0 / altezza_2 
    larghezza_max_2 = int(larghezza_2 * 1200.0 / altezza_2)
    if larghezza_max_1 <= 2400:
     pdb.gimp_image_scale(immagine_n_1,larghezza_max_1,1200)
     altezza_1=1200
    else: 
     larghezza_max_1=larghezza_1
    if larghezza_max_2 <= 2400:
     pdb.gimp_image_scale(immagine_n_2,larghezza_max_2,1200)
     altezza_2=1200
    else:
     larghezza_max_2=larghezza_2   
    sfondo=pdb.gimp_image_new(2400,2400,RGB_IMAGE)
    livello_sfondo=pdb.gimp_layer_new(sfondo,2400,2400,RGB_IMAGE,"Sfondo",100,NORMAL_MODE)
    pdb.gimp_image_add_layer(sfondo,livello_sfondo,0)
    pdb.gimp_context_set_background((255,255,255))
    pdb.gimp_drawable_fill(livello_sfondo, BACKGROUND_FILL)
    livello_1=pdb.gimp_image_get_active_layer(immagine_n_1)
    livello_2=pdb.gimp_image_get_active_layer(immagine_n_2)
    livello_sopra=pdb.gimp_layer_new_from_drawable(livello_1, sfondo)
    livello_sotto=pdb.gimp_layer_new_from_drawable(livello_2, sfondo)
    pdb.gimp_image_add_layer(sfondo,livello_sopra,-1)
    pdb.gimp_image_add_layer(sfondo,livello_sotto,-1)
    #pdb.gimp_layer_set_offsets(livello_sopra,600,0)
    #pdb.gimp_layer_set_offsets(livello_sotto,600,1200)
    x_1 = (2400-larghezza_max_1) / 2
    x_2 = (2400-larghezza_max_2) / 2
    y_1 = (1200-altezza_1) / 2
    y_2 = 1200 + (1200-altezza_2) / 2
    pdb.gimp_layer_set_offsets(livello_sopra,x_1,y_1) #25O DA SINISTRA  
    pdb.gimp_layer_set_offsets(livello_sotto,x_2,y_2) #250 DA SINISTRA E 1200 AL CENTRO ENTRAMBE LE OPZIONI SONO STATE USATE CON FOTO LARGHEZZA 1900
    unita=pdb.gimp_image_merge_visible_layers(sfondo,CLIP_TO_IMAGE)
    pdb.file_png_save_defaults(sfondo, unita, percorso_file, percorso_file)
    lista_file.append(percorso_file)
    lista_file.append(percorso_secondo_file)
    lista_file.append(percorso_terzo_file)
    pdb.gimp_image_delete(immagine_n_1)
    pdb.gimp_image_delete(immagine_n_2)
  except Exception:
   continue   
 salva_foto(lista_file) 
register(
    "python-fu-batch-sdoppia-foto",
    "Duplica e specchia foto",
    "Duplica e specchia foto verticalmente",
    "Khere",
    "Khere",
    "2026",
    "Duplica foto",
    "",
    [],
    [],
    foto_specchiata
)
main()

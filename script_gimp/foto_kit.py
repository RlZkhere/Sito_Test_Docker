#!/opt/python2/bin/python2.7
# -*- coding: utf-8 -*-
from gimpfu import *
import os
import zipfile
lista_file=[]
def salva_foto(percorso):
 file_zip=[]
 percorso_zip = percorso + "foto_nuove.zip"
 for y in os.listdir(percorso):
  if y != "foto_nuove.zip":
   file_zip.append(y)
 with zipfile.ZipFile(percorso_zip, "w", zipfile.ZIP_DEFLATED) as zfile:
  for x in file_zip:   
   zfile.write(percorso + x, arcname=os.path.basename(x))
def setta_posizioni(x,y,z):
 pdb.gimp_image_add_layer(x,y,-1)
 pdb.gimp_image_add_layer(x,z,-1)
 pdb.gimp_layer_set_offsets(y,600,0)
 pdb.gimp_layer_set_offsets(z,600,1200)   
def apri_foto(lista_immagini):
 immagini=[]
 for x in lista_immagini:
  immagine = pdb.gimp_file_load(x, x)
  immagini.append(immagine)
 return immagini 
def crea_foto_finale():
 x=pdb.gimp_image_new(2400,2400,RGB)
 sfondo=pdb.gimp_layer_new(x,2400,2400,RGB_IMAGE,'Sfondo',100,NORMAL_MODE)
 pdb.gimp_image_insert_layer(x,sfondo,None,0)
 pdb.gimp_context_set_foreground((255,255,255))
 pdb.gimp_drawable_fill(sfondo,BACKGROUND_FILL)
 return x
def due_foto(lista_immagini):
 immagini=apri_foto(lista_immagini)
 immagine_1=immagini[0]
 immagine_2=immagini[1]
 percorso_foto_finale=lista_immagini[0]
 livello_1=pdb.gimp_image_get_active_layer(immagine_1)
 livello_2=pdb.gimp_image_get_active_layer(immagine_2)
 foto_finale=crea_foto_finale()
 livello_sopra=pdb.gimp_layer_new_from_drawable(livello_1,foto_finale)
 livello_sotto=pdb.gimp_layer_new_from_drawable(livello_2,foto_finale)
 setta_posizioni(foto_finale,livello_sopra,livello_sotto)
 pdb.gimp_image_delete(immagine_1)
 pdb.gimp_image_delete(immagine_2)
 os.rename(lista_immagini[1],lista_immagini[1].replace('_2.','_3.'))
 os.rename(lista_immagini[0],lista_immagini[0].replace('_1.','_2.'))
 livello_finale=pdb.gimp_image_merge_visible_layers(foto_finale, CLIP_TO_IMAGE)
 pdb.file_png_save_defaults(foto_finale,livello_finale,percorso_foto_finale,percorso_foto_finale)
 pdb.gimp_image_delete(foto_finale)
def unisci_foto():
 lista_foto=[]
 file_zip=[]
 percorso='/var/www/html/storage/MODIFICA-FOTO/'
 for file in os.listdir(percorso):
  if '_1.' in file or '_2.' in file:
   lista_foto.append(percorso+file)
 if len(lista_foto) == 2:
  due_foto(lista_foto)
  salva_foto(percorso)  
register(
"python-fu-unisci-foto-kit",
"Unisci foto",
"Unisci foto prodotti di un kit",
"Khere",
"Khere",
"2026-11-18",
"Unisci le foto kit",
"",
[],
[],
unisci_foto
)
main()

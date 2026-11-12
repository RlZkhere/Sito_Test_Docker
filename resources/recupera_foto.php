<?php
set_time_limit(3600);
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['tipo_modifica'])) {
$scelta_utente = $_POST['tipo_modifica'];
$percorso_foto = '../storage/MODIFICA-FOTO/';
$lista_file_elimina=glob('../storage/MODIFICA-FOTO/*');
foreach ($lista_file_elimina as $file){
if(is_file($file)) {
unlink($file);
}	
}
foreach ($_FILES['file_foto']['name'] as $indice => $file) {
if ($_FILES['file_foto']['error'][$indice] === UPLOAD_ERR_OK) {
$nome_file = basename($file);
$file_temporaneo = $_FILES['file_foto']['tmp_name'][$indice];
$destinazione = $percorso_foto . $nome_file;
}
else{
continue;
}
if (move_uploaded_file($file_temporaneo, $destinazione)) {
}
}
if ($scelta_utente === 'duplica_foto'){
$risultato=shell_exec("gimp -i --new-instance -b '(python-fu-batch-sdoppia-foto RUN-NONINTERACTIVE)' -b '(gimp-quit 0)'");
readfile('HTML/risultato_foto.html');
}
if ($scelta_utente === 'taglio_contenuto') {	
$risultato=shell_exec("gimp -i --new-instance -b '(python-fu-batch-taglia-soggetto RUN-NONINTERACTIVE)' -b '(gimp-quit 0)'");
readfile('HTML/risultato_foto.html');
}
if ($scelta_utente === 'ridimensiona'){
$risultato=shell_exec("gimp -i --new-instance -b '(python-fu-batch-scala-foto RUN-NONINTERACTIVE)' -b '(gimp-quit 0)'");
readfile('HTML/risultato_foto.html');	
}
}
?>

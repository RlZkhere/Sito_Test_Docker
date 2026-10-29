<?php
if (php_sapi_name() !== 'cli') {
die("Non consentito");	
}
$valore_selezionato = isset($argv[1]) ? $argv[1] : '';
$nome_file_zip='../storage/' . strtoupper($valore_selezionato) . "/" . $valore_selezionato . ".zip";
if (file_exists($nome_file_zip)) {
unlink($nome_file_zip);
}
$script_python = "../recuperi_dati/recupero_" . $valore_selezionato . ".py"; //lo script da lanciare si trova in ../recuperi_dati/recupero_$NOME_.py
$script_bash = "../recuperi_dati/controllo/andamento.sh"; //script che controlla l andamento dello script tramite ps dove filtra se ce python attivo
$percorso_python = escapeshellarg($script_python);
$percorso_bash = escapeshellarg($script_bash);
$comando = "python3 $percorso_python >/dev/null 2>&1 && bash $percorso_bash 2>&1"; 
$stato_uscita=0;
$output_python=[];
exec($comando,$output_python,$stato_uscita); //esegue entrambi i comandi e si salva solo il risultato del controllo
if ($stato_uscita === 0){ //se il controllo va a buon fine prende tutti i file presenti nella cartella ../storage/upper($NOME) e li salva nella stessa cartella con $nome.zip
$cartella_comprimi='../storage/' . strtoupper($valore_selezionato) . "/";
$percorso_cartella=realpath($cartella_comprimi);
if ($percorso_cartella && is_dir($percorso_cartella)){
$zip=new ZipArchive();
if ($zip->open($nome_file_zip, ZipArchive::CREATE | ZipArchive::OVERWRITE) === TRUE) {
$lista_file = new RecursiveIteratorIterator(
new RecursiveDirectoryIterator($percorso_cartella, RecursiveDirectoryIterator::SKIP_DOTS),
RecursiveIteratorIterator::LEAVES_ONLY
);
foreach ($lista_file as $name => $file) {
if (!$file->isDir()) {
$filePath = $file->getRealPath();
if ($filePath === realpath($nome_file_zip)) { //ignora il file zip gia presente
continue;
}
$relativePath = substr($filePath, strlen($percorso_cartella) + 1);
$zip->addFile($filePath, $relativePath); //aggiunge il file al file zip
}
}
$zip->close();
$file_da_eliminare = ['dati.csv', 'foto.csv', 'video.csv', 'log.csv','listasku.csv','mancanti.csv','prestazioni.csv','compatibilita.csv','FOTO']; //elimina tutti i file presenti
foreach ($file_da_eliminare as $file_nome) {
$percorso_file = $percorso_cartella . '/' . $file_nome;
if (is_file($percorso_file)) {
unlink($percorso_file);
} elseif (is_dir($percorso_file)) {
array_map('unlink', glob($percorso_file . '/*'));
rmdir($percorso_file);
}
}
}
}
}
?>

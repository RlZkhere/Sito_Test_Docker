<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST'){
if (!empty($_POST['nome_script'])) {
$valore_selezionato=$_POST['nome_script'] ; //Prende il valore dall index
}
if (!empty($_POST['nome_script_no_sku'])){
$valore_selezionato=$_POST['nome_script_no_sku'] ;
}
$worker_script = __DIR__ . '/esegui_recupero.php'; //setta il file php da eseguire in sottofondo
$comando = "nohup php " . escapeshellarg($worker_script) . " " . escapeshellarg($valore_selezionato) . " > /dev/null 2>&1 &";
$file_csv = __DIR__ . '/../storage/' . strtoupper($valore_selezionato) . '/listasku.csv';	
if (!empty($_POST['nome_script'])) {
$lista_codici = isset($_POST['lista_codici']) ? $_POST['lista_codici'] : ''; //prede la lista dei codici che si aprono col popup javascript
$righe = explode("\n", str_replace("\r", "", $lista_codici)); //divide il file per ogni a capo che trova
$righe_pulite = array_filter(array_map('trim', $righe));
$fp=fopen($file_csv,'w'); //apre il file e cicla sulla lista creata dei codici inseriti
if ($fp){
foreach ($righe_pulite as $sku){
fputcsv($fp, [$sku]);
}
fclose($fp);
}
}
exec($comando); //esegue script recupero e script che controlla l andamento
echo "<h2>Avviato recupero, verra salvato in un file zip</h2>";
$nome_cartella_upper = strtoupper($valore_selezionato);
$url_zip = '../storage/' . strtoupper($valore_selezionato) . '/' . $valore_selezionato . '.zip'; //il file zip che conterra l output si trova in $padre/storage/upper($selezionato)/$selezionato.php
echo '<p><a href="' . htmlspecialchars($url_zip) . '" download="' . htmlspecialchars($valore_selezionato) . '">Scarica file di output</a></p>'; //crea il link che si potra scaricare quando finisce
echo '<p><a href="../">Torna al menu</p></a>';
}
else{
echo "<h2>ERRORE durante avvio recupero</h2>" ;
}
?>

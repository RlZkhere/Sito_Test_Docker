<?php
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$link_stampa = [];
$query='';
$lista_link = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['tipo_controllo']) && !empty($_POST['piattaforma'])){
$scelta_controllo=$_POST['tipo_controllo'] ;
$scelta_piattaforma=$_POST['piattaforma'];
require_once '../../db_pwd';
$connessione = pg_connect("host=$host port=$porta dbname=$db user=$user password=$password"); //SI CONNETTE
if (!$connessione){
echo '<h2>ERRORE CONNESSIONE AD ODOO8</h2>';
exit;	
}
if ($scelta_piattaforma === 'listini'){
require __DIR__ . '/controllo_listini.php';
}
if ($scelta_piattaforma === 'vendite'){	
require __DIR__ . '/controllo_vendite.php';
}
if ($scelta_piattaforma === 'no_vendite'){
require __DIR__ . '/controllo_no_vendite.php';
}
if ($scelta_piattaforma === 'magento'){
require __DIR__ . '/controllo_magento.php';
}
if ($scelta_piattaforma === 'ebay'){
require __DIR__ . '/controllo_ebay.php';
}
foreach(($lista_query ?? []) as $nome_query => $query){ //TUTTO QUESTO BLOCCO VALE PER LE QUERY MAGENTO/EBAY DATO CHE SONO MULTIPLE
$risultato=pg_query($connessione,$query);
if (!$risultato){		
echo "Errore query ".$nome_query.": ".pg_last_error($connessione)."<br>";
continue;
}
if (isset($nomi_file[$nome_query])){ //CONTROLLA SE IN nomi_file ESISTE UN VALORE CHIAMATO COME IL VALORE DELLA FUNZIONE
$nome_file=$nomi_file[$nome_query];
$file=fopen('../../storage/MARKETPLACE/' . strtoupper($scelta_piattaforma) . '/' . $nome_file,'w');
$n_colonne=pg_num_fields($risultato);
while($riga=pg_fetch_assoc($risultato)){ //FINO A QUANDO NON FINISCE L OUTPUT DELLA QUERY SCRIVE NEL FILE
fputcsv($file,$riga,';');
}
fclose($file);
$file_scarica='../../storage/MARKETPLACE/' . strtoupper($scelta_piattaforma) . '/' . $nome_file;
$lista_link[] = $file_scarica;	
}
else{
while($riga=pg_fetch_row($risultato)){
$link_stampa[] = $nome_query.": ".implode(" ; ",$riga)."<br>";
}	
}
}
foreach ($lista_link as $link){
$link_stampa [] = '<a href="' . $link . '">' . basename($link) . '</a><br>';
}
pg_close($connessione);
$_SESSION['link_stampa'] = $link_stampa;
header('Location: output_analisi.php');
exit;
}
?>

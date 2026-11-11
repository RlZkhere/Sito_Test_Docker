<?php
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$link_stampa = [];
$query='';
$lista_link = [];
require_once '../../db_pwd';
if ($_SERVER['REQUEST_METHOD'] === 'POST'){
$connessione = pg_connect("host=$host port=$porta dbname=$db user=$user password=$password"); //SI CONNETTE
if (!$connessione){
echo '<h2>ERRORE CONNESSIONE AD ODOO8</h2>';
exit;	
}
if (!empty($_POST['tipo_controllo']) && !empty($_POST['piattaforma'])){
$pagina_home='/resources/analisi_ecommerce.html';
$scelta_controllo=$_POST['tipo_controllo'] ;
$scelta_piattaforma=$_POST['piattaforma'];
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
}
if (!empty($_POST['controllo_db'])){
$pagina_home='/resources/controlli_tecnici.html';
$scelta_controllo=$_POST['controllo_db'] ;
if ($scelta_controllo === 'inc_des'){ //Descrizione in IR translation diversa da quella in product_translations
require __DIR__ . '/CONTROLLI-DB/' . 'controllo_descrizioni_ir.php';
}
if ($scelta_controllo === 'prod_no_comp'){ //Prodotto online su Magento con titolo corto ma senza compatibilita
require __DIR__ . '/CONTROLLI-DB/' . 'controllo_prodotti_nocmp.php';
}
pg_close($connessione);
}
$_SESSION['link_stampa'] = $link_stampa;
$_SESSION['pagina_home'] = $pagina_home;
header('Location: output_analisi.php');
exit;
}
?>

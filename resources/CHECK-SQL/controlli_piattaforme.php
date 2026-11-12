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
$pagina_home='/resources/HTML/analisi_ecommerce.html';
$scelta_controllo=$_POST['tipo_controllo'] ;
$scelta_piattaforma=$_POST['piattaforma'];
$controlli = [
'listini'    => 'controllo_listini.php',
'vendite'    => 'controllo_vendite.php',
'no_vendite' => 'controllo_no_vendite.php',
'magento'    => 'controllo_magento.php',
'ebay'       => 'controllo_ebay.php'
];
if (isset($controlli[$scelta_piattaforma])) {
require __DIR__ . '/' . $controlli[$scelta_piattaforma];
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
//IL BLOCCO DELLE QUERY MULTIPLE TERMINA QUI
}
elseif (!empty($_POST['controllo_db'])){
$pagina_home='/resources/HTML/controlli_tecnici.html';
$scelta_controllo=$_POST['controllo_db'] ;
$controlli_db = [
'inc_des'      => 'controllo_descrizioni_ir.php',
'prod_no_comp' => 'controllo_prodotti_nocmp.php'
];
if (isset($controlli_db[$scelta_controllo])){
require __DIR__ . '/CONTROLLI-DB/' .
$controlli_db[$scelta_controllo];	
}
}
pg_close($connessione);
$_SESSION['link_stampa'] = $link_stampa;
$_SESSION['pagina_home'] = $pagina_home;
header('Location: output_analisi.php');
exit;
}
?>

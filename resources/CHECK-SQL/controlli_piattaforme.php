<?php
session_start();
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
if ($scelta_controllo === 'generale'){	
if ($scelta_piattaforma === 'magento'){ //POPOLA L ARRAY CON QUERY MAGENTO
//Prende lista prodotti con pubblica non su magento	
$n_pub_nomag='select count(distinct(id)) from product_template pt where mmac_ebay_pubblica = true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_stock <> 0';
$sku_pub_nomag='select distinct("name") from product_template pt where mmac_ebay_pubblica = true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_stock <> 0';
$brand_pub_nomag='select mmac_partner,count(id) from product_template pt where mmac_ebay_pubblica = true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_stock <> 0 group by pt.mmac_partner order by count(id) desc';
$lista_query=array(
'Prodotti con pubblica non su magento' => $n_pub_nomag,
'sku_pub_nomag' => $sku_pub_nomag,
'brand_pub_nomag' => $brand_pub_nomag
);
}
elseif ($scelta_piattaforma === 'ebay'){ //POPOLA L ARRAY CON QUERY EBAY
//Prende lista prodotti con pubblica non su ebay
$n_pub_noebay='select count(id) from product_template pt where mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id where ebay_site_id = 1) and id not in (select child_id from mmac_grouped_product_rel)';
$sku_pub_noebay='select "name" from product_template pt where mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id where ebay_site_id = 1) and id not in (select child_id from mmac_grouped_product_rel)';
$brand_pub_noebay='select mmac_partner,count(pt.id) from product_template pt where mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id where ebay_site_id = 1) and id not in (select child_id from mmac_grouped_product_rel) group by mmac_partner order by count(pt.id) desc';
$lista_query=array(
'Prodotti con pubblica non su ebay' => $n_pub_noebay,
'sku_pub_noebay' => $sku_pub_noebay,
'brand_pub_noebay' => $brand_pub_noebay
);
}
$nomi_file=array( //DEFINISCE IL FILE CSV ASSOCIATO ALLA QUERY
'sku_pub_nomag' => 'sku_pubblica_no_magento.csv',
'brand_pub_nomag' => 'brand_pubblica_no_magento.csv',
'sku_pub_noebay' => 'sku_pubblica_no_ebay.csv',
'brand_pub_noebay' => 'brand_pubblica_no_ebay.csv'
);
foreach($lista_query as $nome_query => $query){
$risultato=pg_query($connessione,$query);
if (!$risultato){		
echo "Errore query ".$nome_query.": ".pg_last_error($connessione)."<br>";
continue;
}
if (isset($nomi_file[$nome_query])){ //CONTROLLA SE IN nomi_file ESISTE UN VALORE CHIAMATO COME IL VALORE DELLA FUNZIONE
$nome_file=$nomi_file[$nome_query];
$file=fopen('../storage/MARKETPLACE/' . strtoupper($scelta_piattaforma) . '/' . $nome_file,'w');
$n_colonne=pg_num_fields($risultato);
while($riga=pg_fetch_assoc($risultato)){ //FINO A QUANDO NON FINISCE L OUTPUT DELLA QUERY SCRIVE NEL FILE
fputcsv($file,$riga,';');
}
fclose($file);
$file_scarica='../storage/MARKETPLACE/' . strtoupper($scelta_piattaforma) . '/' . $nome_file;
$lista_link[] = $file_scarica;	
}
else{
while($riga=pg_fetch_row($risultato)){
echo $nome_query.": ".implode(" ; ",$riga)."<br>";
}	
}
}
}
if ($scelta_controllo === 'brand' && !empty($_POST['lista_dati'])){
$lista_brand=$_POST['lista_dati'];
$brand_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_brand));
$brand_scelti="'" . trim($brand_scelti) . "'";
if ($scelta_piattaforma === 'magento'){	
$query='select "name",mmac_brand from product_template where mmac_ebay_pubblica is true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_brand in (' . $brand_scelti . ')';	
}
else{
$query='select "name",mmac_brand from product_template pt where mmac_brand in (' . $brand_scelti . ') and mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id)';
}
}
if ($scelta_controllo === 'sku' && !empty($_POST['lista_dati'])){
$lista_sku=$_POST['lista_dati'];	
$sku_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_sku));
$sku_scelti="'" . trim($sku_scelti) . "'";
if ($scelta_piattaforma == 'magento'){
$query='select "name" from product_template pt where mmac_ebay_pubblica is true and "name" in (' . $sku_scelti . ') and id not in (select product_id from mmac_magento2020_inventory mmi)';
}
else{
$query='select "name" from product_template where "name" in (' . $sku_scelti . ') and mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id)';
}
}
if ($scelta_controllo !== 'generale' && $scelta_piattaforma !== 'listini' && $scelta_piattaforma != 'vendite' && $scelta_piattaforma != 'no_vendite'){ 
$risultato=pg_query($connessione,$query);
if (!$risultato){
echo '<h2>ERRORE</h2>';
echo pg_last_error($connessione);
pg_close($connessione);
}
$file=fopen('../storage/MARKETPLACE/' . strtoupper($scelta_piattaforma) . '/no_pubblica_' . $scelta_controllo . '.csv','w');
while($riga=pg_fetch_assoc($risultato)){ //FINO A QUANDO NON FINISCE L OUTPUT DELLA QUERY SCRIVE NEL FILE
fputcsv($file,$riga,';');
}
fclose($file);
$link_stampa [] = '<a href="../storage/MARKETPLACE/' . strtoupper($scelta_piattaforma) . '/no_pubblica_' . $scelta_controllo . '.csv' . '">' . 'no_pubblica_' . $scelta_controllo . '</a>';
}
foreach ($lista_link as $link){
$link_stampa [] = '<a href="' . $link . '">' . basename($link) . '</a><br>';
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
pg_close($connessione);
$_SESSION['link_stampa'] = $link_stampa;
header('Location: output_analisi.php');
exit;
}
?>

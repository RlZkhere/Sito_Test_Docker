<?php
$lista_modelli=$_POST['lista_modelli'];
$lista_modelli=str_replace(" ","",$lista_modelli);
$lista_modelli=trim($lista_modelli);
$n_file='cmp_online_obsolete.csv';
$query="select \"name\" from mmac_brx_ebay_inventorycmp mbei where exists (select 1 from mmac_cmp_prodotti mcp where mcp.id = mbei.product_cmp_id and obsoleta is true and mcp.model_id in (" . $lista_modelli . "))";
$risultato=pg_query($connessione,$query);
if (!$risultato){
echo "<h2>ERRORE QUERY</h2>";
return ;
}
$file=fopen('../../storage/REPORT/ODOO/' . $n_file,'w');
while ($riga = pg_fetch_row($risultato)) {
$csv = implode(';', $riga);
fwrite($file, $csv . "\n");
}
fclose($file);
$link_stampa [] ='<a href="../../storage/REPORT/ODOO/' . $n_file . '">COMPATIBILITA OBSOLETE ONLINE</a>';
?>

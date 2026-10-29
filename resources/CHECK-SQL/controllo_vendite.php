<?php
$query='';
$n_file='';
if ($scelta_controllo === 'brand'){
$numero_articoli=$_POST['numero_sku'];
$lista_brand=$_POST['lista_dati'];
$brand_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_brand));
$brand_scelti="'" . trim($brand_scelti) . "'";	
$n_file='bestseller_brand.csv';	
$query="with prodotti_aggregati as 
( select pt.\"name\" as nome_prodotto, pt.mmac_brand as marchio, count(distinct so.id) as totale_ordini, max(so.date_order) as data_ultimo_ordine, ROW_NUMBER() 
over ( partition by pt.mmac_brand order by count(distinct so.id) desc, pt.\"name\" asc ) as posizione from sale_order so 
inner join sale_order_line sol ON sol.order_id = so.id inner join product_product pp on pp.id = sol.product_id inner join product_template pt on pt.id = pp.product_tmpl_id 
where pt.mmac_brand in (" . $brand_scelti . ") group by pt.mmac_brand, pt.\"name\" 
having count(distinct so.id) > 1 ) 
select nome_prodotto, marchio, totale_ordini, data_ultimo_ordine from prodotti_aggregati where posizione <= " . $numero_articoli . " order by marchio asc, totale_ordini desc";
$prima_riga='SKU;MARCHIO;N_ORDINI,ULTIMO_ORDINE';
}
if ($scelta_controllo === 'sku'){
$lista_sku=$_POST['lista_dati'];
$sku_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_sku));
$sku_scelti="'" . trim($sku_scelti) . "'";	
$n_file='vendite.csv';	
$query="select pt.\"name\",so.date_order from sale_order so inner join sale_order_line sol on sol.order_id = so.id inner join product_product pp on pp.id = sol.product_id inner join
product_template pt on pt.id = pp.product_tmpl_id where pt.\"name\" in (" . $sku_scelti .") order by pt.\"name\", so.date_order desc";
$prima_riga='SKU;DATA_ORDINE';
}
$risultato=pg_query($connessione,$query);
if (!$risultato){
echo "<h2>ERRORE QUERY</h2>";
return ;
}
$file=fopen('../../storage/REPORT/VENDITE/' . $n_file,'w');
fwrite($file, $prima_riga . "\n");
while ($riga = pg_fetch_row($risultato)) {
$csv = implode(';', $riga);
fwrite($file, $csv . "\n");
}
fclose($file);
$link_stampa [] ='<a href="../../storage/REPORT/VENDITE/' . $n_file . '">' . strtoupper($scelta_controllo) . '</a>';
?>

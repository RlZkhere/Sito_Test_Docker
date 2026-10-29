<?php
$lista_brand=$_POST['lista_dati'];
$brand_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_brand));
$brand_scelti="'" . trim($brand_scelti) . "'";
$n_file='sku_no_vendite.csv';
$query="select pt.\"name\",replace(cast(mlv.price as varchar),'.',','),replace(cast(pt.mmac_listino as varchar),'.',','),replace(cast(pt.mmac_costo as varchar),'.',',') 
from product_template pt inner join mmac_listino_view mlv on mlv.product_id = pt.id 
where pt.\"name\" not like '%#%' and mlv.listini_id = 1 and pt.mmac_ebay_pubblica is true 
and pt.id not in (select product_tmpl_id from product_product where id in (select product_id from sale_order_line 
where order_id in (select id from sale_order so where so.create_date > CURRENT_DATE - INTERVAL '60 days')))
and pt.mmac_brand in (" . $brand_scelti . ")
union
select pt.\"name\",replace(cast(mlv.price as varchar),'.',','),replace(cast(pt.mmac_listino as varchar),'.',','),replace(cast(pt.mmac_costo as varchar),'.',',')
from product_template pt inner join mmac_listino_view mlv on mlv.product_id = pt.id
where pt.\"name\" like '%#%' and pt.mmac_ebay_pubblica is true and pt.\"name\" not in (
select distinct(sku_kit) from sale_order_line sol where sku_kit is not null and order_id in (select id from sale_order where date_order >= '2026-08-20')
)
and mmac_brand in (" . $brand_scelti . ")";
$prima_riga='SKU;PREZZO;LISTINO;COSTO';
$risultato=pg_query($connessione,$query);
echo 'Colonne restituite dalla query: ' . pg_num_fields($risultato);
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
$link_stampa [] ='<a href="../../storage/REPORT/VENDITE/' . $n_file . '">SKU NO VENDITE</a>';
?>

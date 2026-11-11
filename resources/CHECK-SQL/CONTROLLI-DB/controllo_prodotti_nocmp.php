<?php
$n_file='prodotti_online_nocmp.csv';
$query="
select distinct(pt.\"name\") from mmac_brx_ebay_shorttitles mbes join product_template pt on pt.id = mbes.product_id 
where not exists(
select 1
from mmac_cmp_prodotti mcp 
where mcp.product_id = pt.id
and mcp.obsoleta is not true 
)
and exists(
select 1
from mmac_magento2020_inventory mmi 
where mmi.product_id = pt.id
)
and exists(
select 1
from mmac_pim_product_translations mppt 
where mppt.product_id = pt.id
and type_id = 11 and lang_id = 1
)
";
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
$link_stampa [] ='<a href="../../storage/REPORT/ODOO/' . $n_file . '">PRODOTTI ONLINE SENZA COMPATIBILITA</a>';
?>

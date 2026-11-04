<?php
$query="
select pt.\"name\"
from product_template pt
where pt.mmac_ebay_pubblica is true
and exists (
select 1
from mmac_pim_product_translations mppt
where mppt.product_id = pt.id
and mppt.type_id = 2
and mppt.lang_id = 1
and mppt.value like '%<p>%'
and mppt.value not like '%div'
and mppt.updated_at <> mppt.created_at 
and exists (
select 1
from ir_translation it
where it.res_id = pt.id
and it.name = 'product.template,mmac_ebay_descrizione'
and it.lang = 'it_IT'
and it.value <> ''
and similarity(
regexp_replace(replace(it.value, ' ', ''), E'[\n\r]+', '', 'g'),
regexp_replace(replace(mppt.value, ' ', ''), E'[\n\r]+', '', 'g')
) < 0.70
)
);
";
$n_file='incongruenze_descrizioni.csv';
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
$link_stampa [] ='<a href="../../storage/REPORT/ODOO/' . $n_file . '">DESCRIZIONI INCONGRUENTI NUOVE</a>';
?>

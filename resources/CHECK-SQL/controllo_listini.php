<?php
$query='';
if ($scelta_controllo === 'outlet'){
//CONTROLLA SE IL PADRE HA IL VECCHIO PREZZO OUTLET DEL FIGLIO SU EBAY 
$n_file='outlet_disallineato.csv';	
$query="
WITH ultimo_listino_assoluto AS (
SELECT DISTINCT ON (product_id)
product_id,
listini_id,
\"name\" AS nome_listino,
price AS prezzo_attuale
FROM mmac_listino
ORDER BY product_id, create_date DESC
),
ultimo_listino_outlet AS (
SELECT DISTINCT ON (product_id)
product_id,
price AS prezzo_outlet
FROM mmac_listino
WHERE listini_id = 1
AND \"name\" LIKE 'LISTINO_OUTLET%'
ORDER BY product_id, create_date DESC
)
SELECT
figli.\"name\",
padri.\"name\",
ula.prezzo_attuale AS prezzo_corretto,
mbei.price AS prezzo_su_ebay,
mbei.\"name\" AS numero_interazioni
FROM mmac_grouped_product_rel mgpr
inner join product_template padri on padri.id = mgpr.parent_id
inner join product_template figli on figli.id = mgpr.child_id
INNER JOIN ultimo_listino_assoluto ula
ON ula.product_id = mgpr.child_id
INNER JOIN ultimo_listino_outlet ulo
ON ulo.product_id = mgpr.child_id
INNER JOIN mmac_brx_ebay_inventory mbei
ON mbei.product_id = mgpr.parent_id
WHERE mbei.ebay_site_id = 1
AND ula.nome_listino NOT LIKE 'LISTINO_OUTLET%'
AND mbei.price = ulo.prezzo_outlet
";
$prima_riga='SKU;FIGLIO;PADRE,PREZZO_CORRETTO;PREZZO_SU_EBAY';
}
if ($scelta_controllo === 'ricarico') //CONTROLLA IL RICARICO DEI PRODOTTI SE E SOTTO IL 30
{
$n_file='ricarico_sotto_30.csv';
$query="
with ultimo_listino as (
select distinct on (product_id)
product_id,
listini_id,
\"name\" as nome_listino,
price
from mmac_listino
order by product_id, create_date desc
)
select
\"name\" as sku,
replace(cast(ul.price as varchar), '.', ',') as prezzo,
replace(cast(mmac_costo as varchar), '.', ',') as costo,
replace(cast((round(((mmac_costo * 1.22) * 1.3)::numeric, 2)) as varchar),'.',',') as prezzo_ricarico_30,
replace(cast((round((((ul.price / (mmac_costo * 1.22)) - 1) * 100)::numeric,2)) as varchar),'.',',') as ricarico_attuale
from product_template pt
inner join ultimo_listino ul
on ul.product_id = pt.id
where listini_id = 1
and mmac_costo <> 0
and price < (mmac_costo * 1.22) * 1.3
";
$prima_riga='SKU;PREZZO;COSTO;PREZZO_CON_RICARICO_30;RICARICO_ATTUALE';
}
$risultato=pg_query($connessione,$query);
if (!$risultato){
echo "<h2>ERRORE QUERY</h2>";
return ;
}
$file=fopen('../../storage/REPORT/LISTINI/' . $n_file,'w');
fwrite($file, $prima_riga . "\n");
while ($riga = pg_fetch_row($risultato)) {
$csv = implode(';', $riga);
fwrite($file, $csv . "\n");
}
fclose($file);
$link_stampa [] ='<a href="../../storage/REPORT/LISTINI/' . $n_file . '">' . strtoupper($scelta_controllo) . '</a>'; 
?>

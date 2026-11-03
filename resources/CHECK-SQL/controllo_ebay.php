<?php
if ($scelta_controllo === 'generale'){
$n_pub_noebay='select count(id) from product_template pt where mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id where ebay_site_id = 1) and id not in (select child_id from mmac_grouped_product_rel)';
$sku_pub_noebay='select "name" from product_template pt where mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id where ebay_site_id = 1) and id not in (select child_id from mmac_grouped_product_rel)';
$brand_pub_noebay='select mmac_partner,count(pt.id) from product_template pt where mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id where ebay_site_id = 1) and id not in (select child_id from mmac_grouped_product_rel) group by mmac_partner order by count(pt.id) desc';
$lista_query=array(
'Prodotti con pubblica non su ebay' => $n_pub_noebay,
'sku_pub_noebay' => $sku_pub_noebay,
'brand_pub_noebay' => $brand_pub_noebay
);
}
$nomi_file=array(
'sku_pub_noebay' => 'sku_pubblica_no_ebay.csv',
'brand_pub_noebay' => 'brand_pubblica_no_ebay.csv'
);
if ($scelta_controllo === 'brand' && !empty($_POST['lista_dati'])){
$lista_brand=$_POST['lista_dati'];
$brand_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_brand));
$brand_scelti="'" . trim($brand_scelti) . "'";
$query='select "name",mmac_brand from product_template pt where mmac_brand in (' . $brand_scelti . ') and mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id)';
$lista_query=array(
'brand_pub_noebay' => $query
);
}
if ($scelta_controllo === 'sku' && !empty($_POST['lista_dati'])){
$lista_sku=$_POST['lista_dati'];
$sku_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_sku));
$sku_scelti="'" . trim($sku_scelti) . "'";
$query='select "name" from product_template where "name" in (' . $sku_scelti . ') and mmac_ebay_pubblica is true and mmac_stock <> 0 and id not in (select distinct(pt.id) from mmac_brx_ebay_inventory mbei inner join product_template pt on pt.id = mbei.product_id)';
$lista_query=array(
'sku_pub_noebay' => $query
);
}
?>

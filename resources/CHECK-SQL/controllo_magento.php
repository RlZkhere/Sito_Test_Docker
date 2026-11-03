<?php
if ($scelta_controllo === 'generale'){
$n_pub_nomag='select count(distinct(id)) from product_template pt where mmac_ebay_pubblica = true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_stock <> 0';
$sku_pub_nomag='select distinct("name") from product_template pt where mmac_ebay_pubblica = true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_stock <> 0';
$brand_pub_nomag='select mmac_partner,count(id) from product_template pt where mmac_ebay_pubblica = true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_stock <> 0 group by pt.mmac_partner order by count(id) desc';
$lista_query=array(
'Prodotti con pubblica non su magento' => $n_pub_nomag,
'sku_pub_nomag' => $sku_pub_nomag,
'brand_pub_nomag' => $brand_pub_nomag
);
}
$nomi_file=array(
'sku_pub_nomag' => 'sku_pubblica_no_magento.csv',
'brand_pub_nomag' => 'brand_pubblica_no_magento.csv'
);
if ($scelta_controllo === 'brand' && !empty($_POST['lista_dati'])){
$lista_brand=$_POST['lista_dati'];
$brand_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_brand));
$brand_scelti="'" . trim($brand_scelti) . "'";
$query='select "name",mmac_brand from product_template where mmac_ebay_pubblica is true and id not in (select product_id from mmac_magento2020_inventory mmi) and mmac_brand in (' . $brand_scelti . ')';
$lista_query=array(
'brand_pub_nomag' => $query 
);
}
if ($scelta_controllo === 'sku' && !empty($_POST['lista_dati'])){
$lista_sku=$_POST['lista_dati'];
$sku_scelti=preg_replace('/\s*\n\s*/', "','", trim($lista_sku));
$sku_scelti="'" . trim($sku_scelti) . "'";
$query='select "name" from product_template pt where mmac_ebay_pubblica is true and "name" in (' . $sku_scelti . ') and id not in (select product_id from mmac_magento2020_inventory mmi)';
$lista_query=array(
'sku_pub_nomag' => $query
);
}
?>

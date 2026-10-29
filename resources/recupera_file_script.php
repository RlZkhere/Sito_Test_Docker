<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['nome_file'])) {
$valore_selezionato=$_POST['nome_file'];
$percorso_file='../storage/' . strtoupper($valore_selezionato) . '/' . $valore_selezionato . '.zip';
if (file_exists($percorso_file)){
echo '<p><a href="' . htmlspecialchars($percorso_file) . '" download="' . htmlspecialchars($valore_selezionato) . '">Scarica file</a></p>';
}
else{
$cartella_file='../storage/' . strtoupper($valore_selezionato) . '/';
$files=glob($cartella_file . '/*.csv');
$files=array_filter($files,function($file){
return is_file($file) && basename($file)!=='listasku.csv';
});
usort($files,function($a,$b){
return filemtime($b)<=>filemtime($a);
});
if(empty($files)){
die('Nessun file di recupero creato');
}
$filePiuRecente=$files[0];
$fp=fopen($filePiuRecente,'r');
$ultimaRiga='';
if($fp){
fseek($fp,0,SEEK_END);
$pos=ftell($fp)-1;
while($pos>=0){
fseek($fp,$pos);
$char=fgetc($fp);
if($char==="\n" && $ultimaRiga!==''){
break;
}
if($char!=="\n" && $char!=="\r"){
$ultimaRiga=$char.$ultimaRiga;
}
$pos--;
}
fclose($fp);
}
$campi=explode(';',$ultimaRiga);
$sku=trim($campi[0]);
$fileListaSku=$cartella_file . 'listasku.csv';
$trovato=false;
$skuTrovato='';
$rigaTrovata=0;
$righeTotali=0;
if(file_exists($fileListaSku)){
$handle=fopen($fileListaSku,'r');
while(fgets($handle)!==false){
$righeTotali++;
}
fclose($handle);
$handle=fopen($fileListaSku,'r');
$numeroRiga=0;
while(($riga=fgets($handle))!==false){
$numeroRiga++;
$campiLista=explode(';',trim($riga));
$skuLista=trim($campiLista[0]);
if($skuLista===$sku){
$trovato=true;
$skuTrovato=$skuLista;
$rigaTrovata=$numeroRiga;
break;
}
}
fclose($handle);
if(!$trovato){
$skuSenzaPrefisso=substr($sku,3);
$handle=fopen($fileListaSku,'r');
$numeroRiga=0;
while(($riga=fgets($handle))!==false){
$numeroRiga++;
$campiLista=explode(';',trim($riga));
$skuLista=trim($campiLista[0]);
if($skuLista===$skuSenzaPrefisso){
$trovato=true;
$skuTrovato=$skuLista;
$rigaTrovata=$numeroRiga;
break;
}
}
fclose($handle);
}
if($trovato){
$righeMancanti=$righeTotali-$rigaTrovata;
$percentuale_avanzamento=round(($rigaTrovata/$righeTotali)*100);
echo '<p>Sku ancora da cercare: ' . $righeMancanti . '</p>';
echo '<p>Percentuale di avanzamento: ' . $percentuale_avanzamento . '</p>'; 
}
}
}
}
?>

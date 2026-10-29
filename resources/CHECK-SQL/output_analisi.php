<?php
session_start();
$link_stampa = $_SESSION['link_stampa'] ?? [];
?>
<!DOCTYPE html>
<html>
<?php
foreach ($link_stampa as $stampa){
echo $stampa . '<br>';
}
?>
</html>

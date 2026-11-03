<?php
session_start();
$link_stampa = $_SESSION['link_stampa'] ?? [];
?>
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Elenco Stampe</title>
<style>
:root {
--bg-color: #f4f6f9;
--card-bg: #ffffff;
--primary: #2563eb;
--primary-hover: #1d4ed8;
--text-main: #1f2937;
--text-muted: #6b7280;
--border-color: #e5e7eb;
}
* {
box-sizing: border-box;
margin: 0;
padding: 0;
}
body {
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
background-color: var(--bg-color);
color: var(--text-main);
min-height: 100vh;
display: flex;
justify-content: center;
align-items: center;
padding: 24px;
}
.container {
width: 100%;
max-width: 520px;
background: var(--card-bg);
border-radius: 12px;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
padding: 28px;
}
.header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 24px;
border-bottom: 1px solid var(--border-color);
padding-bottom: 16px;
}
.header h1 {
font-size: 1.25rem;
font-weight: 600;
}
.btn-home {
display: inline-flex;
align-items: center;
gap: 6px;
text-decoration: none;
background-color: var(--primary);
color: #ffffff;
padding: 8px 16px;
border-radius: 8px;
font-size: 0.875rem;
font-weight: 500;
transition: background-color 0.2s ease, transform 0.1s ease;
}
.btn-home:hover {
background-color: var(--primary-hover);
}
.btn-home:active {
transform: scale(0.98);
}
.list-container {
list-style: none;
display: flex;
flex-direction: column;
gap: 10px;
}
.list-item {
background-color: #f9fafb;
border: 1px solid var(--border-color);
border-radius: 8px;
padding: 12px 14px;
font-size: 0.95rem;
word-break: break-all;
color: var(--text-main);
transition: border-color 0.15s ease;
}
.list-item:hover {
border-color: #cbd5e1;
}
.empty-state {
text-align: center;
padding: 32px 16px;
color: var(--text-muted);
font-size: 0.95rem;
}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>Elenco Elementi</h1>
<a href="/resources/analisi_ecommerce.html" class="btn-home">
&larr; Torna indietro
</a>
</div>
<ul class="list-container">
<?php foreach ($link_stampa as $stampa): ?>
<li class="list-item"><?= $stampa ?></li>
<?php endforeach; ?>
</ul>
</div>
</body>
</html>

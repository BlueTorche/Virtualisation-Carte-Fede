

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<?php
require_once 'phpqrcode/qrlib.php';
QRcode::png('some othertext 1234');
?>
</body>
</html>

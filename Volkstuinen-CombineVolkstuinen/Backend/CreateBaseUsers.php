<?php
require_once __DIR__ . "/../Backend/Models/User.php";

//tijdelijke pagina voor het Toevogen van nieuwe Gebruikers
$users = new User();
$users->Name = "John Doe";
$users->Email = "johndoe@gmail.com";
$users->Password = "LostMan123";
$users->PhoneNumber = "580-104-3438";
$users->ZipCode = "2141DB";
$users->Address = "Nethernowstreet 72";
$users->Complex = "1";
$users->CreateUser();
//$users->Name = "Jeff Dober";
//$users->Email = "jeffdober@gmail.com";
//$users->Password = "Faker123";
//$users->PhoneNumber = "587-504-1438";
//$users->ZipCode = "6791BB";
//$users->Address = "westwaystreet 72";
//$users->CreateUser();
$users->Name = "Alphonse Drebber";
$users->Email = "alphonsedrebber@gmail.com";
$users->Password = "IronMan23";
$users->PhoneNumber = "587-504-1124";
$users->ZipCode = "1245XB";
$users->Address = "Woeismestreet 33";
$users->CreateUser();
$users->Name = "Shara Kelsie";
$users->Email = "sharakelsie@gmail.com";
$users->Password = "WeetNiet123!";
$users->PhoneNumber = "587-5 -1438";
$users->ZipCode = "9752ZX";
$users->Address = "DrNolenWeg 89";
$users->CreateUser();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volkstuin Vereniging Sittard</title>
</head>
<body>

</body>
</html>


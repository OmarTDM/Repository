<?php
require_once __DIR__ . "/../../Backend/SessionChecker.php";
require_once __DIR__."/../../Backend/Models/User.php";
checkSession($allowedUserTypes = [1,2,3]);
$user = new User();
$id = $_SESSION['user_id'];

$user->findByIdUser($id)
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volkstuin Vereniging Sittard</title>
    <link rel="stylesheet" href="CSS-Gedeeld/Gebruikerinfo.css">
    </head>
<body>


<div class="sidebar">
    <img src="../../Frontend/Gedeeld/pictures/logo-volkstuinverenigingsittard.png" alt="Logo">
    <div class="Icoontjes">

            <div class="icon1">
                <form id="BackButton" method="POST" action="../../Backend/RedirectUser.php">
                    <button id="BackButton">
                        <img src="../Gedeeld/pictures/HomeMenuButton.svg" alt="huisknop">
                    </button>
                </form>
            </div>
        <a href="../../Frontend/Gedeeld/GebruikerInfo.php">
            <div class="icon2">
                <img src="../Gedeeld/pictures/UserMenuButton.svg" alt="settings">
            </div>
        </a>
        <a href="../../Frontend/login.php">
            <div class="icon2">
                <img src="../Gedeeld/pictures/ExitMenuButton.svg" alt="Uitloggen">
            </div>
        </a>
    </div>

</div>


<div class="header">
    VOLKSTUIN VERENIGING SITTARD
</div>
<div class="">
<div class="">
    <div class="">
        <label>Voornaam</label>
        <input type="text" id="voornaam" placeholder="Voornaam">
        <label>Achternaam</label>
        <input type="text" id="achternaam" placeholder="Achternaam">
        <label>E-mailadres</label>
        <input type="email" id="email" placeholder="E-mailadres">
        <label>Telefoonnummer</label>
        <input type="tel" id="telefoon" placeholder="Telefoonnummer">
        <label>Woonadres</label>
        <input type="text" id="straat" placeholder="Straatnaam">
        <div class="row">
            <input type="text" id="postcode" placeholder="Postcode">
            <input type="text" id="huisnummer" placeholder="Huisnummer">
        </div>
    </div>
    <div class="">
        <label>Complex Naam</label>
        <input type="text" id="complex-naam" placeholder="Complex Naam">
        <label>m²</label>
        <input type="text" id="complex-size" placeholder="?m²">
        <label>Kosten</label>
        <input type="text" id="kosten" placeholder="Kosten">
    </div>
</div>
</div>

</body>
</html>
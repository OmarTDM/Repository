<?php
require_once __DIR__ . "/../../Backend/SessionChecker.php";
require_once __DIR__ . "/../../Backend/Models/User.php";
checkSession($allowedUserTypes = [3]);


$users = new User();
$usersResult = $users->findAllUsers();
        $counter = count($usersResult);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volkstuin Vereniging Sittard</title>
    <link rel="stylesheet" href="CSS-Bestuurder/dashboard.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="dashboard.js" defer></script>
</head>
<body>


<div class="sidebar">
    <img src="../../Frontend/Gedeeld/pictures/logo-volkstuinverenigingsittard-512x512-white%20(1).png" alt="Logo">
    <div class="Icoontjes">

        <a href="dashboard.php">
            <div class="icon1">
                <img src="../Gedeeld/pictures/HomeMenuButton.svg" alt="huisknop">
            </div>
        </a>
        <a href="../../Frontend/Gedeeld/GebruikerInfo.php">
            <div class="icon2">
                <img src="../Gedeeld/pictures/UserMenuButton.svg" alt="settings">
            </div>
        </a>
        <a href="../../Frontend/login.php">
            <div class="icon">
                <p>Uitloggen</p>
            </div>
        </a>
    </div>

</div>

<div class="header">
    VOLKSTUIN VERENING SITTARD
</div>
<div class="main-container">

    <p class="Dashtitle"> Welkom Beheerder</p>
    <div class="content">


        <!-- News Sectie (hier komen alle notificaties) -->
        <div class="news-sectie">
            <h2 class="newstitle">News binnen complex</h2>
            <div class="notificaties" id="notificaties">
                <!-- komen hier te staan als je een stuurt, dus als je iets wilt aanpassen moet dat met deze class -->
            </div>
        </div>

        <!-- Modal voor Full View -->
        <div class="modal" id="modal">
            <div class="modal-content">
                <span class="close-btn" id="close-btn">&times;</span>
                <div id="modal-text">
                    <h2 id="modal-title"></h2>
                    <p id="modal-description"></p>
                </div>
            </div>
        </div>

        <div class="grote-foto">
            <img src="../../Frontend/Gedeeld/pictures/Slachthuis-800px.jpg" alt="tuin foto">
        </div>

        <div class="stats-sectiie">

            <div class="stats-item">
                <h3>Aantal Deelnemers In Complex</h3>
                <div class="number"><a href="Leden-beheer.php"><?php echo $counter?></a></div>

                <div class="stats-item1">
                    <h3>Grond In Gebruik</h3>
                    <div class="Pie_Chart_Container">
                        <canvas id="Pie_Chart" class="Animate_Pie_Chart" width="220" height="560"></canvas>
                        <ul id="Pie_Chart_"></ul>
                    </div>
                </div>

            </div>
        </div>

    </div>

</body>
</html>

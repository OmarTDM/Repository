<?php
require_once __DIR__ . "/../../Backend/SessionChecker.php";

checkSession($allowedUserTypes = [2]);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Volkstuin Vereniging Sittard</title>
  <link rel="stylesheet" href="CSS-Beheerder/Leden-beheer.css">
</head>
<body>
  <!-- Sidebar -->
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

  <!-- Header -->
  <div class="header">
    VOLKSTUIN VERENING SITTARD
  </div>

  <!-- Lijst (main container) -->
  <div class="main-container">
    <h2>Leden Beheer</h2>
    <div class="leden-beheer-table">
      <table id="ledenTable">
        <thead>
          <tr>
            <th>Naam</th>
            <th>Complex</th>
            <th>m²</th>
            <th>Datum</th>
            <th>Email</th>
            <th>Telefoon</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <!-- voorbeeld -->
          <tr id="member1">
            <td id="naam1">Jan Jansen</td>
            <td id="complex1">Complex 1</td>
            <td id="grootte1">50</td>
            <td id="datum1">2024-12-09</td>
            <td id="email1">jan.jansen@gmail.com</td>
            <td id="telefoon1">123-456-7890</td>
            <td>
              <button class="info-button" onclick="showInfo(1)">Meer Info</button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Knop om leden toe te voegen -->
      <button id="addMember">Lid Toevoegen</button>
    </div>
  </div>

  <!-- Modal -->
<div id="modal" class="modal">
  <div class="modal-content">
    <span id="close-btn" class="close-btn">&times;</span>
    <div class="modal-header">
      <h2>Volkstuin Vereniging Sittard</h2>
    </div>
    <div class="modal-body">
      <div class="form-section">
        <div class="left-column">
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
        <div class="right-column">
          <label>Complex Naam</label>
          <input type="text" id="complex-naam" placeholder="Complex Naam">
          <label>m²</label>
          <input type="text" id="complex-size" placeholder="?m²">
          <label>Kosten</label>
          <input type="text" id="kosten" placeholder="Kosten">
          <button class="send-message">Verstuur bericht</button>
        </div>
      </div>
      <button class="edit-button">Wijzigen</button>
    </div>
  </div>
</div>

  <!-- javascript link -->
  <script src="Leden-beheer.js"></script>
</body>
</html>

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
    <!-- javascript link -->
    <script src="leden-beheer.js" defer></script>
</head>
<body>
  <!-- Sidebar -->
  <div class="sidebar">
      <img src="../../Frontend/Gedeeld/pictures/logo-volkstuinverenigingsittard.png" alt="Logo">
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
              <div class="icon2">
                  <img src="../Gedeeld/pictures/ExitMenuButton.svg" alt="Uitloggen">
              </div>
          </a>
      </div>

  </div>

  <!-- Header -->
  <div class="header">
    VOLKSTUIN VERENIGING SITTARD
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
                <th>Email</th>
            </tr>
            </thead>
            <tbody>
            </tbody>
        </thead>
      </table>
    </div>
  </div>

  <!-- Modal -->
  <div id="modal" class="modal">
      <div class="modal-content">
          <h1 id="close-btn" class="close-btn">&times;</h1>
          <div class="modal-header">
              <h2>Volkstuin Vereniging Sittard</h2>
          </div>
          <div class="modal-body">
              <div class="form-section">
                  <div class="left-column">
                      <label>Voornaam</label>
                      <input type="text" id="voornaam" placeholder="Voornaam" disabled>
                      <label>Achternaam</label>
                      <input type="text" id="achternaam" placeholder="Achternaam" disabled>
                      <label>E-mailadres</label>
                      <input type="email" id="email" placeholder="E-mailadres" disabled>
                      <label>Telefoonnummer</label>
                      <input type="tel" id="telefoon" placeholder="Telefoonnummer" disabled>
                      <label>Woonadres</label>
                      <input type="text" id="straat" placeholder="Straatnaam" disabled>
                      <div class="row">
                          <input type="text" id="postcode" placeholder="Postcode" disabled>
                          <input type="text" id="huisnummer" placeholder="Huisnummer" disabled>
                      </div>
                  </div>
                  <div class="right-column">
                      <label>Complex</label>
                      <input type="text" id="complex-naam" placeholder="Complex Naam" disabled>
                      <label>m²</label>
                      <input type="text" id="complex-size" placeholder="?m²" disabled>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>

</body>
</html>

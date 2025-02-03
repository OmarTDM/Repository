<?php
require_once __DIR__ . "/../../Backend/Models/Requests.php";
require_once __DIR__ . "/../../Backend/Models/Complexes.php";

$complexes = new Complexes();
$complexes = $complexes->findAll();
if (!is_array($complexes)) {
    $complexes = [];
}


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $request = new Requests();
    $firstName = $_POST['name'];
    $lastName = $_POST['surname'];
    $request->Name = trim($firstName . ' ' . $lastName);


    $request->ZipCode = $_POST['zipcode'] ?? '';
    $street = $_POST['street'] ?? '';
    $houseNumber = $_POST['house_number'] ?? '';
    $request->Address = trim($street . ' ' . $houseNumber);

    $request->Email = $_POST['email'];
    $request->PhoneNumber = $_POST['phonenumber'] ?? '';
    $request->Motive = $_POST['motive'] ?? '';
    $request->Complex1 = $_POST['complex1'];
    $request->Complex2 = $_POST['complex2'] ?? '';

        $request->Create();
        header('Location: Bedankt.html');
        exit;

}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Volkstuin Vereniging Sittard</title>
  <link rel="stylesheet" href="CSS-Formulier/register.css">
</head>
<body>
  <div class="sidebar">
    <img src="../Gedeeld/pictures/logo-volkstuinverenigingsittard-512x512-white%20(1).png" alt="Logo">
  </div>

  <div class="header">
    VOLKSTUIN VERENIGING SITTARD
  </div>

  <div class="form-container">
  <h2>Aanvraag voor volkstuin</h2>
  <form class="styled-form" action="" method="POST">
    <div class="form-section">
      <div class="form-group">
        <label for="name">Voornaam</label>
        <input type="text" id="name" name="name" placeholder="Voornaam" required>
      </div>
      <div class="form-group">
        <label for="surname">Achternaam</label>
        <input type="text" id="surname" name="surname" placeholder="Achternaam" required>
      </div>
      <div class="form-group">
        <label for="email">E-mailadres</label>
        <input type="email" id="email" name="email" placeholder="E-mailadres" required>
      </div>
      <div class="form-group">
        <label for="phonenumber">Telefoonnummer</label>
        <input type="tel" id="phonenumber" name="phonenumber" placeholder="Telefoonnummer">
      </div>
        <div class="form-group">
            <label>Woonadres</label>
            <div class="address-group">
                <input type="text" id="zipcode" name="zipcode" placeholder="Postcode">
                <input type="text" id="house_number" name="house_number" placeholder="Huisnummer">
                <input type="text" id="street" name="street" placeholder="Straatnaam">
            </div>
        </div>
    </div>

    <div class="form-section">
      <div class="form-group">
        <label for="complex1" class="form-label">Complex 1</label>
        <select name="complex1" id="complex1" required>
    <?php if (empty($complexes)): ?>
        <option value="">Geen complexen beschikbaar</option>
    <?php else: ?>
        <?php foreach ($complexes as $complex): ?>
            <option value="<?php echo htmlspecialchars($complex['Id'], ENT_QUOTES); ?>">
                <?php echo htmlspecialchars($complex['Name'], ENT_QUOTES); ?>
            </option>
        <?php endforeach; ?>
    <?php endif; ?>
</select>
      </div>
      <div class="form-group">
      <label for="complex2" class="form-label">Complex 2</label>
<select name="complex2" id="complex2">
    <?php if (empty($complexes)): ?>
        <option value="">Geen complexen beschikbaar</option>
    <?php else: ?>
        <?php foreach ($complexes as $complex): ?>
            <option value="<?php echo htmlspecialchars($complex['Id'], ENT_QUOTES); ?>">
                <?php echo htmlspecialchars($complex['Name'], ENT_QUOTES); ?>
            </option>
        <?php endforeach; ?>
    <?php endif; ?>
</select>
      </div>
      <div class="form-group">
        <label for="Motive">Uw motivatie</label>
        <textarea id="Motive" name="Motive" placeholder="Type hier"></textarea>
          <div class="more-space">
              <button type="submit" class="submit-button">Indienen</button>
          </div>
          <?php if (isset($error)) : ?>
              <div class="error-message"><?= htmlspecialchars($error) ?></div>
          <?php endif; ?>
      </div>
    </div>
  </form>
</div>
</body>
</html>




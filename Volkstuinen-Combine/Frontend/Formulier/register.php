<?php
require_once "Backend/Models/Requests.php";
require_once "Backend/Models/Complexes.php";

$complexes = new Complexes();
$complexes->findAll();

$request = new Requests();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $request->Name = $_POST['name'] ?? '';
    $request->Email = $_POST['email'] ?? '';
    $request->PhoneNumber = $_POST['phonenumber'] ?? '';
    $request->Address = $_POST['address'] ?? '';
    $request->ZipCode = $_POST['zipcode'] ?? '';
    $request->Motive = $_POST['motive'] ?? '';
    $request->Complex1 = $_POST['complex1'] ?? '';
    $request->Complex2 = $_POST['complex2'] ?? '';
}
if (empty($request->Name) || empty($request->Email) || empty($request->Motive) || empty($request->Complex1))
{
    $error = "naam, email en  zijn nodig.";
}
else
{

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

    <img src="../Temp/pictures/logo-volkstuinverenigingsittard-512x512-white%20(1).png" alt="Logo">

    <div class="Icoontjes">

    <a href="../Temp/dashboard.html">
        <div class="icon1">
            <img src="../Temp/pictures/clipart523723.png" alt="huisknop">
        </div>
    </a>
    <a href="settings">
        <div class="icon2">
            <img src="../Temp/pictures/images-removebg-preview.png" alt="settings">
        </div>
    </a>
    <a href="../Temp/login.html">
        <div class="icon">
            <p>temp</p> 
        </div>
    </a>
    </div>

  </div>

  <div class="header">
    VOLKSTUIN VERENING SITTARD
  </div>
  <div class="main-container">

    <p class="Dashtitle"> Uw gegevens</p>
    <div class="content">

    <div class="form-container">

<form class="registration-form" action="" method="POST">
    <label for="name" class="form-label"></label>
    <input type="text" id="name" name="name" class="form-input" placeholder="Voornaam" required><br>

    <label for="name" class="form-label"></label>
    <input type="text" id="name" name="name" class="form-input" placeholder="Achternaam" required><br>

    <label for="email" class="form-label"></label>
    <input type="email" id="email" name="email" class="form-input" placeholder="E-mailadres" required><br>

    <label for="phonenumber" class="form-label"></label>
    <input type="tel" id="phonenumber" name="phonenumber" class="form-input" placeholder="Telefoonnummer" ><br>
<p id="woonadres">Woonadres </p>
    <label for="zipcode" class="form-label"></label>
    <input type="text" id="zipcode" name="zipcode" class="form-input" placeholder="Postcode" ><br>

    <label for="address" class="form-label"></label>
    <input type="text" id="address" name="address" class="form-input" placeholder="Huisnummer" ><br>

    <label for="address" class="form-label"></label>
    <input type="text" id="address" name="address" class="form-input" placeholder="Straatnaam" ><br>

    <label for="Motive" class="form-label"></label>
    <input type="text" id="Motive" name="Motive" class="form-input" placeholder="Waarom wilt u bij onze organizatie?" ><br>
    <label for="complex1" class="form-label"></label>
    <select name="complex1" id="complex1">
        <?php foreach($complexes as $complex){?>
            <option value="<?php echo $complex->Id ?>"><?php echo $complex->Name ?></option>
        <?php }?>
    </select>
    <label for="complex2" class="form-label"></label>
    <select name="complex2" id="complex2">
        <?php foreach($complexes as $complex){?>
            <option value="<?php echo $complex->Id ?>"><?php echo $complex->Name ?></option>
        <?php }?>
    </select>

    <button type="submit" name="register" class="form-button">Registreren</button>
</form>

    </div>
      
</div>

</body>
</html>




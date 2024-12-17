<?php
session_start();
require_once "../Backend/Models/User.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $identifier = $_POST['identifier'] ?? '';
    $password = $_POST['password'] ?? '';

    if (empty($identifier) || empty($password)) {
        $error = "Naam of email en wachtwoord zijn nodig.";
    } else {
        $user = new User();

        if ($user->LoginUser($identifier, $password)) {
            switch ($_SESSION['user_type']) {
                case 1:
                    header("Location: Frontend/Deelnamer/dashboard.php");
                    exit;
                case 2:
                    header("Location: Frontend/Beheerder/dashboard.php");
                    exit;
                case 3:
                    header("Location: Frontend/Bestuurder/dashboard.php");
                    exit;
                default:
                    $error = "niet bestaande UserType.";
                    break;
            }
        } else {
            $error = "Incorrect Gebruikersnaam, e-mail of wachtwoord.";
        }
    }
}
if (isset($error)) {
    echo htmlspecialchars($error);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Volkstuin Vereniging Sittard</title>
  <link rel="stylesheet" href="login.css">
</head>
<body>


    <div class="sidebar">

        <img src="../Frontend/Gedeeld/pictures/logo-volkstuinverenigingsittard-512x512-white%20(1).png" alt="logo">

    
    </div>

    <div class="header">
        VOLKSTUIN VERENING SITTARD
    </div>


  <div class="main-container">


  </div>
  <div class="login-container">
    <div class="login-box">
      <div class="login-avatar">
        <img src="../Frontend/Gedeeld/pictures/download (11).jpeg" alt="pfp">
      </div>
      <h2>LOGIN</h2>
      <form action="" method="post">
        <label for="identifier">E-MAIL OF GEBRUIKERSNAAM</label>
        <input type="text" id="identifier" name="identifier" required>

  
        <label for="password">WACHTWOORD</label>
        <input type="password" id="password" name="password" required>

        <a href="#">Wachtwoord vergeten?</a>
        <button type="submit">Login</button>
          <?php if (isset($error)) : ?>
              <div class="error-message"><?= htmlspecialchars($error) ?></div>
          <?php endif; ?>
      </form>
    </div>
    <div class="logimgbg">
      <img class="login-image" src="../Frontend/Gedeeld/pictures/Baandert1-800px.jpg" alt="tuinfoto">
    </div>
  </div>
</body>
</html>

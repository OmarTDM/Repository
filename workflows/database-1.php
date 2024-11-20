<?php
if (isset($_POST['submit'])) {
    $conn = mysqli_connect("localhost", "root", "", "VISTA_test");
    
    $bedrijf = $_POST['bedrijf'];
    $naam = $_POST['naam'];
    $email = $_POST['email'];
    $score = $_POST['score'];

    $stmt = $conn->prepare("INSERT INTO `resultaten` (`bedrijf`, `naam`, `email`, `resultaten`) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $bedrijf, $naam, $email, $score);
    $stmt->execute();

    // Close the database connection
    $stmt->close();
    mysqli_close($conn);

    // Redirect to another page

    exit; // Ensure that the script stops after the redirection
    if ($conn === false) {
        die("ERROR: Could not connect. " . mysqli_connect_error());
    }
}
?>





<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" href="styles.css">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div class="endForm">
  <form method="POST" id="endForm">
    <div class="top">
        <label class="lb" for="">Bedrijfsnaam:</label>
        <input class="inp" name="bedrijf" type="text" class="bedrijfsnaam">
        <label class="lb" for="">Naam</label>
        <input class="inp" name="naam" type="text" class="naam">
    </div>
    <label class="lb" for="">Email:</label>
    <input class="inp" name="email" type="text">
    <input id="scoreEl" name="score" type="number" value="1" style=" display: none;" readonly>
    <button id="submitForm"  type="submit" name="submit">Submit</button>
</form>
<div id="load-bar">
    </div>
  </div>
  <script src="script2.js"></script>
</html>
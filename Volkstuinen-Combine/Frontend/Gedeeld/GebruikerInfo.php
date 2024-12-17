<?php
require_once "Backend/SessionChecker.php";
require_once "Backend/Models/User.php";
checkSession($allowedUserTypes = [1,2,3]);
$user = new User();
$id = $_SESSION['user_id'];

$user->findByIdUser($id)
?>

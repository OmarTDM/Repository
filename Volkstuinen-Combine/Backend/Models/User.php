<?php
require_once __DIR__ . "/../UserModel.php";

class User extends UserModel
{
    protected static string $table_name = "users";
    protected static string $primary_key = "Id";



    public array $properties = [
        'Name' => null,
        'Email' => null,
        'Password' => null,
        'PhoneNumber' => null,
        'ZipCode' => null,
        'Address' => null,
        'Complex' => null,
        'Membership' => null,
        'Payment' => null
    ];

}
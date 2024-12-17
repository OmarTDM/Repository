<?php
require_once __DIR__ . "/../DBModel.php";

class Parcel extends DBModel
{
    protected static string $table_name = "parcel";
    protected static string $primary_key = "Id";

    protected array $properties = [
        'Name' => null,
        'Size' => null,
        'User'=> null,
        'Complex'=> null
    ];
}
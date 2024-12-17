<?php
require_once __DIR__ . "/../DBModel.php";

class Complexes extends DBModel
{
    protected static string $table_name = "messages";
    protected static string $primary_key = "Id";

    public array $properties = [
        'Name' => null,
    ];
}
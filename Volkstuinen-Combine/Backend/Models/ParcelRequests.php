<?php
require_once __DIR__ . "/../DBModel.php";

class ParcelRequests extends DBModel
{
    protected static string $table_name = "parcel-request";
    protected static string $primary_key = "Id";

        protected array $properties = [
            'Parcel'=> null,
            'User'=> null,
            'Complex'=> null
        ];
}
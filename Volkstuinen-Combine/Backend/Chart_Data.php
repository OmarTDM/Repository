<?php
declare(strict_types=1);
require_once __DIR__ . "/Models/Parcel.php"; // Make sure to include the correct model file

header('Content-Type: application/json');

try {
    $Data_Owned = 0;
    $Data_Unowned = 0;
    $parcel = new Parcel();

    // Assuming you have a session that provides the Complex ID or set it directly
    $secondary_SearchTerm = 1;
    $tertiary_SearchTerm = "IS NULL";

    // Fetch parcels that are in use (owned)
    $parcelsInUse = $parcel->Search("Complex", $secondary_SearchTerm);
    $Data_Owned = count($parcelsInUse); // Set the count of owned parcels

    // Fetch parcels that are not in use (unowned)
    $parcelsNotInUse = $parcel->SearchWithConstraints("Complex", "User", $tertiary_SearchTerm, $secondary_SearchTerm);
    $Data_Unowned = count($parcelsNotInUse); // Set the count of unowned parcels

    // Send the response as a JSON object
    echo json_encode([
        'In Gebruik' => $Data_Owned,
        'Buiten Gebruik' => $Data_Unowned
    ]);
} catch (Exception $e) {
    // Log the error and send a clear error message in the response
    error_log('Error in Chart_Data.php: ' . $e->getMessage());
    echo json_encode([
        'error' => 'An error occurred while fetching data: ' . $e->getMessage()
    ]);
}
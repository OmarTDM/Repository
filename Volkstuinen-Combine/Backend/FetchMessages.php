<?php
declare(strict_types=1);
header("Content-Type: application/json");
require_once __DIR__ . '/Models/Message.php';

try {
    $messages = new Message();
    $Secondary_SearchTerm = 1;
    $results = $messages->Search("Complex", $Secondary_SearchTerm);

    $formattedResults = array_map(function ($row) {
        return [
            'Id' => $row['Id'],
            'Subject' => $row['Subject'],
            'Message' => $row['Message'],
            'Receiver' => $row['Receiver'],
        ];
    }, $results);

    // Send JSON response
    echo json_encode(['success' => true, 'messages' => $formattedResults]);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}

exit;
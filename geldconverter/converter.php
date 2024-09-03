<?php
// api key
$apiKey = '88539150ba646c7126c380ef';
$apiUrl = "https://v6.exchangerate-api.com/v6/$apiKey/latest/USD";

// exchange rates halen
$response = file_get_contents($apiUrl);
if ($response === FALSE) {
    die('Error met convertion, check api of internet connectie');
}

$exchangeRates = json_decode($response, true);

// Check if the API response is successful
if ($exchangeRates['result'] !== 'success') {
    die('Error' . $exchangeRates['error-type']);
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $fromCurrency = strtoupper(trim($_POST['from_currency']));
    $toCurrency = strtoupper(trim($_POST['to_currency']));
    $amount = floatval($_POST['amount']);

    if ($amount <= 0) {
        echo "<p style='color:red;'>Vul een getal groter dan 0 in</p>";
        exit;
    }

    if (isset($exchangeRates['conversion_rates'][$fromCurrency]) && isset($exchangeRates['conversion_rates'][$toCurrency])) {
        $rateFrom = $exchangeRates['conversion_rates'][$fromCurrency];
        $rateTo = $exchangeRates['conversion_rates'][$toCurrency];
        $convertedAmount = ($amount / $rateFrom) * $rateTo;

        echo "<p>" . number_format($convertedAmount, 2) . " $toCurrency</p>";
    } else {
        echo "<p style='color:red;'>Invalid currency code gegeven</p>";
    }
} else {
    echo "<p>Submit de forum</p>";
}
?>

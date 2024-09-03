document.addEventListener('DOMContentLoaded', function() {
    // map
    const map = L.map('map').setView([51.505, -0.09], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    const countries = {
        'USD': { lat: 40.0902, lng: -95.7129, name: 'VS', currency: 'USD' },
        'EUR': { lat: 52.1326, lng: 5.2913, name: 'Nederland', currency: 'EUR' },
        'GBP': { lat: 51.5074, lng: -0.1278, name: 'Engeland', currency: 'GBP' }
    };

    Object.keys(countries).forEach(key => {
        const country = countries[key];
        const marker = L.marker([country.lat, country.lng]).addTo(map);
        marker.bindPopup(`${country.name} (${country.currency})`);

        marker.on('click', () => {
            document.getElementById('from_currency').value = key;
        });
    });

    // dit zorgt ervoor als je op de currency wegklikt of op het kruis klikt dat het weg gaat
    const modal = document.getElementById("currencyModal");
    const btn = document.getElementById("showCurrencies");
    const span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // voor als ik plaatsen in de map toevoeg (staat ook in de lijst)
    const currencyList = document.getElementById('currencyListItems');
    const currencies = ['USD', 'EUR', 'GBP']; 
    currencies.forEach(currency => {
        const li = document.createElement('li');
        li.textContent = currency;
        currencyList.appendChild(li);
    });

    // Handle form submission
    const form = document.getElementById('currencyForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const fromCurrency = document.getElementById('from_currency').value.trim().toUpperCase();
        const toCurrency = document.getElementById('to_currency').value.trim().toUpperCase();
        const amount = document.getElementById('amount').value;

        if (amount === '' || isNaN(amount) || amount <= 0) {
            resultDiv.innerHTML = '<p style="color: red;">Vul het goede in</p>';
            return;
        }

        const formData = new FormData();
        formData.append('from_currency', fromCurrency);
        formData.append('to_currency', toCurrency);
        formData.append('amount', amount);

        fetch('converter.php', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            resultDiv.innerHTML = data;
        })
        .catch(error => {
            resultDiv.innerHTML = '<p style="color: red;">error</p>';
        });
    });
});

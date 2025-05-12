
const locationInput = document.getElementById('locationInput');
const searchBtn = document.getElementById('searchBtn');
const weatherInfo = document.getElementById('weatherInfo');
const mapContainer = document.getElementById('map');

// api key
const apiKey = 'a4186a4c48a9475321d96497ee9a5988'; 

// map inladen
const mymap = L.map('map').setView([51.505, -0.09], 13);

// openstreet map tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);


searchBtn.addEventListener('click', function() {
    const location = locationInput.value.trim();
    
    if (location !== '') {
        fetchWeather(location);
        fetchMapCoordinates(location);
    } else {
        weatherInfo.innerHTML = '<p>Please enter a location</p>';
    }
});

// functie om wee data te fetchen
async function fetchWeather(location) {
    const weatherUrl = `https://api.openweathermap.org/data/2.5/weather?q=${location}&units=metric&appid=${apiKey}`;
    
    try {
        const response = await fetch(weatherUrl);
        if (!response.ok) {
            throw new Error('Failed to fetch weather data');
        }
        const weatherData = await response.json();
        
        if (weatherData.cod === 200) {
            displayWeather(weatherData);
        } else {
            console.error(`OpenWeatherMap API Error: ${weatherData.message}`);
            weatherInfo.innerHTML = `<p>${weatherData.message}</p>`;
        }
    } catch (error) {
        console.error('Error fetching weather data:', error);
        weatherInfo.innerHTML = '<p>Failed to fetch weather data. Please try again later.</p>';
    }
}

// laat weer data zien
function displayWeather(data) {
    const { name, main, weather, wind, sys } = data;
    
    const weatherHTML = `
        <h2>${name}, ${sys.country}</h2>
        <p><strong>Temperature:</strong> ${main.temp}°C</p>
        <p><strong>Weather:</strong> ${weather[0].description}</p>
        <p><strong>Humidity:</strong> ${main.humidity}%</p>
        <p><strong>Pressure:</strong> ${main.pressure} hPa</p>
        <p><strong>Wind Speed:</strong> ${wind.speed} m/s</p>
    `;
    
    weatherInfo.innerHTML = weatherHTML;
}

// fetch map
async function fetchMapCoordinates(location) {
    const mapUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`;

    try {
        const response = await fetch(mapUrl);
        if (!response.ok) {
            throw new Error('Failed to fetch map coordinates');
        }
        const mapData = await response.json();
        
        if (mapData.length > 0) {
            const { lat, lon } = mapData[0];
            mymap.setView([lat, lon], 13);
            L.marker([lat, lon]).addTo(mymap)
                .bindPopup(`${location}`).openPopup();
        } else {
            console.error(`No coordinates found for location: ${location}`);
            weatherInfo.innerHTML = '<p>No coordinates found for location. Please try another location.</p>';
        }
    } catch (error) {
        console.error('Error fetching map coordinates:', error);
        weatherInfo.innerHTML = '<p>Failed to fetch map coordinates. Please try again later.</p>';
    }
}

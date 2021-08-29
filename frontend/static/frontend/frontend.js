
document.addEventListener('DOMContentLoaded', () => {
  const search = document.querySelector('#search');
  const matchList = document.querySelector('#match-list');

  document.querySelector('#my-location').addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(function(position) {
      getWeatherDataByCoordinates(position.coords.latitude, position.coords.longitude);
    });
  });

  document.querySelector('#random').addEventListener('click', () => {
    randomLocation();
  });

  search.addEventListener('input', () => searchLocation(search.value));
})


const searchLocation = async searchText => {
  // search meteostat-mini.json and filter it
  const res = await fetch('/static/frontend/meteostat-mini.json');
  const locations = await res.json();

  // Get matches to current text input
  let matches = locations.filter(location => {
    const regex = new RegExp(`^${searchText}`, 'gi');
    return location.name.match(regex); // || location.country.match(regex)
  });

  if (searchText.length === 0) {
    matches = [];
    document.querySelector('#match-list').innerHTML = '';
  }
  outputHtml(matches);
}


const randomLocation = async () => {
  const res = await fetch('/static/frontend/meteostat-mini.json');
  const locations = await res.json();
  const count = Object.keys(locations).length;
  const random = Math.floor(Math.random() * count);
  const lat = locations[random].lat;
  const long = locations[random].long;
  getWeatherDataByCoordinates(lat, long);
}


// Show results in HTML
const outputHtml = matches => {
  if (matches.length > 0) {
    const html = matches.map(match => `
      <div class="result-card card card-body mb-1" data-name="${match.name}" data-lat="${match.lat}" data-long="${match.long}">
        <h4>${match.name} (${match.country})</h4>
        <small>Lat: ${match.lat}, Long: ${match.long}</small>
      </div>
    `).join('');

    document.querySelector('#match-list').innerHTML = html;

    document.querySelectorAll('.result-card').forEach(item =>
      item.addEventListener('click', () => {
        document.querySelector('#search').value = item.getAttribute('data-name');
        document.querySelector('#match-list').innerHTML = "";
        getWeatherDataByCoordinates(item.getAttribute('data-lat'), item.getAttribute('data-long'));
      })
    );
  }
}


const getWeatherDataByCoordinates = (lat, long) => {
  // Make an API request for the weather data for a given set of coordinates
  // Inputs: lat and long (strings)
  // Output: TODO
  console.log(`lat: ${lat} / long: ${long}`);
  const requestOptions = {
    method: 'GET',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      lat: lat,
      long: long,
    })
  };
  fetch(`/api/monthly/${lat}/${long}`)
  .then(response => response.json())
  .then(data => console.log(data));
}
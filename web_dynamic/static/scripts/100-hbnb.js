$(document).ready(init);

const HOST = '0.0.0.0';

function init() {
  // Dictionaries to store selected amenities, states, and cities
  const amenityObj = {};
  const stateObj = {};
  const cityObj = {};

  // Function to update the text of the h4 tag inside the div Locations
  function updateLocationsH4() {
    const locations = []
      .concat(Object.values(stateObj))
      .concat(Object.values(cityObj))
      .sort();
    $('.locations h4').text(locations.join(', '));
  }

  // Listen for changes on the amenities checkboxes
  $('.amenities .popover input').change(function() {
    if ($(this).is(':checked')) {
      amenityObj[$(this).attr('data-name')] = $(this).attr('data-id');
    } else {
      delete amenityObj[$(this).attr('data-name')];
    }
    const names = Object.keys(amenityObj);
    $('.amenities h4').text(names.sort().join(', '));
  });

  // Listen for changes on the states checkboxes
  $('.locations .popover input[type="checkbox"].state').change(function() {
    if ($(this).is(':checked')) {
      stateObj[$(this).attr('data-name')] = $(this).attr('data-id');
    } else {
      delete stateObj[$(this).attr('data-name')];
    }
    updateLocationsH4();
  });

  // Listen for changes on the cities checkboxes
  $('.locations .popover input[type="checkbox"].city').change(function() {
    if ($(this).is(':checked')) {
      cityObj[$(this).attr('data-name')] = $(this).attr('data-id');
    } else {
      delete cityObj[$(this).attr('data-name')];
    }
    updateLocationsH4();
  });

  // When the button is clicked, perform the search
  $('button').click(function() {
    fetchPlaces({
      amenities: Object.values(amenityObj),
      states: Object.values(stateObj),
      cities: Object.values(cityObj),
    });
  });

  apiStatus();
  fetchPlaces();
}

function apiStatus () {
  const API_URL = `http://${HOST}:5001/api/v1/status/`;
  $.get(API_URL, (data, textStatus) => {
    if (textStatus === 'success' && data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
}

// Modify the fetchPlaces function to use the passed parameters
function fetchPlaces(data = {}) {
  const PLACES_URL = `http://${HOST}:5001/api/v1/places_search/`;
  $.ajax({
    url: PLACES_URL,
    type: 'POST',
    headers: { 'Content-Type': 'application/json' },
    data: JSON.stringify(data),
    success: function(response) {
      $('SECTION.places').empty();
      response.forEach(function(r) {
        const article = $(`<article>
          <div class="title_box">
            <h2>${r.name}</h2>
            <div class="price_by_night">$${r.price_by_night}</div>
          </div>
          <div class="information">
            <div class="max_guest">${r.max_guest} Guest(s)</div>
            <div class="number_rooms">${r.number_rooms} Bedroom(s)</div>
            <div class="number_bathrooms">${r.number_bathrooms} Bathroom(s)</div>
          </div>
          <div class="description">
            ${r.description}
          </div>
        </article>`);
        $('SECTION.places').append(article);
      });
    },
    error: function(error) {
      console.log(error);
    }
  });
}


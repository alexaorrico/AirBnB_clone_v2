const $ = window.$;
const amenitiesIds = [];
const amenitiesNames = [];
$(document).ready(function () {
    $('input').click(function () {
	const amenityId = $(this).data('id');
	const amenityName = $(this).data('name');
	if (amenitiesIds.includes(amenityId)) {
            const index = amenitiesIds.indexOf(amenityId);
            if (index !== -1) {
		amenitiesIds.splice(index, 1);
		amenitiesNames.splice(index, 1);
            }
	} else {
            amenitiesIds.push(amenityId);
	    amenitiesNames.push(amenityName);
	}
	$('DIV.amenities h4').text(amenitiesNames.join(', '));
    });
    const request = $.getJSON('http://0.0.0.0:5001/api/v1/status/');
    request.done(function (data) {
	if (data.status === 'OK') {
	    console.log(data.status);
	    $('DIV#api_status').addClass('available');
	} else {
	    $('DIV#api_status').removeClass('available');
	}
    });
y    $.ajax({
    url: 'http://localhost:5001/api/v1/places_search/',
    type: 'POST',
    data: JSON.stringify({}),
    contentType:"application/json; charset=utf-8",
    success: function (response) {
    for (const place of response) {
        $('SECTION.places').append(`
          <article>
            <div class="title_box">
              <h2>` + place.name + `</h2>
            <div class="price_by_night">` + place.price_by_night + `</div>
            </div>
            <div class="information">
              <div class="max_guest">` + place.max_guest + `Guests </div>
                <div class="number_rooms">` + place.number_rooms + `</div>
                <div class="number_bathrooms">` + place.number_bathrooms + `</div>
            </div>
            <div class="user">
              <b>Owner:</b> first name last name
            </div>
            <div class="description">` + place.description + `</div>
            </article>
        `);
      }
    }
  });
});

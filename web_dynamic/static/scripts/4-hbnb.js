const $ = window.$;
const amenities = {};
$(document).ready(function () {
    $('input').click(function () {
	if ($(this).is(':checked')) {
            amenities[($(this).attr('data-name'))] = ($(this).attr('data-id'));
	} else {
	    delete amenities[($(this).attr('data-name'))];
	}
	$('DIV.amenities h4').text(Object.keys(amenities).join(', '));
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
    data: JSON.stringify({amenities}),
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

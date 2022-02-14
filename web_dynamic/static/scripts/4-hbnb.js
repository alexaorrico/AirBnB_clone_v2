$(function () {
  const listAmenities = {};

  $('div.amenities li input').change(
    function () {
      if ($(this).is(':checked')) {
        listAmenities[($(this).attr('data-id'))] = $(this).attr('data-name');
      } else {
        delete listAmenities[($(this).attr('data-id'))];
      }
      $('div.amenities h4').html(Object.values(listAmenities).join(', ') || '&nbsp;');
    });

  $('.filters button').click(function (event) {
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search',
      type: 'POST',
      contentType: 'application/json',
      dataType: 'JSON',
      data: JSON.stringify({ amenities: Object.keys(listAmenities) }),
      success: function (data) {
        let newHTML = [];
        for (let i = 0; i < data.length; i++) {
          newHTML.push(htmlCode(data[i]));
        }
        newHTML = newHTML.join('');
        $('section.places > article').remove();
        $('section.places').append(newHTML);
      }
    });
  });

  $.getJSON('http://0.0.0.0:5001/api/v1/status/', (data) => {
    if (data.status === 'OK') {
      $('DIV#api_status').addClass('available');
    } else {
      $('DIV#api_status').removeClass('available');
    }
  });


  // task 4
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    contentType: 'application/json',
    data: JSON.stringify({})
  }).done(function (data) {
    for (const place of data) {
      const template = `<article>
        <div class="title">

          <h2>${place.name}</h2>

          <div class="price_by_night">

        $${place.price_by_night}
          </div>
        </div>

        <div class="information">
          <div class="max_guest">
        <i class="fa fa-users fa-3x" aria-hidden="true"></i>
        
        <br />

        ${place.max_guest} Guests

          </div>

          <div class="number_rooms">
        <i class="fa fa-bed fa-3x" aria-hidden="true"></i>
        <br />
        
        ${place.number_rooms} Bedrooms
          </div>

          <div class="number_bathrooms">
        <i class="fa fa-bath fa-3x" aria-hidden="true"></i>
        
        <br />
        
        ${place.number_bathrooms} Bathroom
          </div>
        </div>

        <div class="description">
          ${place.description}
        </div>
        
      </article> <!-- End 1 PLACE Article -->`;
      $('section.places').append(template);
    }
  });
});


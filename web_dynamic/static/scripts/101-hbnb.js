let chosenAmens = {};
$(document).ready(function () {
  function fillPlaces (filter) {
    $.when($.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      type: 'POST',
      data: JSON.stringify(filter),
      dataType: 'json',
      contentType: 'application/json',
      success: function (data) {
        data = data.sort(function (first, second) {
          if (first.name < second.name) {
            return (-1);
          } else if (first.name === second.name) {
            return (0);
          } else {
            return (1);
          }
        });
      }
    })).done(function (data) {
      setPlaces(data);
    });
  }

  function setPlaces (places) {
    let i, len, pDict;
    $('section.places').empty();
    for (i = 0, len = places.length; i < len; i++) {
      pDict = places[i];
      let place = $('<article></article>');

      let title = $('<div class="title"></div>');
      title.append($('<h2></h2>').text(pDict.name));
      title.append($('<div class="price_by_night"></div>').text(pDict.price_by_night));

      let info = $('<div class="information"></div>');

      let guests = $('<div class="max_guest"></div>');
      guests.append($('<i class="fa fa-users fa-3x" aria-hidden="true"></i>'), $('<br />'), pDict.max_guest + ' Guests');

      let rooms = $('<div class="number_rooms"></div>');
      rooms.append($('<i class="fa fa-bed fa-3x" aria-hidden="true"></i>'), $('<br />'), pDict.number_rooms + ' Bedrooms');

      let bathrooms = $('<div class="number_bathrooms">');
      bathrooms.append($('<i class="fa fa-bath fa-3x" aria-hidden="true"></i>'), $('<br />'), pDict.number_bathrooms + ' Bathroom');

      info.append(guests, rooms, bathrooms);

      let desc = $('<div class="description"></div>').text(pDict.description);

      let reviews = $('<div class="reviews"></div>');
      reviews.append($('<h2>Reviews</h2>').append($('<span name="boo" data-id="' + pDict.id + '"> show</span>')));

      place.append(title, info, desc, reviews);
      $('SECTION.places').append(place);
    }
  }

  $('div.amenities ul.popover li input').click(function () {
    if ($(this).is(':checked')) {
      chosenAmens[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete chosenAmens[$(this).attr('data-id')];
    }
    if (!$.isEmptyObject(chosenAmens)) {
      $('div.amenities h4').text(Object.values(chosenAmens).join(', '));
    } else {
      $('div.amenities h4').text('\xA0');
    }
  });

  $('.container button').click(function () {
    let amen = {};
    amen['amenities'] = Object.keys(chosenAmens);
    setPlaces(fillPlaces(amen));
  });

  $('section.places').on('click', '.reviews h2 span', function () {
    let reviews = $(this).parent().parent();
    if ($(this).text() === ' show') {
      let i;
      let len;
      let ul = $('<ul></ul>');
      $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/places/' + $(this).attr('data-id') + '/reviews',
        type: 'GET',
        success: function (data) {
          for (i = 0, len = data.length; i < len; i++) {
            let username;
            let review = $('<li></li>');
            let place = data[i];
            $.when($.ajax({
              url: 'http://0.0.0.0:5001/api/v1/users/' + data[i].user_id,
              type: 'GET',
              success: function (udata) {
                username = udata.first_name + ' ' + udata.last_name;
              }
            })).done(function () {
              review.append($('<h3></h3>').text('From ' + username));
              review.append($('<p></p>').text(place.text));
              ul.append(review);
            });
          }
          reviews.append(ul);
        }
      });
      $(this).text(' hide');
    } else {
      $('.reviews ul').remove();
      $(this).text(' show');
    }
  });

  $.ajax({
    'url': 'http://0.0.0.0:5001/api/v1/status/',
    'type': 'GET',
    'success': function (data) {
      if (data.status === 'OK') {
        $('div#api_status').addClass('available');
      }
    }
  });

  fillPlaces({});
});

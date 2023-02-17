const $ = window.$;
$(document).ready(function () {
  const myAmenities = {};
  let myList = [];
  const checkbox = $('.amenities input[type="checkbox"]');
  checkbox.prop('checked', false);
  checkbox.change(function () {
    const dataId = $(this).attr('data-id');
    const dataName = $(this).attr('data-name');
    if (this.checked) {
      myAmenities[dataId] = dataName;
    } else {
      delete (myAmenities[dataId]);
    }
    for (const key in myAmenities) {
      myList.push(myAmenities[key]);
    }
    const output = myList.join(', ');
    $('div.amenities > h4').text(output);
    myList = [];
  });
  const apiStatus = $('DIV#api_status');
  $.ajax('http://0.0.0.0:5001/api/v1/status/').done(function (data) {
    if (data.status === 'OK') {
      apiStatus.addClass('available');
    } else {
      apiStatus.removeClass('available');
    }
  });
  const placesSearch = $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    dataType: 'json',
    contentType: 'application/json',
    method: 'POST',
    data: JSON.stringify({})
  });
  placesSearch.done(function (data) {
    for (let i = 0; i < data.length; i++) {
      /** Prepare data **/
      const placeName = data[i].name;
      const priceByNight = data[i].price_by_night;
      const maxGuest = data[i].max_guest;
      const maxRooms = data[i].number_rooms;
      const maxBathrooms = data[i].number_bathrooms;
      const desc = data[i].description;
      /** Prepare HTML **/
      const article = $('<article></article>');
      const titleBox = $("<div class='title_box'><h2></h2><div class='price_by_night'></div></div>");
      titleBox.find('> h2').html(placeName);
      titleBox.find('.price_by_night').html('$' + priceByNight);
      article.append(titleBox);
      const information = $("<div class='information'></div>");
      let guestString = ' Guest';
      if (maxGuest > 1) { guestString = ' Guests'; }
      const guest = $("<div class='max_guest'></div>").html(maxGuest + guestString);
      information.append(guest);
      let roomString = ' Bedroom';
      if (maxRooms > 1) { roomString = ' Bedrooms'; }
      const rooms = $("<div class='number_rooms'></div>").html(maxRooms + roomString);
      information.append(rooms);
      let bathString = ' Bathroom';
      if (maxBathrooms > 1) { bathString = ' Bathrooms'; }
      const bathrooms = $("<div class='number_bathrooms'></div>").html(maxBathrooms + bathString);
      information.append(bathrooms);
      article.append(information);
      const description = $("<div class='description'></div>").html(desc);
      article.append(description);
      $('SECTION.places').append(article);
    }
  });
});

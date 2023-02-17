const $ = window.$;
$(document).ready(function () {
  const myAmenities = {};
  const myStates = {};
  const myCities = {};
  let myList = [];
  const checkbox = $('.amenities input[type="checkbox"]');
  const checkboxStates = $('.locations .popover li > h2 > input[type="checkbox"]');
  const checkboxCities = $('.locations .popover li > ul li > input[type="checkbox"]');
  checkbox.prop('checked', false);
  checkboxStates.prop('checked', false);
  checkboxCities.prop('checked', false);

  function checkBoxActions (checkbox, dict, additionalDict = null) {
    myList = [];
    const dataId = $(checkbox).attr('data-id');
    const dataName = $(checkbox).attr('data-name');
    if (checkbox.checked) {
      dict[dataId] = dataName;
    } else {
      delete (dict[dataId]);
    }
    for (const key in dict) {
      myList.push(dict[key]);
    }
    if (additionalDict != null) {
      for (const key in additionalDict) {
        myList.push(additionalDict[key]);
      }
    }
    myList = myList.join(', ');
    return myList;
  }

  checkbox.change(function () {
    myList = checkBoxActions(this, myAmenities);
    $('div.amenities > h4').text(myList);
  });

  checkboxStates.change(function () {
    myList = checkBoxActions(this, myStates, myCities);
    $('div.locations > h4').text(myList);
  });

  checkboxCities.change(function () {
    myList = checkBoxActions(this, myCities, myStates);
    $('div.locations > h4').text(myList);
  });

  /**
   * Task 3:
   * Request http://0.0.0.0:5001/api/v1/status/:
   * - If in the status is “OK”, add the class available to the DIV#api_status
   * - Otherwise, remove the class available to the DIV#api_status
   * **/
  const apiStatus = $('DIV#api_status');
  $.ajax('http://0.0.0.0:5001/api/v1/status/').done(function (data) {
    if (data.status === 'OK') {
      apiStatus.addClass('available');
    } else {
      apiStatus.removeClass('available');
    }
  });

  function search (theAmenities, theStates, theCities) {
    const datas = {};
    if (theAmenities != null) {
      datas.amenities = theAmenities;
    }
    if (theStates != null) {
      datas.states = theStates;
    }
    if (theCities != null) {
      datas.cities = theCities;
    }
    const placesSearch = $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      dataType: 'json',
      contentType: 'application/json',
      method: 'POST',
      data: JSON.stringify(datas)
    });
    placesSearch.done(function (data) {
      for (let i = 0; i < data.length; i++) {
        const placeName = data[i].name;
        const priceByNight = data[i].price_by_night;
        const maxGuest = data[i].max_guest;
        const maxRooms = data[i].number_rooms;
        const maxBathrooms = data[i].number_bathrooms;
        const desc = data[i].description;
        const article = $('<article></article>');
        const titleBox = $("<div class='title_box'><h2></h2><div class='price_by_night'></div></div>");
        titleBox.find('> h2').html(placeName);
        titleBox.find('.price_by_night').html('$' + priceByNight);
        article.append(titleBox);
        const information = $("<div class='information'></div>");
        let guestString = ' Guest';
        if (maxGuest > 1) {
          guestString = ' Guests';
        }
        const guest = $("<div class='max_guest'></div>").html(maxGuest + guestString);
        information.append(guest);
        let roomString = ' Bedroom';
        if (maxRooms > 1) {
          roomString = ' Bedrooms';
        }
        const rooms = $("<div class='number_rooms'></div>").html(maxRooms + roomString);
        information.append(rooms);
        let bathString = ' Bathroom';
        if (maxBathrooms > 1) {
          bathString = ' Bathrooms';
        }
        const bathrooms = $("<div class='number_bathrooms'></div>").html(maxBathrooms + bathString);
        information.append(bathrooms);
        article.append(information);
        const description = $("<div class='description'></div>").html(desc);
        article.append(description);
        $('SECTION.places').append(article);
      }
    });
  }

  search();

  $('.filters > button').click(function () {
    $('SECTION.places').empty();
    search(myAmenities, myStates, myCities);
  });
});

$(document).ready(function() {
  // Function to check and update the API status
  function checkAPIStatus() {
    // Make an AJAX request to the API status endpoint
    $.ajax({
      type: 'GET',
      url: 'http://0.0.0.0:5001/api/v1/status/',
      success: function(response) {
        if (response.status === 'OK') {
          // If the status is "OK," add the "available" class to div#api_status
          $('#api_status').addClass('available');
        } else {
          // If the status is not "OK," remove the "available" class from div#api_status
          $('#api_status').removeClass('available');
        }
      },
      error: function() {
        // Handle the case where the AJAX request encounters an error
        $('#api_status').removeClass('available');
      }
    });
  }

  var selectedAmenities = [];

  // Listen for changes on the checkboxes with data-id attribute
  $('input[type="checkbox"][data-id]').change(function(event) {
    var amenityID = $(event.target).data("id"); // Retrieve amenityID from the event target

    if ($(this).is(":checked")) {
      // If the checkbox is checked, add the Amenity ID to the array
      selectedAmenities.push(amenityID);
    } else {
      var index = selectedAmenities.indexOf(amenityID);
      if (index !== -1) {
        selectedAmenities.splice(index, 1);
      }
    }
    // Update the <h4> tag with the list of selected Amenities
    var amenitiesText = selectedAmenities.join(", ");
    $(".amenities-list").text("Selected Amenities: " + amenitiesText);
  });
});
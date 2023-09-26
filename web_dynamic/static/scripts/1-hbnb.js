$(document).ready(function() {
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
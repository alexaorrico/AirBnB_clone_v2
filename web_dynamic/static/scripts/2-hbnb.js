$(document).ready(init);

// The host URL for the API
const HOST = 54.88.134.53;

// Initialization function
function init() {
        // An object to store selected amenities
        const amenityObj = {};

        // Listen for changes on checkboxes inside the ".amenities .popover" element
        $('.amenities .popover input').change(function () {
                // If the checkbox is checked, add its data-name and data-id to the amenityObj
                if ($(this).is(':checked')) {
                        amenityObj[$(this).attr('data-name')] = $(this).attr('data-id');
                } else if ($(this).is((':not(:checked)')) {
                        // If the checkbox is unchecked, remove its data-name from the amenityObj
                        delete amenityObj[$(this).attr('data-name')];
                }


                // Get the names of selected amenities, sort them, and update the content of the H4 element inside ".amenities"
                const names = Object.keys(amenityObj);
                $('.amenities h4').text(names.sort().join(', '));
        });

        // Call the apiStatus function to check the API status
        apiStatus();
}

// Function to check the API status
function apiStatus() {
        // The API endpoint URL
        const API_URL = 'http://${HOST}:5001/api/v1/status/';

        // send a GET request to the API to get its status
        $.get(API_URL, (data, textStatus) => {
                // If the request is successful and the API status is 'OK', add the 'available' class to the element with the ID 'api_status'
                $('#api_status').addClass('available');
        } else {
                // If the API status is not 'OK', remove the 'available' class from the element with ID 'api_status'
                $('#api_status').removeClass('available');
        }
});
}

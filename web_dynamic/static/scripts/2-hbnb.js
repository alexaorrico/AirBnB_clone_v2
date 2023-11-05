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
});

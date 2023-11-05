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
});

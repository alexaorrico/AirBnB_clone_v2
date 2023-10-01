$(function() {
    const amenityDict = {};
    $(':checkbox').change(function() {
        if (this.checked) {
            amenityDict[$(this).data('id')] = $(this).data('name');
        } else {
            delete amenityDict[$(this).data('id')];
        }
        if ($.isEmptyObject(amenityDict)) {
            $('.amenities h4').html('&nbsp');
        } else {
            $('.amenities h4').text(Object.values(amenityDict).join(', '));
        }
    });
});

$.get('http://0.0.0.0:5001/api/v1/status/', function(data) {
    if (data.status === 'OK') {
        $('div#api_status').addClass('available');
    } else {
        $('div#api_status').removeClass('available');
    }
});
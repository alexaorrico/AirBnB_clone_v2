$(function () {
  const amenityDict = {};
  $(':checkbox').change(function () {
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
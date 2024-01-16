$(document).ready(function () {
  let checkAmenities = {};
  $(document).on('change', "input[type='checkbox']", function () {
    if (this.checked) {
      checkAmenities[$(this).data('id')] = $(this).data('name');
    } else {
      delete checkAmenities[$(this).data('id')];
    }
    let lst = Object.values(checkAmenities);
    if (lst.length > 0) {
      $('div.amenities > h4').text(Object.values(checkAmenities).join(', '));
    } else {
      $('div.amenities > h4').html('&nbsp;');
    }
  });
});

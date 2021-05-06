$(function () {
  const listAmenities = {};

  $('div.amenities li input').change(
    function () {
      if ($(this).is(':checked')) {
        listAmenities[($(this).attr('data-id'))] = $(this).attr('data-name');
      } else {
        delete listAmenities[($(this).attr('data-id'))];
      }
      $('div.amenities h4').html(Object.values(listAmenities).join(', ') || '&nbsp;');
    });
});

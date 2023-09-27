$(document).ready(function () {
    const nameAmenity = [];

    $('input:checkbox').click(function () {
      if ($(this).is(":checked")) {
        nameAmenity.push($(this).attr('data-name'));
      } else {
        const nameIndex = nameAmenity.indexOf($(this).attr('data-name'));
        nameAmenity.splice(nameIndex, 1);
      }
      $('.amenities h4').text(nameAmenity.join(', '));
    });
  });
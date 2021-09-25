$(function() {
    const myAmenities = {};
    const li = [];
    const DId = $(this).attr('data-id');
    const DName = $(this).attr('data-name');
    $('.amenities input[type="checkbox"]').on('click', function() {
        if($(this).prop("checked") == true) {
          myAmenities[DId] = DName;
        } else {
          delete (myAmenities[DId]);
    }
      for (const key in myAmenities) {
      li.push(myAmenities[key]);
    }
      const res = li.join(', ');
    $('div.amenities > h4').text(res);
    li = [];
    });
});

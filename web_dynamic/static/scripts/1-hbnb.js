const $ = window.$;
$(document).ready(function () {
  const myAmenities = {};
  let myList = [];
  const checkbox = $('.amenities input[type="checkbox"]');
  checkbox.prop('checked', false);
  checkbox.change(function () {
    const dataId = $(this).attr('data-id');
    const dataName = $(this).attr('data-name');
    if (this.checked) {
      myAmenities[dataId] = dataName;
    } else {
      delete (myAmenities[dataId]);
    }
    for (const key in myAmenities) {
      myList.push(myAmenities[key]);
    }
    const output = myList.join(', ');
    $('div.amenities > h4').text(output);
    myList = [];
  });
});

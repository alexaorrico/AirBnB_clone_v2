$(document).ready(function () {
  const amenitiesHeading4 = $('div.amenities h4');
  const amenities = $('div.amenities .popover ul input:checkbox');
  const amenitiesDict = {};

  amenities.on('click', function () {
    const dataId = $(this).attr('data-id');

    if ($(this).is(':checked')) {
      const dataName = $(this).attr('data-name');

      amenitiesDict[dataId.toString()] = dataName;
    } else {
      delete amenitiesDict[dataId];
    }

    amenitiesHeading4.text(Object.values(amenitiesDict).join(', '));
  });
});

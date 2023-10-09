// web_dynamic/static/scripts/3-hbnb.js
// Espera a que el documento HTML esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Solicitud AJAX para obtener las ubicaciones
    fetch('http://0.0.0.0:5001/api/v1/places_search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) //empty dirct
    })
    .then(response => response.json())
    .then(data => {
        // Procesa los datos y crea elementos de lugar
        data.forEach(place => {
            const placeArticle = document.createElement('article');
            placeArticle.innerHTML = `
                <div class="title_box">
                    <h2>${place.name}</h2>
                    <div class="price_by_night">$${place.price_by_night}</div>
                </div>
                <div class="information">
                    <div class="max_guest">${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</div>
                    <div class="number_rooms">${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>
                    <div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>
                </div>
                <div class="description">
                    ${place.description}
                </div>`;
            document.querySelector('.places').appendChild(placeArticle);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// web_dynamic/static/scripts/4-hbnb.js
// Load
document.addEventListener('DOMContentLoaded', function () {
    // New event boton "Apply Filter"
    document.getElementById('apply-filter').addEventListener('click', function () {
        // Amenities list
        const selectedAmenities = [];

        // Elements checkbox
        const checkboxes = document.querySelectorAll('input[type="checkbox"][data-id]:checked');
        checkboxes.forEach(checkbox => {
            selectedAmenities.push(checkbox.getAttribute('data-id'));
        });

        //Ajax
        fetch('/4-hbnb/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amenities: selectedAmenities }),
        })
        .then(response => response.text())
        .then(html => {
            // Reemplaza la sección de lugares con la nueva información filtrada
            const placesSection = document.querySelector('.places');
            placesSection.innerHTML = html;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// Allows for filtering using checkboxes
document.addEventListener('DOMContentLoaded', (event) => {
    // Get all checkboxes
    const checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(checkbox => {
        // Set the initial checked state from local storage
        const checkboxValue = checkbox.value;
        const storedValue = localStorage.getItem(checkboxValue);
        if (storedValue !== null) {
            checkbox.checked = true;
        }
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                // Store the value in local storage
                localStorage.setItem(checkboxValue, 'true');
            } else {
                // Remove the value from local storage when unchecked
                localStorage.removeItem(checkboxValue);
            }
            // Delay form submission to ensure local storage is updated
            setTimeout(() => {
                document.getElementById('regionForm').submit();
            }, 0);
        });
    });
});


// Maps API (NOTE THIS IS MOSTLY TAKEN FROM LEAFLET'S API WEBSITE TUTORIAL)
document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([43.726, -72.586], 7);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Load GeoJSON data from the static folder and add markers
    fetch('/static/skiing_areas.geojson')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                filter: function (feature) {
                    // Filter out the mountains with no name or no runs
                    return (
                        feature.properties.name !== undefined &&
                        feature.properties.name !== null &&
                        feature.properties.name.trim() !== '' &&
                        feature.properties.statistics.runs.byActivity &&
                        Object.keys(feature.properties.statistics.runs.byActivity).length > 0
                    );
                },
                onEachFeature: function (feature, layer) {
                    // Bind a popup to the layer
                    var popupContent = feature.properties.name;
                    layer.bindPopup(popupContent);

                    // Check if the layer is polygon or point
                    if (layer instanceof L.Polygon) {
                        var center = layer.getBounds().getCenter();
                        L.marker(center).addTo(map).bindPopup(popupContent);
                    }
                }
            }).addTo(map);
        });
});

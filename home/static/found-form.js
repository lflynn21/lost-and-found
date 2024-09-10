var map;
var marker;
var rotundaPos = { lat: 38.033554, lng: -78.507980 }
var latitude = document.getElementById('latitude')
var longitude = document.getElementById('longitude')


function initMap() {
    var mapOptions = {
        zoom: 17,
        center: rotundaPos, // Replace with your default map center
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng)
    });

    placeMarker(rotundaPos)

}

    // Function to place a marker at the clicked location
function placeMarker(location) {
    const priceTag = document.createElement("div");
    priceTag.class = "price-tag";
    priceTag.textContent = "$2.5M";
    var newMarker = new google.maps.Marker({
        position: location,
        map: map,
        content: priceTag,
    });

    latitude.value = newMarker.getPosition().lat()
    longitude.value = newMarker.getPosition().lng()

    if (marker) {
        marker.setMap(null)
    }

    marker = newMarker

}

google.maps.event.addDomListener(window, 'load', initMap);
function setMarker(positionSet, map, markers) {
    var myMarker = new google.maps.Marker({
        position: positionSet,
        map: map,
    });

    // Remove the previous markers
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.push(myMarker);
}

function getPosition(latitude, longitude) {
    var map;
    var markers = [];

    var positionSet = new google.maps.LatLng(latitude, longitude);
    var mapOptions = {
        center   : positionSet, // Where the center of the card is
        zoom     : 15, // Level of zoom
        draggable : false,
        disableDoubleClickZoom : true,
        streetViewControl : false,
        zoomControl : false,
        mapTypeControl : false,
        mapTypeId: google.maps.MapTypeId.ROADMAP // Type of map
        /**
         * Types of maps :
            * ROADMAP (normal, default 2D map)
            * SATELLITE (photographic map)
            * HYBRID (photographic map + roads and city names)
            * TERRAIN (map with mountains, rivers, etc.)
         */
    };

    map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);
    setMarker(positionSet, map, markers);
}


function showLocation(position) {
    getPosition(position.coords.latitude, position.coords.longitude);
}

function errorHandler(error) {
    console.log("Geolocation error : code " + error.code +
                " - " + error.message);
    getPosition(49.175180, -0.339846);
}

/**
 * Initialize the map in the form
 */
function initialize() {
    if(navigator.geolocation) {
        /**
         * showLocation: get the position of the user
         * errorHandler: if we couldn't get the position, we manage the error
         * Object:
            * enableHighAccuracy: If the navigator could, we get the exact position of the user
            * maximumAge        : Used to return a position that would have been kept in hiding
            * timeout           : Maximum time to wait to get the position.
         */
        navigator.geolocation.getCurrentPosition(showLocation, errorHandler,
            {enableHighAccuracy:true, maximumAge:60000, timeout:27000});
    }
    else {
        alert("Error");
    }
}

google.maps.event.addDomListener(window, 'load', initialize);
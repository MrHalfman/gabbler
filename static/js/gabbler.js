/* ----------------------------------------------------------------- */
/* ------------------------ GEOLOCALISATION ------------------------ */
/* ----------------------------------------------------------------- */

/**
 * Traforms coords into a real address and save it in the form
 * @param  positionSet  The latitude and the longitude of a point
 */
function saveAddress(positionSet) {

    // Get the city form the latitude and the longitude
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({'latLng': positionSet}, function(results, status) {
        if(status == google.maps.GeocoderStatus.OK) {
            if(results[0]) {
                var results = results[0].address_components;

                for(var i = 0; i < results.length; i ++) {
                    if(results[i].types.indexOf("locality") >= 0) {
                        var city = results[i].long_name;
                        var latitude = positionSet.lat();
                        var longitude = positionSet.lng();
                        var zoom = 10;
                    }
                }
            }
        }
    });
}

function setMarker(positionSet, map, markers) {
    var myMarker = new google.maps.Marker({
        position: positionSet,
        map: map
    });

    // Remove the previous markers
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.push(myMarker);
}

function getPosition(latitude, longitude) {
    var map;
    // var markers = [];

    var positionSet = new google.maps.LatLng(latitude, longitude);
    var mapOptions = {
        center   : positionSet, // Where the center of the card is
        zoom : 10,
        scrollwheel: false,
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
    // setMarker(positionSet, map, markers);
    saveAddress(positionSet);
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

/* ----------------------------------------------------------------- */
/* ----------------------------------------------------------------- */

// Redirect the user when he want to update his profile
function updateRedirection(){
    document.location.href = "update";
}

function confirmDeletion(gabId){
    event.preventDefault();
    swal({
        title: "Are you sure to delete your gab?",
        text: "You will not be able to recover it!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it forever!",
        cancelButtonText: "No, I miss click!",
        closeOnConfirm: false
    },
    function(isConfirm){
        if (isConfirm) {
            link = "delete-gab/" + gabId + "/";
            console.log(link);
            window.location = link;
        }
    });
}


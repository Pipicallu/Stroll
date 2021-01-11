const menuBtn = document.querySelector('.menu-btn');

let menuOpen = false;

menuBtn.addEventListener('click', () => {
    if (!menuOpen) {
        menuBtn.classList.add('open');
        menuOpen = true;
    } else {
        menuBtn.classList.remove('open');
        menuOpen = false;
    }
});

/* nav bar display */

const navbarLinks = document.getElementsByClassName('NavBar-links')[0]
const navbarWrapper = document.getElementById('nav-link-wrapper')
menuBtn.addEventListener('click', () => {
    navbarLinks.classList.toggle('active');
    navbarWrapper.classList.toggle('active');
    menuBtn.style.borderColor = "#eeedff";
    
    

});

/* walk Modal */

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})


/* map */

let directionsService;


function initMap() {
    // as its only referenced in the call back this is only called once
    directionsService = new google.maps.DirectionsService();
}
// THe function takes the variables and matches the map id by adding a loop index
function renderRoute(start_lat, start_lng, end_lat, end_lng, loop_index) {

    var startPoint = {
        lat: start_lat,
        lng: start_lng
    };

    var endPoint = {
        lat: end_lat,
        lng: end_lng
    };

    var mapOptions = {
        zoom: 13.4,
        center: startPoint,
        styles: [
            { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
            {
                featureType: "administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "poi",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{ color: "#263c3f" }],
            },
            {
                featureType: "poi.park",
                elementType: "labels.text.fill",
                stylers: [{ color: "#6b9a76" }],
            },
            {
                featureType: "road",
                elementType: "geometry",
                stylers: [{ color: "#38414e" }],
            },
            {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{ color: "#212a37" }],
            },
            {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{ color: "#9ca5b3" }],
            },
            {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{ color: "#746855" }],
            },
            {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{ color: "#1f2835" }],
            },
            {
                featureType: "road.highway",
                elementType: "labels.text.fill",
                stylers: [{ color: "#f3d19c" }],
            },
            {
                featureType: "transit",
                elementType: "geometry",
                stylers: [{ color: "#2f3948" }],
            },
            {
                featureType: "transit.station",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "water",
                elementType: "geometry",
                stylers: [{ color: "#17263c" }],
            },
            {
                featureType: "water",
                elementType: "labels.text.fill",
                stylers: [{ color: "#515c6d" }],
            },
            {
                featureType: "water",
                elementType: "labels.text.stroke",
                stylers: [{ color: "#17263c" }],
            },
        ],
    };

    var map = new google.maps.Map(document.getElementById('map' + loop_index), mapOptions);
    var directionsRenderer = new google.maps.DirectionsRenderer({ preserveViewport: true });
    // this is called for every map 
    directionsRenderer.setMap(map);

    var request = {
        origin: startPoint,
        destination: endPoint,
        travelMode: "WALKING"
    };

    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            directionsRenderer.setDirections(result);
        }
    });
}



/* cloudinary configuration parameters */
$.cloudinary.config({ cloud_name: 'tumascloud', secure: true });

/* cloudinary upload function */

$(document).ready(function () {
    $("input.cloudinary-fileupload[type=file]").cloudinary_fileupload();
});

/* autocomplete jquery */
// this is done so that the data can be injected dynamically, with each new city added the search will automatically expand.
   
var locEnv= locations.concat(environments)
$(function () {
    $("#query").autocomplete({
        source: locEnv
    });
});

/* form function */



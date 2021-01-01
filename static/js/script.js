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
menuBtn.addEventListener('click', () => {
    navbarLinks.classList.toggle('active');
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

/* autocomplete jquery */
// this is done so that the data can be injected dynamically, with each new city added the search will automatically expand.
let locations = document.querySelectorAll('[data-locations]')
let environments = document.querySelectorAll('[data-environments]')
$(function(){
    $("#query").autocomplete({
        source: locations, environments
    });
});


/* cloudinary configuration parameters */
$.cloudinary.config({ cloud_name: 'tumascloud', secure: true});

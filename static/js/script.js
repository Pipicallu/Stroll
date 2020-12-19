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
    directionsService = new google.maps.DirectionsService();
}

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
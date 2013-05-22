var leafShadow= {
    url: '/static/img/leaf_shadow.png',
    anchor: new google.maps.Point(12, 15)
};


function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(-34.610323, -58.422203),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);

    function placeMarker(location) {
        var marker = new google.maps.Marker({
            position: location,
            map: map,
            icon: '/static/img/leaf_marker.png',
            shadow: leafShadow
        });
    }

    var i;
    if(plants){
        for (i = 0; i < plants.length; i++) {
            placeMarker(new google.maps.LatLng(plants[i]["lat"], plants[i]["lng"]));
        }
    }
//    var socket = io.connect();
//    socket.on('marker', function (data) {
//        placeMarker(new google.maps.LatLng(data["lat"], data["lng"]));
//        console.log(data);
//    });
}
google.maps.event.addDomListener(window, 'load', initialize);
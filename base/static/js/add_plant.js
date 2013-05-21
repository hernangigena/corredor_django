/**
 * Created with JetBrains WebStorm.
 * User: mlambir
 * Date: 5/13/13
 * Time: 11:43 PM
 * To change this template use File | Settings | File Templates.
 */


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

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(-34.610323, -58.422203),
        map: map,
        draggable:true,
        shadow: leafShadow,
        icon: '/static/img/leaf_marker.png'
    });

    var geocoder = new google.maps.Geocoder();

    function markerChanged(){
        pos = marker.getPosition();
        $("#id_lat").val(pos.lat());
        $("#id_lng").val(pos.lng());
    }

    google.maps.event.addListener(marker, "dragend", function(event) {
        markerChanged();
    });

    $("#search-form").submit(function(){
        var address = $('#address').val();
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                marker.setPosition(results[0].geometry.location);
                markerChanged();
            } else {
            }
        });
        return false;
    });

    markerChanged();
}

google.maps.event.addDomListener(window, 'load', initialize);

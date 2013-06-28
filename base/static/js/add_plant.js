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

    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    var input = (document.getElementById('address'));
    var autocomplete = new google.maps.places.Autocomplete(input);

    autocomplete.bindTo('bounds', map);

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(-34.610323, -58.422203),
        map: map,
        draggable:true,
        shadow: leafShadow,
        icon: '/static/img/leaf_marker.png'
    });

    var infowindow = new google.maps.InfoWindow();

    var geocoder = new google.maps.Geocoder();

    function markerChanged(){
        pos = marker.getPosition();
        $("#id_lat").val(pos.lat());
        $("#id_lng").val(pos.lng());
    }


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

    google.maps.event.addListener(marker, "dragstart", function() {   
        infowindow.close();
    });

    google.maps.event.addListener(marker, "dragend", function(event) {
        markerChanged();
        map.setCenter(marker.getPosition());  
        map.setZoom(17);
        var latlng = new google.maps.LatLng(marker.getPosition().lat(), marker.getPosition().lng());

        geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var address1 = '';
                var address2 = '';
                if (results[0].address_components) {
                    address1 = [
                        (results[0].address_components[1] && results[0].address_components[1].short_name || ''),
                        (results[0].address_components[0] && results[0].address_components[0].short_name || ''),
                    ].join(' ');
                }

                if (results[1]){
                    address2 = results[1].formatted_address
                }


                infowindow.setContent('<div><strong>' + address1 + '</strong><br>' + address2 + '</div>');
                infowindow.open(map, marker);
            }
        } else {
            alert("Geocoder failed due to: " + status);
        }
        });

    });

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        infowindow.close();
        marker.setVisible(false);
        input.className = '';
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            // Inform the user that the place was not found and return.
            input.className = 'notfound';
            return;
        }

        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
        }

        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        var address = '';
        if (place.address_components) {
        address = [
            (place.address_components[0] && place.address_components[0].short_name || ''),
            (place.address_components[1] && place.address_components[1].short_name || ''),
            (place.address_components[2] && place.address_components[2].short_name || '')
        ].join(' ');
        }

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open(map, marker);
    });

    markerChanged();
}

google.maps.event.addDomListener(window, 'load', initialize);

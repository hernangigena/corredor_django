
function initialize() {

    var mapOptions = {
        center: new google.maps.LatLng(-34.610323, -58.422203),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

     map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);

    var i;

    leafShadow= {
        url: '/static/img/leaf_shadow.png',
        anchor: new google.maps.Point(12, 15)
    };

    infowindow = new google.maps.InfoWindow({
        content: "cargando..."
    });

    if(plants){
        for (i = 0; i < plants.length; i++) {
            placeMarker(plants[i])
        }
    }
}

function placeMarker(plant){
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(plant["lat"], plant["lng"]),
            map: map,
            icon: '/static/img/leaf_marker.png',
            shadow: leafShadow,
        });

        var contentString = '<div id="xcontent">'+
                        '<div id="siteNotice">'+
                        '</div>'+
                        '<h1 id="firstHeading" class="firstHeading">' + plant["user_name"] + '</h1>'+
                        '<div id="bodyContent">'+
                        '<p>Parte del corredor desde el ' + plant["date_joined"] + ' (' + plant["days"] + ' días)</p>'+
                        '</div>'+
                        '</div>';


        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(contentString);
            infowindow.open(map,this);
        });
}

google.maps.event.addDomListener(window, 'load', initialize);

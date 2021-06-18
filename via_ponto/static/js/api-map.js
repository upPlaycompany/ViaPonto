let map;
let geocoder;
let marker;
var latlng;


function initMap() {
    latlng = new google.maps.LatLng(-8.76194, -63.90389);

    map = new google.maps.Map(document.getElementById('map'), {
        center: latlng,
        zoom: 8,
        disableDefaultUI: true
    });

    geocoder = new google.maps.Geocoder();

    // Adicionar
    marker = new google.maps.Marker({
        map: map,
        draggable: true
    })

    marker.setPosition(latlng);

    map.addListener('click', function(e) {
        var clickPosition = e.latLng;
        marker.setPosition(clickPosition);
    });

    marker.addListener('click', function() {
        // Remover
        marker.setMap(null);
    })

    map.addListener('dblclick', function(e) {
        clickZoom = e.zoom + 1,
        map.setZoom(clickZoom);
    });

    google.maps.event.addListener(marker, 'drag', function() {
        geocoder.geocode({ 'latLng': marker.getPosition() }, function(results, status) {
            if(status == google.maps.GeocoderStatus.OK) {
                if(results[0]) {
                    document.getElementById('txtEndereco').value = results[0].formatted_address;
                    document.getElementById('txtLatitude').value = marker.getPosition().lat();
                    document.getElementById('txtLongitude').value = marker.getPosition().lng();
                }
            }
        })
    })

    // Circle
    // const circle = new google.maps.Circle({
    //     strokeColor: '#ff0000',
    //     strokeWeight: 2,
    //     strokeOpacity: 1,
    //     fillColor: 'white',
    //     fillOpacity: .4,
    //     center: centerMap,
    //     radius: 1000,
    //     map: map,
    //     editable: true
    // })
}

function pegarEndereco() {
    txtEndereco = document.getElementById('txtEndereco').value;

    if(txtEndereco !== "") {
        geocoder.geocode({
            'address': txtEndereco + ', Brasil', 'region': 'BR'
        }, function(results, status) {
            if(status == google.maps.GeocoderStatus.OK) {
                if(results[0]) {
                    var latitude = results[0].geometry.location.lat();
                    var longitude = results[0].geometry.location.lng();

                    document.getElementById('txtEndereco').value = results[0].formatted_address;
                    document.getElementById('txtLatitude').value = latitude;
                    document.getElementById('txtLongitude').value = longitude;

                    var location = new google.maps.LatLng(latitude, longitude);
                    marker.setPosition(location);
                    map.setCenter(location);
                    map.setZoom(16);
                }
            }
        })
    }
}
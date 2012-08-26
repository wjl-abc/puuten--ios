function initialize_for_dairy(lat, lng, scale){
	var base = new google.maps.LatLng(lat,lng);
	var myOptions = {
			zoom: scale,
			center: base,
			mapTypeId: google.maps.MapTypeId.ROADMAP 
	};
	var map = new google.maps.Map(document.getElementById("new_map_canvas"), myOptions);
	return map;
}

function set_marker_diary( latitude, longitude, lat, lng){
	var base = new google.maps.LatLng(lat, lng);
	
	var infowindow = new google.maps.InfoWindow({
        content: "I am here"
    });
 
    var marker = new google.maps.Marker({
        position: base,
        map: map_for_diary  
    });
    google.maps.event.addListener(map, 'click', function(event){
        if(marker)
        	marker.setMap(null);
        marker = new google.maps.Marker({
            position: event.latLng,
            map: map
        });
        tileStr = "Location:"+"<br />"+event.latLng.lat()+";"+"<br />"+ event.latLng.lng(); 
	    latitude.val(event.latLng.lat());
        longitude.val(event.latLng.lng());
        infowindow.setContent(tileStr);
        infowindow.open(map,marker);
    });	
}
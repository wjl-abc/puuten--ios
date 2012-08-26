function initialize(lat, lng, scale){
	var base = new google.maps.LatLng(lat,lng);
	var myOptions = {
			zoom: scale,
			center: base,
			mapTypeId: google.maps.MapTypeId.ROADMAP 
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	return map;
}

function set_marker(latitude, longitude, lat, lng, map){
	var base = new google.maps.LatLng(lat, lng);
	
	var infowindow = new google.maps.InfoWindow({
        content: "I am here"
    });
    var marker = new google.maps.Marker({
        position: base,
        map: map  
    });
    google.maps.event.addListener(map, 'click', function(event){
        if(marker)
        	marker.setMap(null);
        marker = new google.maps.Marker({
            position: event.latLng,
            map: map
        });
        tileStr = "Location:"+"<br />"+event.latLng.lat()+";"+"<br />"+ event.latLng.lng(); 
        //latitude = event.latLng.lat();
        //longitude = event.latLng.lng();
        latitude.val(event.latLng.lat());
        longitude.val(event.latLng.lng());
        infowindow.setContent(tileStr);
        infowindow.open(map,marker);
    });	
}

function set_your_area(latitude,longitude, lat_northeast, long_northeast, lat_southwest, long_southwest, scale, input_lat, input_lng, input_scale) {
    var map = initialize(input_lat,input_lng,input_scale);      
    google.maps.event.addListener(map, 'dragend', function() {  
        var center = map.getCenter();
        var bounds= map.getBounds();
        var northeast = bounds.getNorthEast();
        var southwest = bounds.getSouthWest();
        latitude.val(center.lat());
        longitude.val(center.lng());
        lat_northeast.val(northeast.lat());
        long_northeast.val(northeast.lng());
        lat_southwest.val(southwest.lat());
        long_southwest.val(southwest.lng());
        });  
    google.maps.event.addListener(map, 'zoom_changed', function() {  
        scale.val(map.getZoom());
        var center = map.getCenter();
        var bounds= map.getBounds();
        var northeast = bounds.getNorthEast();
        var southwest = bounds.getSouthWest(); 
        lat_northeast.val(northeast.lat());
        long_northeast.val(northeast.lng());
        lat_southwest.val(southwest.lat());
        long_southwest.val(southwest.lng()); 
        }); 
  }

function set_area_test(map){
    var area;
    var centers = map.getCenter();
    var bounds = map.getBounds();
    var NE = bounds.getNorthEast();
    var SW = bounds.getSouthWest();
    area = {"Center_lat":center.lat(), "Center_lng":center.lng(),"NE_lat":NE.lat(), "NE_lng":NE.lng(), "SW_lat":SW.lat(), "SW_lng":SW.lng(), "scale":map.getZoom()};
    return area;
}

function get_your_area(map){
    var area;
    var bounds= map.getBounds();
    var NE = bounds.getNorthEast();
    var SW = bounds.getSouthWest();
    area = {"NE_lat":NE.lat(), "NE_lng":NE.lng(), "SW_lat":SW.lat(), "SW_lng":SW.lng(), "scale":map.getZoom()};
    return area;
}

var infowindow;
var marker_array = [];
function add_marker(lat, lng, title,body,author_name, link, author_link) {
    var length;
    length = body.length;
    if(length>40)
	body = body.substring(0,40);
    var contentString = '<h2><a href="'+
	link+
	'">'+
	title+
	'</a></h2>'+
	'<div class="blog-post-tease">'+
	body+"......"+
	'</div><br>'+
	'<p><a href="'+
	author_link+
	'">'+
	author_name+
	'</a></p>';
    var location = new google.maps.LatLng(lat, lng);
    var marker = new google.maps.Marker({
	  position: location,
	  map: map
	});

    marker_array.push(marker);
    google.maps.event.addListener(marker, 'click', function() {
		if(infowindow)
	    	infowindow.close();
		infowindow = new google.maps.InfoWindow({
			content: contentString,
		});
	    infowindow.open(map,marker);
	    });
}

function add_marker_tweet(lat, lng, text, author_name, author_link,  forward_link, num_forward, comment_link, num_comment) {
    var contentString = '<p><a href="'+author_link+'">'+author_name+':</a></p>'+
	'<div class="blog-post-tease">'+text+'</div><br>'+
        '<a href="'+forward_link+'" rel="facebox">Forward('+num_forward+')</a>  '+
        '<a href="'+comment_link+'" rel="facebox">Comment('+num_comment+')</a>';
    var location = new google.maps.LatLng(lat, lng);
    var marker = new google.maps.Marker({
	  position: location,
	  map: map
	});

    marker_array.push(marker);
    google.maps.event.addListener(marker, 'click', function() {
		if(infowindow)
	    	infowindow.close();
		infowindow = new google.maps.InfoWindow({
			content: contentString,
		});
	    infowindow.open(map,marker);
	    });
}

function delete_marker() {
    if (marker_array) {
      for (i in marker_array) {
        marker_array[i].setMap(null);
      }
      marker_array.length = 0;
    }
  }

function show_markers() {
	if(marker_array){
		for(i in marker_array){
			marker_array[i].setMap(map);
		}
	}
}
function show_marker(lat, lng, map) {
    var location = new google.maps.LatLng(lat, lng);
    var marker = new google.maps.Marker({
          position: location,
          map: map
        });
}

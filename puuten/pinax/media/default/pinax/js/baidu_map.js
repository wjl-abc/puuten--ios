function initialize_b(lat, lng, scale){
	var map = new BMap.Map("map_canvas");
	var base = new BMap.Point(lng, lat);
	map.centerAndZoom(base, scale);
	map.addControl(new BMap.NavigationControl());  
	map.addControl(new BMap.ScaleControl());  
	map.addControl(new BMap.OverviewMapControl());  
	map.addControl(new BMap.MapTypeControl()); 
	return map;
}

function set_marker_b( latitude, longitude, lat, lng, map){
	var base = new BMap.Point(lng, lat);
	var opts = {
			width:500,
			height:300,
			title:"hello"
	};
	var marker = new BMap.Marker(base);
	map.addOverlay(marker);
	map.addEventListener("click", function(event){
	    if(marker)
	    	map.removeOverlay(marker);
		marker = new BMap.Marker(event.point);
		latitude.val(event.point.lat);
        longitude.val(event.point.lng);
		map.addOverlay(marker);
	});
	map.addEventListener("dblclick", function(event) {
		map.removeOverlay(marker);
    });
}

function set_your_area_b(latitude,longitude, lat_northeast, long_northeast, lat_southwest, long_southwest, scale, input_lat, input_lng, input_scale) {     
    map.addEventListener("dragend", function(){  
    	var center = map.getCenter();  
    	var bounds = map.getBounds();  
    	latitude.val(center.lat);
        longitude.val(center.lng);
        SW = bounds.getSouthWest();
        NE = bounds.getNorthEast();
        lat_northeast.val(NE.lat);
        long_northeast.val(NE.lng);
        lat_southwest.val(SW.lat);
        long_southwest.val(SW.lng);
    });
    map.addEventListener("zoomend", function(){
    	scale.val(map.getZoom());
    	var center = map.getCenter();  
    	var bounds = map.getBounds();
    	latitude.val(center.lat);
        longitude.val(center.lng);
        SW = bounds.getSouthWest();
        NE = bounds.getNorthEast();
        lat_northeast.val(NE.lat);
        long_northeast.val(NE.lng);
        lat_southwest.val(SW.lat);
        long_southwest.val(SW.lng);
    });
  }


function get_your_area_b(map){
	var area;
	var bounds= map.getBounds();
	var NE = bounds.getNorthEast();
    var SW = bounds.getSouthWest();
	area = {"NE_lat":NE.lat, "NE_lng":NE.lng, "SW_lat":SW.lat, "SW_lng":SW.lng, "scale":map.getZoom()};
	return area;
}

var infowindow_b;
var marker_array_b =  [];

function show_marker_infor_b(lat, lng, info, icon) {
    var location = new BMap.Point(lng, lat);
    var my_icon = new BMap.Icon(icon, new BMap.Size(30,47));
    var marker = new BMap.Marker(location, {icon:my_icon});
    map.addOverlay(marker);
    var opts = {
    	width:500,
    	height:300
    };
    var info_window = new BMap.InfoWindow(info, opts);
    marker.openInfoWindow(info_window, location);
    return marker;
}

function show_marker_infor_test(lat, lng, info, icon) {
    var location = new BMap.Point(lng, lat);
    var my_icon = new BMap.Icon(icon, new BMap.Size(30,47));
    var marker = new BMap.Marker(location, {icon:my_icon});
    map.addOverlay(marker);
    var opts = {
    	width:500,
    	height:300
    };
    var info_window = new BMap.InfoWindow(info, opts);
    marker.addEventListener("click", function(event){
    	alert(3333);
    });
    return marker;
}
function show_marker_infor_test1(lat, lng, icon) {
    var location = new BMap.Point(lng, lat);
    var my_icon = new BMap.Icon(icon, new BMap.Size(30,47));
    var marker = new BMap.Marker(location, {icon:my_icon});
    map.addOverlay(marker);
    marker.addEventListener("click", function(){
            var data_for_fresh = {"lat":marker.point.lat, "lng":marker.point.lng, "click":1, "NE_lat":1 };
        	var args = {type:"POST",
        			    url:"",
        			    data:data_for_fresh,
        			    complete:done_for_click};
        	$.ajax(args);
        	return false;
        });
    return marker;
}

function show_marker_infor_b_cluster(lat, lng, info, array, icon) {
    array.push(show_marker_infor_b(lat, lng, info, icon));
}

function show_marker_infor_test_cluster(lat, lng, info, array, icon) {
    array.push(show_marker_infor_test(lat, lng, info, icon));
}

function delete_marker_b() {
    if (marker_array_b) {
      for (i in marker_array_b) {
        map.removeOverlay(marker_array_b[i]);
      }
      marker_array_b.length = 0;
    }
  }

function show_markers() {
	if(marker_array){
		for(i in marker_array){
			marker_array[i].setMap(map);
		}
	}
}
function show_marker_b(lat, lng, map) {
    var location = new BMap.Point(lng, lat);
    var marker = new BMap.Marker(location);
    map.addOverlay(marker);
}
function new_test(city){
    alert(city);
    alert("111");
}

function get_lat_and_lng(city, keyword, lat, lng){
    var local = new BMap.LocalSearch(city);
    local.search(keyword);
    local.getResults();
    local.setSearchCompleteCallback(function(searchResult){
        var num_pois = searchResult.getNumPois()
    	if(num_pois>0){
    	    var poi = searchResult.getPoi(0);
    	    lat.val(poi.point.lat);
    	    lng.val(poi.point.lng);
    	}
    });
}

function group_get_lat_and_lng(business_id, city, keyword, lat, lng, id_list){
    var temp_lat, temp_lng, temp_id;
    var local = new BMap.LocalSearch(city);
    local.search(keyword);
    local.getResults();
    local.setSearchCompleteCallback(function(searchResult){
    	var num_pois = searchResult.getNumPois()
    	if(num_pois>0){
    	    temp_lat = lat.val();
    	    temp_lng = lng.val();
    	    temp_id  = id_list.val();
         	var poi = searchResult.getPoi(0);
        	lat.val(poi.point.lat+","+temp_lat);
        	lng.val(poi.point.lng+","+temp_lng);
        	id_list.val(business_id+","+temp_id);
    	}
    	else{
    	    temp_lat = lat.val();
    	    temp_lng = lng.val();
    	    temp_id  = id_list.val();
        	lat.val(500.1+","+temp_lat);
        	lng.val(500.1+","+temp_lng);
        	id_list.val(business_id+","+temp_id);
    	}
    });
    
}
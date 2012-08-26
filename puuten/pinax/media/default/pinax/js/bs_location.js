function get_lat_and_lng(city, keyword, lat, lng){
	var local = new BMap.LocalSearch(city);
    local.search(keyword);
    local.getResults()
    local.setSearchCompleteCallback(function(searchResult){
    	var num_pois = searchResult.getNumPois()
    	if(num_pois>0){
         	var poi = searchResult.getPoi(0);
        	lat.val(poi.point.lat);
        	lng.val(poi.point.lng);
    	}
    });
}

function group_get_lat_and_lng(id, city, keyword, lat, lng, id_list){
    var temp_lat;
    var temp_lng£»
    var temp_id;
    temp_id  = id_list.val();
    id_list.val(id+","+temp_lat);
    var local = new BMap.LocalSearch(city);
    local.search(keyword);
    local.getResults()
    local.setSearchCompleteCallback(function(searchResult){
    	var num_pois = searchResult.getNumPois()
    	if(num_pois>0){
         	var poi = searchResult.getPoi(0);
         	temp_lat = lat.val();
         	temp_lng = lng.val();
         	//temp_id  = id_list.val();
        	lat.val(poi.point.lat+","+temp_lat);
        	lng.val(poi.point.lng+","+temp_lng);
        	//id_list.val(poi.point.lat+","+temp_lat);
    	}
    	else{
    	    temp_lat = lat.val();
         	temp_lng = lng.val();
         	//temp_id  = id_list.val();
        	lat.val(500.1+","+temp_lat);
        	lng.val(500.1+","+temp_lng);
        	//id_list.val(500.1+","+temp_lat);
    	}
    });
}
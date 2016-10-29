$(document).ready(function(){


var lat,lon
var address
var travelTime
var kidsID = 1
var kidsName = "Jimmy Neutron"
var destination

function do_something(a,b) {
	alert(a,b)
}

  function getIp() {
    $.getJSON("http://ipinfo.io", function(data) {
    	var a = data.city
    	lat = data.loc.split(',')[0].toString();
        lon = data.loc.split(',')[1].toString();
    	console.log(lat,lon)
    	getTravelTime()
    })
  }


   function getTravelTime() {
   	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" +lat+ "," + lon + "&destinations=" + destination;
   	$.getJSON(url, function(data) {
		travelTime = data.rows[0].elements[0].duration.text
		console.log(travelTime)
		$('.travTime').text('Travel time is ' + travelTime)
   })
   }

/*
   function createCORSRequest(method, url) {
	  var xhr = new XMLHttpRequest();
	  if ("withCredentials" in xhr) {

	    // Check if the XMLHttpRequest object has a "withCredentials" property.
	    // "withCredentials" only exists on XMLHTTPRequest2 objects.
	    xhr.open(method, url, true);

	  } else if (typeof XDomainRequest != "undefined") {

	    // Otherwise, check if XDomainRequest.
	    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
	    xhr = new XDomainRequest();
	    xhr.open(method, url);

	  } else {

	    // Otherwise, CORS is not supported by the browser.
	    xhr = null;

	  }
	  return xhr;
	}


	var xhr = createCORSRequest('GET', url);
	if (!xhr) {
	  throw new Error('CORS not supported');
	}

	xhr.onload = function() {
	 var responseText = xhr.responseText;
	 console.log(responseText);
	 // process the response.
	};

	xhr.onerror = function() {
	  console.log('There was an error!');
	};


*/

$('img').attr('src', "https://api.qrserver.com/v1/create-qr-code/?data="+ kidsID+ "&amp;size=100x100")
$('#name').text(kidsName)


$('.btn-success').on('click', function(){
	destination= document.getElementById('destInput').value
	getIp()
})


})

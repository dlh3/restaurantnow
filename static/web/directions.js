var initialLocation;
var vancouver = new GLatLng(49.275,-122.9);
var browserSupportFlag =  new Boolean();
var infowindow = new google.maps.InfoWindow();
var myOptions = { zoom: 15, mapTypeId: google.maps.MapTypeId.ROADMAP };
var map;


function initialize()
{
    if (GBrowserIsCompatible())
    {
        map = new GMap2(document.getElementById("map_canvas"));
        map.setCenter(vancouver, 13);
        map.setUIToDefault();
    }

    // Try W3C Geolocation method (Preferred)
    if(navigator.geolocation)
    {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position)
        {
            initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            contentString = "Location found using W3C standard";
            map.setCenter(initialLocation);
            infowindow.setContent(contentString);
            infowindow.setPosition(initialLocation);
            infowindow.open(map);
            map.addOverlay(new GMarker(initialLocation));
        }, function()
        {
            handleNoGeolocation(browserSupportFlag);
        });
    }
    else if (google.gears)
    {
        // Try Google Gears Geolocation
        browserSupportFlag = true;
        var geo = google.gears.factory.create('beta.geolocation');
        geo.getCurrentPosition(function(position)
        {
            initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
            contentString = "Location found using Google Gears";
            map.setCenter(initialLocation);
            infowindow.setContent(contentString);
            infowindow.setPosition(initialLocation);
            infowindow.open(map);
            map.addOverlay(new GMarker(initialLocation));
        }, function()
        {
            handleNoGeolocation(browserSupportFlag);
        });
    }
    else
    {
        // Browser doesn't support Geolocation
        browserSupportFlag = false;
        handleNoGeolocation(browserSupportFlag);
    }
}

function handleNoGeolocation(errorFlag)
{
    if (errorFlag == true)
    {
        initialLocation = vancouver;
        contentString = "Error: The Geolocation service failed.";
    }
    else
    {
        initialLocation = vancouver;
        contentString = "Error: Your browser doesn't support geolocation.";
    }
    map.setCenter(initialLocation);
    infowindow.setContent(contentString);
    infowindow.setPosition(initialLocation);
    infowindow.open(map);
}

$(function()
{
    initialize();
});
$(window).unload(function()
{
    GUnload();
});

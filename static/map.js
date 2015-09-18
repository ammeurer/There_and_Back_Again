
// Mapbox access token
L.mapbox.accessToken = 'pk.eyJ1IjoiYW1tZXVyZXIiLCJhIjoiMjg1M2JlM2QwMmE2NjIzZjJmODRjYWM1NDRjODg5YWEifQ.SZQ4FO0OqKTTE4tiv4Au4A';

// Define bounding box of San Francisco
var southWest = L.latLng(37.697965, -122.528500),
    northEast = L.latLng(37.822694, -122.355458),
    bounds = L.latLngBounds(southWest, northEast);
// Initialize Map
var map = L.mapbox.map('map', 'ammeurer.5d704af1', {
    zoomControl: false,
    maxBounds: bounds 
 }).setView([37.78, -122.416], 13);

// Move the attribution control out of the way
map.attributionControl.setPosition('bottomleft');

// Object that decodes all the turn codes returned by request
// to OSRM in the instructions
var turnCode = 
{
    0: "Continue straight on ",
    1: "Continue straight on ",
    2: "Turn slightly right onto ",
    3: "Turn right onto ",
    4: "Turn sharply right onto ",
    5: "Take a U turn at",
    6: "Turn sharply left onto ",
    7: "Turn left onto ",
    8: "Turn slightly left onto ",
    9: "ReachViaLocation",
    10: "Head staight on ",
    11: "Enter the Round About",
    12: "Leave the Round About",
    13: "Stay On Round About",
    14: "StartAtEndOfStreet",
    15: "You have arrived at your destination!",
    16: "EnterAgainstAllowedDirection",
    17: "LeaveAgainstAllowedDirection",
    127: "InverseAccessRestrictionFlag",
    128: "AccessRestrictionFlag",
    129: "AccessRestrictionPenalty"
};

// Show modals when buttons are clicked
$('#signup').click(function(){
  $('#signupModal').modal('show');
});

$('#login').click(function(){
  $('#loginModal').modal('show');
});

// When 'Find a Path' is clicked, fit map view to the routes
// returned.
var zoomBounds = function(maxLat, minLat, maxLon, minLon){
	var sw = L.latLng(minLat, minLon);
	var ne = L.latLng(maxLat, maxLon);
	var newBounds = L.latLngBounds(sw, ne);
	map.fitBounds(newBounds);
};

// Initialize polyline variables
var pl = null;  
var pl_mb = null;

var maxLon, maxLat, minLon, minLat;
var polyline_ll_array = null;
var polyline_ll_array_mb = null;
  $('#submit-route').click(function() {

    if(pl !== null){
      map.removeLayer(pl);
      $('#directions').slideUp(200);
      $('#instructions li').remove();
    } 
    $.get(
      "/get-route",
      $("#route-form").serialize(),
      function (result) {
        var parsedOSRM = JSON.parse(result);
        console.log(parsedOSRM);
        polyline_ll_array = polyline.decode(parsedOSRM.route_geometry, 6);
        console.log(polyline_ll_array);
        var polyline_options = {
          color: '#D6AD33',
          opacity: 0.9
        };
        pl = L.polyline(polyline_ll_array, polyline_options);
        pl.addTo(map);
        maxLon, maxLat, minLon, minLat;
        var via_pts = parsedOSRM.via_points;
        if(via_pts[0][0] >= via_pts[1][0]){
          maxLat = via_pts[0][0];
          minLat = via_pts[1][0];
        }else{
          maxLat = via_pts[1][0];
          minLat = via_pts[0][0];
        }
        if(via_pts[0][1] >= via_pts[1][1]){
          maxLon = via_pts[0][1];
          minLon = via_pts[1][1];
        }else{
          maxLon = via_pts[1][1];
          minLon = via_pts[0][1];
        }
        zoomBounds(maxLat, minLat, maxLon, minLon);
        var instructions = parsedOSRM.route_instructions
        // var route_name = "<h4>" + parsedOSRM.route_name[0] + "</h4>";
        // $('#instructions').append(route_name);
        for(var i = 0; i < instructions.length; i++){
          var instruct = "<li>"  + turnCode[instructions[i][0]] + " " + instructions[i][1]+"</li>";
          $('#instructions ul').append(instruct);
        }
        
        $('#directions').slideDown(300);


       });

  });

  var countDensity = function(){
      // var datasets_value = [];

      $.get(
          '/get-leg-counts',
          JSON.stringify(polyline_ll_array),
          function(density_list){
            id = '.modal-body #safeRoute';
            densities = JSON.parse(density_list);
            // datasets_value.push(densities);
            // console.log(datasets_value);
            // console.log(densities);
            var sum= 0;
            for(var i = 0; i<densities.length; i++){
              sum += densities[i];
            }
            var avg = sum / densities.length;
            console.log(avg);
            createChart(densities, id);
            $('#chartModal').modal('show');

          });
  
      

  };
$('#submit-route').click(function() {
    console.log("got into click");
    if(pl_mb !== null){
      map.removeLayer(pl_mb);
      //$('#directions').slideUp(200);
      //$('#instructions li').remove();
    } 
    $.get(
      "/get-mb-route",
      $("#route-form").serialize(),
      function (result) {
        console.log(result);
        var parsedMB = JSON.parse(result);
        console.log(parsedMB);
        console.log(parsedMB.routes[0].geometry);
        console.log(parsedMB.routes);
        polyline_ll_array_mb = polyline.decode(parsedMB.routes[0].geometry, 6);
        console.log(polyline_ll_array_mb);
        var polyline_options = {
          color: 'red',
          opacity: 0.3
        };
        pl_mb = L.polyline(polyline_ll_array_mb, polyline_options);
        pl_mb.addTo(map);

        //var instructions = parsedOSRM.route_instructions
        // for(var i = 0; i < instructions.length; i++){
        //   var instruct = "<li>"  + instructions[i][1] + " " + "" + instructions[i][6] +"</li>";
        //   $('#instructions ul').append(instruct);
        // }
        //var route_name = "<h4>" + parsedOSRM.route_name[0] + "</h4>";
        //$('#routes').add(route_name);
        //$('#directions').slideDown(300);

      });

  });
var createChart = function(datasets_value, id){
  $('#chartModal').on('shown.bs.modal', function (event) {

    // var button = $(event.relatedTarget);
    var modal = $(this);
    var canvas = modal.find(id);
    var ctx = canvas[0].getContext("2d");

  // var ctx = $("#myChart").get(0).getContext("2d");
    console.log(datasets_value);
    // console.log(datasets_value[0]);
    // console.log(datasets_value[0].length);
    // console.log(datasets_value[1].length);
    label_list = [];
    for(var i=0; i < datasets_value.length; i++){
      label_list.push(' ');
    }

     var data = {
            labels: label_list,
            datasets: [
              {
                label: "Safe Route",
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: datasets_value
              }
      

            ]
            };
   
            var myLineChart = new Chart(ctx).Line(data);
            });

};


  $('#compare-btn').click(function(){
    countDensity();
  

  });
  
  // $('#origin').on('change', function(){
  //   $('#directions').slideUp(300);
  //   $('#instructions li').remove();
  //   map.removeLayer(pl);
  // });
  // $('#destination').on('change', function(){
  //   $('#directions').slideUp(300);
  //   $('#steps li').remove();
  //   map.removeLayer(pl);

  // });
  var heat = L.heatLayer([], {    //define heat layer options
        maxOpacity: 0.4, 
        minOpacity: 0.1,
        radius: 8,
        blur: 15, 
        maxZoom: 16,
      
    });

  var toggle_heat = false;
  $("#add-heat_btn").click(function(){
    if (toggle_heat == false){
      // Add all my points to the heat map
      $.get('/get-crime-ll',
        JSON.stringify([maxLat, minLat, maxLon, minLon]),
        function(ll){
          var llList = JSON.parse(ll);
          for (var i = 0; i < llList.length; i++){
            heat.addLatLng(llList[i]);
            console.log(llList[i]);
          }
          heat.addTo(map);

        });
        

          $('#add-heat_btn').text("Hide Heat Map");
          toggle_heat = true;
      }
      else{
        map.removeLayer(heat);
        $('#add-heat_btn').text("Generate Heat Map");
        toggle_heat = false
      }

    });

  
  var defaultBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(37.697965, -122.528500),
    new google.maps.LatLng(37.822694, -122.355458));

  var origin = document.getElementById('origin');
  var destination = document.getElementById('destination');
  var options = {
    bounds: defaultBounds,
    types: ['address'] 
  };

  var autocomplete_origin = new google.maps.places.Autocomplete(origin, options);
  var autocomplete_dest = new google.maps.places.Autocomplete(destination, options);
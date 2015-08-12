<script>
L.mapbox.accessToken = 'pk.eyJ1IjoiYW1tZXVyZXIiLCJhIjoiMjg1M2JlM2QwMmE2NjIzZjJmODRjYWM1NDRjODg5YWEifQ.SZQ4FO0OqKTTE4tiv4Au4A';
var map = L.mapbox.map('map', 'ammeurer.5d704af1', {
    zoomControl: true
}).setView([37.78, -122.416], 13);

// move the attribution control out of the way
map.attributionControl.setPosition('bottomleft');

// create the initial directions object, from which the layer
// and inputs will pull data.
var directions = L.mapbox.directions({
    profile: 'mapbox.walking'
});
console.log(directions);
var directionsLayer = L.mapbox.directions.layer(directions)
    .addTo(map);

var directionsInputControl = L.mapbox.directions.inputControl('inputs', directions)
    .addTo(map);

var directionsErrorsControl = L.mapbox.directions.errorsControl('errors', directions)
    .addTo(map);

var directionsRoutesControl = L.mapbox.directions.routesControl('routes', directions)
    .addTo(map);

var directionsInstructionsControl = L.mapbox.directions.instructionsControl('instructions', directions)
    .addTo(map);
</script>
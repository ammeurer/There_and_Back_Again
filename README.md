# There and Back Again
With its Lord of the Rings inspired UI, There and Back Again delivers walking routes to pedestrians in SF that avoid high crime areas. The app uses a branch of OSRM as its routing engine, which returns the optimum route based on a custom routing profile. This profile weights graph edges using a rasterized crime data set. Users can also view a heat map of crime near their route, as well as a chart that illustrates how the crime density of the route varies throughout the route.
![There and Back Again Homepage](/static/thereandbackagain.png)

There and Back Again is a web app created by Amanda Meurer. Amanda is passionate about using big data to influence everyday decisions. She set out to create the ultimate pedestrian routing app. This repository is the result of several weeks' work, and weights routes based on crime densities in San Francisco. In the future Amanda hopes to pull in more datasets (elevation, lighting, construction, coffee shop locations, etc) to craft the optimum walking experience for any user. She would also like to make a mobile app version.




## Table of Contents
* [Technologies Used](#technologiesused)
* [How to locally run There and Back Again](#run)
* [How to use There and Back Again](#use)
* [Version 2.0](#v2)

## <a name="technologiesused"></a>Technologies Used

* Python
* C++
* LUA
* OSRM (Open Source Routing Machine)
* Flask
* numpy
* PostgresSQL/PostGIS
* GeoAlchemy/SQLAlchemy
* Javascript/jQuery
* AJAX/JSON
* Jinja2
* Chart.js
* polyline.js
* Bootstrap
* MapBox API
* Google Maps API

(dependencies are listed in requirements.txt)

## <a name="run"></a>How to locally run There and Back Again
###Run your own instance of OSRM
Use this branch of OSRM: https://github.com/ammeurer/osrm-backend/tree/osrm_there_and_back_again

 * Set up your C++ dependencies
 	* `source ./bootstrap.sh`
 * Compile your source
    * `source ./build_osrm.sh`
 * Run OSRM
   * "Running OSRM" is here https://github.com/Project-OSRM/osrm-backend/wiki/Running-OSRM 
   However, this is exactly what you need to do for There and Back Again:
  	* `osrm-extract san-francisco_california.osm.pbf -p profiles/foot_crime.lua` (the `*.osm.pbf` file is downloaded from [here](https://mapzen.com/data/metro-extracts))
  	* `osrm-prepare myextract.osrm -p profiles/foot_crime.lua`
  	* `osrm-routed myextract.osrm` -- this command is what will actually start your server, as long as the last two steps were successful; you can now go to `localhost:5000/viaroute?…` as described [here](https://github.com/Project-OSRM/osrm-backend/wiki/Server-api#service-viaroute)


## <a name="use"></a>How to use There and Back Again

####Enter starting point and destination, then click 'Find a Path'



## <a name="v2"></a>Version 2.0


## <a name="author"></a>Author
Amanda Meurer is a software engineer in San Francisco, CA.

# There and Back Again
With its Lord of the Rings inspired UI, There and Back Again delivers walking routes to pedestrians in SF that avoid high crime areas. The app uses a branch of OSRM as its routing engine, which returns the optimum route based on a custom routing profile. This profile weights graph edges using a rasterized crime data set. Users can also view a heat map of crime near their route, as well as a chart that illustrates how the crime density of the route varies throughout the route.
![There and Back Again Homepage](/static/thereandbackagain.png)

There and Back Again is a web app created by Amanda Meurer. Amanda is passionate about using big data to influence everyday decisions. She set out to create the ultimate pedestrian routing app. This repository is the result of several weeks' work, and weights routes based on crime densities in San Francisco. In the future Amanda hopes to pull in more datasets (elevation, lighting, construction, coffee shop locations, etc) to craft the optimum walking experience for any user. She would also like to make a mobile app version.




## Table of Contents
* [Technologies Used](#technologiesused)
* [How to locally run There and Back Again](#run)
* [How to use There and Back Again](#use)

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

There and Back Again has not yet been deployed, so here is how to run the app locally on your machine.

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
  	* `osrm-prepare san-francisco_california.osrm -p profiles/foot_crime.lua`
  	* `osrm-routed san-francisco_california.osrm` -- this command is what will actually start your server, as long as the last two steps were successful; you can now go to `localhost:5000/viaroute?…` as described [here](https://github.com/Project-OSRM/osrm-backend/wiki/Server-api#service-viaroute)

### Run the There and Back Again Flask App

  * Set up and activate a python virtualenv, and install all dependencies:
    * `pip install -r requirements.txt`
  * Make sure you have PostgreSQL running. Create a new database in psql named lotr:
	* `psql`
  	* `CREATE DATABASE lotr;`
  * Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
    * Seed the crimes table with crime latitudes and longitudes: `CrimePoints.seed_points()`
  * Now, quit interactive mode. Start up the flask server:
    * `python server.py`
  * Go to localhost:9000 to see the web app


## <a name="use"></a>How to use There and Back Again

###Enter starting point and destination, then click `Find a Path`
Two routes will appear on the map. The red route is the regular walking route returned by the MapBox Directions API. The golden route is the custom route returned from OSRM that routes the pedestrian around paths with high crime density.

The walking directions will also slide down at this time. 

![There and Back Again Route and Directions](/static/routed.png)

###Press the `Generate Heat Map` button
This button will query the database for all the crime occurrences in the bounding box of the current route. It will display these points as a heat map overlaying the map. Press 'Hide Heat Map' to make the heat map go away.

![There and Back Again Heat Map](/static/heatmap.png)

###Press the `View Crime Density Graph` button
This button will query the database for all points within 5 meters of the safe route, and represent that data as a graph to the user. This graph shows the user how the crime density changes throughout the course of their journey.

![There and Back Again Graph](/static/graph.png)

## <a name="author"></a>Author
Amanda Meurer is a software engineer in San Francisco, CA.

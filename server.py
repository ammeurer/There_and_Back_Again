"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, jsonify, redirect, request, flash, session, json
from flask_debugtoolbar import DebugToolbarExtension
import requests
import geojson
import ast

from model import User, Contact, Route, CrimePoints, connect_to_db, db
from random import choice

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Mapbox Access Token
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYW1tZXVyZXIiLCJhIjoiMjg1M2JlM2QwMmE2NjIzZjJmODRjYWM1NDRjODg5YWEifQ.SZQ4FO0OqKTTE4tiv4Au4A'

@app.route('/')
def index():
    """Homepage."""
    quote = pick_quote()
    if session.get('logged_in_user') is None:
    	print "***************", "No logged in user"
    	user = None
    else:
    	print "****************", "there is a user logged in", session.get('logged_in_user')
    	user = User.get_user_by_id(session.get('logged_in_user'))
    return render_template("lotr_map.html", quote=quote, user=user)

def pick_quote():
	quote_list = [
		"'All we have to decide is what to do with the time that is given to us.' -Gandalf the Grey",
		"'If more of us valued food and cheer and song above hoarded gold, it would be a merrier world.'  -Thorin Oakenshield",
		"'But in the end it's only a passing thing, this shadow; even darkness must pass.' -Samwise Gamgee",
		"'Not all those who wander are lost.' -J.R.R. Tolkien",
		"'It's a dangerous business, Frodo, going out your door. You step onto the road, and if you don't keep your feet, there's no knowing where you might be swept off to.' -Bilbo Baggins",
		"'But no living man am I! You look upon a woman.' -Eowyn",
		"'It is not the strength of the body, but the strength of the spirit.' -J.R.R. Tolkien",
		"'Deeds will not be less valiant because they are unpraised.' -Aragorn",
		"'Even the smallest person can change the course of history.' -Lady Galadriel"
	]
	quote = choice(quote_list)
	return quote

@app.route('/signup', methods=['POST'])
def sign_up():
	user_name = request.form.get('name')
	user_email = request.form.get('email')
	user_password = request.form.get('password')

	new_user = User.create_new_user(user_name, user_email, user_password)
	session['logged_in_user'] = new_user.user_id
	return redirect('/')


@app.route("/login", methods=["POST"])
def process_login():
	"""Log user into siteself.
	Find the user's login credentials located in the 'request.form'
	dictionary, look up the user, and store them in the session.
	"""
	email_input = request.form.get("email")
	pword_input = request.form.get("password")

	user = User.get_user(email_input)
	print "******************", user
	if user is None:
		flash("Your email is not in our system. Please sign up!")
	else:
		if pword_input != user.password:
			# flash("Incorrect password, try again")
			return redirect("/")
		else:
			# flash("Login successful!!")
			session['logged_in_user'] = user.user_id
			return redirect("/")

@app.route('/logout')
def process_logout():
	del session['logged_in_user']
	return redirect("/")

@app.route('/get-route')
def get_data():
	origin = request.args.get('start').replace(' ', '+')
	dest = request.args.get('dest').replace(' ', '+')

	origin_lat, origin_lon = process_geojson(origin)
	dest_lat, dest_lon = process_geojson(dest)
	resp = requests.get('http://127.0.0.1:5000/viaroute?loc=' + str(origin_lat) + ',' + str(origin_lon) +'&loc=' + str(dest_lat) + ',' 
		+ str(dest_lon) + '&instructions=true').content
	
	return resp


@app.route('/get-leg-counts')
def get_leg_counts():
	print "*********** Got into get-leg-counts"
	ll_list = ast.literal_eval(request.args.keys()[0])

	print "************ ", ll_list
	density_list = []
	for ll in range(1, len(ll_list)):

		start = ll_list[ll-1]
		# print "*********** Start[0]", start[0]
		# start = ast.literal_eval(start)
		print "**********", start
		end = ll_list[ll]
		# end = ast.literal_eval(end)
		print "*************", end
		leg_ct = CrimePoints.count_crimes_on_leg(str(start[0]), str(start[1]), str(end[0]), str(end[1]))
		density_list.append(leg_ct)
	print "************* Density list", density_list
	return json.dumps(density_list)


@app.route('/get-mb-route')
def get_mb_data():
	print "************", "Got into /get-mb-route"
	origin = request.args.get('start').replace(' ', '+')
	dest = request.args.get('dest').replace(' ', '+')

	origin_lat, origin_lon = process_geojson(origin)
	dest_lat, dest_lon = process_geojson(dest)
	# resp = requests.get('https://api.mapbox.com/v4/directions/mapbox.walking/' 
	# 	+ str(origin_lon) +','+ str(origin_lat) + ';' + str(dest_lon) + ','+ str(dest_lat) +'.json?' + 'geometry=polyline' 
	# 	+ '?' +'access_token=' + MAPBOX_ACCESS_TOKEN)
	resp = requests.get('https://api.mapbox.com/v4/directions/mapbox.walking/' 
	 	+ str(origin_lon) +','+ str(origin_lat) + ';' + str(dest_lon) + ','+ str(dest_lat)
	 	 +'.json?geometry=polyline&alternatives=false&access_token=' + MAPBOX_ACCESS_TOKEN).content

	return resp


@app.route('/get-crime-ll')
def get_ll():
	ll_list = ast.literal_eval(request.args.keys()[0])
	print "**************** Heat ll list: ", ll_list
	ll_pts = CrimePoints.get_heat_pts(ll_list[0], ll_list[1], ll_list[2], ll_list[3])
	# crime_ll_list = []
	# fh = open('crime_ll')
	# for line in fh:
	# 	lat, lon = line.split()
	# 	crime_ll_list.append((float(lat),float(lon)))
	return json.dumps(ll_pts)

def process_geojson(location):
	# print "************", "got into process_geojson"
	decode_loc = requests.get('https://api.mapbox.com/v4/geocode/mapbox.places/'+ location + '.json?access_token=' + MAPBOX_ACCESS_TOKEN).content
	# Returns a FeatureCollection geojson object of all possible geocoding results for the address
	# print "***************", decode_loc

	features = geojson.loads(decode_loc)['features']
	# Find the GeoJson feature that is located in San Francisco
	for feature in features:
		# print "**************", feature
		if 'San Francisco,' in feature['place_name']:
			lon, lat = feature['center']
			# print "****************", lat, lon
			return (lat, lon)
	# TODO: Return something to indicate that the forward geocoding failed
	# print "****************", lat, lon
	# return (0, 0)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host='localhost', port=9000)

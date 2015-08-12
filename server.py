"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Contact, Route, connect_to_db, db
from random import choice

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


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
    return render_template("map_walking_sample.html", quote=quote, user=user)

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
	# return render_template('user_profile.html', email=new_user.email, name=new_user.user_name)

# @app.route('/users')
# def user_list():
# 	""" Show list of users """
#
# 	users = User.query.all()
# 	return render_template("user_list.html", users=users)
#
# @app.route('/movies')
# def movie_list():
# 	""" Show list of movies """
#
# 	movies = Movie.query.order_by(Movie.title).all()
# 	return render_template("movie_list.html", movies=movies)
# @app.route('/login')
# def show_login():
# 	"""Show login form."""
# 	return render_template("login.html")
#
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
	# flash("You have been logged out")
	return redirect("/")
#
# @app.route('/users/<int:user_id>')
# def display_user_details(user_id):
# 	display_user = User.query.get(user_id)
# 	rating_list = Rating.get_user_ratings(user_id)
#
#
# 	# print "*******************" , movie_list
# 	# for rating in rating_list:
# 	# 	print rating.movie.title
# 	return render_template("user_details.html", display_user=display_user, rating_list=rating_list)
#
#
# @app.route('/movies/<int:movie_id>')
# def display_movie_details(movie_id):
# 	display_movie = Movie.query.get(movie_id)
# 	rating_list = Rating.get_movie_ratings(movie_id)
#
# 	user_id = session.get('logged_in_user')
#
# 	if user_id:
# 		rating = Rating.get_rating(movie_id, user_id)
# 	else:
# 		rating = None
#
# 	# rating = Rating.get_rating(movie_id, user_id)
# 	rating_scores = [r.score for r in rating_list]
# 	avg_score = float(sum(rating_scores)) / len(rating_scores)
#
# 	prediction = None
# 	# print "******************** Score for current user on current movie", rating.score
# 	if (not rating) and user_id:
# 		user = User.query.get(user_id)
# 		if user:
# 			print "******************** current movie", display_movie
# 			prediction = user.predict_rating(display_movie)
#
#
# 	if prediction:
# 		# User hasn't scored; use our prediction if we made one
# 		effective_rating = prediction
#
# 	elif rating:
# 	    # User has already scored for real; use that
# 	    effective_rating = rating.score
#
# 	else:
# 	    # User hasn't scored, and we couldn't get a prediction
# 	    effective_rating = None
#
# 	# Get the eye's rating, either by predicting or using real rating
#
# 	the_eye = User.query.filter_by(email="the-eye@of-judgment.com").one()
# 	eye_rating = Rating.query.filter_by(
# 	    user_id=the_eye.user_id, movie_id=display_movie.movie_id).first()
#
# 	if eye_rating is None:
# 	    eye_rating = the_eye.predict_rating(display_movie)
#
# 	else:
# 	    eye_rating = eye_rating.score
#
# 	if eye_rating and effective_rating:
# 	    difference = abs(eye_rating - effective_rating)
#
# 	else:
# 	    # We couldn't get an eye rating, so we'll skip difference
# 	    difference = None
#
#
# 	BERATEMENT_MESSAGES = [
# 	    "I suppose you don't have such bad taste after all.",
# 	    "I regret every decision that I've ever made that has brought me" +
# 	        " to listen to your opinion.",
# 	    "Words fail me, as your taste in movies has clearly failed you.",
# 	    "That movie is great. For a clown to watch. Idiot.",
# 	    "Words cannot express the awfulness of your taste."
# 	]
#
# 	if difference is not None:
# 	    beratement = BERATEMENT_MESSAGES[int(difference)]
#
# 	else:
# 	    beratement = None
#
# 	print "************************ beratement", beratement
# 	return render_template("movie_details.html", display_movie=display_movie, rating_list=rating_list, user_rating=rating, average=avg_score, prediction=prediction, beratement=beratement)
#
#
# @app.route('/rate_movie/<int:movie_id>')
# def rate_movie(movie_id):
# 	if session.get('logged_in_user') is None:
# 		flash("You must be logged in to rate a movie. Log in now!")
# 		return redirect('/login')
# 	else:
# 		user_id = session['logged_in_user']
# 		rating = request.args.get('rating')
# 		rating_row = Rating.get_rating(movie_id, user_id)
# 		if rating_row is None:
# 			Rating.create_new_rating(movie_id, user_id, rating)
# 		else:
# 			rating_row.update_rating(rating)
# 		flash("Your rating has been successfully received!")
# 		return redirect('/movies/%s' % movie_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run()

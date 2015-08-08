"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import sqlite3

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions


# User class
class User(db.Model):
    """ User of routing website """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(64), nullable=True)


    @classmethod
    def create_new_user(cls, name, email, password):
        new_user = cls(email=email, password=password, user_name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s password=%s user_name=%s>" % (self.user_id,
            self.email, self.password, self.user_name)

# Routes class
class Route(db.Model):
    """ Routes of Users in routing website """

    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    route_name = db.Column(db.String(32), nullable=True)
    src_lat = db.Column(db.Float, nullable=False)
    src_lon = db.Column(db.Float, nullable=False)
    dest_lat = db.Column(db.Float, nullable=False)
    dest_lon = db.Column(db.Float, nullable=False)
    safety_rating = db.Column(db.Integer, nullable=True)


    user = db.relationship("User",
                            backref=db.backref("routes", order_by=route_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Route route_id=%s user_id=%s route_name=%s src=(%s, %s) \
        dest=(%s, %s) safety_rating=%s>" % (self.route_id, self.user_id,
        self.route_name, self.src_lat, self.src_lon, self.dest_lat,
        self.dest_lon, self.safety_rating)

# Emergency Contacts class
class Contact(db.Model):
    """ Contacts of users of routing website """

    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    contact_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("contacts", order_by=contact_id))


    # def update_rating(self, new_rating):
    #     self.score = new_rating
    #     db.session.commit()
    #
    # @classmethod
    # def create_new_rating(cls, movie_id, user_id, score):
    #     new_rating_row = cls(movie_id=movie_id, user_id=user_id, score=score)
    #     db.session.add(new_rating_row)
    #     db.session.commit()
    #     return new_rating_row
    #
    # @classmethod
    # def get_rating(cls, movie_id, user_id):
    #     rating = db.session.query(cls).filter(cls.movie_id == movie_id,
    #                                             cls.user_id == user_id).first()
    #     return rating
    #
    #
    #
    # @classmethod
    # def get_user_ratings(cls, user_id):
    #     # print "******************", user_id
    #
    #     rating_list = db.session.query(cls).filter(cls.user_id == user_id).all()
    #     return rating_list
    #
    # @classmethod
    # def get_movie_ratings(cls, movie_id):
    #     # print "******************", user_id
    #
    #     rating_list = db.session.query(cls).filter(cls.movie_id == movie_id).all()
    #     return rating_list

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Contact contact_id = %s user_id=%s contact_name=%s \
        phone_number=%s>" % (self.contact_id, self.user_id, self.contact_name, self.phone_number)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ammeurer@localhost/lotr'
    # postgresql://scott:tiger@localhost/mydatabase
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

#!/usr/bin/python3

from datetime import datetime
from MPS import db, login_manager
from flask_login import UserMixin


"""takes user id as an argumment"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""
   Flask-login requires a User model with the following properties:

   has an is_authenticated() method that returns True if the user has provided valid credentials
   has an is_active() method that returns True if the user’s account is active
   has an is_anonymous() method that returns True if the current user is an anonymous user
   has a get_id() method which, given a User instance, returns the unique ID for that object
   UserMixin class provides the implementation of this properties. Its the reason you can call for example is_authenticated to check if
   login credentials provide is correct or not instead of having to write a method to do that yourself.
   so its better to import this class from flask called usermixin

"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    """Database relationships are associations between tables that are created using join statements
       to retrieve data. ... Both tables can have only one record on each side of the relationship.
       Each primary key value relates to none or only one record in the related table.
    """
    posts = db.relationship('Post', backref="author", lazy=True)
    """ __repr__(self) this will prove how our object is printed after print it out"""
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

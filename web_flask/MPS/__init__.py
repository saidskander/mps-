#!/usr/bin/python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "4314efba6ab58612339a0a1133ea2115"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///MPS.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from MPS import app_routes

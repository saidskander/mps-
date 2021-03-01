#!/usr/bin/python3


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "4314efba6ab58612339a0a1133ea2115"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///MPS.db'

db = SQLAlchemy(app)

from MPS import app_routes

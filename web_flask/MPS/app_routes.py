#!/usr/bin/python3
from MPS.forms import RegistrationForm, LoginForm, email_validator
from flask import render_template, url_for, flash, redirect
from MPS.models import User, Post
from wtforms.validators import email
import email_validator
from MPS import app
posts = [
    {
        "author": 'Skander amireche',
        "title": 'mps post 1',
        "content": 'First post content',
        "date_posted": 'april 20, 2021'
    },
    {
        "author": 'Skander amireche',
        "title": 'mps post 2',
        "content": 'Second post content',
        "date_posted": 'april 21, 2021'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/world")
def world():
    return render_template('world.html', title='world')


@app.route("/freinds")
def freinds():
    return render_template('freinds.html', title='freinds')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('home'))
    return render_template('register.html', title='register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "a@live.fr" and form.password.data == "aaa":
            flash("You have been succesfully logged in!")
            return redirect(url_for("home"))
        else:
            flash("wrong email or password")
    return render_template('login.html', title='Login', form=form)

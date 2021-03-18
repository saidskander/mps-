#!/usr/bin/python3
import os
from MPS.forms import RegistrationForm, LoginForm, email_validator, UpdateEmailForm, UpdateUsernameForm, UpdateProfilePicForm
from flask import render_template, url_for, flash, redirect, request
from MPS.models import User, Post
from wtforms.validators import email
import email_validator
import secrets
from MPS import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_img', picture_fn)
    form_picture.save(picture_path)


    return picture_fn


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    form = UpdateProfilePicForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash("Your account updated")
        return redirect(url_for('home'))
    image_file = url_for('static', filename="profile_img/" + current_user.image_file)
    return render_template('home.html', posts=posts, image_file=image_file, form=form)



@app.route("/world")
def world():
    return render_template('world.html', title='world')


@app.route("/freinds")
@login_required
def freinds():
    return render_template('freinds.html', title='freinds')


@app.route("/register", methods=["GET", "POST"])
def register():
    """the first 2 lines for making
       the session active without login again
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.
                                                        password.
                                                        data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Sign in to your account!")
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.
                                        email.data).first()
            if user and bcrypt.check_password_hash(user.password,
                                                   form.password.data):
                login_user(user, remember=form.remember.data)
                """Turnery condition cool i like it"""
                samePage = request.args.get('next')
                return redirect(samePage) if samePage else redirect(url_for
                                                                    ("home"))
            else:
                flash("wrong email or password")
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    """NOTE:!! i can redirect it to the home if i want.
       2operational --> home --> logout --> login templates
    """
    return redirect(url_for("login"))


@app.route("/setting")
@login_required
def setting():
    return render_template('setting.html', title='Settings')


@app.route("/email", methods=["GET", "POST"])
@login_required
def email():
    form = UpdateEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your email has been updated!')
        return redirect(url_for('email'))
    elif request.method == 'Get':
        form.email.data = current_user.email
    return render_template('email.html', title='Settings', form=form)


@app.route("/username", methods=["GET", "POST"])
@login_required
def username():
    form = UpdateUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your username has been updated!')
        return redirect(url_for('username'))
    elif request.method == 'Get':
        form.username.data = current_user.username
    return render_template('username.html', title='Settings', form=form)

@app.route("/")
@app.route("/landing")
def landing():
    return render_template('landing.html', title='landing')

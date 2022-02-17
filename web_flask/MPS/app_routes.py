#!/usr/bin/python3
import os
from MPS.forms import RegistrationForm, LoginForm, email_validator, PostForm, UpdateEmailForm, UpdateUsernameForm, UpdateProfilePicForm
from flask import render_template, url_for, flash, abort, redirect, request
from MPS.models import User, Post
from wtforms.validators import email
import email_validator
import secrets
from MPS import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required



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
    """after suffering long day this is how to order
    only current user posts in home page"""
    posts = Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())
    """this line is for making the posts by order"""
    """posts = Post.query.order_by(Post.date_posted.desc())"""
    """this line query all the posts but not by order"""
    """posts = current_user.posts.order_by(Post.id.desc())"""
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash("Your Picture has been updated")
        return redirect(url_for('home'))
    image_file = url_for('static', filename="profile_img/" + current_user.image_file)
    return render_template('home.html', posts=posts, image_file=image_file, form=form)


@app.route("/world", methods=["GET", "POST"])
@login_required
def world():
    form = PostForm()
    """this line is for making the posts by order"""
    posts = Post.query.order_by(Post.date_posted.desc())
    """this line query all the posts but not by order"""
    """posts = Post.query.all()"""
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post created!")
        return redirect(url_for('world'))
    return render_template('world.html', posts=posts, form=form, title='World')


@app.route("/current_post_id/<int:post_id>")
def current_post_id(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('current_post_id.html', post=post, title=post.title)


@app.route("/current_post_id/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        """no need db.session.add(post) becasue i already adedd them in the database"""
        db.session.commit()
        flash("Your post has been Edited")
        return redirect(url_for('current_post_id', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('world.html',
                           form=form,
                           legend="Edit Post",
                           title='Edit Post')


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

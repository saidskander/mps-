#!/usr/bin/python3
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, TextAreaField
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length, Email, EqualTo, email_validator
from wtforms.validators import Email, ValidationError
from flask_login import current_user
from MPS.models import User
import email_validator


class RegistrationForm(FlaskForm):
    """StringField from wtforms"""
    """DataRequired from wtformsvalidator"""
    """username length will be between 3-20"""
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3,
                                       max=22)])
    """Email imported from wtformsvalidators """
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    """passwordField imported from wtforms"""
    password = PasswordField("Password",
                             validators=[DataRequired()])

    """making sure the password and the password confirmation
    are equal using Equalto imported from wtformsvalidators
    """
    confirm_passwd = PasswordField("Confirm Passwd",
                                   validators=[DataRequired(),
                                               EqualTo("password")])
    """submit information"""
    submit = SubmitField("Sign Up")

    """Username is taken"""
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')

    """Email taken"""
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken')


class LoginForm(FlaskForm):
    """Email imported from wtformsvalidators """
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    """passwordField imported from wtforms"""
    password = PasswordField("Password",
                             validators=[DataRequired()])

    """ IMPORTANT Note !!! we dont need confirmation password because its
        a login and it is only for users whos already registered
    """

    """submit information"""
    submit = SubmitField("Login")

    """allow users to stay login using a Secure cookie """
    remember = BooleanField('Remember Me')


class UpdateEmailForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])

    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken')


class UpdateUsernameForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3,
                                       max=22)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')


class UpdateProfilePicForm(FlaskForm):
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField("Post")

#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length, Email, EqualTo, email_validator
from wtforms.validators import email
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

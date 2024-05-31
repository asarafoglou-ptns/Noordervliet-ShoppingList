from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class signupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
    """
    Checks if a user with the entered username already exists.
    :param self: current instance of the class
    :param username: username entered into the form
    :return: an error message on the page only if user already exists
    """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Someone beat you to it, please choose a different username.')

    def validate_email(self, email):
    """
    Checks if a user with the entered email already exists.
    :param self: current instance of the class
    :param email: email entered into the form
    :return: an error message on the page only if user already exists
    """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already linked to an account!')


class loginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

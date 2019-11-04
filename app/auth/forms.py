import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    length,
    EqualTo,
    NumberRange,
)

from app.models import User
from config import Constants


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            length(max=Constants.NAME_LENGTH, message='Too long name.')
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=Constants.SURNAME_LENGTH, message='Too long surname.')
        ]
    )

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            length(max=Constants.USERNAME_LENGTH, message='Too long username.')
        ]
    )

    age = IntegerField(
        'Age',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=Constants.MAX_AGE)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            Email(),
            length(max=Constants.EMAIL_LENGTH, message='Too long email.')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            length(
                min=Constants.MIN_PASSWORD_LENGTH,
                max=Constants.MAX_PASSWORD_LENGTH,
                message='Password is short or too long'
            )
        ]
    )

    confirm_password = PasswordField(
        'Confirm',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    submit = SubmitField('Submit')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).count():
            raise ValueError('This username already taken.')

        if not re.match('[0-9a-zA-Z]', username.data):
            raise ValueError('Only letters and digits are allowed.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count():
            raise ValueError('This email already taken.')


class ResetPassRequestForm(FlaskForm):
    email = StringField(
        'Email from your account',
        validators=[
            Email(),
            length(max=Constants.EMAIL_LENGTH, message='Too long email.')
        ]
    )


class ResetPassForm(FlaskForm):
    new_password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            length(
                min=Constants.MIN_PASSWORD_LENGTH,
                max=Constants.MAX_PASSWORD_LENGTH,
                message='Password is short or too long.'
            )
        ]
    )

    confirm_password = PasswordField(
        'Enter new password again.',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match.')
        ]
    )

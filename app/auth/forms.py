import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    PasswordField,
    SubmitField,
    BooleanField,
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
            length(max=Constants.NAME_LENGTH, message='Too long name')
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=Constants.SURNAME_LENGTH, message='Too long surname')
        ]
    )

    nick = StringField(
        'Nick',
        validators=[
            DataRequired(),
            length(max=Constants.NICK_LENGTH, message='Too long nick')
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
            length(max=Constants.EMAIL_LENGTH, message='Too long email')
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
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Submit')

    def validate_nick(self, nick):
        if User.query.filter_by(nick=nick.data).count():
            raise ValueError('This nick already taken')

        if not re.match('[0-9a-zA-Z-]', nick.data):
            raise ValueError('Only letters and digits are allowed')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count():
            raise ValueError('This email already taken')


class LoginForm(FlaskForm):
    def __init__(self):
        self._user = None
        super().__init__()

    login = StringField(
        'Nick or email',
        validators=[
            DataRequired(),
            length(max=Constants.NAME_LENGTH, message='Too long login')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            length(
                min=Constants.MIN_PASSWORD_LENGTH,
                max=Constants.MAX_PASSWORD_LENGTH,
                message='Incorrect password'
            )
        ]
    )

    remember = BooleanField('Remember me')

    @staticmethod
    def _is_email(email):
        return re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email)

    def get_user(self):
        return self._user

    def validate_password(self, password):
        if self._is_email(self.login.data):
            self._user = User.query.filter_by(email=self.login.data).first()
        else:
            self._user = User.query.filter_by(nick=self.login.data).first()

        if self._user is None or not self._user.check_password(password=password.data):
            raise ValueError('Username or password is incorrect')


class ResetPassRequestForm(FlaskForm):
    email = StringField(
        'Email from your account',
        validators=[
            Email(),
            length(max=Constants.EMAIL_LENGTH, message='Too long email')
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
                message='Password is short or too long'
            )
        ]
    )

    confirm_password = PasswordField(
        'Enter new password again',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match')
        ]
    )

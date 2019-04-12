import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    PasswordField,
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    Email,
    length,
    EqualTo,
    NumberRange
)

from app.models import User
from config import Constants


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            length(max=Constants.NAME_LENGTH, message='Very big name')
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=Constants.SURNAME_LENGTH, message='Very big surname')
        ]
    )

    nick = StringField(
        'Nick',
        validators=[
            DataRequired(),
            length(max=Constants.NICK_LENGTH, message='Very big nick')
        ]
    )

    age = IntegerField(
        'Age',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=Constants.MAX_AGE)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            Email(),
            length(max=Constants.EMAIL_LENGTH, message='Very big email')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Very big password')
        ]
    )

    confirm_password = PasswordField(
        'Confirm',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Very big password'),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Submit')

    def validate_nick(self, nick):
        if User.query.filter_by(nick=nick.data).count():
            raise ValueError('This nick already taken')

        if not re.match('[0-9a-zA-Z-]', nick.data):
            raise ValueError('Incorrect type of nick')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count():
            raise ValueError('This email already taken')


class LoginForm(FlaskForm):
    login = StringField(
        'Nick or email',
        validators=[
            DataRequired(),
            length(max=Constants.NAME_LENGTH, message='Very big name')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Incorrect password')
        ]
    )

    remember = BooleanField('Remember me')

    @staticmethod
    def _is_email(email):
        return re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email)

    def get_user(self):
        return self._user

    def validate_password(self, password):
        self._user = None

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
            length(max=Constants.EMAIL_LENGTH, message='Very big email')
        ]
    )


class ResetPassForm(FlaskForm):
    new_password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Very big password')
        ]
    )

    confirm_password = PasswordField(
        'Enter new password again',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Very big password'),
            EqualTo('new_password', message='Passwords must match')
        ]
    )

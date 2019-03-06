import re
import requests
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    PasswordField,
    SubmitField,
    BooleanField
)
from wtforms.validators import DataRequired, Email, length, EqualTo, NumberRange

from app.models import User

# Global variables for forms
NAME_LENGTH = 50
NICK_LENGTH = 50
EMAIL_LENGTH = 50
SURNAME_LENGTH = 50
PASSWORD_LENGTH = 30
MESSAGE_LENGTH = 1024


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            length(max=NAME_LENGTH, message='Very big name')
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=SURNAME_LENGTH, message='Very big surname')
        ]
    )

    nick = StringField(
        'Nick',
        validators=[
            DataRequired(),
            length(max=NICK_LENGTH, message='Very big nick')
        ]
    )

    age = IntegerField(
        'Age',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=150)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            Email(),
            length(max=EMAIL_LENGTH, message='Very big email')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Very big password')
        ]
    )

    confirm_password = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Very big password'),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Submit')

    def validate_nick(self, nick):
        if User.query.filter_by(nick=nick.data).count():
            raise ValueError('This nick already taken')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count():
            raise ValueError('This email already taken')


class LoginForm(FlaskForm):
    login = StringField(
        'Nick or email',
        validators=[
            DataRequired(),
            length(max=NAME_LENGTH, message='Very big name')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Incorrect password')
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


class ChatForm(FlaskForm):
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(),
            length(max=MESSAGE_LENGTH, message='Very big message'),
        ],
    )


class EditProfileForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            length(max=NAME_LENGTH, message='Very big name')
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=SURNAME_LENGTH, message='Very big surname')
        ]
    )

    nick = StringField(
        'Nick',
        validators=[
            DataRequired(),
            length(max=NICK_LENGTH, message='Very big nick')
        ]
    )

    age = IntegerField(
        'Age',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=150)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            Email(),
            length(max=EMAIL_LENGTH, message='Very big email')
        ]
    )

    photo = StringField('URL on avatar')

    password = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Incorrect password')
        ]
    )

    save = SubmitField('Save')

    @staticmethod
    def _is_url_image(image_url):
        try:
            image_formats = ("image/png", "image/jpeg", "image/jpg")
            r = requests.head(image_url, verify=False, timeout=5)
            if r.headers["content-type"] in image_formats:
                return True
            return False
        except Exception:
            return False

    def validate_nick(self, nick):
        if User.query.filter_by(nick=nick.data).count() and \
                nick.data != current_user.nick:
            raise ValueError('This nick already taken')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count() and \
                email.data != current_user.email:
            raise ValueError('This email already taken')

    def validate_password(self, password):
        if not current_user.check_password(password.data):
            raise ValueError('Password dont match')

    def validate_photo(self, photo):
        if photo.data and not self._is_url_image(photo.data):
            raise ValueError('Invalid url')


class EditPasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current password',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Incorrect password')
        ]
    )

    new_password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Very big password')
        ]
    )

    confirm_password = PasswordField(
        'Enter new password again',
        validators=[
            DataRequired(),
            length(max=PASSWORD_LENGTH, message='Very big password'),
            EqualTo('new_password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Save')

    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValueError('Password dont match')

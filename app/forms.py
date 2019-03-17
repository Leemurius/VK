import re
import requests
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import (
    StringField,
    TextAreaField,
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
    NumberRange,
)

from app.models import User

# Global variables for forms
NAME_LENGTH = 50
NICK_LENGTH = 50
EMAIL_LENGTH = 50
ADDRESS_LENGTH = 50
SURNAME_LENGTH = 50
PASSWORD_LENGTH = 30
ARTICLE_LENGTH = 512
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
        'Confirm',
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


class ProfSettingsForm(FlaskForm):
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

    address = StringField(
        'Address',
        validators=[
            DataRequired(),
            length(max=ADDRESS_LENGTH, message='Very big address')
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

    photo = FileField(
        "Photo",
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], message='Images only')
        ]
    )

    save = SubmitField('Save')

    def validate_nick(self, nick):
        if User.query.filter_by(nick=nick.data).count() and \
                nick.data != current_user.nick:
            raise ValueError('This nick already taken')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count() and \
                email.data != current_user.email:
            raise ValueError('This email already taken')

    def validate_photo(self, photo):
        pass
        # Check size


class SecSettingsForm(FlaskForm):
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


class AboutSettingsForm(FlaskForm):
    about_me = TextAreaField(
        'About me',
        validators=[
            DataRequired(),
            length(max=ARTICLE_LENGTH, message='Very big article'),
        ],
    )

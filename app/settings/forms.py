import requests
from flask import current_app
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    StringField,
    TextAreaField,
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


# -------------------------------------------------------------------------------------
class ProfSettingsForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            length(max=current_app.config['NAME_LENGTH'], message='Very big name')
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=current_app.config['SURNAME_LENGTH'], message='Very big surname')
        ]
    )

    nick = StringField(
        'Nick',
        validators=[
            DataRequired(),
            length(max=current_app.config['NICK_LENGTH'], message='Very big nick')
        ]
    )

    address = StringField(
        'Address',
        validators=[
            DataRequired(),
            length(max=current_app.config['ADDRESS_LENGTH'], message='Very big address')
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
            length(max=current_app.config['EMAIL_LENGTH'], message='Very big email')
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
        # FIXME: check size


# -------------------------------------------------------------------------------------
class SecSettingsForm(FlaskForm):
    current_password = PasswordField(
        'Current password',
        validators=[
            DataRequired(),
            length(max=current_app.config['PASSWORD_LENGTH'], message='Incorrect password')
        ]
    )

    new_password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            length(max=current_app.config['PASSWORD_LENGTH'], message='Very big password')
        ]
    )

    confirm_password = PasswordField(
        'Enter new password again',
        validators=[
            DataRequired(),
            length(max=current_app.config['PASSWORD_LENGTH'], message='Very big password'),
            EqualTo('new_password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Save')

    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValueError('Password dont match')


# -------------------------------------------------------------------------------------
class AboutSettingsForm(FlaskForm):
    about_me = TextAreaField(
        'About me',
        validators=[
            DataRequired(),
            length(max=current_app.config['ARTICLE_LENGTH'], message='Very big article'),
        ],
    )

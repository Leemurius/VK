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
from config import Constants


class ProfSettingsForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            length(max=Constants.NAME_LENGTH, message='Too long name')  # FIXME: Min?
        ]
    )

    surname = StringField(
        'Surname',
        validators=[
            DataRequired(),
            length(max=Constants.SURNAME_LENGTH, message='Too long surname')  # FIXME: Min?
        ]
    )

    nick = StringField(
        'Nick',
        validators=[
            DataRequired(),
            length(max=Constants.NICK_LENGTH, message='Too long nick')  # FIXME: Min?
        ]
    )

    address = StringField(
        'Address',
        validators=[
            DataRequired(),
            length(max=Constants.ADDRESS_LENGTH, message='Too long address')  # FIXME: Min?
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

    photo = FileField(
        "Photo",
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], message='Images only')  # FIXME: bmp?
        ]
    )

    save = SubmitField('Save')

    def validate_nick(self, nick):
        if (User.query.filter_by(nick=nick.data).count() and
                nick.data != current_user.nick):
            raise ValueError('This nick already taken')

    def validate_email(self, email):
        if (User.query.filter_by(email=email.data).count() and
                email.data != current_user.email):
            raise ValueError('This email already taken')

    def validate_photo(self, photo):
        pass
        # TODO: check size


class SecSettingsForm(FlaskForm):
    current_password = PasswordField(
        'Current password',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Incorrect password')
        ]
    )

    new_password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            length(max=Constants.PASSWORD_LENGTH, message='Too long password')  # FIXME: Min?
        ]
    )

    confirm_password = PasswordField(
        'Enter new password again',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Save')

    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValueError('Incorrect current password')


class AboutSettingsForm(FlaskForm):
    about_me = TextAreaField(
        'About me',
        validators=[
            DataRequired(),
            length(max=Constants.ARTICLE_LENGTH, message='Too long article')
        ]
    )

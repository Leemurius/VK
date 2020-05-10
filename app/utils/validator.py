import os
import re

from flask import current_app
from flask_login import current_user

from config import Constants
from app.models import User


class Validator:
    @classmethod
    def validate(cls, required_fields, data):
        cls.validate_required_fields(required_fields, data)

        error_list = cls._validate(data)
        if any(error_list):
            raise ValueError(error_list)

    @classmethod
    def _validate(cls, data):
        pass

    @classmethod
    def validate_required_fields(cls, fields, data):
        for field, type in fields.items():
            if not (field in data and isinstance(data.get(field), type)):
                raise ValueError('Template of arguments must be' +
                                 str(fields) + ' !')

    @classmethod
    def validate_id(cls, id):
        try:
            if User.query.get(id) is None:
                raise ValueError("User id is incorrect")

        except ValueError as exception:
            return 'user_id', str(exception)
        return None

    @classmethod
    def validate_login(cls, login):
        try:
            if User.get_user_from_login(login) is None:
                raise ValueError("Login is incorrect")

        except ValueError as exception:
            return 'login', str(exception)
        return None

    @classmethod
    def validate_block_name(cls, block_name):
        try:
            allowed_names = ('head', 'main', 'js_files')
            if block_name not in allowed_names:
                raise ValueError('Block name should be ' + str(allowed_names))

        except ValueError as exception:
            return 'block name', str(exception)
        return None

    @classmethod
    def validate_filename(cls, filename):
        try:
            if not os.path.isfile(current_app.root_path + filename):
                raise ValueError("Incorrect filepath")

        except ValueError as exception:
            return 'filename', str(exception)
        return None

    @classmethod
    def validate_reset_email(cls, email):
        try:
            if User.query.filter_by(email=email).first() is None:
                raise ValueError("This email doesn't registered on the website")

        except ValueError as exception:
            return 'email', str(exception)
        return None

    @classmethod
    def validate_message(cls, message):
        try:
            cls._line_is_not_empty(message)

            if len(message) > Constants.MAX_MESSAGE_LENGTH:
                raise ValueError('Too long message')

        except ValueError as exception:
            return 'name', str(exception)
        return None

    @classmethod
    def validate_name(cls, name):
        try:
            cls._line_is_not_empty(name)

            if len(name) > Constants.NAME_LENGTH:
                raise ValueError('Too long name')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я]+$', name):
                raise ValueError('Incorrect name format')

        except ValueError as exception:
            return 'name', str(exception)
        return None

    @classmethod
    def validate_surname(cls, surname):
        try:
            cls._line_is_not_empty(surname)
            if len(surname) > Constants.SURNAME_LENGTH:
                raise ValueError('Too long surname')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я]+$', surname):
                raise ValueError('Incorrect surname format')

        except ValueError as exception:
            return 'surname', str(exception)
        return None

    @classmethod
    def validate_new_username(cls, old_username, new_username):
        try:
            cls._line_is_not_empty(new_username)

            if len(new_username) > Constants.USERNAME_LENGTH:
                raise ValueError('Too long username')

            if (old_username != new_username and
                    User.query.filter_by(username=new_username).first()):
                raise ValueError('This username already taken')

            if not re.match('^[0-9a-zA-Z]+$', new_username):
                raise ValueError('Only letters and digits are allowed')

        except ValueError as exception:
            return 'username', str(exception)
        return None

    @classmethod
    def validate_new_email(cls, old_email, new_email):
        try:
            cls._line_is_not_empty(new_email)

            if len(new_email) > Constants.EMAIL_LENGTH:
                raise ValueError('Too long email')

            if (old_email != new_email and
                    User.query.filter_by(email=new_email).first()):
                raise ValueError('This email already registered')

            if not re.match(
                    '^[0-9a-zA-Zа-яА-Я.-_]+'
                    '@[0-9a-zA-Zа-яА-Я-_]+'
                    '(\.[0-9a-zA-Zа-яА-Я]+)+$',
                    new_email
            ):
                raise ValueError('Incorrect email format')

        except ValueError as exception:
            return 'email', str(exception)
        return None

    @classmethod
    def validate_age(cls, age):
        try:
            # It's not important field
            if age is None:
                return None

            if age < 0:
                raise ValueError("Don't try to cheat me")

            if age < Constants.MIN_AGE:
                raise ValueError('You are too young for this website')

            if age > Constants.MAX_AGE:
                raise ValueError('Thank you for testing of the website')

        except ValueError as exception:
            return 'age', str(exception)
        return None

    @classmethod
    def validate_photo(cls, photo):
        try:
            if photo is None:
                raise ValueError('Photo field is empty')

            photo.seek(0, os.SEEK_END)  # Go to the end of file
            if photo.tell() / 1024 / 1024 > Constants.MAX_PHOTO_SIZE:
                raise ValueError('Max size of photo is {} MB'.format(
                    Constants.MAX_PHOTO_SIZE))

        except ValueError as exception:
            return 'photo', str(exception)
        return None

    @classmethod
    def validate_address(cls, address):
        try:
            if len(address) > Constants.ADDRESS_LENGTH:
                raise ValueError('Too long address')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я.,; ]*$', address):
                raise ValueError('Incorrect address format')

        except ValueError as exception:
            return 'address', str(exception)
        return None

    @classmethod
    def validate_old_password(cls, password, user):
        try:
            # When we sign in we can have user of NoneType type
            if user is None:
                raise ValueError("Password is incorrect")

            if not user.check_password(password):
                raise ValueError('Password is incorrect')

        except ValueError as exception:
            return 'old_password', str(exception)
        return None

    @classmethod
    def validate_new_password(cls, password):
        try:
            cls._line_is_not_empty(password)

            if len(password) < Constants.MIN_PASSWORD_LENGTH:
                raise ValueError('Too short password')

            if len(password) > Constants.MAX_PASSWORD_LENGTH:
                raise ValueError('Too long password')

        except ValueError as exception:
            return 'new_password', str(exception)
        return None

    @classmethod
    def validate_confirm_password(cls, new_password, confirm_password):
        try:
            cls._line_is_not_empty(confirm_password)

            if new_password != confirm_password:
                raise ValueError('Passwords don\'t match')

        except ValueError as exception:
            return 'confirm_password', str(exception)
        return None

    @classmethod
    def _line_is_not_empty(cls, line):
        if line.strip() == '':
            raise ValueError('This field is required')


class LoginValidator(Validator):
    @classmethod
    def _validate(cls, data):
        login = cls.validate_login(data['login'])
        old_password = cls.validate_old_password(
            data['password'],
            User.get_user_from_login(data['login'])
        )

        if login is not None or old_password is not None:
            return (
                ('login', 'Login or password is incorrect'),
                ('password', 'Login or password is incorrect')
            )
        else:
            return None, None


class RegistrationValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return (
            cls.validate_name(data['name']),
            cls.validate_surname(data['surname']),
            cls.validate_new_username(None, data['username']),
            cls.validate_new_email(None, data['email']),
            cls.validate_new_password(data['new_password']),
            cls.validate_confirm_password(data['new_password'],
                                          data['confirm_password'])
        )


class SettingsValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return (
            cls.validate_id(data['user_id']),
            cls.validate_name(data['name']),
            cls.validate_surname(data['surname']),
            cls.validate_new_username(current_user.username, data['username']),
            cls.validate_age(data['age']),
            cls.validate_new_email(current_user.email, data['email']),
            cls.validate_address(data['address'])
        )


class PhotoValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return (
            cls.validate_id(data['user_id']),
            cls.validate_photo(data['photo'])
        )


class PasswordValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return (
            cls.validate_old_password(data['old_password'], current_user),
            cls.validate_new_password(data['new_password']),
            cls.validate_confirm_password(data['new_password'],
                                          data['confirm_password'])
        )


class ResetPasswordValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return (
            cls.validate_new_password(data['new_password']),
            cls.validate_confirm_password(data['new_password'],
                                          data['confirm_password'])
        )


class ResetProfileValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return cls.validate_reset_email(data['email']),


class MessageValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return cls.validate_message(data['message']),


class ContentValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return (cls.validate_block_name(data['block_name']),
                cls.validate_filename(data['filename']))


class FilenameValidator(Validator):
    @classmethod
    def _validate(cls, data):
        return cls.validate_filename(data['filename']),

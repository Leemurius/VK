import os
import re

import werkzeug
from flask import current_app
from flask_login import current_user

from config import Constants
from app.models import User


class Validator:
    def validate(self, required_fields, data):
        Validator.validate_required_fields(required_fields, data)

        error_list = self._validate(data)
        if any(error_list):
            raise ValueError(error_list)

    def _validate(self, data):
        pass

    @staticmethod
    def validate_required_fields(fields, data):
        for field, type in fields.items():
            if not (field in data and isinstance(data.get(field), type)):
                raise ValueError('Template of arguments ' + str(fields) + ' !')

    @staticmethod
    def validate_login(login):
        try:
            if User.get_user_from_login(login) is None:
                raise ValueError("Login is incorrect")

        except ValueError as exception:
            return 'login', str(exception)
        return None

    @staticmethod
    def validate_blockname(blockname):
        try:
            Validator._check_type(blockname, str)

            allowed_names = ('head', 'main', 'js_files')
            if blockname not in allowed_names:
                raise ValueError('Block name should be ' + str(allowed_names))

        except ValueError as exception:
            return 'blockname', str(exception)
        return None

    @staticmethod
    def validate_filename(filename):
        try:
            Validator._check_type(filename, str)

            if not os.path.isfile(current_app.root_path + filename):
                raise ValueError("Incorrect filepath")

        except ValueError as exception:
            return 'blockname', str(exception)
        return None

    @staticmethod
    def validate_reset_email(email):
        try:
            if User.query.filter_by(email=email).first() is None:
                raise ValueError('This email doesn\'t registered on the website')

        except ValueError as exception:
            return 'email', str(exception)
        return None

    @staticmethod
    def validate_message(message):
        try:
            Validator._check_type(message, str)
            Validator._line_is_not_empty(message)

            if len(message) > Constants.MAX_MESSAGE_LENGTH:  # Check length
                raise ValueError('Too long message')

        except ValueError as exception:
            return 'name', str(exception)
        return None

    @staticmethod
    def validate_name(name):
        try:
            Validator._check_type(name, str)
            Validator._line_is_not_empty(name)

            if len(name) > Constants.NAME_LENGTH:
                raise ValueError('Too long name')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я]+$', name):
                raise ValueError('Incorrect name format')

        except ValueError as exception:
            return 'name', str(exception)
        return None

    @staticmethod
    def validate_surname(surname):
        try:
            Validator._check_type(surname, str)
            Validator._line_is_not_empty(surname)
            if len(surname) > Constants.SURNAME_LENGTH:
                raise ValueError('Too long surname')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я]+$', surname):
                raise ValueError('Incorrect surname format')

        except ValueError as exception:
            return 'surname', str(exception)
        return None

    @staticmethod
    def validate_new_username(old_username, new_username):
        try:
            Validator._check_type(new_username, str)
            Validator._line_is_not_empty(new_username)

            if len(new_username) > Constants.USERNAME_LENGTH:
                raise ValueError('Too long username')

            if old_username != new_username and User.query.filter_by(username=new_username).first():
                raise ValueError('This username already taken')

            if not re.match('^[0-9a-zA-Z]+$', new_username):
                raise ValueError('Only letters and digits are allowed')

        except ValueError as exception:
            return 'username', str(exception)
        return None

    @staticmethod
    def validate_new_email(old_email, new_email):
        try:
            Validator._check_type(new_email, str)
            Validator._line_is_not_empty(new_email)

            if len(new_email) > Constants.EMAIL_LENGTH:
                raise ValueError('Too long email')

            if old_email != new_email and User.query.filter_by(email=new_email).first():
                raise ValueError('This email already registered')

            if not re.match(
                    '^[0-9a-zA-Zа-яА-Я.-_]+@[0-9a-zA-Zа-яА-Я-_]+(\.[0-9a-zA-Zа-яА-Я]+)+$',
                    new_email
            ):
                raise ValueError('Incorrect email format')

        except ValueError as exception:
            return 'email', str(exception)
        return None

    @staticmethod
    def validate_age(age):
        try:
            # It's not important field
            if age is None:
                return None

            Validator._check_type(age, int)

            if age < 0:
                raise ValueError('Don\'t try to cheat me')

            if age < Constants.MIN_AGE:
                raise ValueError('You are too young for this website')

            if age > Constants.MAX_AGE:
                raise ValueError('Thank you for testing of the website')

        except ValueError as exception:
            return 'age', str(exception)
        return None

    @staticmethod
    def validate_photo(photo):
        try:
            # It's not important field
            if photo is None:
                return None

            Validator._check_type(photo, werkzeug.datastructures.FileStorage)

            photo.seek(0, os.SEEK_END)  # Go to the end of file
            if photo.tell() / 1024 / 1024 > Constants.MAX_PHOTO_SIZE:
                raise ValueError('Max size of photo is {} MB'.format(Constants.MAX_PHOTO_SIZE))

        except ValueError as exception:
            return 'photo', str(exception)
        return None

    @staticmethod
    def validate_address(address):
        try:
            Validator._check_type(address, str)

            if len(address) > Constants.ADDRESS_LENGTH:
                raise ValueError('Too long address')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я.,; ]*$', address):
                raise ValueError('Incorrect address format')

        except ValueError as exception:
            return 'address', str(exception)
        return None

    @staticmethod
    def validate_old_password(password, user):
        try:
            Validator._check_type(password, str)

            # When we sign in we can have user of NoneType type
            if user is None:
                raise ValueError("Password is incorrect")

            if not user.check_password(password):
                raise ValueError('Password is incorrect')

        except ValueError as exception:
            return 'old_password', str(exception)
        return None

    @staticmethod
    def validate_new_password(password):
        try:
            Validator._check_type(password, str)
            Validator._line_is_not_empty(password)

            if len(password) < Constants.MIN_PASSWORD_LENGTH:
                raise ValueError('Too short password')

            if len(password) > Constants.MAX_PASSWORD_LENGTH:
                raise ValueError('Too long password')

        except ValueError as exception:
            return 'new_password', str(exception)
        return None

    @staticmethod
    def validate_confirm_password(new_password, confirm_password):
        try:
            Validator._check_type(confirm_password, str)
            Validator._line_is_not_empty(confirm_password)

            if new_password != confirm_password:
                raise ValueError('Passwords don\'t match')

        except ValueError as exception:
            return 'confirm_password', str(exception)
        return None

    @staticmethod
    def _line_is_not_empty(line):
        if line.strip() == '':
            raise ValueError('This field is required')

    @staticmethod
    def _check_type(variable, type):
        if not isinstance(variable, type):
            raise ValueError('Type must be ' + str(type))


class LoginValidator(Validator):
    def _validate(self, data):
        if (LoginValidator.validate_login(data['login']) is not None or
                LoginValidator.validate_old_password(
                    data['password'], User.get_user_from_login(data['login'])) is not None):
            return (
                ('login', 'Login or password is incorrect'),
                ('password', 'Login or password is incorrect')
            )
        else:
            return None, None


class RegistrationValidator(Validator):
    def _validate(self, data):
        return (
            RegistrationValidator.validate_name(data['name']),
            RegistrationValidator.validate_surname(data['surname']),
            RegistrationValidator.validate_new_username(None, data['username']),
            RegistrationValidator.validate_new_email(None, data['email']),
            RegistrationValidator.validate_new_password(data['new_password']),
            RegistrationValidator.validate_confirm_password(
                data['new_password'], data['confirm_password']
            )
        )


class SettingsValidator(Validator):
    def _validate(self, data):
        return (
            SettingsValidator.validate_name(data['name']),
            SettingsValidator.validate_surname(data['surname']),
            SettingsValidator.validate_new_username(current_user.username, data['username']),
            SettingsValidator.validate_age(data['age']),
            SettingsValidator.validate_new_email(current_user.email, data['email']),
            SettingsValidator.validate_address(data['address'])
        )


class PhotoValidator(Validator):
    def _validate(self, data):
        return PhotoValidator.validate_photo(data['photo']),


class PasswordValidator(Validator):
    def _validate(self, data):
        return (
            PhotoValidator.validate_old_password(data['old_password'], current_user),
            PhotoValidator.validate_new_password(data['new_password']),
            PhotoValidator.validate_confirm_password(data['new_password'], data['confirm_password'])
        )


class ResetPasswordValidator(Validator):
    def _validate(self, data):
        return (
            PhotoValidator.validate_new_password(data['new_password']),
            PhotoValidator.validate_confirm_password(data['new_password'], data['confirm_password'])
        )


class ResetValidator(Validator):
    def _validate(self, data):
        return ResetValidator.validate_reset_email(data['email']),


class MessageValidator(Validator):
    def _validate(self, data):
        return MessageValidator.validate_message(data['message']),


class ContentValidator(Validator):
    def _validate(self, data):
        return (ContentValidator.validate_blockname(data['blockname']),
                ContentValidator.validate_filename(data['filename']))


class FilenameValidator(Validator):
    def _validate(self, data):
        return ContentValidator.validate_filename(data['filename']),

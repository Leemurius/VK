import re

from flask_login import current_user

from config import Constants
from app.auth.validate import RegistrationValidator
from app.models import User


class PersonalSettingsValidator(RegistrationValidator):
    def __init__(self, name, surname, username, age, email, address, photo=None):
        RegistrationValidator.__init__(self, name, surname, username, email, None, None)
        self._age = age
        self._address = address
        self._photo = photo

    def validate(self):
        """
        :return tuple of error messages from every field
        """
        return (
            self.validate_name(),
            self.validate_surname(),
            self.validate_username(),
            self.validate_age(),
            self.validate_email(),
            self.validate_address()
        )

    def validate_username(self):
        try:
            self._validate_is_not_empty(self._username)

            if len(self._username) > Constants.USERNAME_LENGTH:
                raise Exception('Too long username')

            if self._username != current_user.username and \
                    User.query.filter_by(username=self._username).first():
                raise Exception('This username already taken')

            if not re.match('^[0-9a-zA-Z]+$', self._username):
                raise Exception('Only letters and digits are allowed')

        except Exception as exception:
            return 'username', str(exception)
        return None

    def validate_email(self):
        try:
            self._validate_is_not_empty(self._email)

            if len(self._email) > Constants.EMAIL_LENGTH:
                raise Exception('Too long email')

            if self._email != current_user.email and \
                    User.query.filter_by(email=self._email).first():
                raise Exception('This email already registered')

            if not re.match('^[0-9a-zA-Zа-яА-Я.]+@[0-9a-zA-Zа-яА-Я]+\.[0-9a-zA-Zа-яА-Я]+$',
                            self._email):
                raise Exception('Email has incorrect format')

        except Exception as exception:
            return 'email', str(exception)
        return None

    def validate_age(self):
        try:
            if self._age < Constants.MIN_AGE:
                raise Exception('You too young for this website')

            if self._age > Constants.MAX_AGE:
                raise Exception('It\'s impossible:)')

        except Exception as exception:
            return 'age', str(exception)
        return None

    def validate_address(self):
        try:
            if len(self._address) > Constants.ADDRESS_LENGTH:
                raise Exception('Too long address')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я.,; ]*$', self._address):
                raise Exception('Address has incorrect format')

        except Exception as exception:
            return 'address', str(exception)
        return None


class PasswordSettingsValidator:
    def __init__(self, old_password, new_password, confirm_password):
        self._old_password = old_password
        self._new_password = new_password
        self._confirm_password = confirm_password

    def validate(self):
        """
        :return tuple of error messages from every field
        """
        return (
            self.validate_old_password(),
            self.validate_new_password(),
            self.validate_confirm_password()
        )

    def validate_old_password(self):
        try:
            if not current_user.check_password(password=self._old_password):
                raise Exception('Password is incorrect')

        except Exception as exception:
            return 'old_password', str(exception)
        return None

    def validate_new_password(self):
        try:
            self._validate_is_not_empty(self._new_password)

            if len(self._new_password) < Constants.MIN_PASSWORD_LENGTH:
                raise Exception('Too short password')

            if len(self._new_password) > Constants.MAX_PASSWORD_LENGTH:
                raise Exception('Too long password')

        except Exception as exception:
            return 'new_password', str(exception)
        return None

    def validate_confirm_password(self):
        try:
            if self._new_password != self._confirm_password:
                raise Exception('Passwords don\'t match')

            self._validate_is_not_empty(self._new_password)  # if password fields are empty

        except Exception as exception:
            return 'confirm_password', str(exception)
        return None

    def _validate_is_not_empty(self, line):
        if len(line) == 0:
            raise Exception('This field is required')

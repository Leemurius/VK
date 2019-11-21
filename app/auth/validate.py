import re


from app.models import User
from config import Constants


class LoginValidator:
    def __init__(self, login, password):
        self._login = login
        self._password = password

    def get_user(self):
        self.validate()
        return self._get_user()

    def validate(self):
        self.validate_login()
        self.validate_password()

    def validate_login(self):
        if not self._get_user():
            raise Exception('Login or password is incorrect')

    def validate_password(self):
        """
        Use only after 'validate_login'
        """
        if not self._get_user().check_password(password=self._password):
            raise Exception('Login or password is incorrect')

    def _get_user(self):
        return User.query.filter_by(username=self._login).first() or \
               User.query.filter_by(email=self._login).first()


class RegistrationValidator:
    def __init__(self, name, surname, username, email, password, confirm_password):
        self._name = name
        self._surname = surname
        self._username = username
        self._email = email
        self._password = password
        self._confirm_password = confirm_password

    def validate(self):
        """
        :return tuple of error messages from every field
        """
        return (
            self.validate_name(),
            self.validate_surname(),
            self.validate_username(),
            self.validate_email(),
            self.validate_password(),
            self.validate_confirm_password()
        )

    def validate_name(self):
        try:
            self._validate_is_not_empty(self._name)

            if len(self._name) > Constants.NAME_LENGTH:
                raise Exception('Too long name')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я]+$', self._name):
                raise Exception('Name has incorrect format')

        except Exception as exception:
            return 'name', str(exception)
        return None

    def validate_surname(self):
        try:
            self._validate_is_not_empty(self._surname)

            if len(self._surname) > Constants.SURNAME_LENGTH:
                raise Exception('Too long surname')

            if not re.match('^[a-zA-Z0-9\-а-яА-Я]+$', self._surname):
                raise Exception('Surname has incorrect format')

        except Exception as exception:
            return 'surname', str(exception)
        return None

    def validate_username(self):
        try:
            self._validate_is_not_empty(self._username)

            if len(self._username) > Constants.USERNAME_LENGTH:
                raise Exception('Too long username')

            if User.query.filter_by(username=self._username).first():
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

            if User.query.filter_by(email=self._email).first():
                raise Exception('This email already registered')

            if not re.match('^[0-9a-zA-Zа-яА-Я.-]+@[0-9a-zA-Zа-яА-Я]+\.[0-9a-zA-Zа-яА-Я]+$',
                            self._email):
                raise Exception('Email has incorrect format')

        except Exception as exception:
            return 'email', str(exception)
        return None

    def validate_password(self):
        try:
            self._validate_is_not_empty(self._password)

            if len(self._password) < Constants.MIN_PASSWORD_LENGTH:
                raise Exception('Too short password')

            if len(self._password) > Constants.MAX_PASSWORD_LENGTH:
                raise Exception('Too long password')

        except Exception as exception:
            return 'password', str(exception)
        return None

    def validate_confirm_password(self):
        try:
            if self._password != self._confirm_password:
                raise Exception('Passwords don\'t match')

            self._validate_is_not_empty(self._password)  # if password fields are empty

        except Exception as exception:
            return 'confirm_password', str(exception)
        return None

    def _validate_is_not_empty(self, line):
        if len(line) == 0:
            raise Exception('This field is required')


# TODO: added because i have recursion
class ResetPasswordValidator:
    def __init__(self, new_password, confirm_password):
        self._new_password = new_password
        self._confirm_password = confirm_password

    def validate(self):
        """
        :return tuple of error messages from every field
        """
        return (
            self.validate_new_password(),
            self.validate_confirm_password()
        )

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

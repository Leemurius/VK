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
            raise Exception('Login or password is incorrect.')

    def validate_password(self):
        """
        Use only after 'validate_login'
        """
        if not self._get_user().check_password(password=self._password):
            raise Exception('Login or password is incorrect.')

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

            if self._name > Constants.NAME_LENGTH:
                raise Exception('Too long name.')

        except Exception as exception:
            return 'name', str(exception)
        return None

    def validate_surname(self):
        try:
            self._validate_is_not_empty(self._surname)

            if self._surname > Constants.SURNAME_LENGTH:
                raise Exception('Too long surname.')

        except Exception as exception:
            return 'surname', str(exception)
        return None

    def validate_username(self):
        try:
            self._validate_is_not_empty(self._username)

            if self._username > Constants.USERNAME_LENGTH:
                raise Exception('Too long username.')

            if User.query.filter_by(username=self._username).first():
                raise Exception('This username already taken.')

        except Exception as exception:
            return ('username', str(exception))
        return None

    def validate_email(self):
        pass

    def validate_password(self):
        pass

    def validate_confirm_password(self):
        pass

    def _validate_is_not_empty(self, line):
        if len(line) == 0:
            return Exception('This field is required.')

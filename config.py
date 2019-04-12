import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'kldsjgmoid4yt834f84mtemvt74tv437vmetm'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = 'kldsjgmoid4yt834f84mtemvt74tv437vmetm'

    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'no-reply@ugmi.me'
    MAIL_PASSWORD = 'FjskH_48'
    ADMINS = ['sidorevich.anton@gmail.com']


class Constants(object):
    IMAGE_UPLOAD_FOLDER = "Data/UsersPhotos/"
    ROOM_IMAGE_UPLOAD_FOLDER = "Data/RoomPhotos/"
    CONST_DEFAULT_USER_PHOTO = '/static/images/no_photo.png'
    CONST_DEFAULT_ROOM_PHOTO = '/static/images/no_photo.png'

    TIME_OF_ACTUAL_REQUEST = 500
    TIME_OF_ONLINE = 5  # minutes

    MAX_AGE = 150
    NAME_LENGTH = 50
    NICK_LENGTH = 50
    EMAIL_LENGTH = 50
    PHOTO_LENGTH = 50
    ADDRESS_LENGTH = 50
    SURNAME_LENGTH = 50
    PASSWORD_LENGTH = 30
    ARTICLE_LENGTH = 512
    ROOM_NAME_LENGTH = 50
    MESSAGE_LENGTH = 1024

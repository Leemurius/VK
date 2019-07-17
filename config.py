import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'vtn73y777ct847ytn7347ct348ctny83378'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = 'vtn73y777ct847ytn7347ct348ctny83378'

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'sidorevich.toxa@mail.ru'
    MAIL_PASSWORD = 'Leemur2001top36+27=63'
    ADMINS = ['sidorevich.anton@gmail.com']

    ELASTICSEARCH_URL = 'http://localhost:9200'


class Constants(object):
    IMAGE_UPLOAD_FOLDER = "Data/UsersPhotos/"
    ROOM_IMAGE_UPLOAD_FOLDER = "Data/RoomPhotos/"
    CONST_DEFAULT_USER_PHOTO = '/static/images/no_photo.png'
    CONST_DEFAULT_ROOM_PHOTO = '/static/images/no_photo.png'

    USER_PER_PAGE = 8
    MESSAGE_PER_PAGE = 20

    TIME_OF_ACTUAL_REQUEST = 500
    TIME_OF_ONLINE = 5  # minutes

    MAX_AGE = 150
    NAME_LENGTH = 50
    NICK_LENGTH = 50
    EMAIL_LENGTH = 50
    PHOTO_LENGTH = 50
    REQUEST_LENGTH = 50
    ADDRESS_LENGTH = 50
    SURNAME_LENGTH = 50
    MIN_PASSWORD_LENGTH = 3
    MAX_PASSWORD_LENGTH = 30
    ARTICLE_LENGTH = 512
    ROOM_NAME_LENGTH = 50
    MESSAGE_LENGTH = 1024

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'dima_pidor_its_true'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    ADMINS = ['sidorevich.anton@gmail.com']

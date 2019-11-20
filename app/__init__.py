import os
import logging
from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import Config, Constants

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.registration'
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)

    with app.app_context():
        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

    with app.app_context():
        from app.settings import bp as settings_bp
        app.register_blueprint(settings_bp, url_prefix='/my_profile')

    with app.app_context():
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

    # Create folder for user photos
    if not os.path.isdir(Constants.IMAGE_UPLOAD_FOLDER):
        os.makedirs(Constants.IMAGE_UPLOAD_FOLDER)

    # Create folder for room photos
    if not os.path.isdir(Constants.ROOM_IMAGE_UPLOAD_FOLDER):
        os.makedirs(Constants.ROOM_IMAGE_UPLOAD_FOLDER)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()

            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_USERNAME'],
                toaddrs=app.config['ADMINS'], subject='Failed',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Write logs
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/leemurchat.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Leemur chat')

    return app


@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))


from app import models

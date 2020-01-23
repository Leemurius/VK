import os
import logging
from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import SMTPHandler

from config import Config, Constants

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
sio = SocketIO()


def create_app(config_class=Config, debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    sio.init_app(app, async_mode='eventlet')

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

    # Create folder for logs
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    if not app.debug:
        if app.config['MAIL_SERVER']:
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_USERNAME'],
                toaddrs=app.config['ADMINS'],
                subject='Your server broke down',
                credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
                secure=(() if app.config['MAIL_USE_TLS'] else None)
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app


@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))


from app import models

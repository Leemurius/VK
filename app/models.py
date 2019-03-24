import os
import jwt
import datetime
import operator
from time import time
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


rooms = db.Table('rooms',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
)


class User(UserMixin, db.Model):
    CONST_DEFAULT_PHOTO = '/static/images/no_photo.png'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    nick = db.Column(db.String(20), unique=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    photo = db.Column(db.String(100), default=CONST_DEFAULT_PHOTO)
    about_me = db.Column(db.String(512))
    last_seen = db.Column(db.DateTime, index=True)
    password_hash = db.Column(db.String(256))

    rooms = db.relationship(
        'Room',
        secondary=rooms,
        backref=db.backref('members', lazy="dynamic")
    )

    @property
    def status(self):
        time_difference = datetime.datetime.utcnow() - self.last_seen
        if time_difference.total_seconds() / 60 > 5:
            return False
        else:
            return True

    def __init__(self, name, surname, nick, age, email):
        self.name = name
        self.surname = surname
        self.nick = nick
        self.age = age
        self.email = email

    def get_reset_password_token(self, expires_in=500):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def last_message(id_1, id_2):
        pass

    def set_profile_form(self, form):
        self.name = form.name.data
        self.surname = form.surname.data
        self.nick = form.nick.data
        self.age = form.age.data
        self.email = form.email.data
        self.address = form.address.data
        self.upload_photo(form.photo)
        db.session.commit()

    def set_about_form(self, form):
        self.about_me = form.about_me.data
        db.session.commit()

    def update_status(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.commit()

    def send_message(self, text, recipient_room):
        recipient_room.add_message(self, text)

    def upload_photo(self, photo):
        if photo.data:
            filename = photo.data.filename

            dir_path = os.path.join(
                'app/static',
                current_app.config['IMAGE_UPLOAD_FOLDER']
            )
            file_path = os.path.join(
                dir_path,
                str(self.id) + "." + filename.rsplit('.', 1)[1]
            )
            file_path_db = os.path.join(
                '/', file_path.split('/', 1)[1]
            )

            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

            photo.data.save(file_path)
            self.photo = file_path_db

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def create_new_room():
        room = Room()
        room.commit_to_db()
        room.create_chat()
        return room

    @staticmethod
    def get_room_or_create(user1, user2):
        for room1 in user1.rooms:
            for room2 in user2.rooms:
                if room1 == room2:
                    return room1.id

        room = Room.create_new_room()
        room.add_user(user1)
        room.add_user(user2)
        return room.id

    def create_chat(self):
        self.chat = self.get_class_chat
        print(type(self.chat))

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_class_chat(self):
        DynamicBase = declarative_base(class_registry=dict())

        class Message(DynamicBase):
            __tablename__ = 'message_{}'.format(self.id)
            id = db.Column(db.Integer, primary_key=True)
            text = db.Column(db.String(512))
            sender = None
            time = db.Column(db.DateTime, index=True)

            @property
            def is_over_a_day(self):
                if datetime.datetime.utcnow().weekday() != self.time.weekday():
                    return True
                else:
                    return False

            def commit_to_db(self):
                db.session.add(self)
                db.session.commit()

        DynamicBase.metadata.drop_all(db.engine)
        DynamicBase.metadata.create_all(db.engine)
        return Message

    def add_user(self, user):
        self.members.append(user)
        db.session.commit()

    def is_member(self, user):  # FIXME: make me fast, pls
        for member in self.members:
            if member == user:
                return True
        return False

    def add_message(self, sender, text):
        self.chat(text=text, sender=sender).commit_to_db()

    def get_messages(self):
        messages = self.chat.query.all()
        messages.sort(key=operator.attrgetter('time'))
        return messages

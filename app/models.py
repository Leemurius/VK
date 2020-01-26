import os
import jwt
import datetime
from time import time
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from config import Constants

rooms = db.Table('rooms',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
                 )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(Constants.NAME_LENGTH))
    surname = db.Column(db.String(Constants.SURNAME_LENGTH))
    username = db.Column(db.String(Constants.USERNAME_LENGTH), unique=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(Constants.ADDRESS_LENGTH))
    email = db.Column(db.String(Constants.EMAIL_LENGTH), unique=True)
    photo = db.Column(
        db.String(Constants.PHOTO_LENGTH),
        default=Constants.DEFAULT_USER_PHOTO
    )
    about_me = db.Column(db.String(Constants.ARTICLE_LENGTH))
    last_seen = db.Column(
        db.DateTime, index=True,
        default=datetime.datetime.utcnow()
    )
    password_hash = db.Column(db.String(256))

    rooms = db.relationship(
        'Room',
        secondary=rooms,
        backref=db.backref('members', lazy="dynamic")
    )

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.username = kwargs.get('username')
        self.age = kwargs.get('age', 0)
        self.email = kwargs.get('email')

    @property
    def status(self):
        time_difference = datetime.datetime.utcnow() - self.last_seen
        if time_difference.total_seconds() / 60 > 5:
            return False
        else:
            return True

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return None
        return User.query.get(id)

    def get_reset_password_token(self, expires_in=Constants.TIME_OF_ACTUAL_REQUEST):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    def get_sorted_rooms_by_timestamp(self, current_user):
        rooms = []
        for room in sorted(self.rooms,
                           key=lambda room: (room.get_time_of_last_message()),
                           reverse=True):
            rooms.append(room.to_dict(current_user))
        return rooms

    @staticmethod
    def get_user_from_login(login):
        return User.query.filter_by(username=login).first() or \
               User.query.filter_by(email=login).first()

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'status': self.status,
            'photo': self.photo,
            'age': self.age,
            'email': self.email,
            'address': self.address
        }

    def set_profile_information(self, **kwargs):
        self.name = kwargs.get('name', self.name)
        self.surname = kwargs.get('surname', self.surname)
        self.username = kwargs.get('username', self.username)
        self.age = kwargs.get('age', self.age)
        self.email = kwargs.get('email', self.email)
        self.address = kwargs.get('address', self.address)
        self.upload_photo(kwargs.get('photo', self.photo))
        db.session.commit()

    def set_about_form(self, form):
        self.about_me = form.about_me.data
        db.session.commit()

    def update_status(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.commit()

    def send_message(self, text, recipient_room):
        recipient_room.add_message(self.id, text)

    def upload_photo(self, photo):
        if self.photo != photo:
            # Delete old photo
            old_path = os.path.join(Constants.IMAGE_UPLOAD_FOLDER, os.path.basename(self.photo))
            if os.path.isfile(old_path):
                os.unlink(old_path)

            filename = '{}_{}.{}'.format(self.id, int(time()), photo.filename.rsplit('.', 1)[-1])
            file_path = os.path.join(Constants.IMAGE_UPLOAD_FOLDER, filename)
            file_path_db = os.path.join(Constants.IMAGE_DB_FOLDER, filename)

            photo.seek(0)  # put cursor at the beginning
            photo.save(file_path)
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
    title = db.Column(db.String(Constants.ROOM_NAME_LENGTH))
    photo = db.Column(
        db.String(Constants.PHOTO_LENGTH),
        default=Constants.DEFAULT_ROOM_PHOTO
    )
    unread_messages_count = db.Column(db.Integer, default=0)
    is_dialog = db.Column(db.Boolean)

    @staticmethod
    def create_new_room(is_dialog=False):
        room = Room(is_dialog=is_dialog)
        room.commit_to_db()
        room.create_chat()
        return room

    @staticmethod
    def get_or_create_dialog(user1, user2):
        if user1 == user2:  # Not create room with yourself
            return None

        for room1 in user1.rooms:  # FIXME: make faster
            for room2 in user2.rooms:
                if room1 == room2 and room1.is_dialog:
                    return room1.id

        room = Room.create_new_room(is_dialog=True)
        room.add_user(user1)
        room.add_user(user2)
        return room.id

    @property
    def chat(self):
        chat_name = 'chat_{}'.format(self.id)
        chat_table = None

        # If table not exists in metadata - create
        if chat_name not in db.metadata.tables.keys():
            chat_table = db.Table(
                'chat_{}'.format(self.id), db.metadata,
                db.Column('id', db.Integer, primary_key=True),
                db.Column('text', db.String(Constants.MAX_MESSAGE_LENGTH)),
                db.Column('sender_id', db.Integer),
                db.Column('time', db.DateTime, index=True),
                db.Column('read', db.Boolean)
            )
        else:
            chat_table = db.metadata.tables[chat_name]

        return chat_table

    def add_message(self, sender_id, text):
        insert = self.chat.insert().values(
            text=text,
            sender_id=sender_id,
            time=datetime.datetime.utcnow()
        )
        self.unread_messages_count += 1
        db.engine.connect().execute(insert)
        self.commit_to_db()

    @staticmethod
    def get_message_sender(sender_id):
        return User.query.get(sender_id)

    def get_messages(self):
        messages = db.session.query(self.chat).all()

        class Message(object):
            def __init__(self, message):
                self.id = message[0]
                self.text = message[1]
                self.sender = User.query.get(message[2])
                self.time = message[3]

        messages = [Message(message) for message in messages]
        return messages

    def get_last_message(self):
        messages = db.session.query(self.chat).all()

        last_message = None
        if messages:
            last_message = messages[-1].text

        if last_message and len(last_message) > 30:
            last_message = last_message[:30] + '...'

        if last_message is None:
            last_message = 'It\'s new chat'

        return last_message

    def get_time_of_last_message(self):
        messages = db.session.query(self.chat).all()
        if len(messages):
            return messages[-1][3]
        else:
            return datetime.datetime.now()

    def create_chat(self):
        dynamic_base = declarative_base(class_registry=dict())

        class Message(dynamic_base):
            __tablename__ = 'chat_{}'.format(self.id)
            id = db.Column(db.Integer, primary_key=True)
            text = db.Column(db.String(Constants.MAX_MESSAGE_LENGTH))
            sender_id = db.Column(db.Integer)
            time = db.Column(db.DateTime, index=True)
            read = db.Column(db.Boolean)

        Message.__table__.create(db.engine)

    def add_user(self, user):
        self.members.append(user)
        db.session.commit()

    def upload_photo(self, photo):
        if self.photo != photo:
            # Delete old photo
            old_path = os.path.join(
                Constants.ROOM_IMAGE_UPLOAD_FOLDER, os.path.basename(self.photo)
            )
            if os.path.isfile(old_path):
                os.unlink(old_path)

            filename = '{}_{}.{}'.format(self.id, int(time()), photo.filename.rsplit('.', 1)[-1])
            file_path = os.path.join(Constants.ROOM_IMAGE_UPLOAD_FOLDER, filename)
            file_path_db = os.path.join(Constants.ROOM_IMAGE_DB_FOLDER, filename)

            photo.seek(0)  # put cursor at the beginning
            photo.save(file_path)
            self.photo = file_path_db

    def get_recipient(self, user):
        if not self.is_dialog:  # Chat
            return None

        for member in self.members:  # Dialog
            if user != member:
                return member

        return self.members[0]  # Dialog with yourself

    def get_title(self, current_user):
        title = self.title
        if self.is_dialog:
            recipient = self.get_recipient(current_user)
            title = recipient.name + ' ' + recipient.surname
        return title if len(title) <= 25 else title[:25] + '...'

    def get_photo(self, current_user):
        if self.is_dialog:
            return self.get_recipient(current_user).photo
        else:
            return self.photo

    def get_status(self, current_user):
        if self.is_dialog:
            return self.get_recipient(current_user).status
        else:
            return None

    def is_member(self, user):
        if user in self.members:
            return True
        else:
            return False

    def to_dict(self, current_user):
        return {
            'id': self.id,
            'status': self.get_status(current_user),
            'is_dialog': self.is_dialog,
            'title': self.get_title(current_user),
            'photo': self.get_photo(current_user),
            'last_message': self.get_last_message(),
            'unread_messages_count': self.unread_messages_count,
            'time_of_last_message': str(self.get_time_of_last_message())
        }

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

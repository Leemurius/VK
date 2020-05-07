import os
import jwt
import datetime
from time import time

import werkzeug
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from config import Constants

dialogs = db.Table(
    'dialogs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('dialog_id', db.Integer, db.ForeignKey('dialog.id')),
    db.Column('unread_messages', db.Integer, default=0)
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
    last_seen = db.Column(
        db.DateTime, index=True,
        default=datetime.datetime.utcnow()
    )
    password_hash = db.Column(db.String(256))

    dialogs = db.relationship(
        'Dialog',
        secondary=dialogs,
        backref=db.backref('members', lazy='dynamic')
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

    def get_reset_password_token(self,
                                 expires_in=Constants.TIME_OF_ACTUAL_REQUEST):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    def get_sorted_rooms_by_timestamp(self, current_user):
        # TODO: CHAT
        rooms = []
        for dialog in sorted(self.dialogs,
                             key=lambda dialog:
                             (dialog.get_last_message()['time']),
                             reverse=True):
            rooms.append(dialog.to_dict(current_user))
        return rooms

    @staticmethod
    def is_correct_id(id):
        try:
            User.query.get_or_404(id)
        except werkzeug.exceptions.NotFound:
            return False
        else:
            return True

    @staticmethod
    def get_user_from_login(login):
        return User.query.filter_by(username=login).first() or \
               User.query.filter_by(email=login).first()

    def to_dict(self):
        return {
            'id': self.id,
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

    def send_message(self, room, text):
        room.add_message(self.id, text)

    def upload_photo(self, photo):
        if self.photo != photo:
            # Delete old photo
            old_path = os.path.join(Constants.IMAGE_UPLOAD_FOLDER,
                                    os.path.basename(self.photo))
            if os.path.isfile(old_path):
                os.unlink(old_path)

            filename = '{}_{}.{}'.format(self.id,
                                         int(time()),
                                         photo.filename.rsplit('.', 1)[-1])
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


class Dialog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def create(user1, user2):
        dialog = Dialog()

        dialog.members.append(user1)
        # if it's monolog
        if user1 != user2:
            dialog.members.append(user2)

        dialog.commit_to_db()
        dialog.create_chat()
        return dialog

    @staticmethod
    def get_or_create(user1, user2):
        dialog_id = Dialog.get_id(user1, user2)
        if dialog_id is None:
            return Dialog.create(user1, user2)
        else:
            return Dialog.query.get(dialog_id)

    @staticmethod
    def get_id(user1, user2):
        if user1 == user2:
            for dialog in user1.dialogs:
                if len(list(dialog.members)) == 1:
                    return dialog.id
        else:
            for dialog1 in user1.dialogs:  # FIXME: make normal request
                for dialog2 in user2.dialogs:
                    if dialog1 == dialog2:
                        return dialog1.id
        return None

    @staticmethod
    def get_object(user1, user2):
        dialog_id = Dialog.get_id(user1, user2)
        if dialog_id is None:
            return None
        else:
            return Dialog.query.get(dialog_id)

    def create_chat(self):
        dynamic_base = declarative_base(class_registry=dict())

        class Message(dynamic_base):
            __tablename__ = 'dialog_{}'.format(self.id)
            id = db.Column(db.Integer, primary_key=True)
            text = db.Column(db.String(Constants.MAX_MESSAGE_LENGTH))
            sender_id = db.Column(db.Integer)
            time = db.Column(db.DateTime, index=True)

        Message.__table__.create(db.engine)

    @property
    def dialog(self):
        dialog_name = 'dialog_{}'.format(self.id)

        # If table not exists in metadata - create
        if dialog_name not in db.metadata.tables.keys():
            dialog_table = db.Table(
                dialog_name, db.metadata,
                db.Column('id', db.Integer, primary_key=True),
                db.Column('text', db.String(Constants.MAX_MESSAGE_LENGTH)),
                db.Column('sender_id', db.Integer),
                db.Column('time', db.DateTime, index=True),
            )
        else:
            dialog_table = db.metadata.tables[dialog_name]

        return dialog_table

    def add_message(self, sender_id, text):
        insert = self.dialog.insert().values(
            text=text,
            sender_id=sender_id,
            time=datetime.datetime.utcnow()
        )
        db.engine.connect().execute(insert)

        for user in self.members:
            db.session.query(dialogs).filter(
                dialogs.c.user_id == user.id,
                dialogs.c.dialog_id == self.id).update(
                {dialogs.c.unread_messages: dialogs.c.unread_messages + 1},
                synchronize_session=False
            )
        db.session.commit()

    def get_messages(self):
        messages = db.session.query(self.dialog).all()
        messages = [message_to_dict(message, self) for message in messages]
        return messages

    def read_messages(self, user):
        db.session.query(dialogs).filter(
            dialogs.c.user_id == user.id,
            dialogs.c.dialog_id == self.id).update(
            {dialogs.c.unread_messages: 0},
            synchronize_session=False
        )
        db.session.commit()

    def get_last_message(self):
        messages = db.session.query(self.dialog).all()

        last_message = None
        if messages:
            last_message = message_to_dict(messages[-1], self)

        return last_message

    def get_count_of_unread_messages(self, user):
        return db.session.query(dialogs).filter(
            dialogs.c.user_id == user.id,
            dialogs.c.dialog_id == self.id
        ).one().unread_messages

    def is_dialog(self):
        return True

    def has_member(self, user):
        return user in self.members

    def get_recipient(self, user):
        if len(list(self.members)) == 2:
            return (self.members[1] if self.members[0] == user
                    else self.members[0])
        else:
            return self.members[0]

    def get_title(self, current_user):
        recipient = self.get_recipient(current_user)
        title = recipient.name + ' ' + recipient.surname
        return title

    def to_dict(self, current_user):
        return {
            'id': self.id,
            'recipient_id': self.get_recipient(current_user).id,
            'status': self.get_recipient(current_user).status,
            'is_dialog': self.is_dialog(),
            'title': self.get_title(current_user),
            'photo': self.get_recipient(current_user).photo,
            'last_message': self.get_last_message(),
            'unread_messages_count': self.get_count_of_unread_messages(
                current_user)
        }

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


def message_to_dict(message, room):
    return {'is_dialog': room.is_dialog(),
            'room_id': room.id,
            'text': message[1],
            'sender': User.query.get(message[2]).to_dict(),
            'time': str(message[3])}

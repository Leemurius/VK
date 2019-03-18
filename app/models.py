import os
import datetime
import operator

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


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

    sent_messages = db.relationship(
        'Message',
        backref='sender',
        lazy='dynamic',
        foreign_keys='Message.sender_id'
    )

    recipient_messages = db.relationship(
        'Message',
        backref='recipient',
        lazy='dynamic',
        foreign_keys='Message.recipient_id'
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

    def set_profile_form(self, form):
        self.name = form.name.data
        self.surname = form.surname.data
        self.nick = form.nick.data
        self.age = form.age.data
        self.email = form.email.data
        self.address = form.address.data
        db.session.commit()

    def set_about_form(self, form):
        self.about_me = form.about_me.data
        db.session.commit()

    def update_status(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.commit()

    def send_message(self, text, recipient):
        m = Message(
            text=text,
            sender=self,
            recipient=recipient,
            recipient_id=recipient.id,
            time=datetime.datetime.utcnow()
        )
        m.commit_to_db()

    def upload_photo(self, photo):
        if photo.data:
            filename = photo.data.filename
            path = os.path.join(
                '/static',
                current_app.config['IMAGE_UPLOAD_FOLDER'],
                str(self.id) + "." + filename.rsplit('.', 1)[1]
            )
            photo.data.save('app/' + path)
            self.photo = path
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, index=True)

    @staticmethod
    def get_dialog(current_user, recipient):
        messages_sender = Message.query.filter_by(
            sender_id=current_user.id,
            recipient_id=recipient.id
        ).all()

        messages_recipient = Message.query.filter_by(
            sender_id=recipient.id,
            recipient_id=current_user.id
        ).all()

        messages = messages_sender
        if current_user != recipient:
            messages += messages_recipient

        messages.sort(key=operator.attrgetter('time'))
        return messages

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

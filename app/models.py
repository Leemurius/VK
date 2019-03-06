import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    CONST_DEFAULT_PHOTO = '/static/image/no_photo.png'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    nick = db.Column(db.String(20), unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(20), unique=True)
    photo = db.Column(db.String(1024), default=CONST_DEFAULT_PHOTO)
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

    def __init__(self, name, surname, nick, age, email, photo=None):
        self.name = name
        self.surname = surname
        self.nick = nick
        self.age = age
        self.email = email
        self.photo = photo if photo else User.CONST_DEFAULT_PHOTO

    def send_message(self, text, recipient):
        m = Message(
            text=text,
            sender=self,
            recipient=recipient,
            recipient_id=recipient.id,
            time=datetime.datetime.now()
        )
        m.commit_to_db()

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_ep_form(self, form):
        self.name = form.name.data
        self.surname = form.surname.data
        self.nick = form.nick.data
        self.age = form.age.data
        self.email = form.email.data
        self.photo = form.photo.data
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, index=True)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

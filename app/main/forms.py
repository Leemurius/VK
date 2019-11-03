from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, length

from config import Constants
from app.models import Room


class ChatForm(FlaskForm):
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Message is empty'),
            length(max=Constants.MESSAGE_LENGTH, message='Too long message')
        ]
    )

    def validate_message(self, message):
        self.message.data = message.data.strip('\r\n')  # delete excess new lines

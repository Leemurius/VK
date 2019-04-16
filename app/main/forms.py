from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, length

from config import Constants


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


class SearchForm(FlaskForm):
    request = StringField(
        'Search line',
        validators=[
            DataRequired(message='Request is empty'),
            length(max=Constants.MESSAGE_LENGTH, message='Too long request')
        ]
    )

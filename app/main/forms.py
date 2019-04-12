from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired, length

from config import Constants


class ChatForm(FlaskForm):
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(),
            length(max=Constants.MESSAGE_LENGTH, message='Very big message')
        ]
    )

    def validate_message(self, message):
        self.message.data = message.data.strip('\r\n')  # delete excess new lines


class SearchForm(FlaskForm):
    request = StringField(
        'Search',
        validators=[
            DataRequired(),
            length(max=Constants.REQUEST_LENGTH, message='Request is very big')
        ]
    )

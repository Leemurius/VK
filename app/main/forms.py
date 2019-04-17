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


class SearchForm(FlaskForm):
    request = StringField(
        'Search line',
        validators=[
            DataRequired(message='Request is empty'),
            length(max=Constants.MESSAGE_LENGTH, message='Too long request')
        ]
    )

    def get_founding_room(self, current_user):
        rooms = current_user.rooms  # your own rooms

        if self.validate_on_submit():
            rooms = []
            for room in Room.query.all():  # TODO : normal search
                if room.get_title(current_user) == self.request.data:
                    rooms.append(room)

        return rooms


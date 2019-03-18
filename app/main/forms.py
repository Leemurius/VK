from flask import current_app
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, length


class ChatForm(FlaskForm):
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(),
            length(max=current_app.config['MESSAGE_LENGTH'], message='Very big message'),
        ],
    )

    def validate_message(self, message):
        self.message.data = message.data.strip('\r\n')

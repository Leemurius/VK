from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

from app import sio
from app.models import Dialog, User
from app.utils.tools import format_message


@sio.on('send_message', namespace='/user')
def send_message(recipient_id, text):
    room = None
    if User.is_correct_id(recipient_id):
        recipient = User.query.get(recipient_id)
        dialog_id = Dialog.get_id(current_user, recipient)

        if dialog_id is None:
            room = Dialog.create(current_user, recipient)

            # Send new dialog to all users
            for user in room.members:
                emit('get_new_room', room.to_dict(user),
                     namespace='/user', room=str(user.id))
        else:
            room = Dialog.query.get(dialog_id)
    else:
        pass
        # TODO: CHAT

    if room is not None and format_message(text) != '':
        current_user.send_message(room, format_message(text))

        last_message = room.get_last_message()
        if last_message['text'] == '':
            return

        for user in room.members:
            emit('get_message', last_message,
                 namespace='/user', room=str(user.id))


@sio.on('read_messages', namespace='/user')
def read_messages(recipient_id):
    room = None
    if User.is_correct_id(recipient_id):
        room = Dialog.get_object(current_user, User.query.get(recipient_id))
    else:
        pass
        # TODO: CHAT

    if room is not None:
        room.read_messages(current_user)
        for user in room.members:
            emit('update_room', room.to_dict(user),
                 namespace='/user', room=(str(user.id)))


@sio.on('join', namespace='/user')
def on_join():
    join_room(str(current_user.id), namespace='/user')


@sio.on('leave', namespace='/user')
def on_leave():
    leave_room(str(current_user.id), namespace='/user')


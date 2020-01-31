from flask_login import current_user

from app import sio
from flask_socketio import join_room, leave_room


@sio.on('join', namespace='/rooms')
def join():
    # TODO: CHAT
    for dialog in current_user.dialogs:
        join_room(str(dialog.id), namespace='/rooms')


@sio.on('leave', namespace='/rooms')
def join():
    # TODO: CHAT
    for dialog in current_user.dialogs:
        leave_room(str(dialog.id), namespace='/rooms')

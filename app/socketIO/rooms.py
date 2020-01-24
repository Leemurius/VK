from flask_login import current_user

from app import sio
from flask_socketio import join_room, leave_room


@sio.on('join', namespace='/rooms')
def join():
    for room in current_user.rooms:
        join_room(str(room.id), namespace='/rooms')


@sio.on('leave', namespace='/rooms')
def join():
    for room in current_user.rooms:
        leave_room(str(room.id), namespace='/rooms')

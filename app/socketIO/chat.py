from flask_login import current_user

from app import sio
from flask_socketio import emit, join_room, leave_room

from app.models import Room


@sio.on('send_message', namespace='/chat')
def send_message(room_id, message):
    if not current_user in Room.query.get_or_404(room_id).members:
        return

    current_user.send_message(
        recipient_room=Room.query.get_or_404(room_id),
        text=message
    )
    emit('get_message', (message, current_user.to_dict()), namespace='/chat', room=str(room_id))
    emit('get_new_list', namespace='/rooms', room=str(room_id))


@sio.on('join', namespace='/chat')
def on_join(room_id):
    if current_user in Room.query.get_or_404(room_id).members:
        join_room(str(room_id), namespace='/chat')


@sio.on('leave', namespace='/chat')
def on_leave(room_id):
    if current_user in Room.query.get_or_404(room_id).members:
        leave_room(str(room_id), namespace='/chat')

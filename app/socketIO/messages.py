from flask_login import current_user

from app import sio
from flask_socketio import emit, join_room, leave_room

from app.models import Dialog, User


@sio.on('send_message', namespace='/messages')
def send_message(recipient_id, text):
    recipient = User.query.get_or_404(recipient_id)
    dialog_id = Dialog.get_id(current_user, recipient)

    if dialog_id is None:
        dialog = Dialog.create(current_user, recipient)
        emit('get_updated_room',
             dialog.to_dict(current_user),
             namespace='/rooms',
             room=str(dialog.id))
    else:
        dialog = Dialog.query.get(dialog_id)

    current_user.send_message(dialog, text)
    emit('get_message', dialog.get_last_message(), namespace='/messages', room=str(dialog.id))
    emit('get_updated_room', dialog.to_dict(current_user), namespace='/rooms', room=str(dialog.id))


@sio.on('join', namespace='/messages')
def on_join(recipient_id):
    dialog_id = Dialog.get_id(current_user, User.query.get_or_404(recipient_id))
    if dialog_id is not None and Dialog.query.get_or_404(dialog_id).has_member(current_user):
        join_room(str(dialog_id), namespace='/messages')


@sio.on('leave', namespace='/messages')
def on_leave(recipient_id):
    dialog_id = Dialog.get_id(current_user, User.query.get_or_404(recipient_id))
    if dialog_id is not None and Dialog.query.get_or_404(dialog_id).has_member(current_user):
        leave_room(str(dialog_id), namespace='/messages')

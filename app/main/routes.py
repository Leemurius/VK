from flask import render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required

from app import sio
from flask_socketio import emit
from app.main import bp
from app.models import User, Room


@bp.route('/my_profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template(
        'main/profile.html',
        current_user=current_user,  # for base.html
        rooms=current_user.get_sorted_rooms_by_timestamp(),  # for base.html
    )


@sio.on('send_message', namespace='/chat')
def send_message(room_id, message):
    current_user.send_message(
        recipient_room=Room.query.get_or_404(room_id),
        text=message
    )
    emit('get_message', (message, current_user.photo), namespace='/chat', broadcast=True)


@bp.route('/chat/<room_id>', methods=['GET'])
@login_required
def chat(room_id):
    room = Room.query.get_or_404(room_id)

    if not room.is_member(current_user):
        return redirect(url_for('main.profile'))

    return render_template(
        'main/chat.html',
        current_user=current_user,  # for base.html
        rooms=current_user.get_sorted_rooms_by_timestamp(),  # for base.html
        room=room,
        recipient=room.get_recipient(current_user),  # if chat is dialog
        title=room.get_recipient(current_user).username,
        messages=room.get_messages()
    )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    users = list(User.query.order_by(User.username.desc()))
    users.remove(current_user)  # fixed bug with button on yourself
    users = sorted(users, key=lambda user: (user.name, user.surname))

    return render_template(
        'main/search.html',
        current_user=current_user,  # for base.html
        rooms=current_user.get_sorted_rooms_by_timestamp(),  # for base.html
        users=users,
    )


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()

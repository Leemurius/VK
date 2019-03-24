from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import ChatForm
from app.models import User, Room


@bp.route('/my_profile')
@login_required
def my_profile():

    users = User.query.all()

    return render_template(
        'main/profile.html',
        room=-1,
        user=current_user,
        chats=User.rooms
    )


@bp.route('/profile/<nick>')
@login_required
def profile(nick):
    if nick == current_user.nick:
        return redirect(url_for('main.my_profile'))

    user = User.query.filter_by(nick=nick).first_or_404()
    chats = User.rooms

    return render_template(
        'main/profile.html',
        room=Room.get_room_or_create(user, current_user),
        user=user,
        chats=chats
    )


@bp.route('/chat/<room_id>', methods=['GET', 'POST'])
@login_required
def chat(room_id):
    room = Room.query.filter_by(id=room_id).first()

    if not room.is_member(current_user):
        return redirect(url_for('main.my_profile'))  # FIXME: redirect back

    form = ChatForm()

    if form.validate_on_submit():
        current_user.send_message(
            text=form.message.data,
            recipient_room=room
        )
        return redirect(url_for('main.chat', room_id=room_id))

    return render_template(
        'main/chat.html',
        form=form,
        current_user=current_user,
        messages=room.get_messages(),
        users=User.query.all(),
)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()


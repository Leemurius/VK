from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import ChatForm, SearchForm
from app.models import User, Room


@bp.route('/<nick>')
@login_required
def profile(nick):
    user = User.query.filter_by(nick=nick).first_or_404()

    return render_template(
        'main/profile.html',
        current_user=current_user,  # for base.html
        rooms=current_user.rooms,  # for base.html
        user=user,
        get_or_create_room=Room.get_or_create_room  # if click 'write message'
    )


@bp.route('/chat/<room_id>', methods=['GET', 'POST'])
@login_required
def chat(room_id):
    room = Room.query.get_or_404(room_id)

    if not room.is_member(current_user):
        return redirect(url_for('main.profile', nick=current_user.nick))  # TODO: redirect back

    form = ChatForm()

    if form.validate_on_submit():
        current_user.send_message(
            recipient_room=room,
            text=form.message.data
        )
        return redirect(url_for('main.chat', room_id=room_id))

    return render_template(
        'main/chat.html',
        current_user=current_user,  # for base.html
        rooms=current_user.rooms,  # for base.html
        form=form,
        room=room,
        recipient=room.get_recipient(current_user),  # if chat is dialog
        title=(
            room.get_recipient(current_user).nick
            if room.is_dialog
            else room.title
        ),
        messages=room.get_messages()
    )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('main.search'))

    return render_template(
        'main/search.html',
        current_user=current_user,  # for base.html
        rooms=current_user.rooms,  # for base.html
        users=User.query.all(),
        form=form
    )


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()

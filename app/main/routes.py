from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app.main import bp
from config import Constants
from app.models import User, Room
from app.main.forms import ChatForm, SearchForm


@bp.route('/<nick>', methods=['GET', 'POST'])
@login_required
def profile(nick):
    base_form = SearchForm()
    rooms = base_form.get_founding_room(current_user)  # validate inside
    user = User.query.filter_by(nick=nick).first_or_404()

    return render_template(
        'main/profile.html',
        base_form=base_form,  # for base.html
        current_user=current_user,  # for base.html
        rooms=rooms,  # for base.html
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
    base_form = SearchForm()
    rooms = base_form.get_founding_room(current_user)  # validate inside

    if form.validate_on_submit():
        current_user.send_message(
            recipient_room=room,
            text=form.message.data
        )

    return render_template(
        'main/chat.html',
        base_form=base_form,  # for base.html
        current_user=current_user,  # for base.html
        rooms=rooms,  # for base.html
        form=form,
        room=room,
        recipient=room.get_recipient(current_user),  # if chat is dialog
        title=room.get_title(current_user),
        messages=room.get_messages()
    )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    base_form = SearchForm()
    users = User.query.order_by(User.nick.desc())
    rooms = base_form.get_founding_room(current_user)  # validate inside

    if form.validate_on_submit():
        # Get list of found users
        users = User.query.filter_by(nick=form.request.data)  # TODO : normal search

    # pagination
    page = request.args.get('page', default=1, type=int)
    users = users.paginate(page, Constants.USER_PER_PAGE, True)
    prev_url = url_for('main.search', page=users.prev_num) \
        if users.has_prev else None
    next_url = url_for('main.search', page=users.next_num) \
        if users.has_next else None

    return render_template(
        'main/search.html',
        base_form=base_form,  # for base.html
        current_user=current_user,  # for base.html
        rooms=rooms,  # for base.html
        users=users.items,
        prev_url=prev_url,  # pagination
        next_url=next_url,  # pagination
        form=form
    )


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()

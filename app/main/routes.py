from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import ChatForm
from app.models import User, Message


@bp.route('/my_profile')
@login_required
def my_profile():

    users = User.query.all()

    return render_template(
        'main/profile.html',
        user=current_user,
        users=users
    )


@bp.route('/profile/<nick>')
@login_required
def profile(nick):
    if nick == current_user.nick:
        return redirect(url_for('main.my_profile'))

    user = User.query.filter_by(nick=nick).first_or_404()
    users = User.query.all()

    return render_template(
        'main/profile.html',
        user=user,
        users=users
    )


@bp.route('/chat/<nick>', methods=['GET', 'POST'])
@login_required
def chat(nick):
    recipient = User.query.filter_by(nick=nick).first_or_404()

    form = ChatForm()

    if form.validate_on_submit():
        current_user.send_message(
            text=form.message.data,
            recipient=recipient
        )
        return redirect(url_for('main.chat', nick=nick))

    return render_template(
        'main/chat.html',
        form=form,
        current_user=current_user,
        messages=Message.get_dialog(current_user, recipient),
        users=User.query.all(),
        recipient=recipient
)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()


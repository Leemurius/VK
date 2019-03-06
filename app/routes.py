import operator

from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user

from app import app
from app.models import User, Message
from app.custom_decorators import login_required
from app.forms import RegistrationForm, LoginForm, ChatForm, EditProfileForm, EditPasswordForm
from app.utils import get_user_avatar_url


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            nick=form.nick.data,
            age=form.age.data,
            email=form.email.data
        )
        user.commit_to_db()
        user.set_password(form.password.data)
        return redirect(url_for('login'))

    return render_template('registration.html', form=form, title='Registration')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.get_user())
        return redirect(url_for('home'))

    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', users=User.query.all())


@app.route('/profile/<nick>')
@login_required
def profile(nick):
    user = User.query.filter_by(nick=nick).first_or_404()
    return render_template('profile.html', user=user)


@app.route('/profile/<nick>/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile(nick):
    form = EditProfileForm(
        name=current_user.name,
        surname=current_user.surname,
        nick=current_user.nick,
        age=current_user.age,
        email=current_user.email,
        photo=get_user_avatar_url(current_user.photo)
    )

    if form.validate_on_submit():
        current_user.set_ep_form(form)
        return redirect(url_for('profile', nick=current_user.nick))

    return render_template('edit_profile.html', form=form)


@app.route('/profile/<nick>/edit_password/', methods=['GET', 'POST'])
@login_required
def edit_password(nick):
    form = EditPasswordForm()

    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        return redirect(url_for('profile', nick=current_user.nick))

    return render_template('edit_password.html', form=form)


@app.route('/chat/<nick>', methods=['GET', 'POST'])
@login_required
def chat(nick):
    user = User.query.filter_by(nick=nick).first_or_404()

    form = ChatForm()

    if form.validate_on_submit():
        current_user.send_message(
            text=form.message.data,
            recipient=user
        )
        return redirect(url_for('chat', nick=nick))

    messages_sender = Message.query.filter_by(
        sender_id=current_user.id,
        recipient_id=user.id
    ).all()

    messages_recipient = Message.query.filter_by(
        sender_id=user.id,
        recipient_id=current_user.id
    ).all()

    messages = messages_sender + messages_recipient
    for i in range(len(messages)):
        messages[i].sender_nick = User.query.get(messages[i].sender_id).nick
    messages.sort(key=operator.attrgetter('time'))

    times = map(lambda date: date.time.replace(microsecond=0), messages)
    times = list(map(lambda it: str(it.time()) + ' | ' + str(it.date()), times))

    return render_template('chat.html', form=form, user=user, messages=messages, times=times)

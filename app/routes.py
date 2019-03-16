from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user

from app import app
from app.models import User, Message
from app.custom_decorators import login_required
from app.forms import RegistrationForm, LoginForm, ChatForm, ProfSettingsForm


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()


@app.route('/', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if current_user.is_authenticated:
        redirect('my_profile', )

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

    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.get_user(), remember=form.remember.data)
        return redirect(url_for('my_profile'))

    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/my_profile')
@login_required
def my_profile():

    users = User.query.all()

    return render_template(
        'profile.html',
        user=current_user,
        users=users
    )


@app.route('/profile/<nick>')
@login_required
def profile(nick):
    if nick == current_user.nick:
        return redirect(url_for('my_profile'))

    user = User.query.filter_by(nick=nick).first_or_404()
    users = User.query.all()

    return render_template(
       'profile.html',
        user=user,
        users=users
    )


@app.route('/my_profile/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ProfSettingsForm()

    users = User.query.all()

    return render_template(
        'settings.html',
        form=form,
        user=current_user,
        users=users
    )


@app.route('/chat/<nick>', methods=['GET', 'POST'])
@login_required
def chat(nick):
    recipient = User.query.filter_by(nick=nick).first_or_404()

    form = ChatForm()

    if form.validate_on_submit():
        current_user.send_message(
            text=Message.minimize_mess(form.message.data),
            recipient=recipient
        )
        return redirect(url_for('chat', nick=nick))

    return render_template(
        'chat.html',
        form=form,
        current_user=current_user,
        messages=Message.get_dialog(current_user, recipient),
        users=User.query.all(),
        recipient=recipient
)

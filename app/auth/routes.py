from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user

from app.auth import bp
from app.models import User
from app.auth.email import send_password_reset_email
from app.auth.forms import(
    RegistrationForm,
    LoginForm,
    ResetPassForm,
    ResetPassRequestForm
)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.profile', nick=current_user.nick))

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
        return redirect(url_for('auth.login'))

    return render_template('auth/registration.html', form=form)


@bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', nick=current_user.nick))

    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.get_user(), remember=form.remember.data)
        return redirect(url_for('main.profile', nick=current_user.nick))

    return render_template('auth/login.html', form=form)


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', nick=current_user.nick))

    form = ResetPassRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', nick=current_user.nick))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('auth.login'))

    form = ResetPassForm()

    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

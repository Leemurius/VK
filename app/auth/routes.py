from flask import render_template, redirect, url_for
from flask_login import logout_user, current_user

from app.auth import bp


@bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html')


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    return render_template('auth/registration.html')


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    return render_template('auth/reset_password_request.html')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    return render_template('auth/reset_password.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

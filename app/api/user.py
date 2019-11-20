import os
import re

from flask import jsonify, request
from flask_login import login_required, current_user, login_user

from app.api.errors import bad_request
from app.auth.validate import LoginValidator, RegistrationValidator, ResetPasswordValidator
from app.settings.validate import PersonalSettingsValidator, PasswordSettingsValidator
from app.models import User, Queue
from app.api import bp
from config import Constants
from app.auth.email import send_password_reset_email
from app.main.queue import QueueControl


@bp.route('/self/id', methods=['GET'])
@login_required
def get_self_id():
    return jsonify(current_user.id)


@bp.route('/self/photo', methods=['GET'])
@login_required
def get_self_photo():
    return jsonify(current_user.photo)


@bp.route('/self/username', methods=['GET'])
@login_required
def get_self_username():
    return jsonify(current_user.username)


@bp.route('/self/information', methods=['GET'])
@login_required
def get_self_information():
    return jsonify(current_user.get_profile_information())


@bp.route('/self/update/information', methods=['POST'])
@login_required
def update_self_information():
    data = request.get_json() or {}

    required_fields = ('name', 'surname', 'username', 'age', 'email', 'address')
    if not all(field in data for field in required_fields):
        return bad_request('Must include ' + str(required_fields) + ' fields!')

    try:
        validator = PersonalSettingsValidator(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            age=data['age'],
            email=data['email'],
            address=data['address']
        )
        errors = validator.validate()

        # Check that we don't have exceptions
        if any(errors):
            raise Exception(errors)

        # Accept changes
        current_user.set_profile_information(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            age=data['age'],
            email=data['email'],
            address=data['address']
        )

    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)


@bp.route('/self/update/photo', methods=['POST'])
@login_required
def update_photo():
    try:
        photo = request.files.get('photo')
        # TODO: separate function for validation

        photo.seek(0, os.SEEK_END)  # Go to the end of file
        if photo.tell() / 1024 / 1024 > Constants.MAX_PHOTO_SIZE:
            raise Exception('Max size of photo is {} MB'.format(Constants.MAX_PHOTO_SIZE))

        current_user.set_profile_information(photo=photo)
    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)


@bp.route('/self/update/password', methods=['POST'])
@login_required
def update_self_password():
    data = request.get_json() or {}

    # TODO: Man-in-the-middle
    required_fields = ('old_password', 'new_password', 'confirm_password')
    if not all(field in data for field in required_fields):
        return bad_request('Must include ' + str(required_fields) + ' fields!')

    try:
        validator = PasswordSettingsValidator(
            old_password=data['old_password'],
            new_password=data['new_password'],
            confirm_password=data['confirm_password'],
        )
        errors = validator.validate()

        # Check that we don't have exceptions
        if any(errors):
            raise Exception(errors)

        # Accept changes
        current_user.set_password(data['new_password'])
    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)


@bp.route('/user/update/password/<token>', methods=['POST'])
def update_user_password(token):
    data = request.get_json() or {}

    # TODO: Man-in-the-middle
    required_fields = ('new_password', 'confirm_password')
    if not all(field in data for field in required_fields):
        return bad_request('Must include ' + str(required_fields) + ' fields!')

    try:
        validator = ResetPasswordValidator(
            new_password=data['new_password'],
            confirm_password=data['confirm_password']
        )
        errors = validator.validate()

        # Check that we don't have exceptions
        if any(errors):
            raise Exception(errors)

        # Accept changes
        user = User.verify_reset_password_token(token)
        user.set_password(data['new_password'])
    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)


@bp.route('/user/information/<string:username>', methods=['GET'])
@login_required
def get_user_information(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.get_profile_information())


@bp.route('/user/id/<string:username>', methods=['GET'])
@login_required
def get_id(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.id)


@bp.route('/reset', methods=['POST'])
def reset_password():
    data = request.get_json() or {}

    if 'email' not in data:
        return bad_request('Must include email field!')

    try:
        user = User.query.filter_by(email=data['email']).first()

        if user is None:
            raise Exception('This email doesn\'t registered on the website')

        send_password_reset_email(user)
    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)


@bp.route('/login', methods=['POST'])
def sign_in_user():
    data = request.get_json() or {}

    if 'login' not in data or 'password' not in data:
        return bad_request('Must include login and password fields!')

    try:
        # TODO: Man-in-the-middle
        validator = LoginValidator(login=data['login'], password=data['password'])
        user = validator.get_user()
        login_user(user, remember=True)
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    required_fields = ('name', 'surname', 'username', 'email', 'password', 'confirm_password')
    if not all(field in data for field in required_fields):
        return bad_request('Must include ' + str(required_fields) + ' fields!')

    try:
        # TODO: Man-in-the-middle
        validator = RegistrationValidator(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            email=data['email'],
            password=data['password'],
            confirm_password=data['confirm_password']
        )
        errors = validator.validate()

        # Check that we don't have exceptions
        if any(errors):
            raise Exception(errors)

        # Add new user to db
        new_user = User(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        new_user.commit_to_db()

    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)

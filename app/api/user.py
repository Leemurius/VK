import werkzeug
from flask import jsonify, request
from flask_login import login_required, current_user, login_user

from app.api import bp
from app.utils.errors import bad_request
from app.auth.email import send_password_reset_email
from app.models import User
from app.utils.validator import (SettingsValidator, PhotoValidator,
                                 PasswordValidator, ResetProfileValidator,
                                 LoginValidator, RegistrationValidator,
                                 ResetPasswordValidator, Validator)


# GET INFORMATION --------------------------------------------------------------


@bp.route('/user/get', methods=['POST'])
@login_required
def get_user_information():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'user_id': int}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    return jsonify(User.query.get_or_404(data['user_id']).to_dict())


@bp.route('/user/getSelf', methods=['GET'])
@login_required
def get_self_information():
    return jsonify(current_user.to_dict())


@bp.route('/user/getId', methods=['POST'])
@login_required
def get_id():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'username': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    return jsonify(
        User.query.filter_by(username=data['username']).first_or_404().id)


# INTERNAL OPERATIONS ----------------------------------------------------------


@bp.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    # Validation
    try:
        RegistrationValidator.validate(
            {
                'name': str,
                'surname': str,
                'username': str,
                'email': str,
                'new_password': str,
                'confirm_password': str
            },
            data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Add new user to db
    new_user = User(
        name=data['name'],
        surname=data['surname'],
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['new_password'])
    new_user.commit_to_db()
    return jsonify(True)


@bp.route('/user/signIn', methods=['POST'])
def sign_in_user():
    data = request.get_json() or {}

    # Validation
    try:
        LoginValidator.validate({'login': str, 'password': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Sign in
    login_user(User.get_user_from_login(data['login']), remember=True)
    return jsonify(True)


@bp.route('/user/setInformation', methods=['POST'])
@login_required
def user_set_information():
    data = request.get_json() or {}

    # Validation
    try:
        SettingsValidator.validate(
            {
                'user_id': int,
                'name': str,
                'surname': str,
                'username': str,
                'age': object,  # not required
                'email': str,
                'address': str  # not required
            },
            data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Accept changes
    current_user.set_profile_information(
        name=data['name'],
        surname=data['surname'],
        username=data['username'],
        age=data['age'],
        email=data['email'],
        address=data['address']
    )
    return jsonify(True)


@bp.route('/user/setPhoto', methods=['POST'])
@login_required
def user_set_photo():
    # Validation
    data = {
        'user_id': request.form.get('user_id'),
        'photo': request.files.get('photo')
    }

    if data['user_id'].isdigit():
        data['user_id'] = int(data['user_id'])

    try:
        PhotoValidator.validate(
            {
                'user_id': int,
                'photo': werkzeug.datastructures.FileStorage
            },
            data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    User.query.get(data['user_id']).set_profile_information(photo=data['photo'])
    return jsonify(True)


@bp.route('/user/setPassword', methods=['POST'])
@login_required
def update_self_password():
    data = request.get_json() or {}

    # Validation
    try:
        PasswordValidator.validate(
            {
                'old_password': str,
                'new_password': str,
                'confirm_password': str
            },
            data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Accept changes
    current_user.set_password(data['new_password'])
    return jsonify(True)


@bp.route('/user/setPassword/<token>', methods=['POST'])
def update_user_password(token):
    data = request.get_json() or {}

    # Validation
    try:
        ResetPasswordValidator.validate(
            {
                'new_password': str,
                'confirm_password': str
            },
            data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Accept changes
    user = User.verify_reset_password_token(token)
    user.set_password(data['new_password'])
    return jsonify(True)


@bp.route('/user/reset', methods=['POST'])
def reset_password():
    data = request.get_json() or {}

    # Validation
    try:
        ResetProfileValidator.validate({'email': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Send reset to the email
    send_password_reset_email(User.query.filter_by(email=data['email']).first())
    return jsonify(True)

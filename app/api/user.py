from flask import jsonify, request
from flask_login import login_required, current_user, login_user

from app.api import bp
from app.api.errors import bad_request
from app.auth.email import send_password_reset_email
from app.models import User
from app.utils.validator import (SettingsValidator, PhotoValidator,
                                 PasswordValidator, ResetValidator,
                                 LoginValidator, RegistrationValidator,
                                 ResetPasswordValidator, Validator)


# GET --------------------------------------------------------------------------


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
    return jsonify(current_user.to_dict())


@bp.route('/user/information', methods=['POST'])
@login_required
def get_user_information():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'id': int}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    return jsonify(User.query.get_or_404(data['id']).to_dict())


@bp.route('/user/id', methods=['POST'])
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


# POST -------------------------------------------------------------------------


@bp.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    # Validation
    try:
        RegistrationValidator().validate(
            {
                'name': str,
                'surname': str,
                'username': str,
                'email': str,
                'new_password': str,
                'confirm_password': str
            }, data
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


@bp.route('/login', methods=['POST'])
def sign_in_user():
    data = request.get_json() or {}

    # Validation
    try:
        LoginValidator().validate({'login': str, 'password': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Sign in
    login_user(User.get_user_from_login(data['login']), remember=True)
    return jsonify(True)


@bp.route('/self/update/information', methods=['POST'])
@login_required
def update_self_information():
    data = request.get_json() or {}

    # Validation
    try:
        SettingsValidator().validate(
            {
                'name': str,
                'surname': str,
                'username': str,
                'age': object,  # not required
                'email': str,
                'address': str  # not required
            }, data
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


@bp.route('/self/update/photo', methods=['POST'])
@login_required
def update_self_photo():
    data = {'photo': request.files.get('photo')}

    # Validation
    try:
        PhotoValidator().validate({'photo': object}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Accept changes. It's not important field
    if data['photo']:
        current_user.set_profile_information(photo=data['photo'])
    return jsonify(True)


@bp.route('/self/update/password', methods=['POST'])
@login_required
def update_self_password():
    data = request.get_json() or {}

    # Validation
    try:
        PasswordValidator().validate(
            {
                'old_password': str,
                'new_password': str,
                'confirm_password': str
            }, data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Accept changes
    current_user.set_password(data['new_password'])
    return jsonify(True)


@bp.route('/user/update/password/<token>', methods=['POST'])
def update_user_password(token):
    data = request.get_json() or {}

    # Validation
    try:
        ResetPasswordValidator().validate(
            {
                'new_password': str,
                'confirm_password': str
            }, data
        )
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Accept changes
    user = User.verify_reset_password_token(token)
    user.set_password(data['new_password'])
    return jsonify(True)


@bp.route('/reset', methods=['POST'])
def reset_password():
    data = request.get_json() or {}

    # Validation
    try:
        ResetValidator().validate({'email': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # Send reset to the email
    send_password_reset_email(User.query.filter_by(email=data['email']).first())
    return jsonify(True)

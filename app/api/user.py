from flask import jsonify, request
from flask_login import login_required, current_user, login_user

from app.api.errors import bad_request
from app.auth.validates import LoginValidator, RegistrationValidator
from app.models import User
from app.api import bp


@bp.route('/self/id', methods=['GET'])
@login_required
def get_self_id():
    return jsonify(current_user.id)


@bp.route('/self/photo', methods=['GET'])
@login_required
def get_self_photo():
    return jsonify(current_user.photo)


@bp.route('/self/information', methods=['GET'])
@login_required
def get_self_information():
    return jsonify(current_user.get_profile_information())


@bp.route('/self/update/information', methods=['POST'])
@login_required
def update_self_information():
    data = request.get_json() or {}

    try:
        # TODO: check that fields are normal
        current_user.set_profile_information(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            age=data['age'],
            email=data['email'],
            address=data['address'],
        )
        if 'photo' in data['photo']:
            current_user.set_profile_information(photo=data['photo'])

    except Exception:
        return jsonify(False)
    return jsonify(True)


@bp.route('/self/update/password', methods=['POST'])
@login_required
def update_self_password():
    data = request.get_json() or {}

    try:
        # TODO: Man-in-the-middle
        current_user.set_password(data['password'])
    except Exception:
        return jsonify(False)
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


@bp.route('/user/login', methods=['POST'])
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
        if errors:
            raise Exception(errors)

    except Exception as exception:
        print(str(exception))
        return bad_request(str(exception))
    return jsonify(True)

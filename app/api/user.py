from flask import jsonify, request
from flask_login import login_required, current_user, login_user

from app.models import User
from app.api import bp


@bp.route('/self/user_id', methods=['GET'])
@login_required
def get_self_id():
    return jsonify(current_user.id)


@bp.route('/self/user_photo', methods=['GET'])
@login_required
def get_self_photo():
    return jsonify(current_user.photo)


@bp.route('/profile_id/<string:username>', methods=['GET'])
def get_id(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.id)


@bp.route('/self/profile_information/<string:username>', methods=['GET'])
def get_profile_information(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.get_profile_information())


@bp.route('/login_user', methods=['POST'])
def sign_in_user():
    data = request.get_json() or {}

    try:
        user = User.query.filter_by(username=data['login']).first() or \
               User.query.filter_by(email=data['login']).first()

        # TODO: Meet-in-the-middle
        new_password = data['password']
        if user and user.check_password(password=new_password):
            login_user(user)
        else:
            raise Exception()

    except Exception:
        return jsonify(False)
    return jsonify(True)


@bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    try:
        # TODO: check that fields are normal

        if User.query.filter_by(username=data['username']).first():
            Exception()
        if User.query.filter_by(email=data['email']).first():
            Exception()

        new_user = User(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            email=data['email']
        )

        # TODO: Meet-in-the-middle
        new_password = data['password']
        new_user.set_password(password=new_password)
        new_user.commit_to_db()
    except Exception:
        return jsonify(False)
    return jsonify(True)

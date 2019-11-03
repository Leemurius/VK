from flask import jsonify
from flask_login import login_required, current_user

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


@bp.route('/profile_id/<string:nick>', methods=['GET'])
def get_id(nick):
    user = User.query.filter_by(nick=nick).first_or_404()
    return jsonify(user.id)


@bp.route('/self/profile_information/<string:nick>', methods=['GET'])
def get_profile_information(nick):
    user = User.query.filter_by(nick=nick).first_or_404()
    return jsonify(user.get_profile_information())

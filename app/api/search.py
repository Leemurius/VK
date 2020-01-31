import re

from flask import jsonify, request
from flask_login import login_required, current_user

from app.api.errors import bad_request
from app.api import bp
from app.models import User
from app.utils.validator import Validator


@bp.route('/self/find/room', methods=['POST'])
@login_required
def find_room():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'request': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    rooms_list = []
    for room in current_user.get_sorted_rooms_by_timestamp(current_user):
        if re.search(data['request'].lower(), room['title'].lower()):
            rooms_list.append(room)
    return jsonify(rooms_list)


@bp.route('/self/find/user', methods=['POST'])
@login_required
def find_user():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'request': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    user_list = []
    for user in User.query.all():
        search_line = (user.name + ' ' + user.surname + ' ' + user.username).lower()
        if re.search(data['request'].lower(), search_line) and user != current_user:
            user_list.append(user.to_dict())
    return jsonify(user_list)

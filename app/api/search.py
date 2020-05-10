from flask import jsonify, request
from flask_login import login_required, current_user

from app.api import bp
from app.models import User
from app.utils.validator import Validator
from app.utils.errors import bad_request


@bp.route('/search/room', methods=['POST'])
@login_required
def find_room():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'request': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # TODO: Normal request to the database
    rooms_list = []
    for room in current_user.get_sorted_rooms_by_timestamp(current_user):
        search_line = room['title'].lower()
        request_line = data['request'].lower()
        if search_line.find(request_line) > -1:
            rooms_list.append(room)
    return jsonify(rooms_list)


@bp.route('/search/user', methods=['POST'])
@login_required
def find_users():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'request': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    # TODO: Normal request to the database
    user_list = []
    for user in User.query.all():
        search_line = ' '.join([user.name, user.surname, user.username]).lower()
        request_line = data['request'].lower()
        if search_line.find(request_line) > -1 and user != current_user:
            user_list.append(user.to_dict())
    return jsonify(user_list)

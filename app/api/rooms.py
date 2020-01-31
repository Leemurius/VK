from flask import jsonify, request
from flask_login import current_user

from app.api import bp
from app.api.errors import bad_request
from app.models import User, Dialog
from app.utils.validator import Validator


@bp.route('/dialog/get/messages', methods=['POST'])
def get_dialog():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'profile_id': int}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    dialog = Dialog.get_object(current_user, User.query.get_or_404(data['profile_id']))
    if dialog is None:
        return jsonify([])
    else:
        return jsonify(dialog.get_messages())


# @bp.route('/rooms/get/recipient/<int:room_id>', methods=['GET'])
# def get_recipient_username(room_id):
#     user = Chat.query.get(room_id).get_recipient(current_user)
#     if user is None:
#         return bad_request('This room is not chat')
#     else:
#         return jsonify(user.username)
